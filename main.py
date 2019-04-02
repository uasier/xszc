#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
info:
author:uasier
github:https://github.com/uasier/
update_time:2019-4-1
"""

import time  # 用来延时
from selenium import webdriver  # selenium方式爬数据
import pymysql  # 用来操作数据库
import logging  # 设置日志

# 日志相关配置
logger = logging.Logger('log', level=logging.WARNING)
sh = logging.StreamHandler()
fh = logging.FileHandler('log.log', encoding='utf-8')
fmt = logging.Formatter('%(threadName)s %(levelname)s %(lineno)s行: - %(asctime)s\n\t %(message)s', '%d %H:%M')
sh.setFormatter(fmt)
fh.setFormatter(fmt)
logger.addHandler(sh)
logger.addHandler(fh)
logger.setLevel(logging.INFO)


def mysql_connect_init():  # 打开数据库连接
    print("mysql_connect_init()函数开始执行")
    global db  # 设置db为全局变量
    try:
        db = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='xszc',
            charset='utf8'
        )
        global cursor  # 设置游标对象 cursor为全局变量
        # 使用 cursor() 方法关联游标对象 cursor
        cursor = db.cursor()
    except Exception as error:
        print("数据库打开失败：", error)
    else:
        print("数据库打开成功")
    finally:
        print("setup_mysqlDB()函数执行完毕")


def create_table():  # 创建数据表
    print("create_table()函数开始执行")
    try:
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        cursor.execute("DROP TABLE IF EXISTS qa")
        # 使用预处理语句创建表
        sql = """CREATE TABLE qa (
                  id  int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                  question varchar(200) ,
                  answer varchar(200) ,
                  option1 varchar(200) ,
                  option2 varchar(200) ,
                  option3 varchar(200) ,
                  option4 varchar(200) ,
                  option5 varchar(200)
                  )"""
        # 执行语句
        cursor.execute(sql)
    except Exception as error:
        print("数据表创建失败：", error)
    else:
        print("数据表创建成功")
        print("执行execute()方法后影响的行数为：%d" % cursor.rowcount)
    finally:
        print("create_table()函数执行完毕")


def add_data(question, answer, option1='', option2='', option3='', option4='', option5=''):  # 向数据库中插入数据,选项默认全为空
    print("add_data()函数开始执行")
    try:
        # SQL 插入语句
        sql = "INSERT INTO qa(question, answer, option1, option2, option3, option4, option5)\
                    VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
              % (question, answer, option1, option2, option3, option4, option5)
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as error:
        print("数据插入失败：", error)
        # 发生错误数据库回滚
        db.rollback()
    else:
        print("数据插入成功")
        print("执行execute()方法后影响的行数为：%d" % cursor.rowcount)
    finally:
        print("add_multiple()函数执行完毕")


def select_data(question):  # 向数据库查询
    print("select_data()函数开始执行")
    try:
        # SQL 查询语句
        sql = "SELECT id FROM  qa \
               WHERE question = '%s'" % question
        # 执行sql语句
        cursor.execute(sql)
        result = cursor.fetchall()
        # 打印结果
        if not result:
            res = False
        else:
            res = True
    except Exception as error:
        print("数据查询失败：", error)
        # 发生错误数据库回滚
        db.rollback()
    else:
        print("数据数据查询成功")
        print("执行execute()方法后影响的行数为：%d" % cursor.rowcount)
        return res
    finally:
        print("select_data()函数执行完毕")


def close_mysql():  # 关闭数据库连接
    print("close_mysqlDB()函数开始执行")
    try:
        db.close()
    except Exception as error:
        print("数据库关闭失败：", error)
    else:
        print("数据库关闭成功")
        print("执行execute()方法后影响的行数为：%d" % cursor.rowcount)
    finally:
        print("close_mysqlDB()函数执行完毕")


def login():    # 登录系统
    tel = input('请输入你的账号：')
    pwd = input('请输入你的密码：')
    driver.get("https://user.scctedu.com/login")

    driver.find_element_by_id('doc-vld-name-2-1').clear()
    driver.find_element_by_id('doc-vld-name-2-1').send_keys(tel)  # 此处输入账号
    driver.find_element_by_id('doc-vld-pwd-1-0').clear()
    driver.find_element_by_id('doc-vld-pwd-1-0').send_keys(pwd)  # 此处输入密码
    driver.find_element_by_id('login-button').click()
    time.sleep(5)  # 等待


def single(num):   # 单选题处理
    driver.get("https://exam.scctedu.com/#/exam_analysis/" + num + "/1")
    time.sleep(5)  # 等待
    for index in range(1, 51):
        question = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
            index) + "]/div[1]/div/div/span[2]").text
        if select_data(question):
            continue
        else:
            option1 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[1]/span[2]/span[2]").text
            option2 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[2]/span[2]/span[2]").text
            option3 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[3]/span[2]/span[2]").text
            option4 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[4]/span[2]/span[2]").text
            answer1 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[1]/span[1]").get_attribute('class')
            answer2 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[2]/span[1]").get_attribute('class')
            answer3 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[3]/span[1]").get_attribute('class')
            answer4 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[4]/span[1]").get_attribute('class')
            answer = ''
            if answer1 == "ivu-radio ivu-radio-checked":
                answer = 'A'
            if answer2 == "ivu-radio ivu-radio-checked":
                answer = 'B'
            if answer3 == "ivu-radio ivu-radio-checked":
                answer = 'C'
            if answer4 == "ivu-radio ivu-radio-checked":
                answer = 'D'
            add_data(question, answer, option1, option2, option3, option4)


def multiple(num):   # 多选题处理
    driver.get("https://exam.scctedu.com/#/exam_analysis/" + num + "/2")
    time.sleep(5)  # 等待
    for index in range(1, 21):
        question = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
            index) + "]/div[1]/div/div/span[2]").text
        if select_data(question):
            continue
        else:
            option1 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[1]/span[2]/span[2]").text
            option2 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[2]/span[2]/span[2]").text
            option3 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[3]/span[2]/span[2]").text
            option4 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[4]/span[2]/span[2]").text
            option5 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[5]/span[2]/span[2]").text
            answer1 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[1]/span[1]").get_attribute('class')
            answer2 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[2]/span[1]").get_attribute('class')
            answer3 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[3]/span[1]").get_attribute('class')
            answer4 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[4]/span[1]").get_attribute('class')
            answer5 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[5]/span[1]").get_attribute('class')
            answer = ''
            if answer1 == "ivu-checkbox ivu-checkbox-checked":
                answer += 'A'
            if answer2 == "ivu-checkbox ivu-checkbox-checked":
                answer += 'B'
            if answer3 == "ivu-checkbox ivu-checkbox-checked":
                answer += 'C'
            if answer4 == "ivu-checkbox ivu-checkbox-checked":
                answer += 'D'
            if answer5 == "ivu-checkbox ivu-checkbox-checked":
                answer += 'E'
            print(answer)
            add_data(question, answer, option1, option2, option3, option4, option5)


def judge(num):   # 判断题处理
    driver.get("https://exam.scctedu.com/#/exam_analysis/" + num + "/3")
    time.sleep(5)  # 等待
    for index in range(1, 11):
        question = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
            index) + "]/div[1]/div/div/span[2]").text
        if select_data(question):
            continue
        else:
            answer1 = driver.find_element_by_xpath("//*[@class='paper-inner']/div/div[1]/div[" + str(
                index) + "]/div[2]/div/div/div/div[2]/div/label[1]/span[1]").get_attribute('class')
            if answer1 == "ivu-radio ivu-radio-checked":
                answer = '对'
            else:
                answer = '错'
            add_data(question, answer)


if __name__ == '__main__':  # 测试主函数
    driver = webdriver.Chrome()  # 选择浏览器，此处我选择的Chrome
    login()
    try:
        mysql_connect_init()  # 初始化数据库
        create_table()  # 数据库
        ran = 266902
        while ran < 267100:
            # noinspection PyBroadException
            try:
                driver.get("https://exam.scctedu.com/#/home")  # 用来强制更新页面
                single(str(ran))
                multiple(str(ran))
                judge(str(ran))
            except Exception as err:    # 捕捉任何异常，保证程序可以继续运行下去
                logger.critical(str(ran) + " : " + str(err))
                # 如果出问题了，那就直接跳过这个
            finally:
                ran = ran + 1
    except Exception as err:
        print("程序执行出错：", err)
    else:
        print("程序执行成功")
    finally:
        print("main执行完毕")
