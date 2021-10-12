# FC2-FREE-list  latest version：Ver 1.4

用于搜索最近已有的fc2磁链资源并形成网页列表的傻瓜式小工具，方便自行选择下载
#
使用方法（仅适合windows 10环境，win7需要自行安装环境包）：

1.下载FC2freelist ver1.4.zip.001和FC2freelist ver1.4.zip.002并解压缩到任意位置

2.在config.ini选择是否代理及是否下载预览原图（选填，不更改将使用默认配置运行）

3.双击FC2freelist.exe→输入3，回车→等待爬虫程序爬完所需资源（速度快慢由您的网络环境决定）

4.打开home.html→选择文件（./data/FC2_ALL.xlsx）→enjoy


PS：如果下载预览图片经常出现下载失败，可以在data文件夹FC2_ALL.xlsx查找并修改对应num列的ispic的值改为 no，程序会在下次更新图片库时重新尝试下载

#  


后续优化：

ver 1.1

新增可选配置选项：是否代理，自定义代理端口，是否下载预览原图，自定义获取页数


ver 1.2

1.更新数据库时如果链接出错不再是强制退出程序，而是跳过当前链接，尝试获取下一页

2.优化config.ini文件读取问题，文件不存在，参数缺少，参数填写错误，则使用默认参数。

3.更新图片库时，将使用多线程下载，速度更快（后期考虑是否变为可配置项，目前将根据当前页面已有的图片数创建线程）

ver 1.3

1.更新图片库时同时获取当前作品的作者

2.home页面显示作者信息，新增作品对应官网的跳转链接

ver 1.4

1.修复无法正确识别config.ini配置的bug

2.修复使用全局代理时报错的bug

#

推荐的文件存放树：

./

├FC2freelist.exe 

├config.ini

├home.html

├data/

┊    └───...

├pic/

┊    ├───nodata.jpg

┊    ├───new.jpg

┊    └───...

└js/

┊    └───xlsx.mini.js
     
以上！

不对代码安全性，程序可用性做出保证，如有需要，请自行检查并修改代码，或自建环境自行编译：

pyinstaller -F FC2magnet.py -p getnewlist.py -p checklist.py -p getpic.py -p Config.py --hidden-import getnewlist.py --hidden-import checklist.py --hidden-import getpic.py --hidden-import Config.py 
