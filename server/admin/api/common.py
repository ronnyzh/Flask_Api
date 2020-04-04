#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: $Project$
Filename: $Filename$
Author: $Date$
Date: $Date$
Revision: $Revision$
Description: $Description$
"""

from datetime import datetime
from flask import request, session
from flask_restplus import Resource
from server import StrictRedis as redis
from server.event import EventErrorResponse, EventSuccessResponse
from server import adminApi
from server.document import DocumentFormart
import time
import traceback

GAME_SETTING_RESPONSE_LIST_DOC = {"data": {
    "gameId": "游戏ID",
    "gameName": "游戏名称",
    "gameRule": [
        {
            "id": "场次ID",
            "title": "场次标题",
            "need": "限制[最低, 最高]",
            "baseScore": "低分",
            "cost": "准入",
            "maxMultiples": "倍率"
        },
    ],
    }
}

class GameSetting(Resource):
    @DocumentFormart.response_code(data=GAME_SETTING_RESPONSE_LIST_DOC)
    def get(self):
        """
        获取游戏设置列表
        """
        data = []
        try:
            return EventSuccessResponse.success_200({}, data=data)
        except Exception as err:
            return EventErrorResponse.error_401(msg=u'获取游戏设置列表失败')

    @DocumentFormart.request_model(data=GAME_SETTING_RESPONSE_LIST_DOC['data'])
    def post(self):
        """
        修改游戏设置
        """
        gameId = request.json.get("gameId", '').strip()
        data = []
        try:
            return EventSuccessResponse.success_200({}, data=data)
        except Exception as err:
            return EventErrorResponse.error_401(msg=u'修改游戏设置失败')

    @DocumentFormart.request_model(data=GAME_SETTING_RESPONSE_LIST_DOC['data'])
    def put(self):
        """
        新增游戏设置
        """
        gameId = request.json.get("gameId", '').strip()

        data = []
        try:
            return EventSuccessResponse.success_200({}, data=data)
        except Exception as err:
            return EventErrorResponse.error_401(msg=u'新增游戏设置失败')

    @DocumentFormart.request_param(data={"gameId": "游戏ID"})
    def delete(self):
        """
        删除游戏设置
        """
        gameId = request.args.get("gameId", '')
        data = []
        try:
            return EventSuccessResponse.success_200({}, data=data)
        except Exception as err:
            return EventErrorResponse.error_401(msg=u'删除游戏设置失败')


ns = adminApi.namespace('common', description=u"公共部分数据操作")
ns.add_resource(GameSetting, '/game/')
