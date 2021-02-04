#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import jsonpath
import time
import sys
import json


def get_token():
    # 获取认证的token
    data = {
        "username": "admin",
        "password": "admin123"
    }
    headers = {
        "Accept": "application/json"
    }
    request = requests.post(api_url + "ldapauth", data=data, headers=headers)
    request = request.json()
    print(request)
    token = jsonpath.jsonpath(request, "$.token")[0]
    return token


if __name__ == "__main__":
    api_url = "http://yearning.hgj.net/api/v1/"
    token = get_token()
    print(token)