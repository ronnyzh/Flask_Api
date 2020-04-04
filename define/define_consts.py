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

# app配置
APP_SECRET_KEY = 'B1Zr98j/3yX RTTG4!28N]3X31FE/,GOP'
APP_SESSION_TYPE = 'redis'
APP_SESSION_PERMANENT = False
APP_SESSION_USE_SIGNER = False
APP_SESSION_KEY_PREFIX = 'FlaskSession:'
APP_PERMANENT = True
APP_PERMANENT_SESSION_LIFETIME = 3600

# 查询在线玩家时,缓存保存时间(秒)
ONLINECACHESAVETIME = 30
# 是否使用mysql7+的版本
MYSQLVERSION7 = False
# 是否显示API文档
ISSHOWAPIDOC = True