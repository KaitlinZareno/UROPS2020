import csv
import os
import pickle
import glob

nested_list = []
x = 0

os.chdir("./pkl_data")
files = glob.glob("*.pkl")
for x in range(len(files)):
	f = "merged_" + str(x) + ".pkl"
	p = pickle.load(open(f,"rb"))
	nested_list +=p


try:
	if not os.path.isdir("./demo_data2"):
		os.mkdir("./demo_data2")
	os.chdir("./demo_data2")
except OSError:
	print ("Creation of the directory failed")

outfile = open("./all_merged2_demo_data.pkl", "wb")
pickle.dump(nested_list[:300], outfile) #obtain 300 state data file
outfile.close()