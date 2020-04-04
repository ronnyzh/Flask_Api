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

from flask import Flask, Blueprint
from flask_session import Session
from flask_restplus import Api
from define.define_consts import *
from configs import CONFIGS
from imp import reload
import logging.config
import logging.handlers
import redis
import logging
import sys
import datetime

reload(sys)
try:
    sys.setdefaultencoding('utf-8')
except Exception as err:
    pass

# 蓝图配置
app = Flask(__name__)
adminPrint = Blueprint('admin', __name__, url_prefix='/admin')

adminApiPrint = Blueprint('admin_api', __name__, url_prefix='/admin/api')
adminApi = Api(adminApiPrint, doc='/doc/', version='1.0.0', title=u'API列表', description='')

# redis配置
redis_config = CONFIGS['redis']
StrictRedis = redis.StrictRedis(host=redis_config['host'], port=redis_config['port'], db=redis_config['db'],
                                password=redis_config['password'])

# app配置
app.config['SECRET_KEY'] = APP_SECRET_KEY
app.config['SESSION_TYPE'] = APP_SESSION_TYPE
app.config['SESSION_PERMANENT'] = APP_SESSION_PERMANENT
app.config['SESSION_USE_SIGNER'] = APP_SESSION_USE_SIGNER
app.config['SESSION_KEY_PREFIX'] = APP_SESSION_KEY_PREFIX
app.config['SESSION_REDIS'] = StrictRedis
app.config['PERMANENT'] = APP_PERMANENT
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(seconds=APP_PERMANENT_SESSION_LIFETIME)
Session(app)


def __logger():
    logging.config.dictConfig(CONFIGS['logger'])
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger = logging.getLogger("jobs")
    logger.addHandler(console)
    return logger


logger = __logger()

from server import admin

app.register_blueprint(adminApiPrint)
