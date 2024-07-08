# # Using Pandas to process vaccine adverse events
#
# ## Data Access
#
# Go to https://vaers.hhs.gov/data/datasets.html and Download 2021 **zip** Data. Please do not download only the CSV File.
#
# Drop it on the directory where this notebook is.


# !unzip 2021VAERSData.zip
# !gzip -9 *csv
## this is diractly asking the command line to unzip the VAERS data file 
## and then make it a csv. 


import pandas as pd
import matplotlib.pyplot as plt

vdata = pd.read_csv(
    "2021VAERSDATA.csv.gz", encoding="iso-8859-1")
##This reads the vaccine data in for us. 

vdata.columns
##titles of the columns

vdata.dtypes
##data types for each column

vdata.shape
## identifies the shape of the data frame (752988 rows and 35 columns)

vdata.iloc[0]
## What is the first entry in the data frame?

vdata = vdata.set_index("VAERS_ID")
##changes the index to the VAERS_ID instead of the numerical index

vdata.loc[916600]
##calls the same value as before, but now by VAERS_ID.

vdata.head(3)
##Gives the head of the VAERS Data, indexed by VAERS_ID

vdata.iloc[:3]
## Calls the first 3 rows. 

vdata.iloc[:5, 2:4]
##calls the first five entries on data frame; 
##the second part (2:4) calls only columns 2 and three (count from zero)

vdata["AGE_YRS"].max()
##identifies the greatest age by finding the maximum number in the AGE_YRS column 
## AGE_YRS as a dictionary key

vdata.AGE_YRS.max()
##identifies the largest number in the column AGE_YRS.
##AGE_YRS as an object field

vdata["AGE_YRS"].sort_values().plot(use_index=False)
##y axis is age, x axis is frequency

fig, ax = plt.subplots(1, 2, sharey=True, dpi=300)
fig.suptitle("Age of adverse events")
vdata["AGE_YRS"].sort_values().plot(
    use_index=False, ax=ax[0],
    xlabel="Obervation", ylabel="Age")
vdata["AGE_YRS"].plot.hist(bins=20, orientation="horizontal")
fig.savefig("adverse.png")

vdata["AGE_YRS"].dropna().apply(lambda x: int(x)).value_counts()
# Lists number of adverse reactions by age (most adverse reactions at age 50, fewest at age 109)

vdata.DIED.value_counts(dropna=False)
# This is the count of how many people were marked as dead and how many people were marked null
## Null is a problem because it could mean alive or it could mean no data, so we make a new category


vdata["is_dead"] = (vdata.DIED == "Y")
##Created new column that is Boolean, and that allows for masking and basic numerical stats
##Null data is eliminated by only conting those marked as dead as being dead


dead = vdata[vdata.is_dead]##only rows where people died
vax = pd.read_csv("2021VAERSVAX.csv.gz", encoding="iso-8859-1").set_index("VAERS_ID")
print(vax.columns)
print(vax.shape)
print(vax.VAX_TYPE.unique())
## this is a new data frame 
##with only the specifics of the vaccine they took. 

vax.groupby("VAX_TYPE").size().sort_values()
## lists the number of each type of vaccine that had an adverse reaction

vax19 = vax[vax.VAX_TYPE == "COVID19"]
vax19_dead = dead.join(vax19)
# join on id, where 
vax19_dead.head()

vax19_dead.iloc[917793]

baddies = vax19_dead.groupby("VAX_LOT").size().sort_values(ascending=False)
for i, (lot, cnt) in enumerate(baddies.items()):
    print(lot, cnt, len(vax19_dead[vax19_dead.VAX_LOT == lot].groupby("STATE")))
    if i == 10:
        break


# The data above is not totally correct - at least in terms of interpretation, but for that we need to check the next recipe
