#!/usr/bin/python3
# -*- coding: utf-8 -*-
#author sq.gui

import requests
import jsonpath
import time
import sys
import json
from flask import Flask
from src.yearning import YearningDb


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

def sql_audit(token,database,dbsource,sql_result,sqltype):
    #sql审核
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer" + " " + token
    }
    if sqltype ==1:
        sqltype=True
    elif  sqltype ==0:
         sqltype=False
    data = {
            "database": database,
            "isDMl": sqltype,
            "source": dbsource,
            "sql": sql_result
    }
    #data = json.dumps(data)
    request = requests.put(api_url + 'api/v2/fetch/test',data=data,headers=headers)
    #print(request)
    return request.json()

def get_affectrow():
    获取工单执行后的信息
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer" + " " + token
    }
    request = requests.get(api_url + 'api/v2/fetch/detail?workid=' + str(id) + '&status=1',headers=headers)
    return request.json()

def data_process(work_list,token):
    #拼接发送消息
    sql_result=[]
    #注意如果msg信息的前面加#字体会加粗
    msg="""
======工单信息======
**工单号**: <font color="info">%s</font>
**提交者**: %s
**工单备注**: %s
**提交时间**: %s
**审核人**: %s
**SQL语句**:%s
**确认执行**:  [执行](http://yearning.hgj.net/myapi/excute/%s/%s)     [驳回](http://yearning.hgj.net/myapi/reject/%s/%s)
====== END ======
"""
    '''查询未执行的语句'''
    query="select * from core_sql_orders where status='2'"
    Yearning=YearningDb()
    work_id,username,date,sql,text,assigned,real_name,executor=Yearning.run(query)
    if work_id:
        for k in sql:
             sql_result.append('`'+k+'`')
             sql_result.append('\n')
        sql_records=''.join(sql_result)
        #sql语句过长会导致发送消息失败
        if len(sql_records) > 4096:
            sql_records="markdown.content exceed max length 4096"
        data= {
            "msgtype": "markdown",
            "markdown": {
            "content": msg %(str(work_id),\
                str(real_name),str(text),\
                str(date),str(assigned),sql_records,token,str(work_id),str(token),str(work_id))
                 }
            }
        return data,work_id
    else:
        return '',''

def send_wechat(data):
    headers={'Content-Type':'application/json','charset':'utf-8'}
    #yearning审核群
    url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=65a61d1a-9c14-4acd-a266-ade7fde04e3f"
    response = requests.post(url,data=json.dumps(data),headers=headers)
    print(response.text)
    return response.json()

def run():
    sendsuccess=[]
    while True:
        token = get_token()
        work_list = get_work(token)
        data,workid=data_process(work_list,token)
        if data and workid not in sendsuccess:
            result=send_wechat(data)
            print(result['errcode'])
            if result['errcode']==0:
                sendsuccess.append(workid)
                print(sendsuccess)
                time.sleep(30)

if __name__ == "__main__":
    api_url = "http://yearning.hgj.net/"
    run()
