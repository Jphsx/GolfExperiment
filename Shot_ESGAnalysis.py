import pandas as pd
import numpy as np

def PrepData(csv):
	#import data
	usecols = []
	if "holePlaythrough" not in csv:
		usecols=['Shot Distance', 'Lie', 'ESG - Gut', 'Club - Gut',
		       'Landing Position - Gut', 'Landing Distance from Pin - Gut (yds)',
		       'ESG - Noonan Recommendations', 'Club - Noonan',
		       'Landing Position - Noonan', 'Landing Distance from Pin - Noonan (yds)',
		       'Club Change (Y/N)?', 'Aim Line Difference (Yds)']
	else:
		usecols=['Shot Distance', 'Lie', 'ESG - Gut', 'Club - Gut',
		       'Landing Position - Gut', 'Landing Distance from Pin - Gut (yds)',
		       'ESG - Noonan Recommendations', 'Club - Noonan',
		       'Landing Position - Noonan', 'Landing Distance from Pin - Noonan (yds)']
	df = pd.read_csv(csv,header=3,usecols=usecols)
	#drop rows that aren't data
	droprows = []
	if "holePlaythrough" not in csv:
		droprows = ['Lie','ESG - Gut']
	else:
		droprows = ['Lie']
	df = df.dropna(subset=droprows)
	if "holePlaythrough" in csv:
		zeroCols = ['ESG - Gut', 'Landing Distance from Pin - Gut (yds)', 'ESG - Noonan Recommendations','Landing Distance from Pin - Noonan (yds)']
		noneCols = ['Club - Gut','Landing Position - Gut','Club - Noonan','Landing Position - Noonan', ]
		df[zeroCols] = df[zeroCols].fillna(0)
		df[noneCols] = df[noneCols].fillna("None")
	#process Y/N entries
	mapdict = {}
	mapdict["N"] = "No"
	mapdict["No"] = "No"
	mapdict["Yes"] = "Yes"
	if "holePlaythrough" not in csv:
		df["Club Change (Y/N)?"] = df["Club Change (Y/N)?"].map(mapdict)
	#do ESG difference column
	#df["ESG noonan - ESG gut"] = df["ESG - Noonan Recommendations"] - df["ESG - Gut"]
	return df
player1 = PrepData("data/shot_ESG_Doug.csv")
player2 = PrepData("data/shot_ESG_Winslow.csv")
player3 = PrepData("data/shot_ESG_Caleb.csv")
player4 = PrepData("data/shot_ESG_Matt_holePlaythrough.csv")
#continuous hole playthrough
players = [player1, player2, player3,player4]



#stats over SG differences
sumSGs_rec = []
avgSGs_rec = []
errAvgSGs_rec = []
sumSGs_norec = []
avgSGs_norec = []
errAvgSGs_norec = []
avgSGpmErrs_rec = []
avgSGpmErrs_norec = []

avgAimDiffs = []
fracClubChanges = []
#create results table
ret = {}
ndig = 3
for idx, df in enumerate(players):
	sumSG_rec = df["ESG - Noonan Recommendations"].sum()
	sumSGs_rec.append(round(sumSG_rec,ndig))
	sumSG_norec = df["ESG - Gut"].sum()
	sumSGs_norec.append(round(sumSG_norec,ndig))

	avgSG_rec = df["ESG - Noonan Recommendations"].mean()
	avgSGs_rec.append(round(avgSG_rec,ndig))
	
	avgSG_norec = df["ESG - Gut"].mean()
	avgSGs_norec.append(round(avgSG_norec,ndig))

	errAvgSG_rec = df["ESG - Noonan Recommendations"].std() / np.sqrt(len(df))
	errAvgSGs_rec.append(round(errAvgSG_rec,ndig))
	
	errAvgSG_norec = df["ESG - Gut"].std() / np.sqrt(len(df))
	errAvgSGs_norec.append(round(errAvgSG_norec,ndig))

	avgSGpmErr_rec = r"{} $\pm$ {}".format(round(avgSG_rec,ndig), round(errAvgSG_rec,ndig))
	avgSGpmErrs_rec.append(avgSGpmErr_rec)
	avgSGpmErr_norec = r"{} $\pm$ {}".format(round(avgSG_norec,ndig), round(errAvgSG_norec,ndig))
	avgSGpmErrs_norec.append(avgSGpmErr_norec)

	if "Aim Line Difference (Yds)" in df.columns:
		avgAimDiff = df["Aim Line Difference (Yds)"].mean()
		avgAimDiffs.append(avgAimDiff)

		nNoChange = len(df[df["Club Change (Y/N)?"] == "No"])
		nChange = len(df[df["Club Change (Y/N)?"] == "Yes"])
		fracClubChange = nChange / len(df)
		fracClubChanges.append(fracClubChange)

print("sumSGs \n rec",sumSGs_rec)
print(" no rec",sumSGs_norec)
print("avg SGs pm errs \n rec",avgSGpmErrs_rec)
print("no rec",avgSGpmErrs_norec)
#ret[r"$\sum$ SG"] = sumSGs
#ret[r"$\bar{SG} \pm SE_{\text{SG}}$"] = avgSGpmErrs
shots = []
ret = []
##ret["avgAimDiff"] = avgAimDiffs
##ret["fracClubChanges"] = fracClubChanges
ret_df = pd.DataFrame(ret)
#print(ret_df.to_latex(column_format="|c|c|c|c||c|c"))




