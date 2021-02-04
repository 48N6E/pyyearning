#!/usr/bin/python3
# -*- coding: utf-8 -*-
#author sq.gui

import requests
import jsonpath
import time
import sys
import json
from flask import Flask


app = Flask(__name__)

def get_token():
    # 获取认证的token
    data = {
        # "username": "admin",
        # "password": "Yearning_admin"
        "username": "admin",
        "password": "admin123"
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    request = requests.post(api_url + "login", data=data, headers=headers)
    request = request.json()
    token = jsonpath.jsonpath(request, "$.token")[0]
    return token

def get_work(token):
    # 获取工单列表
    headers = {
        "Authorization": "Bearer" + " " + token,
        "Content-Type": "application/json"
    }
    data = {
        'page': 1,
        'find': {'picker': ['', ''], 'user': '', 'valve': False}
    }
    #data="{\"page\":1,\"find\":{\"picker\":[\"\",\"\"],\"user\":\"\",\"valve\":false}}"
    data = json.dumps(data)
    request = requests.put(api_url + 'api/v2/audit',data=data, headers=headers)
    return request.json()
    
def get_sql(id,token):
    # 获取工单里面的sql
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer" + " " + token
    }
    request = requests.get(api_url + 'api/v2/audit/sql?k=' + str(id),headers=headers)
    return request.json()

def sql_audit(token,database,dbsource,sql_result):
    #sql审核
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer" + " " + token
    }
    data = {
            "database": database,
            "isDMl": True,
            "source": dbsource,
            "sql": sql_result
    }
    #data = json.dumps(data)
    request = requests.put(api_url + 'api/v2/fetch/test',data=data,headers=headers)
    #print(request)
    return request.json()
    
# def get_affectrow():
    #获取工单执行后的信息
    # headers = {
        # "Accept": "application/json",
        # "Authorization": "Bearer" + " " + token
    # }
    # request = requests.get(api_url + 'api/v2/fetch/detail?workid=' + str(id) + '&status=1',headers=headers)
    # return request.json()
    
def data_process(work_list,token):
    #拼接发送消息
    sql_result=[]
    affect_rows=[]
    #注意如果msg信息的前面加#字体会加粗
    msg="""
======工单信息======
**工单号**:      <font color="info">%s</font>
**提交者**:      %s
**工单备注**:    %s
**提交时间**:    %s
**执行者**:      %s
**SQL语句**:  %s
**影响行数**:    %s
**确认执行**:    [执行](http://yearning.hgj.net/myapi/excute/%s/%s)     [驳回](http://yearning.hgj.net/myapi/reject/%s/%s)
====== END ======
"""
    for v in work_list['data']:
        id=v['WorkId']
        status=v['Status']
        type=v['Type']
        realname=v['RealName']
        text=v['Text']
        date=v['Date']
        executor=v['Executor']
        if status == 2: #1表示已经执行，2表示未执行，status=4表示工单执行失败            
            sql_list=get_sql(id,token)
            dbsource=sql_list['source']
            database=sql_list['base']
            for i in sql_list['sql']:
                sql=i['SQL']
                sql_result.append('`'+sql+'`'+'\n')
                affect_info=sql_audit(token,database,dbsource,sql_result)
                for row in affect_info:
                    affect_rows.append(row['AffectRows'])
            #int型列表转换为字符
            affectRow=map(str,affect_rows)
            affectRowStr=' '.join(affectRow)
            sql_records='\n'.join(sql_result)
            #sql语句过长会导致发送消息失败
            if len(sql_records) > 4096:
                sql_records="markdown.content exceed max length 4096"
            data= {
                "msgtype": "markdown",
                "markdown": {
                    "content": msg %(str(id),\
                    str(realname),str(text),\
                    str(date),str(executor),sql_records,affectRowStr,token,str(id),str(token),str(id))
                    }
                }
            return data

def send_wechat(data):
    headers={'Content-Type':'application/json','charset':'utf-8'}
    #钉钉测试群
    #url="https://oapi.dingtalk.com/robot/send?access_token=2045ac887b4823de09fcc0610af228a28a3b6e39b4af110287c6913ec67ae798"
    #测试专用群
    url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=65a61d1a-9c14-4acd-a266-ade7fde04e3f"
    response = requests.post(url,data=json.dumps(data),headers=headers)
    print(response.text)

def run():
    while True:
        token = get_token()
        work_list = get_work(token)
        # print(work_list)
        data=data_process(work_list,token)
        if data:
            send_wechat(data)
            time.sleep(30)

if __name__ == "__main__":
    api_url = "http://yearning.hgj.net/"
    run()
