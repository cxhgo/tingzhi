import requests
import json
def dingding(num,case_name,api,status,msg):

    """
         通过钉钉进行报警消息推送
         :param num:测试用例编号
         :param case_name：测试用例名称
         :param api：测试接口
         :param status：测试响应状态码
         :param msg：测试响应信息字段msg
         :return: 无
    """
    number = str(num)
    text_status = str(status)
    text_msg = str(msg)
    # text参数必须是str类型，所以需要转化数据格式
    text = str("用例编号："+number+"\n"+"接口:"+case_name+"\n"+api+"\n"+"测试不通过"+"\n"+"响应状态码："+text_status+"\n"+"响应信息msg："+text_msg)
    # 钉钉机器人推送信息接口，不同机器人access_token不同，目前为数据智能中心监控告警机器人
    url='https://oapi.dingtalk.com/robot/send?access_token=b110a5c9050fd5ed76682fc47563a01442306d7dc938a66f0e9ecd68d73c2fcf'
    program={
     "msgtype": "text",
     "text": {"content":text},
    }
    headers={'Content-Type': 'application/json'}
    f=requests.post(url,data=json.dumps(program),headers=headers)
    print("钉钉返回信息：",f.text)