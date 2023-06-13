"""绘制项目中的所有可视化图形"""

from flask import Blueprint

from pyecharts.charts import Bar, Timeline, Grid, Line, Pie, WordCloud
from pyecharts import options as opts
from pyecharts.globals import ThemeType, SymbolType
from sqlalchemy import text

from spider.DBManager import DBManager

chartApi = Blueprint("chartApi", __name__, url_prefix="/chartApi")


def showChart1(data):
    line = Line()
    line.set_global_opts(
        title_opts=opts.TitleOpts(is_show=False),
        legend_opts=opts.LegendOpts(is_show=False),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="none"),
        xaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=False),
                                 axislabel_opts=opts.LabelOpts(is_show=True,
                                                               color="white",
                                                               font_weight="bold",
                                                               interval=1),
                                 axistick_opts=opts.AxisTickOpts(is_show=False),
                                 splitline_opts=opts.SplitLineOpts(is_show=False)
                                 ),
        yaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=False),
                                 axislabel_opts=opts.LabelOpts(is_show=True,
                                                               color="white",
                                                               font_size=10,
                                                               rotate=45,
                                                               distance="insideRight",
                                                               margin=-5
                                                               ),
                                 axistick_opts=opts.AxisTickOpts(is_show=False),
                                 splitline_opts=opts.SplitLineOpts(
                                     is_show=True,
                                     linestyle_opts=opts.LineStyleOpts(type_="dashed", opacity=0.3)
                                 ),
                                 split_number=3,    # y轴均分刻度的数量
                                 ),

    )
    line.add_xaxis(data["x"])
    line.add_yaxis("热度", data["y"],
                   symbol="circle", symbol_size=8,
                   itemstyle_opts=opts.ItemStyleOpts(color="white", opacity=0.8))
    line.set_series_opts(
        linestyle_opts=opts.LineStyleOpts(width=3, color="white"),
        label_opts=opts.LabelOpts(is_show=False),
    )
    grid = Grid(init_opts=opts.InitOpts(width="100%", height="100%"))
    grid.add(
        line,
        grid_opts=opts.GridOpts(
            pos_top="20px",
            pos_left="40px",
            pos_right="20px",
            pos_bottom="30px",
        )
    )
    return grid


def showChart2(data):
    pie = Pie()
    pie.set_global_opts(
        legend_opts=opts.LegendOpts(
            type_="scroll",
            orient="vertical",
            selector_position="start",
            is_page_animation=True,
            pos_left="70%",
            pos_top="5%", pos_bottom="5%",
            border_width=0,
            textstyle_opts=opts.TextStyleOpts(color="#35353b", font_weight="bold")
        )
    )
    pie.add("", data,
            radius="85%",
            center=["35%", "50%"],      # 圆心位置
            label_opts=opts.LabelOpts(is_show=False,
                                      position="inside",
                                      font_size=10,
                                      color="white",))
    return pie


@chartApi.route("/chart1")
def chart1():
    db = DBManager()
    with db.session as cursor:
        # 热搜热度趋势
        hotsearchTrend = cursor.execute(text("select "
                                             "date_format(timeStamp, '%H:%i') as time, hot "
                                             "from hotsearch "
                                             "group by timeStamp "
                                             "order by timeStamp desc "
                                             "limit 10")).fetchall()
        hotsearchTrendData = {"x": list(x for x, y in hotsearchTrend[::-1]),
                              "y": list(y for x, y in hotsearchTrend[::-1])}
    # print(hotsearchTrendData)
    line = showChart1(hotsearchTrendData)
    return line.dump_options_with_quotes()


@chartApi.route("/chart2")
def chart2():
    db = DBManager()
    with db.session as cursor:
        data = cursor.execute(text(
            "select source, count(*) as count "
            "from comments "
            "group by source "
            "having source != '' "
            "order by count desc "
            "limit 15;"
        )).fetchall()

    pie = showChart2(data)
    return pie.dump_options_with_quotes()


# @chartApi.route("/chart2")
# def chart2():
#     db = DBManager()
#     with db.session as cursor:
