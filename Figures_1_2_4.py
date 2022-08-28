#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 11:52:12 2022

@author: ridwanbello
"""

import pandas as pd
import seaborn as sns
import numpy as np
import os
from matplotlib import pyplot as plt

os.chdir('/Users/ridwanbello/Documents/GitHub/Border Closure')

raw_df = pd.read_csv("Figure1_Import_Nigeria_2011_2020.csv")

pivoted_df=raw_df.pivot_table(index="Year",
                              columns="Recoded",
                              values="Trade Value",
                              aggfunc=np.sum,
                              margins=True,
                              margins_name="Totals")

pivoted_df["food_veggie_share"] = (pivoted_df["Food and vegetables"]/pivoted_df["Totals"])*100

pivoted_df.drop("Totals",axis=0, inplace=True)
pivoted_df["food_veggie_share"]=pivoted_df["food_veggie_share"].round(1)
pivoted_df["name"]="Food and Veggies"

sns.set_style("dark")
sns.set_context("poster")
g=sns.relplot(data=pivoted_df,
                 x="Year",
                 y="food_veggie_share",
                 kind="line",
                 style="name",
                 markers=True,
                 legend=False,
                 height=7,
                 aspect=3
                 #s=20
                 )
plt.ylim(8,26)
g.set(xlabel="Year",
    ylabel="Food imports, % of total imports") 
for i, data_point in enumerate(pivoted_df["food_veggie_share"]):
    plt.annotate(data_point, (list(pivoted_df.index)[i], data_point+0.7))
g.fig.suptitle("Figure 1: Nigeria's Food Imports, 2011-2020", y=1.025)
plt.show()


#######################
##Agric_output
ag_output = pd.read_csv("Figure2_nga_agric_output.csv")
ag_output["ag_out($bn)"] = ag_output["Value"]/1000000
ag_output["ag_out($bn)"] = ag_output["ag_out($bn)"].round(1)

sns.set_style("dark")
sns.set_context("poster")
g=sns.relplot(data=ag_output,
                 x="Year",
                 y="ag_out($bn)",
                 kind="line",
                 style="Area",
                 markers=True,
                 legend=False,
                 height=7,
                 aspect=3
                 #s=20
                 )
g.set(xlabel="Year",
    ylabel="Value, real, $USbillion") 
plt.ylim(45,70)
for i, data_point in enumerate(ag_output["ag_out($bn)"]):
    plt.annotate(data_point, (list(pivoted_df.index)[i], data_point+0.7))
g.fig.suptitle("Figure 2: Aggregate agricultural production, Nigeria, 2011-2020", y=1.025)
plt.show()

################################
####Commodity prices
com_prices = pd.read_csv("Figure4_commodity_prices.csv")
com_df = com_prices.loc[com_prices.index.isin(range(702,744)),:].copy()

com_df["Date"] = pd.to_datetime(com_df.Month)
com_df = com_df.melt(id_vars="Date", value_vars=["Beverages","Food"], var_name="Commodity group")
com_df.sort_values(["Date","Commodity group"], ascending=[True, True], inplace=True)

sns.set_style("dark")
sns.set_context("poster")
g=sns.relplot(data=com_df,
                 x="Date",
                 y="value",
                 kind="line",
                 style="Commodity group",
                 hue="Commodity group",
                 markers=True,
                 legend=True,
                 height=10,
                 aspect=1.5
                 #s=20
                 )
g.set(xlabel="Date",
    ylabel="Price index, nominal $US, 2010=100") 
g.fig.suptitle("Figure 4: Monthly Price Index, Commodity Markets, 2018-2021", y=1.025)
plt.show()