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

from flask import abort, jsonify, make_response


class EventFiltersMakeResponse(object):
    """
    默认的filter层
    主要提供make_response的一些默认response
    """

    @classmethod
    def default(cls, response):
        rst = make_response(jsonify(response), response["status"])
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent,x-requested-with,content-type"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst


class EventFiltersControlResponse(object):
    """
    控制器返回层
    主要提供一些控制返回结果
    """
    pass


class EventErrorResponse(object):
    """
    控制器返回层
    主要提供一些失败控制返回结果
    """

    @classmethod
    def error_control(cls, msg="控制器出錯"):
        return make_response(jsonify({"status": 404, "msg": msg, 'code': -1}), 404)

    @classmethod
    def error_404(cls, msg="失败"):
        return make_response(jsonify({"status": 404, "msg": msg, 'code': -1}), 404)

    @classmethod
    def error_401(cls, msg="认证失败"):
        return make_response(jsonify({"status": 401, "msg": msg, 'code': -1}), 401)

    @classmethod
    def error_402(cls, msg="失败"):
        return make_response(jsonify({"status": 402, "msg": msg, 'code': -1}), 402)

    @classmethod
    def error_403(cls, msg="失败"):
        return make_response(jsonify({"status": 403, "msg": msg, 'code': -1}), 403)

    @classmethod
    def error_405(cls, msg="失败"):
        return make_response(jsonify({"status": 405, "msg": msg, 'code': -1}), 405)

    @classmethod
    def error_400(cls, msg="失败"):
        return make_response(jsonify({"status": 400, "msg": msg, 'code': -1}), 400)


class EventSuccessResponse(object):
    """
    控制器返回层
    主要提供一些成功控制返回结果
    """

    @classmethod
    def success_200(cls, response, msg="成功", data={}, code=0, **kwargs):
        if data:
            sucessResponse = {"status": 200, "msg": msg, "data": data, 'code': code}
        else:
            sucessResponse = {"status": 200, "msg": msg, 'code': code}
        sucessResponse.update(kwargs)
        rst = make_response(jsonify(sucessResponse), 200)
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent,x-requested-with,content-type"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst

    @classmethod
    def fail(cls, response, msg="失败", data={}):

        rst = make_response(jsonify(response), 400)
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent,x-requested-with,content-type"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
