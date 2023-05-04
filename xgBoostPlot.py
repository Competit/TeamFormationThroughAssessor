import pandas as pd
import numpy as np
from sklearn import model_selection
import xgboost as xgb
import seaborn as sns
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.inspection import permutation_importance
from sklearn.metrics import explained_variance_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import shap
import collections
Profit=pd.read_excel("accessor.xls")
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

#split the data without random_state
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=test_perc)

X_train.shape
X_train.ndim
  # grid = xgb.XGBRegressor(max_depth=3, n_estimators=100, learning_rate=0.1)
grid = xgb.XGBRegressor(max_depth=4)
grid.fit(X_train, y_train)





y_test1 = np.array(y_test)
y_pred=grid.predict(X_test)
# y_test1 = np.array(y_test)
y_test_pred = grid.predict(X_test).tolist()
sc = r2_score(y_test, grid.predict(X_test))
coef = grid.get_booster().get_score(importance_type='gain')
cont_features = ['Md', 'Dd', 'Ld', 'Rd', 'Ad', 'Mr', 'Dr', 'Lr', 'Rr', 'Ar']

print("r2 score:%0.3f" % sc)

#Scatter plot for figure 2
plt.scatter(y_pred,y_test,c="#A9561E")
plt.title('XGBoost Regression')
plt.xlabel('Predicted')
plt.ylabel('Actual')




plt.show()


#SHAP plot  for figure 5
explainer = shap.TreeExplainer(grid)
shap_values = explainer.shap_values(X)
shap.summary_plot(shap_values, X)
e = explained_variance_score(y_test1, y_test_pred)

cont_features=X.columns


correlation_mat = X[cont_features].corr()

plt.subplots(figsize=(16, 9))

#Triangle Correlation Heatmap for figure 4
mask = np.triu(np.ones_like(correlation_mat, dtype=np.bool))
heatmap=sns.heatmap(correlation_mat, mask=mask,annot=True)
heatmap.set_title('Triangle Correlation Heatmap', fontdict={'fontsize': 18}, pad=16);
plt.show()

node_params = {
  'shape': 'box',
  'style': 'filled,rounded',
  'fillcolor': '#78bceb'
}
leaf_node_params = {
  'shape': 'box',
  'style': 'filled,rounded',
  'fillcolor': '#e48038'
}
#tree plot in appendix figure 6
graph = xgb.to_graphviz(grid, condition_node_params=node_params, leaf_node_params=leaf_node_params)
graph.render('xg')
# shap.dependence_plot(cont_features[4], shap_values, X, interaction_index=None)