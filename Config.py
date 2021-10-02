from configparser import ConfigParser
class Config:
    isproxy = ''
    https_proxy = ''
    http_proxy = ''
    listnum = 0
    isdown_bigpic = ''
    
    def __init__(self,path = './config.ini'):
        config = ConfigParser()
        try:
            config.read(path,encoding='utf-8')
            try:
                self.isproxy = config.get('可选设置','isproxy')
                if self.isproxy != 'yes' or self.isproxy != 'no':
                    self.isproxy = 'yes'
            except Exception:
                self.isproxy = 'yes'
            try:
                self.http_proxy = config.get('可选设置','http_proxy')
            except Exception:
                self.http_proxy = 'http://localhost:7890'
            try:
                self.https_proxy = config.get('可选设置','http_proxy')
            except Exception:
                self.https_proxy = 'http://localhost:7890'
            try:
                self.listnum = int(config.get('可选设置','listnum'))
            except Exception:
                self.listnum = 10
            try:
                self.isdown_bigpic = config.get('可选设置','isdown_bigpic')
                if self.isdown_bigpic != 'yes' or self.isdown_bigpic != 'no':
                    self.isdown_bigpic = 'no'
            except Exception:
                self.isdown_bigpic = 'no'
        except Exception:
            self.isproxy = 'yes'
            self.http_proxy = 'http://localhost:7890'
            self.https_proxy = 'http://localhost:7890'
            self.listnum = 10
            self.isdown_bigpic = 'no'


    def printconfig(self):
        text = f'''
        是否代理：{self.isproxy}
        http：{self.http_proxy}
        https：{self.https_proxy}
        下载页数：{self.listnum}
        是否下载原图：{self.isdown_bigpic}
        '''
        print(text)

