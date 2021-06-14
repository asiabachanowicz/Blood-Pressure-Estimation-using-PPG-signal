import os
import glob
import pandas

# data pre-processing
# extension = 'csv'
# all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#
# # combine all files in the list
# combined_csv = pandas.concat([pandas.read_csv(f) for f in all_filenames ])
#
# # export to csv
# combined_csv.to_csv("results.csv", index=False, encoding='utf-8-sig')

# import data
data = pandas.read_csv("results.csv", sep=",")
data = data[["cp", "st", "dt", "sw10", "dw10", "sw10+dw10", "dw10/sw10", "sw25", "dw25",
             "sw25+dw25", "dw25/sw25", "sw33", "dw33", "sw33+dw33", "dw33/sw33", "sw50",
             "dw50", "sw50+dw50", "dw50/sw50", "sw66", "dw66", "sw66+dw66", "dw66/sw66",
             "sw75", "dw75", "sw75+dw75", "dw75/sw75", "sys", "dia"]]
print(len(data))

# Remove all nan entries
data = data.dropna(inplace=False)

# Clean the data
indexNames = data[data['cp'] < 570].index
data.drop(indexNames, inplace=True)
indexNames = data[data['cp'] > 1100].index
data.drop(indexNames, inplace=True)
indexNames = data[data['st'] < 150].index
data.drop(indexNames, inplace=True)
indexNames = data[data['st'] > 400].index
data.drop(indexNames, inplace=True)
indexNames = data[data['dt'] < 350].index
data.drop(indexNames, inplace=True)
indexNames = data[data['dt'] > 890].index
data.drop(indexNames, inplace=True)
indexNames = data[data["sw10"] < 150].index
data.drop(indexNames, inplace=True)
indexNames = data[data["sw10"] > 300].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw10"] < 300].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw10"] > 700].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw10/sw10"] > 4.2].index
data.drop(indexNames, inplace=True)
indexNames = data[data["sw25"] > 275].index
data.drop(indexNames, inplace=True)
indexNames = data[data["sw25"] < 100].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw25"] < 200].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw25"] > 450].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw25/sw25"] < 1.2].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw25/sw25"] > 3].index
data.drop(indexNames, inplace=True)
indexNames = data[data["sw33"] > 250].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw33"] > 400].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw33"] < 150].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw33/sw33"] > 2.6].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw50"] > 300].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw50/sw50"] < 0.8].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw50/sw50"] > 2].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw66"] > 200].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw66"] < 80].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw66/sw66"] > 2].index
data.drop(indexNames, inplace=True)
indexNames = data[data["sw75"] > 150].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw75"] > 170].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw75"] < 80].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dw75/sw75"] > 2].index
data.drop(indexNames, inplace=True)
indexNames = data[data["dia"] > 100].index
data.drop(indexNames, inplace=True)

# data description
described_data = data.describe()
print(described_data)
print(len(data))

# export to csv
data.to_csv("data.csv", index=False, encoding='utf-8-sig')