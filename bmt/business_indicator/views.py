from django import forms
from unfold.widgets import SELECT_CLASSES

from business.models import Business
from business_indicator.choices import ShowChoices
from business_indicator.models import Report
from pyecharts.charts import Bar, Line, Pie, Scatter
from pyecharts import options as opts
from django.utils.safestring import mark_safe

CHART_CHOICES = [
    ('bar', 'Bar Chart'),
    ('line', 'Line Chart'),
    ('pie', 'Pie Chart'),
    ('bubble', 'Scatter Chart'),
]

PLAN_FACT_CHOICES = [
    ('Plan', 'Plan'),
    ('Fact', 'Fact'),
]


class DashboardForm(forms.Form):
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    plan_fact = forms.ChoiceField(choices=PLAN_FACT_CHOICES)
    business =  forms.ModelChoiceField(queryset=Business.objects)

    def __init__(
            self,
            request=None,
            *args,
            **kwargs,
    ) -> None:
        super().__init__(request, *args, **kwargs)

        self.fields["chart_type"].widget.attrs["class"] = " ".join(SELECT_CLASSES)
        self.fields["plan_fact"].widget.attrs["class"] = " ".join(SELECT_CLASSES)
        self.fields["business"].widget.attrs["class"] = " ".join(SELECT_CLASSES)


def get_chart_config(chart_type, x_data, y_data, selected_pf, form_data):
    business = Business.objects.get(id=form_data['business'])
    plan_fact = form_data['plan_fact']
    chart_strategies = {
        'bar': lambda: (
            Bar()
            .add_xaxis(x_data)
            .add_yaxis(f"{selected_pf} Values", y_data)
            .set_global_opts(title_opts=opts.TitleOpts(title=f"{business.name} - {plan_fact}"))
        ),

        'line': lambda: (
            Line()
            .add_xaxis(x_data)
            .add_yaxis(f"{selected_pf} Values", y_data)
            .set_global_opts(title_opts=opts.TitleOpts(title=f"{business.name} - {plan_fact}"))
        ),

        'pie': lambda: (
            Pie()
            .add(
                "",
                [[name, value] for name, value in zip(x_data, y_data)],

                label_opts=opts.LabelOpts(
                    position="outside",  # put labels outside
                    formatter="{b}: {d}%",  # show label and percentage
                    font_size=12,
                    overflow="break",  # helps with long text
                ),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"{business.name} - {plan_fact}", is_show=True),
                legend_opts=opts.LegendOpts(type_="scroll", pos_left="left", pos_bottom=20),
            )
        ),

        'bubble': lambda: (
            Scatter()
            .add_xaxis([i for i in range(len(y_data))])
            .add_yaxis("Bubble", [[i, y, y] for i, y in enumerate(y_data)])
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"{business.name} - {plan_fact}"),
                visualmap_opts=opts.VisualMapOpts(type_="size", min_=min(y_data), max_=max(y_data))
            )
        )
    }

    chart_func = chart_strategies.get(chart_type)
    return mark_safe(chart_func().render_embed()) if chart_func else None


def dashboard_callback(request, context):
    chart_type = request.GET.getlist('chart_type')
    selected_pf = request.GET.getlist('plan_fact')
    business = request.GET.getlist('business')
    charts = [
        {'chart_type': ct, 'plan_fact': pf, 'business': b}
        for ct, pf, b in zip(chart_type, selected_pf, business)
    ]

    chart_forms = []

    for chart in charts:
        chart_forms.append(
            DashboardForm(request.GET, initial=chart)
        )
    chart_forms.append(DashboardForm())

    charts_html = []
    for chart_form_data in charts:
        reports = Report.objects.filter(
            business_id=chart_form_data['business'],
            plan_fact=chart_form_data['plan_fact'],
            show=ShowChoices.YES)[:10]  # to fetch 10 rows from Report model with these filters

        x_data = [r.name for r in reports]  # gets the name of each report and will be in x-axis
        y_data = [float(r.value or 0) for r in reports]  # gets value of each report or 0 if empty and set in y-axis

        chart_html = get_chart_config(chart_form_data['chart_type'], x_data, y_data, chart_form_data['plan_fact'], chart_form_data)
        charts_html.append(chart_html)

    context.update(
        {
            'forms': chart_forms,
            'charts': charts_html,
            'add': int(request.GET.get('add', 1)) + 1
        }
    )
    return context
