# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import os
import json

def get_config(key):
	file_path = os.getcwd() + '/config/dbconfig.json'
	fp = open(file_path)
	json_data = json.load(fp)
	fp.close()
	return json_data[key]