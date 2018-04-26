#!/usr/bin/python

#Script formats output to an easily read and stored table


#Packages
import sys
import os
import re
from collections import defaultdict
from collections import Counter
import pandas as pd


#Input arguments
marker_list = sys.argv[1]
name_of_table = sys.argv[2]
snpwts_filename = sys.argv[3]

#Import raw output table from SNPweights
table_name = './output_table.txt' #hard coded because of par file, this is not the final table


#Create dataframe for editing
bob_table = pd.read_table(table_name, sep=' ', header=None, index_col = False)

#Open snpwt reference file for order of columns in output
snpwts_file = open(snpwts_filename)

#Reading populations from the second line of the snpwt.reference file
for i, line in enumerate(snpwts_file):
	if i == 1:
		populations = (line.strip())
		fields = populations.split()	

#Figure out number of reference populations and remove the PC columns associated with them in the raw output
kpop = len(fields)		
columns_to_remove = []
for x in xrange(1, int(kpop)):
	colx = x + 2
	columns_to_remove.append(colx)

#Remove columns
bob_table2 = bob_table.drop(bob_table.columns[columns_to_remove], axis=1)

#Remove the last column of the output it is null
bob_table2.drop(bob_table2.columns[len(bob_table2.columns)-1], axis =1, inplace=True)

#Generate column names
##Columns will always be the same
constant_cols = ['sample_id', 'population_label', 'snps'] 

##The constant columns plus the reference populations in order
header = constant_cols + fields

#Add the column names as the header of the table
bob_table2.columns = header

#Add marker list column
marker_list_abrev = marker_list.split('/')[-1]
bob_table2['marker_list'] = marker_list_abrev

#Add reference group column
bob_table2['reference_group'] = snpwts_filename

#Create column with maximum percentage assigned to one breed
bob_table2['max_per'] = bob_table2[fields].max(axis=1)

#Create column with breed column name that was assigned the highest percentage
bob_table2['max_breed'] = bob_table2[fields].idxmax(axis=1)

#Sort table by ascending "max_breed" and descending "max_per"
bob_table_sorted = bob_table2.sort_values(['population_label', 'max_breed', 'max_per'], ascending=[True, True, False]) #Need to change to sort_values(by=...)

#Make new table without"max_breed" and "max_per" columns while remaining sorted
bob_table_sorted2 = bob_table_sorted[bob_table_sorted.columns[:-2]]

#Final table containing sample_id, population_id, snps, breed columns, marker_list, and reference_set
bob_table_sorted2.to_csv(name_of_table, sep='\t', header=True, index=False) 	
