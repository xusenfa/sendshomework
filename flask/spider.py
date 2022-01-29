# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import requests
import sqlite3
import lxml
import sys
import os


def main():
    newsdatalist = getdata()  #爬取并处理数据
    writedata(newsdatalist) #写入数据到数据库


def getdata():  #爬取并处理数据
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69'}  #UA
    hdxwurl = 'https://www.hqu.edu.cn/hdxw.htm'  #华大新闻URL
    try:
        pagesourcecode = BeautifulSoup((requests.get(hdxwurl, headers=headers).content), 'lxml')  #解析新闻页面
    except Exception:
        print('获取页面失败，请检查网络等原因后重试')
        sys.exit(0)
    a = pagesourcecode.select('#l-container > div > div.col_news > div.col_news_con > div > table')   #用css选择器查找包含新闻标题和链接的部分
    b = str(a[0]) #将结果转换为字符串
    newsdatalist= [] #创建一个列表存储接下来得到的所有标题及链接
    c=re.findall(r'<font color="">(.*?)</font>',b) #搜索标题
    d=re.findall(r'info.+htm',b) #搜索链接
    for i in range(0,25):
        data=[] #存储单个标题及链接
        data.append(c[i])
        data.append('https://www.hqu.edu.cn/'+d[i])
        newsdatalist.append(data) #将单组标题链接写入到newsdatalist
    return newsdatalist


def init_db():  #初始化数据库
    if os.path.exists("newsdata.db"):  #表已经存在，不创建新表
        pass
    else:  #表不存在，创建新表
        sql = '''
        create table hdxw 
        (
        Num INTEGER PRIMARY KEY autoincrement NOT NULL,
        title TEXT NOT NULL,
        link TEXT NOT NULL
        )
        '''  #创建表语句
        connect = sqlite3.connect('newsdata.db')
        cursor = connect.cursor()
        cursor.execute(sql)
        connect.commit()
        cursor.close()
        connect.close()


def writedata(newsdatalist):  #写入数据到数据库
    init_db()
    connect = sqlite3.connect('newsdata.db') #连接到数据库
    cursor = connect.cursor()
    for i in range(len(newsdatalist)):
        sql='''
            replace into hdxw (
                Num,
                title,
                link
            )
            values('%d','%s','%s'
                )
            '''%(i+1,newsdatalist[i][0],newsdatalist[i][1])
        cursor.execute(sql)
        connect.commit()
    cursor.close()
    connect.close()


if __name__ == "__main__":
    print('爬取开始')
    main()
    print('爬取完毕')