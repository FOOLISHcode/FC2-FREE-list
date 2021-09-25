'''
第二阶段：
1.进一步筛选目标信息（排除无效货老旧信息，重复信息【时间：最早，大小：最大】），将旧信息的isnews置换为no
2.将本次获得的数据与已经存在的数据对比，将最新的与已有信息不重复的数据写入xlsx（或者sql）
'''
from datetime import datetime
from numpy import int64
import pandas as pd
import os



def checklist():
  


  newdata_filename = './data/FC2_1to10 %s.xlsx' % str(datetime.today().date())
  #newdata_filename = 'test.xlsx'
  compledata_filename = './data/FC2_ALL.xlsx'

  if not os.path.exists(compledata_filename):
    fc2_data = pd.DataFrame(columns=['num','title','magnet','size','uploadtime','isnews','ispic'])
    fc2_data.to_excel(compledata_filename,index=False)

  newdata = pd.read_excel(newdata_filename)
  olddata = pd.read_excel(compledata_filename)
  '''
  1.进一步筛选目标信息（排除无效货老旧信息，重复信息【时间：最早，大小：最大】），将旧信息的isnews置换为no

  ①去除不合格信息：搜索所有num=‘no num’的数据→删除该行
  ②排除重复信息：以‘num’列进行从大到小的排序→逐个搜索→当存在相同num值的行时→判断uploadtime【日期】，删除较大的→相同项仍然存在→判断size，只保存最大的
  ③将旧信息的isnews置换为no

  '''
  #①去除不合格信息：搜索所有num=‘no num’的数据→删除该行
  newdata.drop(index=newdata.loc[newdata['num']=='no num'].index,inplace=True)

  #②排除重复信息：以‘num’列进行从大到小的排序→逐个搜索→当存在相同num值的行时→判断uploadtime【日期】，删除较大的→相同项仍然存在→判断size，只保存最大的
  newdata.sort_values(by=['num','uploadtime','size'],axis=0,ascending=[False,True,False],inplace=True)
  newdata.drop_duplicates(subset=['num'],inplace=True)

  #将旧信息的isnews置换为no
  olddata['isnews'] = 'no'



  '''
  2.将本次获得的数据与已经存在的数据对比，将最新的与已有信息不重复的数据写入xlsx（或者sql）

  ①删除newdata和alldata 中num列的值相同的行
  ②保存已经筛选好的新数据到FC2_ALL.xlsx
  '''
  #①删除newdata和alldata 中num列的值相同的行
  alldata = newdata.append(olddata,ignore_index=True)
  alldata['num'] = pd.to_numeric(alldata['num'])
  alldata.sort_values(by=['num','isnews'],axis=0,ascending=[False,True],inplace=True)
  alldata.drop_duplicates(subset=['num'],inplace=True)

  #print(alldata)
  #②保存已经筛选好的新数据到FC2_ALL.xlsx
  alldata.to_excel(compledata_filename,index=False)

  #③将今天新获取的番号保存到列表中，显示今日新增资源数

  isnews_list = alldata.loc[(alldata['isnews'] == 'yes')].index

  if len(isnews_list) != 0:
    print('今天新增FC2资源共计%s个，已添加到主记录' % len(isnews_list))

  else:
    print('今天没有新增FC2资源')


if __name__ == '__main__':
  checklist()