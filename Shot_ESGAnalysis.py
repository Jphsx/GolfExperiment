import pandas as pd
import numpy as np

def PrepData(csv):
	#import data
	df = pd.read_csv(csv,header=3,usecols=['Shot Distance', 'Lie', 'ESG - Gut', 'Club - Gut',
	       'Landing Position - Gut', 'Landing Distance from Pin - Gut (yds)',
	       'ESG - Noonan Recommendations', 'Club - Noonan',
	       'Landing Position - Noonan', 'Landing Distance from Pin - Noonan (yds)',
	       'Club Change (Y/N)?', 'Aim Line Difference (Yds)'])
	#drop rows that aren't data
	df = df.dropna(subset=['Lie','ESG - Gut'])
	#process Y/N entries
	mapdict = {}
	mapdict["N"] = "No"
	mapdict["No"] = "No"
	mapdict["Yes"] = "Yes"
	df["Club Change (Y/N)?"] = df["Club Change (Y/N)?"].map(mapdict)
	#do ESG difference column
	df["ESG noonan - ESG gut"] = df["ESG - Noonan Recommendations"] - df["ESG - Gut"]	
	return df
player1 = PrepData("data/shot_ESG_Doug.csv")
player2 = PrepData("data/shot_ESG_Winslow.csv")
player3 = PrepData("data/shot_ESG_Caleb.csv")
players = [player1, player2, player3]



#stats over SG differences
sumSGs = []
avgSGs = []
errAvgSGs = []
avgAimDiffs = []
fracClubChanges = []
avgSGpmErrs = []
#create results table
ret = {}
ndig = 3
for idx, df in enumerate(players):
	sumSG = df["ESG noonan - ESG gut"].sum()
	sumSGs.append(round(sumSG,ndig))

	avgSG = df["ESG noonan - ESG gut"].mean()
	avgSGs.append(round(avgSG,ndig))

	errAvgSG = df["ESG noonan - ESG gut"].std() / np.sqrt(len(df))
	errAvgSGs.append(round(errAvgSG,ndig))

	avgSGpmErr = r"{} $\pm$ {}".format(round(avgSG,ndig), round(errAvgSG,ndig))
	avgSGpmErrs.append(avgSGpmErr)
	print(avgSGpmErr)

	avgAimDiff = df["Aim Line Difference (Yds)"].mean()
	avgAimDiffs.append(avgAimDiff)

	nNoChange = len(df[df["Club Change (Y/N)?"] == "No"])
	nChange = len(df[df["Club Change (Y/N)?"] == "Yes"])
	fracClubChange = nChange / len(df)
	fracClubChanges.append(fracClubChange)


ret[r"sum $\Delta$ SG"] = sumSGs
ret[r"avg $\Delta$ SG $\pm \sigma_{\Delta \text{SG}}$"] = avgSGpmErrs
ret["errSG"] = errAvgSGs
ret["avgAimDiff"] = avgAimDiffs
ret["fracClubChanges"] = fracClubChanges
ret_df = pd.DataFrame(ret)
print(ret_df.to_latex())




