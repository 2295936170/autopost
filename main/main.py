# coding=utf-8
import json
import requests
import getinfo
import mail

def run(user, UA, cook):
    # 读取个人提交信息
    info = getinfo.data(UA, cook)
    # 提交今日打卡
    url = 'https://yq.weishao.com.cn/api/questionnaire/questionnaire/addMyAnswer'
    head = {
        'Host': 'yq.weishao.com.cn',
        'Connection': 'keep-alive',
        'User-Agent': UA,
        'Accept': '*/*',
        'Content-Length': str(len(str(info))),  # json转文字读取长度，再转为字符串
        'Content-Type': 'application/json',
        'Origin': 'https://yq.weishao.com.cn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://yq.weishao.com.cn/questionnaire/addanswer?page_from=onpublic&activityid=5416&can_repeat=1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN, zh;q = 0.9',
        'Cookie': cook,
    }
    data = json.loads(requests.post(url, json=info, headers=head).text)
    if data.get("errcode") == 0:
        print("打卡成功！")
        if user.get("notice") == "true":
            print("正在发送邮件···")
            mail.send(user.get("email"), user.get("name"))

    elif data.get("errcode") == 500:
        print("今日打卡已完成，自动打卡取消\n")
    else:
        print("未知的errcode\n" + str(data))
