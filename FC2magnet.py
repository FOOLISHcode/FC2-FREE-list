import getnewlist,checklist,getpic
import os,time


def main():
    tishi = '''
    1.更新数据库
    2.更新图片库
    3.同时更新
    4：退出程序

    请输入你需要的功能：
    '''
    i= ""

    while(i !='4'):
        os.system('cls')
        i= input(tishi)
        if i == '1':
            os.system('cls')
            print('正在执行步骤1.更新数据库')
            getnewlist.getnewlist()
            checklist.checklist()
            time.sleep(2)
        else: 
            if i == '2':
                os.system('cls')
                print('正在执行步骤2.更新图片库')
                getpic.getpic()
                time.sleep(2)
            else:
                if i == '3':
                    os.system('cls')
                    print('正在执行步骤1.更新数据库')
                    getnewlist.getnewlist()
                    checklist.checklist()
                    time.sleep(1)
                    os.system('cls')
                    print('正在执行步骤2.更新图片库')
                    getpic.getpic()

if __name__ == '__main__':
    main()

