# _*_ coding:utf-8 _*_
from bs4 import BeautifulSoup

import re

def get_htmlvalues(filepath):
    """
         通过钉钉进行报警消息推送
         :param filepath:报告路径
         :return: html报告提取的内容
    """
    with open(filepath,'r',encoding='utf-8')as f_data:
           # 获取html内容
           Soup=BeautifulSoup(f_data,"html.parser")
           # 找到元素路径下的标签内容
           shot_name = Soup.select('body > div > div > p ')
           # 正则需要str格式
           result=str(shot_name)
           # 正则提取测试结果内容，邮件标题为str，需要转化格式
           res = str(re.findall(r'测试结果:</strong>(.*?)</p>',result))
           # 截取多余字符
           l = res.strip("['")
           R = l.strip("']")
           # 以逗号切片获取数据
           # key =R.split('，')
           # # 获取最后一个通过率文案
           # for value in key:
           #     values =value
           # 找到通过率位置，截取字符串
           index=R.find("通过率")
           values = R[index:]

    return values