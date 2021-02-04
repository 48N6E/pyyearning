#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import jsonpath
import time
import sys
import json
from flask import Flask


app = Flask(__name__)

@app.route('/excute/<token>/<id>',methods=['GET'])    
def execute_sql(token,id):
    # 执行工单
    data = {
        "type": 1,
        "perform": "sq.gui",
        "WorkId": id
    }
    data = json.dumps(data)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer" + " " + token
    }
    try:
        request = requests.post(api_url + '/api/v2/audit/execute', data=data, headers=headers)
    except Exception as f:
        print("执行语句发生报错，ErrorMsg：",f)
    else:
        return request.text

@app.route('/reject/<token>/<id>',methods=['GET'])    
def reject_sql(id,token):
    # 执行工单
    data = {
        "text": "驳回",
        "work": id
    }
    data = json.dumps(data)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer" + " " + token
    }
    try:
        request = requests.post(api_url + '/api/v2/audit/reject', data=data, headers=headers)
    except Exception as f:
        print("执行语句发生报错，ErrorMsg：",f)
    else:
        return request.text
      
if __name__ == "__main__":
    api_url = "http://yearning.hgj.net/"
    app.run(host='0.0.0.0',port=7000,debug=True)
