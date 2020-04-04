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

from server import app

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=10334)
