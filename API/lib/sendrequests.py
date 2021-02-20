# _*_ coding:utf-8 _*_
import os,sys,json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import requests
import urllib3
from API.lib.writeexcel import WriteExcel
from API.config import setting
from API.lib.readexcel import ReadExcel
import re
from jsonpath_rw import parse
urllib3.disable_warnings()
class SendRequests():
    def sendRequests(self,apiData):
        """
        发送接口请求
        :param apiData:接口请求数据
        :return: 返回接口响应信息，以json格式
        """
        try:
            # 发送请求数据
            method = apiData["method"]
            url = apiData["url"]
            if apiData["params"] == "":
                par = None
            else:
                par = eval(apiData["params"])
            if apiData["headers"] == "":
                h = None
            else:
                h = eval(apiData["headers"])
            if apiData["body"] == "":
                body_data = None
            else:
                body_data = eval(apiData["body"])

            type = apiData["type"]
            v = False
            if type == "data":
                body = body_data
            elif type == "json":
                body =json.dumps(body_data)
            else:
                body = body_data
            re =requests.request(method=method,url =url, headers =h,params = par,data = body,verify = v)
            msg = json.loads(re.text)
            msg['status_code']=re.status_code
            return msg

        except Exception as e:
            print(e)


    def connect_request(self,data,rowNum,sheetname):
        """
        关联接口：写入关联数据，找到对应关联接口，取出对应数据，作为关联接口的参数传递
        有take_key的，是取数据的接口信息
        有conncet_key，是需要用到取出的数据的接口信息，conncet_id是需要用到取出的数据的接口所关联的那个接口的用例id
        :param data:读取表格的请求数据
        :param rowNum:对应数据的行数
        :param sheetname:读取的表格
        :return: 返回接口响应信息
        """
        #如果有关联参数take_key,则在有take_key的数据那行写入对应响应的数据，为下一个有关联的接口做参数化的数据准备
        if data['take_key']!="":
                result = SendRequests().sendRequests(data)
                #print("响应数据：",result)
                WriteExcel(setting.Source_File,sheetname).connectdata_write(data['take_key'],result,rowNum+1)
                return result
        #没有关联参数take_key，有两种可能：一、不是有关联数据的接口，直接请求；二、需要用到关联数据的接口，会有关联的关键字connect_key
        else:
            #如果是需要关联数据的接口
                if data['connect_key']!="":
                   #写入关联数据后需要重新获取数据信息
                   allDatas=[]
                   for i in range(len(sheetname)):
                      allDatas += ReadExcel(setting.Source_File,sheetname).read_data(sheetname)
                      print("有关联接口的重新获取的表的接口数据：",allDatas)
                   for keys in allDatas:
                       #遍历数据，如果匹配到对应的用例编号，就去找对应id中的关联数据
                      print("新的每一轮数据：",keys)
                      if data['connect_id'] in keys['ID']:
                         connect_list ={}
                         print("需要关联的参数值take_data:",keys['take_data'])
                         #多个关联参数的，需要去掉【】、''的格式
                         keys_word = keys['take_data'].strip().strip('[]')
                         keys_string = re.sub('\'', '',keys_word)
                         take_list=keys_string.split(",")
                         print("以逗号重新切割的参数值列表take_list:",take_list)
                         #需要关联数据的接口如果有多个关联参数
                         if "," in data['connect_key']:
                            connect_key_list=data['connect_key'].split(",")
                            print("以逗号重新切割的关联参数列表connect_key_list：",connect_key_list)
                            connect_list=dict(zip(connect_key_list, take_list))
                            print("对应关联参数和参数值列表connect_list：",connect_list)
                         #需要关联数据的接口只有一个关联参数
                         else:
                            connect_key_list=data['connect_key']
                            print("只有一个关联参数connect_key：",connect_key_list)
                            connect_list[data['connect_key']]=keys['take_data']
                            print("只有一个关联参数组合成的参数与参数值列表connect_list：",connect_list)
                        #找到关联接口数据中参数化的值$XX，取$后面要匹配的参数
                         variable_keys =[str(key).split("$")[1] for key in re.findall("\$[A-za-z0-9]+", str(data))]
                         print("替换数据列表：",variable_keys)
                         i=0
                         target_data=data
                         for variable_key in variable_keys:
                             print("传参中需要替换的值variable_key：",variable_key)
                             for connect_value in connect_list:
                                 print("对应参数列表里面的值connect_value：",connect_value)
                                 if variable_key == connect_value:
                                   connect_target = "\""+connect_list[variable_key]+"\""
                                   print("加上""的替换的值",connect_target)
                                   request_data = str(target_data).replace("$"+variable_key, str(connect_target))
                                   print("替换后的请求数据",request_data)
                                   target_data=request_data
                                   print("下一轮需要替换的请求数据",target_data)
                                 else:
                                   print("数据匹配不一致！")
                         #转化为字符串格式
                         request_dict = eval(request_data)
                         result = SendRequests().sendRequests(request_dict)
                         #print("响应数据：",result)
                         return result
                else:
                   result = SendRequests().sendRequests(data)
                   #print("响应数据：",result)
                   return result


