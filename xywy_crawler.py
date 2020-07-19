# -*- coding: utf-8 -*-

# --------------------------------
# Name:         xywy_crawler.py
# Author:       devshilei@gmail.com
# @Time         2020/7/19 上午11:56
# Description:  寻医问药网站数据爬取器
# --------------------------------

import requests as r
import os
from lxml import etree


def crawl_disease():
    """
    description: 抓取疾病数据
    :return:     将抓取的html数据保存至本地文件中
    """
    url_template = "http://jib.xywy.com/html/%s.html"
    char_list = list("abcdefghijklmnopqrstuvwxyz")
    for char in char_list:
        resp = r.get(url_template % char)
        if resp.status_code == 200:
            resp.encoding = "gb2312"
            with open("html/disease/list/%s.html" % char, mode="w", encoding="utf8") as f:
                f.write(resp.text)


def crawl_disease_detail():
    """
    description: 获取疾病详情页面
    :return:     将疾病详情页面文件存储至本地
    """
    # 疾病字母开头列表html文件存储路径
    root_fp = "html/disease/list"
    # 疾病详情 url 模板（套用后缀之后可以拼出全路径）
    detail_utl_template = "http://jib.xywy.com%s"
    for fn in os.listdir(root_fp):
        full_path = os.path.join(root_fp, fn)
        # 解析 html 文件
        if fn == "m.html":
            # 对于字母m开头的文件用gb2312编码解析【不用gb2312编码报错，原因未知】
            tree = etree.HTML(open(full_path, encoding="gb2312").read())
        else:
            tree = etree.HTML(open(full_path).read())
        # 解读出疾病详情页面 url
        disease_detail_urls = tree.xpath(
            "//div[@class='ks-ill-txt mt20']/ul/li/a/@href|//div[@class='ks-ill-txt']/ul/li/a/@href")
        # 解读出疾病名称【部分显示不全（含...）需要匹配后抓取详情页面，获取疾病全名
        disease_names = tree.xpath(
            "//div[@class='ks-ill-txt mt20']/ul/li/a/text()|//div[@class='ks-ill-txt']/ul/li/a/text()")
        if len(disease_names) > 0:
            for disease_detail_url, disease_name in zip(disease_detail_urls, disease_names):
                html_fn = fn[0] + "__" + disease_name
                if not os.path.exists("html/disease/detail/%s.html" % (html_fn)):
                    full_url = detail_utl_template % disease_detail_url
                    resp = r.get(full_url)
                    if resp.status_code == 200:
                        resp.encoding = "gb2312"
                        html_text = resp.text
                        disease_names = etree.HTML(html_text).xpath("//div[@class='jb-name fYaHei gre']/text()")
                        html_fn = fn[0] + "__" + disease_names[0]
                        if not os.path.exists("html/disease/detail/%s.html" % (html_fn)):
                            with open("html/disease/detail/%s.html" % (html_fn), mode="w", encoding="utf8") as f:
                                f.write(html_text)


def crawl_symptom():
    """
    description: 抓取症状数据
    :return:     将抓取的html数据保存至本地文件中
    """
    url_template = "http://zzk.xywy.com/p/%s.html"
    char_list = list("abcdefghijklmnopqrstuvwxyz")
    for char in char_list:
        resp = r.get(url_template % char)
        if resp.status_code == 200:
            resp.encoding = "gb2312"
            with open("html/symptom/list/%s.html" % char, mode="w", encoding="utf8") as f:
                f.write(resp.text)


def crawl_symptom_detail():
    """
    description: 获取症状详情页面
    :return:     将症状详情页面文件存储至本地
    """
    # 症状字母开头列表html文件存储路径
    root_fp = "html/symptom/list"
    # 症状详情 url 模板（套用后缀之后可以拼出全路径）
    detail_utl_template = "http://zzk.xywy.com%s"
    for fn in os.listdir(root_fp):
        full_path = os.path.join(root_fp, fn)
        # 解析 html 文件
        tree = etree.HTML(open(full_path).read())
        # 解读出症状详情页面 url
        symptom_detail_urls = tree.xpath("//div[@class='mt20']/ul/li/a/@href")
        # 解读出症状名称【部分显示不全（含...）需要匹配后抓取详情页面，获取症状全名
        symptom_names = tree.xpath("//div[@class='mt20']/ul/li/a/text()")
        if len(symptom_names) > 0:
            for symptom_detail_url, symptom_name in zip(symptom_detail_urls, symptom_names):
                html_fn = fn[0] + "__" + symptom_name
                if not os.path.exists("html/symptom/detail/%s.html" % (html_fn)):
                    full_url = detail_utl_template % symptom_detail_url
                    resp = r.get(full_url)
                    if resp.status_code == 200:
                        resp.encoding = "gb2312"
                        html_text = resp.text
                        symptom_names = etree.HTML(html_text).xpath("//div[@class='jb-name fYaHei gre']/text()")
                        html_fn = fn[0] + "__" + symptom_names[0]
                        if not os.path.exists("html/symptom/detail/%s.html" % (html_fn)):
                            with open("html/symptom/detail/%s.html" % (html_fn), mode="w", encoding="utf8") as f:
                                f.write(html_text)


if __name__ == "__main__":
    # 抓取疾病列表数据，保存至本地 html 文件中
    crawl_disease()
    # 抓取疾病详细网页数据
    crawl_disease_detail()
    # 抓取症状列表数据，保存至本地 html 文件中
    crawl_symptom()
    # 抓取症状详细网页数据
    crawl_symptom_detail()
    # pass
