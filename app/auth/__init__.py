#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/4/25

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
