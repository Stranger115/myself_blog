#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _author: Stranger
# date: 2018/5/29
from flask import Blueprint

article = Blueprint('article', __name__)

from . import view