# -*- coding: utf-8 -*-
from pyecharts import Kline
from pyecharts import Grid
from pyecharts import Page
import pandas as pd
from sqlalchemy import create_engine
import datetime as dt
import os
def GreenArrow(datepoint, valuepoint, kaiping):
    dictionary = {"coord": [datepoint, valuepoint], "symbol": "arrow",
                  "value": str(valuepoint) + " " + kaiping, "symbolRotate": "180",
                  "itemStyle": {"normal": {"color": "#008000"}},
                  "symbolSize": "35"}
    return dictionary


def RedArrow(datepoint, valuepoint, kaiping):
    dictionary = {"coord": [datepoint, valuepoint], "symbol": "arrow",
                  "value": str(valuepoint) + " " + kaiping, "symbolSize": "35"}
    return dictionary


def drawKline(datadf, tradeRecorddf):
    datadf["datetime"] = datadf["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
    OHLC = df[["open", "close", "low", "high"]]
    OHLC = OHLC.values
    DATETIME = df["datetime"].values

    longOrderDF = tradeRecorddf[tradeRecorddf["direction"] == "long position"]
    longOrderDF = longOrderDF[["time", "deal price", "kaiping"]].values
    shortOrderDF = tradeRecorddf[tradeRecorddf["direction"] == "short position"]
    shortOrderDF = shortOrderDF[["time", "deal price", "kaiping"]].values
    markpointlist = []
    for longorders in longOrderDF:
        markpointlist.append(RedArrow(longorders[0], longorders[1], longorders[2]))
    for shortorders in shortOrderDF:
        markpointlist.append(GreenArrow(shortorders[0], shortorders[1], shortorders[2]))

    page = Page()
    grid = Grid(width=1920, height=900)
    kline = Kline("candlestick")
    kline.add("candlestick", DATETIME, OHLC, is_datazoom_show=True, datazoom_type='inside',
              datazoom_range=[90, 100], tooltip_tragger_on='mousemove|click', tooltip_axispointer_type='cross',
              is_label_show=False, mark_point_raw=markpointlist)
    grid.add(kline, grid_top="3%", grid_height="95%")
    page.add(grid)
    now = dt.datetime.now()
    today = now.strftime('%Y%m%d')
    time = now.strftime("%H_%M_%S")
    home = os.environ['HOME']
    page.render(home + "/Pictures/" + today + "/" + "plotKlineChartandSignal" + time + ".html")


if __name__ == "__main__":

    df = pd.read_csv(
        "/home/jiangsheng/TB.csv")
    tradeRecorddf = pd.read_csv(
        "/home/jiangsheng/git/gitflow-jsnanotrader/cmake-build-debug/src/strategy/JIANG_MT_IF_V1/traderecord/JIANG_MT_IF_V1_IF.csv")

    drawKline(df, tradeRecorddf)
