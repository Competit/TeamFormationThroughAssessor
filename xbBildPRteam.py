import pandas as pd
import numpy as np
from sklearn import model_selection
import xgboost as xgb
from sklearn.metrics import r2_score
import joblib
import xlwt
import xlrd


mselist=[]
maelist=[]
rmselist=[]
coefT={}
coef1T=list()
test_perc = 0.1

df_train=pd.DataFrame(data=None)
df_test=pd.DataFrame(data=None)
def MSE(y, t):
  return 0.5 * np.sum((y - t) ** 2)



for x in range(0,1):

#找出最弱队
  # 3乘3
  table = xlrd.open_workbook("three3600v2.xls")
  sheet3 = table.sheet_by_name("three")
  # 2乘2
  # table = xlrd.open_workbook("two900v2.xls")
  # sheet3 = table.sheet_by_name("two")

  row_count = sheet3.nrows
  column_count = sheet3.ncols
  Mr=[]
  Dr=[]
  Lr=[]
  Rr=[]
  Ar=[]
  R=[]

  RindL=[]

  workbook = xlwt.Workbook(encoding='utf-8')
  sheetRmin = workbook.add_sheet('sheet1')  # 创建sheet页
  u=0
  Mr1 = []
  Dr1 = []
  Lr1 = []
  Rr1 = []
  Ar1 = []
  for i in range(1, row_count):
    Mr = []
    Dr = []
    Lr = []
    Rr = []
    Ar = []
    a=0
    R = []
    ind = 0
    Rmin = 0
    for j in range(0, 11):
      if j == 0:
        Mr.append(sheet3.cell(i, j).value)
        Mr1.append(sheet3.cell(i, j).value)
      elif j == 1:
        Dr.append(sheet3.cell(i, j).value)
        Dr1.append(sheet3.cell(i, j).value)
      elif j == 2:
        Lr.append(sheet3.cell(i, j).value)
        Lr1.append(sheet3.cell(i, j).value)
      elif j == 3:
        Rr.append(sheet3.cell(i, j).value)
        Rr1.append(sheet3.cell(i, j).value)
      elif j == 4:
        Ar.append(sheet3.cell(i, j).value)
        Ar1.append(sheet3.cell(i, j).value)

      elif j == 10:
        R.append(sheet3.cell(i, j).value)
    Rmin=R[0]
    for k in range(i + 1, row_count):
      if sheet3.cell(k, 0).value == Mr[0] and sheet3.cell(k, 1).value == Dr[0] and sheet3.cell(k, 2).value == Lr[
        0] and sheet3.cell(k, 3).value == Rr[0] and sheet3.cell(k, 4).value == Ar[0]:
        aa=sheet3.cell(k, 10).value

        # print(aa)
        if sheet3.cell(k, 10).value < Rmin:
          Rmin = sheet3.cell(k, 10).value
          ind = k
        if k==row_count-1:
          ddd=1
    if Rmin == R[0] and ind == 0:
      ind = i
    if ind != 0:
      for h in range(0,len(Ar1)):
        # print(Mr1[h],Dr1[h],Lr1[h],Rr1[h],Ar1[h])
        # print(sheet3.cell(ind, 5).value,sheet3.cell(ind, 6).value,sheet3.cell(ind, 7).value,sheet3.cell(ind, 8).value,sheet3.cell(ind, 9).value)
        if Mr1[h] == sheet3.cell(ind, 0).value and Dr1[h]==sheet3.cell(ind, 1).value and Lr1[h]==sheet3.cell(ind, 2).value and Rr1[h]==sheet3.cell(ind,3).value and Ar1[h]==sheet3.cell(ind, 4).value:

          a=a+1
      if a==1:
          RindL.append(ind)

    workbook = xlwt.Workbook(encoding='utf-8')
    sheet2R = workbook.add_sheet('sheet2')  # 创建sheet页
    sheet3R = workbook.add_sheet('sheet3')  # 创建sheet页
    u=0
    for u in range(0,len(RindL)):
      for k in range(0, 11):
        b = RindL[u]

        a = sheet3.cell(RindL[u], k).value
        sheet2R.write(u, k, a)



    # for u in range(0, 3240):
    #     sheet3.write(u, 0, round(y_test3[u],0))
    #
    #     u = u + 1
    workbook.save('BstPR3.xls')




