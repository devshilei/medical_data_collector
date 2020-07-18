# -*- coding: utf-8 -*-#

# --------------------------------
# Name:         xywy_crawler.py
# Author:       devshilei@gmail.com
# Description:  收集寻医问药网站数据【疾病、症状、药品等信息】
# --------------------------------
import requests as r
from lxml import etree
char_list = list("abcdefghijklmnopqrstuvwxyz")
url_template = "http://jib.xywy.com/html/%s.html"
# 症状：http://zzk.xywy.com/p/a.html

html = r.get(url_template % "a")
html.encoding = "gb2312"
print(html.text)
