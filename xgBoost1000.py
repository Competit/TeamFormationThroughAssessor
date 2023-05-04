import pandas as pd
import numpy as np
from sklearn import model_selection
import xgboost as xgb
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.inspection import permutation_importance
from sklearn.metrics import explained_variance_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import collections
Profit=pd.read_excel("accessor.xls")
repetitions =1000
sclist = []

mselist=[]
maelist=[]
rmselist=[]
evslist=[]
coefT={}
test_perc = 0.1


Profit=pd.DataFrame(Profit)
Profit.columns=["Md","Dd","Ld","Rd","Ad","Mr","Dr","Lr","Rr","Ar","R"]
X=Profit.iloc[:,0:10]
y=Profit.iloc[:,10:11]

df_train=pd.DataFrame(data=None)
df_test=pd.DataFrame(data=None)
def MSE(y, t):
  return 0.5 * np.sum((y - t) ** 2)
for x in range(0,repetitions):

  #split the data without random_state
  X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=test_perc)

  X_train.shape
  X_train.ndim
  # grid = xgb.XGBRegressor(max_depth=3, n_estimators=100, learning_rate=0.1)
  grid = xgb.XGBRegressor()
  grid.fit(X_train, y_train)

  sc = r2_score(y_test, grid.predict(X_test))
  print("r2 score:%0.3f" % sc)

  sclist.append(sc)

  y_test1 = np.array(y_test).tolist()

  y_test_pred = grid.predict(X_test).tolist()

  e = explained_variance_score(y_test1, y_test_pred)

  coef1=grid.feature_importances_

  coef1=coef1.tolist()
  mselist.append(mean_squared_error(y_test1, y_test_pred))
  rmselist.append(np.sqrt(mean_squared_error(y_test1, y_test_pred)))
  maelist.append(mean_absolute_error(y_test1, y_test_pred))
  if x==0:
         coef1T=coef1

  else:
     coef1T=list(np.add(coef1,coef1T))

features = []
coefT1 = []
# for key, value in coefT.items():
#     coefT[key] = coefT[key] / repetitions
#coef1T1存贮feature_importances_计算的特征重要性.不需要调整特征顺序
coef1T1 = []

for item in coef1T:
    coef1T1.append(item / repetitions)

#调整顺序
key_order = ('Md', 'Dd', 'Ld', 'Rd', 'Ad', 'Mr', 'Dr', 'Lr', 'Rr', 'Ar')
coefTOD = collections.OrderedDict()


for key, value in coefTOD.items():
    features.append(key)
    coefT1.append(value)

print("r2 score average:%0.3f, standard deviation:%0.3f, MSE:%0.3f,RMSE:%0.3f,MAE:%0.3f," % (
np.average(sclist), np.std(sclist), np.average(mselist), np.average(rmselist), np.average(maelist)))
print('Coefficients: \n', coefT)

for i, val in enumerate(features):
    if val == 'Md':
        features[i] = r'$M_d$'
    if val == 'Dd':
        features[i] = r'$D_d$'
    if val == 'Ld':
        features[i] = r'$L_d$'
    if val == 'Rd':
        features[i] = r'$R_d$'
    if val == 'Ad':
        features[i] = r'$\alpha_d$'
    if val == 'Mr':
        features[i] = r'$M_r$'
    if val == 'Dr':
        features[i] = r'$D_r$'
    if val == 'Lr':
        features[i] = r'$L_r$'
    if val == 'Rr':
        features[i] = r'$R_r$'
    if val == 'Ar':
        features[i] = r'$\alpha_r$'

features = [r'$\alpha_r$', r'$R_r$', r'$L_r$', r'$D_r$', r'$M_r$', r'$\alpha_d$', r'$R_d$', r'$L_d$', r'$D_d$',
            r'$M_d$']



#feature_importances_ plot for figure 3
coef1T1=list(reversed(coef1T1))
plt.show()
plt.barh(features, coef1T1, height=0.7)
plt.xlabel('Features importance') # x 轴

plt.ylabel('Features')
plt.show()

f, axs = plt.subplots(1, 2, figsize=(15, 5))
