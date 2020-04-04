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

from flask import request
from flask import session
from flask import redirect
from functools import wraps
from define.define_consts import *
from server import StrictRedis as redis
from datetime import datetime
from datetime import timedelta
import json
import types
import re


class DictModel(dict):
    """
    字典模板
    """
    def __init__(self, *args, **kwarg):
        super(model, self).__init__(*args, **kwarg)
        for __attrbute in self.keys():
            setattr(self, __attrbute, self[__attrbute])

    def __values_to_model(self, value):
        if isinstance(value, (list, tuple, set)):
            _aval = []
            for _val in value:
                if isinstance(_val, dict):
                    _val = DictModel(_val)
                elif isinstance(_val, (list, tuple, set)):
                    _val = self.__values_to_model(_val)
                _aval.append(_val)
            _aval = value.__class__(_aval)
            return _aval
        elif isinstance(value, dict):
            value = DictModel(value)
        return value

    def __setattr__(self, key, value):
        try:
            if not hasattr(self, key):
                self[key] = value
                value = self.__values_to_model(value)
        except Exception as e:
            raise (e)
        super(DictModel, self).__setattr__(key, value)

    def __getattr__(self, key):
        return super(DictModel, self).__getattr__(self, key)

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        elif key in self.keys():
            return self.get(key)
        else:
            return super(DictModel, self).__getitem__(key)

    def __getattribute__(self, *args, **kwargs):
        return object.__getattribute__(self, *args, **kwargs)


