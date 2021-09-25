'''
1.获取正确的url地址（）
2.发送网络请求（获得完整html代码）
3.筛选目标信息（番号，标题，磁力链接，上传时间，大小，news标记）
4.保存目标信息为xlsx
'''

from re import IGNORECASE
from numpy import e
import parsel
import requests
import pandas as pd
import re
from datetime import datetime
import os
import warnings
from configparser import ConfigParser
import time

def getresponse (isproxy,url,http_proxy,https_proxy):
    proxies = {'http': http_proxy, 'https': https_proxy}
    ex_proxy = {'http': 'http://localhost:7890', 'https': 'http://localhost:7890'}
    #定义代理地址
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
    #定义访问头
    i = 0
    while i < 3:
        try:
            if isproxy == 'no':                   
                response = requests.get(url=url,headers=headers,verify=False,timeout=5)
                    #get(链接地址，访问头，代理端口，不检测ssl证书)
                return response
            else:
                if isproxy == 'yes':
                    response = requests.get(url=url,headers=headers,proxies=proxies,verify=False,timeout=5)
                    return response
                else:
                    response = requests.get(url=url,headers=headers,proxies=ex_proxy,verify=False,timeout=5)
                    return response
                #get(链接地址，访问头，代理端口，不检测ssl证书)
                
        except Exception:
            i += 1
            print('与服务器断开链接，5s后进行第%s次尝试' % i)
            if i == 3:
                input('警告：与服务器链接失败，请设置代理或重试\n输入任意键退出程序')
                return exit()
            time.sleep(5)

#1.获取正确的url地址（）
def getnewlist():
    warnings.filterwarnings("ignore")       #忽略ssl认证警告
    getconfig = ConfigParser()
    try:
        getconfig.read('./config.ini',encoding='utf-8')
        isproxy = getconfig.get('可选设置','isproxy')
        http_proxy = getconfig.get('可选设置','http_proxy')
        https_proxy = getconfig.get('可选设置','https_proxy')
    except IOError as e:
        print(e)
    

    filedir = ['./data','./pic']
    for i in filedir:
        if not os.path.exists(i):
            os.makedirs(i)
    #proxies = {'http': 'http://localhost:7890', 'https': 'http://localhost:7890'}
    #定义代理地址
    url_list = ['https://sukebei.nyaa.si/?f=0&c=0_0&q=fc2&p=1']
    #定义真实地址池
    #headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
    #定义headers字典，伪装成真实chrome浏览器
    fc2_data = pd.DataFrame(columns=['num','title','magnet','size','uploadtime','isnews','ispic'])

    #将搜索fc2前十页真实地址添加到数组url_list中
    ''''''
    for i in range(2, 11):      #生成2-10的真实地址
        # %s 表示把URL变量转换为字符串
        url = 'https://sukebei.nyaa.si/?f=0&c=0_0&q=fc2&p=%s' % i
        #print(url)
        url_list.append(url)  
    ''''''
    #print(url_list)      

    #2发送网络请求（获得完整html代码）+ 3.筛选目标信息（番号，标题，磁力链接，上传时间，大小）
    for url in url_list:
        #2.发送网络请求（获得完整html代码）
        response = getresponse(isproxy,url,http_proxy,https_proxy)
        #get(链接地址，访问头，代理端口，不检测ssl证书)
        html_data = response.text
        print('正在处理：',url)
        #print(html_data) 用于返回状态码
        selector=parsel.Selector(html_data)
        #3.初步筛选目标信息（番号，标题，磁力链接，上传时间，大小）
        fc2_title_list = selector.xpath('//tbody/tr/td[2]/a/@title').getall()
        fc2_magnet_list = selector.xpath('//tbody/tr/td[3]/a[2]/@href').getall()
        fc2_size_list = selector.xpath('//tbody/tr/td[4]/text()').getall()
        fc2_uploadtime_list = selector.xpath('//tbody/tr/td[5]/text()').getall()
        for i in range(0,len(fc2_size_list)):
            #获取对应的番号
            x=re.compile('\d{6,7}').findall(fc2_title_list[i])
            if x != []:
                fc2_num = x[0]    
            else:
                fc2_num = 'no num'
            #格式化uploadtime为年月日，去掉时分
            fc2_uploadtime_go = datetime.strptime(fc2_uploadtime_list[i],'%Y-%m-%d %H:%M').date()
            #格式化size，统一单位为mib，并只保存数字部分，以便以后判断
            fc2_size_splitlist = str(fc2_size_list[i]).split(' ')
            if fc2_size_splitlist[1] == 'GiB':
                fc2_size_go = float(fc2_size_splitlist[0])*1000
            else:
                fc2_size_go=float(fc2_size_splitlist[0])
            #将番号，标题，磁链，大小，上传时间加入data词典，并逐行写入fc2_data中
            data = {'num':fc2_num, 'title': fc2_title_list[i], 'magnet': fc2_magnet_list[i], 'size': fc2_size_go, 'uploadtime': fc2_uploadtime_go,'isnews':'yes','ispic':'no'}
            #print(data)
            fc2_data = fc2_data.append(data,ignore_index=True)
            print('已添加第%s条数据:FC2-PPV-%s' % (i+1,fc2_num))


    #print(fc2_data)
    #4.保存目标信息为csv或者xlsx
    #fc2_data.to_csv('FC2_1to10.csv', index=False)
    filename = './data/FC2_1to10 %s.xlsx' % str(datetime.today().date())
    fc2_data.to_excel(filename,index=False)

if __name__ == '__main__' :
    getnewlist()
