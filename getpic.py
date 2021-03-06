'''
第三阶段：
1.获取当天已经更新的all数据，提取isnews列为yes对应的num列的值
2.获取正确的链接地址列表（将得到num值与fc2官网寻找页面结合形成列表
3.发送网络请求（获得完整html代码）
4.筛选目标信息（是否存在预览图片，是则保存图片数量、图片链接，否则返回nodata）
5.逐一访问图片链接并按（fc2番号_图片序号）保存目标信息为jpg，保存到pic文件夹
'''


import pandas as pd
import requests
import parsel
import time
import warnings
import threading

from getnewlist import getresponse
from Config import Config

class Download_Thread (threading.Thread):
    def __init__(self, threadID, this_url_num, isproxy, pic_url, http_proxy, https_proxy, i):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.this_url_num = this_url_num
        self.isproxy = isproxy
        self.pic_url = pic_url
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.i = i
    def run(self):
        #print ("开始线程：" + self.threadID)
        downloadpic(self.this_url_num, self.isproxy,self.pic_url,self.http_proxy,self.https_proxy,self.i)
        #print ("退出线程：" + self.threadID)

def getpicresponse (isproxy,url,http_proxy,https_proxy):
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
            if i==3:
                return '0'

def downloadpic(this_url_num,isproxy,pic_url,http_proxy,https_proxy,i):
    
    #print(pic_url)
    pic_response = getpicresponse(isproxy,pic_url,http_proxy,https_proxy)
    if pic_response !='0':
        pic_data = pic_response.content
        pic_filename = './pic/%s_%s.jpg' % (this_url_num,i+1)
        with open(pic_filename,'wb') as f:
            f.write(pic_data)
            print('%s_%s.jpg 下载完毕' % (this_url_num,i+1))
            f.close
    else:
        print('%s_%s.jpg 下载失败' % (this_url_num,i+1))

def getpic():            

    warnings.filterwarnings("ignore")       #忽略ssl认证警告
    
    #获取config.ini配置参数
    getconfig = Config()
    isproxy = getconfig.isproxy
    http_proxy = getconfig.http_proxy
    https_proxy = getconfig.https_proxy
    isdown_bigpic = getconfig.isdown_bigpic
    getconfig.printconfig()

    
    #1.获取当天已经更新的all数据，提取isnews列为yes对应的num列的值

    try:
        filename = './data/FC2_ALL.xlsx'
        all_df = pd.read_excel(filename)
    except Exception:
        input('没有找到主记录文件，请先运行 1.更新数据库\n任意键退出')
        exit()
    index_list = all_df.loc[(all_df['ispic'] == 'no')].index
    num_list = []
    for i in index_list:
        num_list.append(all_df['num'][i])

    #2.获取正确的链接地址列表（将得到num值与fc2官网寻找页面结合形成列表

    links_list = []
    for num in num_list:
        links_list.append('https://adult.contents.fc2.com/article/%s/' % num)

    #3.发送网络请求（获得完整html代码）


    tiktok = 0
    sum = 0

    for url in links_list:
        this_url_num = url.split('/')[-2]

        #2.发送网络请求（获得完整html代码）

        html_data = getresponse(isproxy,url,http_proxy,https_proxy).text
        if html_data != '0':
            print('正在处理：',url)
            #print(html_data) 用于返回状态码
            selector=parsel.Selector(html_data)

            #4.筛选目标信息（是否存在预览图片，是则保存图片数量、图片链接，否则返回nodata）
            if isdown_bigpic =='yes':
            #预览原图（清晰，体积大）
                fc2_pic_list = selector.xpath("//ul[@class ='items_article_SampleImagesArea']/li/a/@href").getall()
            else:
            #缩略版预览图（较模糊，体积小）
                fc2_pic_list = selector.xpath("//ul[@class ='items_article_SampleImagesArea']/li/a/img/@src").getall()
            if fc2_pic_list != []:
                #5.逐一访问图片链接并按（fc2番号_图片序号）保存目标信息为jpg，保存到pic文件夹
                threads = []
                print('找到的预览图片共%s张' % len(fc2_pic_list))
                for i in range(0,len(fc2_pic_list)):
                    if isdown_bigpic == 'yes':
                        pic_url = fc2_pic_list[i]
                    else:
                        pic_url = 'https:' + fc2_pic_list[i]
                    try:
                        thread = Download_Thread(i,this_url_num,isproxy,pic_url,http_proxy,https_proxy,i)
                        thread.start()
                        threads.append(thread)
                    except:
                        print ("Error: 无法启动线程")
                if threads != []:        
                    for t in threads:
                        t.join()                    
            else:
                print('当前资源没有预览图')
            time.sleep(1)

            all_df.loc[all_df['num'] == int(this_url_num),['ispic']] = 'yes'

            #设置休眠，防止被服务器拒绝
            tiktok=tiktok + 1
            if tiktok == 5:
                print('休眠5s中，防止服务器拒绝')
                time.sleep(5)
                tiktok = 0

            #每下载20个资源的预览图片，保存一次数据
            sum += 1
            if sum > 20 :
                all_df.to_excel(filename,index=False)
                sum = 0
            
    all_df.to_excel(filename,index=False)

if __name__ == '__main__' :
    getpic()