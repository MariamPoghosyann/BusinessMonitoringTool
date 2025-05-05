import pandas as pd

from django.db.models import OuterRef, Subquery, F, DateField
from django.db.models.functions import ExtractYear, ExtractMonth

from business.models import Business
from business_indicator.choices import ShowChoices
from business_indicator.models import Report
from business_indicator.serializers import BusinessSerializer


def normalize(df):
    df['type'] = df['type'].replace('', None)
    df['value'] = df['value'].replace('', 0.0)

    df['value'] = df['value'].astype(float)
    # with pd.option_context('future.no_silent_downcasting', True):
    #     df.replace('', np.nan)
    return df


def get_deviations(request, business_id=None, user_id=None):
    queryset = Report.objects.filter(show=ShowChoices.YES)
    latest_report_date_subquery = (
        Report.objects.filter(business=OuterRef("business"), plan_fact='Fact')
        .order_by("-date")
        .values("date")[:1]
    )

    queryset = queryset.annotate(
        last_report_date=Subquery(latest_report_date_subquery, output_field=DateField()),
        last_report_year=ExtractYear(F("last_report_date")),
        last_report_month=ExtractMonth(F("last_report_date")),
    ).filter(
        date__year=F("last_report_year"),
        date__month=F("last_report_month"),
    )

    if user_id:
        queryset = queryset.filter(business__responsible_person_id=user_id)

    if business_id:
        queryset = queryset.filter(business_id__in=business_id.split(','))

    queryset = queryset.values_list(
        'id', 'business', 'record_id',
        'plan_fact', 'date', 'parent_id', 'name',
        'type', 'operation', 'reverse_sign', 'value', 'color_code'
    )
    column_names = [
        'id', 'business', 'record_id', 'plan_fact', 'date', 'parent_id', 'name',
        'type', 'operation', 'reverse_sign', 'value', 'color_code'
    ]

    deviations = []

    df = pd.DataFrame(list(queryset), columns=column_names)
    df = normalize(df)

    # Make sure 'value' is numeric
    df['value'] = pd.to_numeric(df['value'], errors='coerce').fillna(0.0)
    df = df[df['value'] != 0.0]

    business_group = df.groupby('business')
    business_obj = None
    for business, grouped_business in business_group:
        business_list = []
        # Group by record_id
        grouped = grouped_business.groupby('record_id')
        for _, group in grouped:
            # We expect at most one Plan row and one Fact row for the same record_id, for last month
            plan_row = group.loc[(group['plan_fact'] == 'Plan')]
            fact_row = group.loc[(group['plan_fact'] == 'Fact')]

            row_dict = group.iloc[0].to_dict()
            if not row_dict['operation']:
                row_dict['operation'] = 'sum'
            plan_value = apply_operation(row_dict, plan_row)
            fact_value = apply_operation(row_dict, fact_row)

            # 5) Compute % deviation: (Fact - Plan) / Plan
            #    If plan_value == 0 but fact_value != 0, we can treat the deviation as infinite or skip
            if plan_value != 0.0 and fact_value != 0.0:
                deviation = (fact_value - plan_value) / abs(plan_value)
            else:
                # This is not normal when nothing was planned!
                # we can't provide a deviations from that plans!
                continue

            if deviation < -0.10 or deviation > 0.10:
                # Add to results
                # Use the row from either Fact or Plan for metadata – or build a custom data structure
                # We'll pick the first row from the group for demonstration
                business_obj = str(row_dict['business'])
                row_dict.pop('business', None)
                row_dict.pop('parent_id', None)
                row_dict.pop('color_code', None)
                row_dict.pop('plan_fact', None)
                row_dict['plan_value'] = plan_value
                row_dict['fact_value'] = fact_value
                row_dict['value'] = fact_value - plan_value
                row_dict['pct_deviation'] = round(deviation * 100, 2)
                row_dict['pct_deviation_sign'] = int(float(row_dict.pop('reverse_sign', 0)))
                business_list.append(row_dict)
        if business_list:
            business_obj = Business.objects.select_related('responsible_person').get(pk=str(business_obj))
            business_detail = BusinessSerializer(business_obj).data
            business_detail.update({'data': sorted(business_list, key=lambda x: abs(x['value']), reverse=True)})
            deviations.append(business_detail)
    return deviations


def apply_operation(row, group, col='value'):
    if row['operation'] == 'avg':
        return group[col].mean()
    elif row['operation'] == 'max':
        return group[col].max()
    else:
        return group[col].sum()