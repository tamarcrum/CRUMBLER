#!/usr/bin/python

#Added a --keep-allele-order flag to all plink commands

#Packages
import sys
import os
import re
from collections import defaultdict

def mylistdir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period."""
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]

#Arguments:
path_of_inputs = sys.argv[1]
path_of_outputs = sys.argv[2]
marker_list = sys.argv[3]
plink_species_ID = sys.argv[4]
mapfiles = sys.argv[5]
# filter_plink_call_rate = sys.argv[6]

		
#Getting MAP file dict
with open(mapfiles) as f:
	mapfiledict = {}
	for line in f:
		k,v = line.split(':')
		v = v.rstrip('\n')
		mapfiledict[k] = v


#Making Output Directory
if not os.path.exists(path_of_outputs):
    os.makedirs(path_of_outputs)

file_names_list = mylistdir(path_of_inputs)
ped_file_list = []
for x in file_names_list:
	if x.split('.')[-1] == "ped":   
		ped_file_list.append(x)


counter = 0
for x in ped_file_list:	
	path_file_name = path_of_inputs + x
	if os.path.getsize(path_file_name) > 0:
		counter +=1
		assay = x.split('.')[-2]
		for k,v in mapfiledict.items():
			if k == assay:
				PLINK_map = v
				plink_filter_markers_command = "plink --ped " + path_of_inputs + x + " --map " + PLINK_map + " --extract " + marker_list + " --recode --keep-allele-order --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs + x + "_filt_" + str(counter)
				os.system(plink_filter_markers_command)
				# if filter_plink_call_rate == 'Y':
# 					plink_filter_markers_command = "plink --ped " + path_of_inputs + x + " --map " + PLINK_map + " --recode --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs + x + "_filt_" + str(counter)
# 					os.system(plink_filter_markers_command)
# 				else:
# 					plink_filter_markers_command = "plink --ped " + path_of_inputs + x + " --map " + PLINK_map + " --extract " + marker_list + " --recode --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs + x + "_filt_" + str(counter)
# 					os.system(plink_filter_markers_command)
			elif len(mapfiledict) <= 1:
				k,v = mapfiledict.items()[0]
				PLINK_map = v
				plink_filter_markers_command = "plink --ped " + path_of_inputs + x + " --map " + PLINK_map + " --extract " + marker_list + " --recode --keep-allele-order --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs + x + "_filt_" + str(counter)
				os.system(plink_filter_markers_command)
				# if filter_plink_call_rate == 'Y':
# 					plink_filter_markers_command = 
# 					os.system(plink_filter_markers_command)
# 				else:
# 					plink_filter_markers_command = "plink --ped " + path_of_inputs + x + " --map " + PLINK_map + " --extract " + marker_list + " --recode --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs + x + "_filt_" + str(counter)
# 					os.system(plink_filter_markers_command)