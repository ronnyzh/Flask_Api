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

from flask_restplus import fields
from server import adminApi as api
from server.response.code import build_result
from flask_restplus.utils import merge
import json
import uuid

Token = api.header("token", description=u"TOKEN")


class DocumentFormart(object):
    __swich_fields_keys = {
        "str": fields.String,
        "int": fields.Integer,
        "float": fields.Float,
        "Decimal": fields.Arbitrary,
        "unicode": fields.String
    }

    @classmethod
    def NestedList(self, data):
        """
        返回列表中的数据
        """
        _fileds = {}
        for _key in data:
            if isinstance(_key, dict):
                _fileds = self.NestedDict(_key)
        return _fileds

    @classmethod
    def NestedDict(self, data):
        """
        返回字典里面的数据
        """
        return self.ResponseBody(data, "", response_fileds=True)

    @classmethod
    def ResponseBody(self, data, model_name, response_model="model", response_code="200", response_data="成功",
                     response_templates=None, response_fileds=False, function=None):
        """
        返回整个BODY
        """
        models = {}
        for _key in data:
            if isinstance(data[_key], dict):
                _fields = fields.Nested(model=api.model(
                    str(uuid.uuid1()).replace("-", ''), self.NestedDict(data[_key])))
            elif isinstance(data[_key], list):
                _fields = fields.List(fields.Nested(
                    model=api.model(str(uuid.uuid1()).replace("-", ''), self.NestedList(data[_key]))))
            else:
                try:
                    value = data[_key].decode("utf8")
                    _fields = self.__swich_fields_keys[value.__class__.__name__](
                        value, Description=value)
                except Exception as err:
                    _fields = self.__swich_fields_keys[data[_key].__class__.__name__](
                        data[_key], Description=data[_key])

            models[_key] = _fields
        if response_fileds:
            return models
        if response_model == "response":
            return api.response(
                response_code, response_data, model=api.model(model_name, models))
        return api.doc(body=api.model(model_name, models))

    @classmethod
    def response_code(self, code="200", response_data="成功", name=None, data={}):
        if not name:
            name = str(uuid.uuid1()).replace("-", '')
        return self.ResponseBody(data, name, response_model="response", response_data=response_data, response_code=code)

    @classmethod
    def request_model(self, code=0, name=None, data={}, **kwarg):
        if not name:
            name = str(uuid.uuid1()).replace("-", '')
        return self.ResponseBody(data, name, response_model="model")

    @classmethod
    def request_param(self, name=None, data={}, **kwarg):

        return api.doc(params=data)

    @classmethod
    def response_error(cls, code='200', msg="", data={}):
        code = int(code)
        result = build_result(status=code, data=data)
        if msg:
            result["msg"] = msg
        return cls.response_code(code=str(code), data=result, response_data=msg)
