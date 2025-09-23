import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, a, b):
	return a/np.sqrt(x) + b

def GenerateGausData(mean, cov, ndata, seed=111 ):
	np.random.seed(seed)
	data = np.random.multivariate_normal(mean, cov, ndata)
	return data
def SideToOffside(x):
	if "'" in x:
		ft = x[:x.find("'")]
		ins = x[x.find("'")+1:x.find("\"")]
	elif "." in x:
		ft = x[:x.find(".")]
		ins = ""
	else:
		ft = ""
		ins = x[:x.find("\"")]
	if ft == "":
		ft = 0
	else:
		ft = int(ft)
	if ins == "":
		ins = 0
	else:
		ins = int(ins)
	yds = ft/3.
	yds += ins/36.
	if "L" in x:
		yds = -yds
	return yds

def PrepData(csv):
	df = pd.read_csv(csv)
	#convert ft + in to yds
	df["Offside (yds)"] = df["Carry Side"].transform(SideToOffside)
	return df

def MakeDispersionModel(df):
	cov = []
	mux = df["Offside (yds)"].mean()
	muy = df["Total (yds)"].mean()
	mu = [mux, muy]
	shots = df[["Offside (yds)", "Total (yds)"]]
	cov = shots.cov()
	cov = [[cov.iloc[0,0], cov.iloc[0,1]], [cov.iloc[1,0], cov.iloc[1,1]]]
	return mu, cov

df_dr = PrepData("data/Caleb_LaunchMonitor_Driver.csv")
df_7i = PrepData("data/Caleb_LaunchMonitor_7i.csv")
print("7i has",len(df_7i),"shots")
df_8i = PrepData("data/Caleb_LaunchMonitor_8i.csv")
print("8i has",len(df_8i),"shots")
df_9i = PrepData("data/Caleb_LaunchMonitor_9i.csv")
print("9i has",len(df_9i),"shots")
df_SW = PrepData("data/Caleb_LaunchMonitor_SW.csv")
print("SW has",len(df_SW),"shots")


#generate data from dispersion patterns to study how model parameters change with # of input samples
df = df_9i #iron with most original shots
mu, cov = MakeDispersionModel(df)
ntrials = 50
mux_mean = []
mux_err = []
muy_mean = []
muy_err = []

nshots = np.arange(10,60,10)
print("original mean",mu,"original cov",cov)
for nshot in nshots:
	muxs = []
	muys = []
	#simulate ntrials distributions for nshot to get distribution of parameters
	for i in range(ntrials):
		data = GenerateGausData(mu, cov, nshot,seed = 111+i)
		#print("trial #",i,"nshots",nshot,"mean",np.mean(data,axis=0),"cov",np.cov(data,rowvar=False))
		mean = np.mean(data,axis=0)
		cov = np.cov(data,rowvar=False)
		muxs.append(mean[0])
		muys.append(mean[1])
	mux_mean.append(np.mean(muxs))
	mux_err.append(np.std(muxs))
#plt.errorbar(nshots, mux_mean, yerr=mux_err)
plt.scatter(nshots, mux_err)
params = curve_fit(func, nshots, mux_err)[0]
func_ptsx = np.arange(10,60,0.01)
func_ptsy = params[0]/np.sqrt(func_ptsx) + params[1]
plt.scatter(func_ptsx, func_ptsy)

plt.show()	


