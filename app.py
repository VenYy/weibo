from flask import Flask, render_template, Blueprint
from showCharts import *
from datetime import timedelta
from spider.DBManager import *

app = Flask(__name__)

app.config["DEBUG"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=1)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=1)

# 注册蓝图
app.register_blueprint(chartApi)


@app.route('/')
def index():
    db = DBManager()
    with db.session as cursor:
        # 话题数量变化
        topicsData = cursor.execute(text("SELECT COUNT(DISTINCT word), "
                                         "CONCAT(IF(COUNT(DISTINCT CASE WHEN DATE(timeStamp) = DATE(NOW()) "
                                         "THEN word ELSE NULL END) - COUNT(DISTINCT CASE WHEN DATE(timeStamp) = "
                                         "DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)) "
                                         "THEN word ELSE NULL END) >= 0, '+', '-'),"
                                         "ABS(COUNT(DISTINCT CASE WHEN DATE(timeStamp) = DATE(NOW()) "
                                         "THEN word ELSE NULL END) - COUNT(DISTINCT CASE WHEN DATE(timeStamp) = "
                                         "DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)) THEN word ELSE NULL END))) "
                                         "FROM topic")).fetchone()
        if topicsData:
            topicCount = topicsData[0]
            topicCountChanged = topicsData[1]

        # 热搜数量变化
        searchData = cursor.execute(text("SELECT COUNT(DISTINCT word),"
                                         "CONCAT("
                                         "IF(COUNT(DISTINCT "
                                         "IF(DATE(timeStamp) = DATE(NOW()), word, NULL)) - COUNT(DISTINCT "
                                         "IF(DATE(timeStamp) ="
                                         "DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)),"
                                         "word, NULL)) >= 0, '+', '-'),"
                                         "ABS(COUNT(DISTINCT "
                                         "IF(DATE(timeStamp) = DATE(NOW()), word, NULL)) - COUNT(DISTINCT IF("
                                         "DATE(timeStamp) = DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)), word, NULL)))"
                                         ") FROM hotsearch;")).fetchone()
        if searchData:
            searchCount = searchData[0]
            searchCountChanged = searchData[1]

        # 发文数量变化
        mData = cursor.execute(text("SELECT COUNT(DISTINCT mid),"
                                    "CONCAT("
                                    "IF(COUNT(DISTINCT "
                                    "IF(DATE(timeStamp) = DATE(NOW()), mid, NULL)) - COUNT(DISTINCT "
                                    "IF(DATE(timeStamp) ="
                                    "DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)),"
                                    "mid, NULL)) >= 0, '+', '-'),"
                                    "ABS(COUNT(DISTINCT "
                                    "IF(DATE(timeStamp) = DATE(NOW()), mid, NULL)) - COUNT(DISTINCT IF("
                                    "DATE(timeStamp) = DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)), mid, NULL)))"
                                    ") FROM hotsearch;")).fetchone()
        if mData:
            mCount = mData[0]
            mCountChanged = mData[1]

        # 评论数量变化
        commentsData = cursor.execute(text(
            "SELECT COUNT(DISTINCT comment_id), CONCAT(IF(COUNT(DISTINCT IF(DATE(created_at) = DATE(NOW()), "
            "comment_id, NULL)) - COUNT(DISTINCT IF(DATE(created_at) = DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)), "
            "comment_id, NULL)) >= 0, '+', '-'), ABS(COUNT(DISTINCT IF(DATE(created_at) = DATE(NOW()), comment_id, "
            "NULL)) - COUNT(DISTINCT IF(DATE(created_at) = DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)), comment_id, "
            "NULL))))FROM comments;")).fetchone()
        if commentsData:
            commentsCount = commentsData[0]
            commentsCountChanged = commentsData[1]

        # 今日热搜数量
        searchCountToday = cursor.execute(text("SELECT COUNT(distinct word) "
                                               "FROM hotsearch "
                                               "WHERE DATE(timeStamp) = CURDATE() "
                                               "AND word NOT IN "
                                               "(SELECT DISTINCT word FROM hotsearch "
                                               "WHERE DATE(timeStamp) < CURDATE())")).fetchone()[0]

        # 最新话题
        topicList = cursor.execute(text(
            "SELECT word, mention, `read`, link, timeStamp "
            "FROM topic "
            "WHERE date(timeStamp) = (SELECT MAX(date(timeStamp)) FROM topic) "
            "order by timeStamp desc limit 10;"
        )).fetchall()

        # 热搜Top 10
        hotsearchList = cursor.execute(text(
            "select distinct word, hot, href "
            "from hotsearch "
            "order by timeStamp desc, "
            "hot desc limit 10;"
        )).fetchall()

    return render_template("index.html",
                           topicsCount=topicCount, topicCountChanged=topicCountChanged,
                           searchCount=searchCount, searchCountChanged=searchCountChanged,
                           mCount=mCount, mCountChanged=mCountChanged,
                           searchCountToday=searchCountToday,
                           commentsCount=commentsCount, commentsCountChanged=commentsCountChanged,
                           topicList=topicList, hotsearchList=hotsearchList)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/topics")
def topics():
    return render_template("topics.html")


if __name__ == '__main__':
    app.run(debug=True)
