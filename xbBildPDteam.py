import pandas as pd
import numpy as np
from sklearn import model_selection
import xgboost as xgb
from sklearn.metrics import r2_score
import joblib
import xlwt
import xlrd

repetitions =1
sclist = []

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



table = xlrd.open_workbook("two900v2.xls")
sheet3 = table.sheet_by_name("two")

row_count = sheet3.nrows
column_count = sheet3.ncols
Mr=[]
Dr=[]
Lr=[]
Rr=[]
Ar=[]
R=[]
Rmax=0
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
  Rmax = 0
  for j in range(5, 11):
      if j == 5:
        Mr.append(sheet3.cell(i, j).value)
        Mr1.append(sheet3.cell(i, j).value)
      elif j == 6:
        Dr.append(sheet3.cell(i, j).value)
        Dr1.append(sheet3.cell(i, j).value)
      elif j == 7:
        Lr.append(sheet3.cell(i, j).value)
        Lr1.append(sheet3.cell(i, j).value)
      elif j == 8:
        Rr.append(sheet3.cell(i, j).value)
        Rr1.append(sheet3.cell(i, j).value)
      elif j == 9:
        Ar.append(sheet3.cell(i, j).value)
        Ar1.append(sheet3.cell(i, j).value)

      elif j == 10:
        R.append(sheet3.cell(i, j).value)
  for k in range(i + 1, row_count):
      if sheet3.cell(k, 5).value == Mr[0] and sheet3.cell(k, 6).value == Dr[0] and sheet3.cell(k, 7).value == Lr[
        0] and sheet3.cell(k, 8).value == Rr[0] and sheet3.cell(k, 9).value == Ar[0]:
        if sheet3.cell(k, 10).value > Rmax:
          Rmax = sheet3.cell(k, 10).value
          ind = k





  if ind != 0:
    for h in range(0,len(Ar1)):
      print(Mr1[h],Dr1[h],Lr1[h],Rr1[h],Ar1[h])
      print(sheet3.cell(ind, 5).value,sheet3.cell(ind, 6).value,sheet3.cell(ind, 7).value,sheet3.cell(ind, 8).value,sheet3.cell(ind, 9).value)
      if Mr1[h] == sheet3.cell(ind, 5).value and Dr1[h]==sheet3.cell(ind, 6).value and Lr1[h]==sheet3.cell(ind, 7).value and Rr1[h]==sheet3.cell(ind, 8).value and Ar1[h]==sheet3.cell(ind, 9).value:
        a = a + 1


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
workbook.save('BstPD2.xls')




