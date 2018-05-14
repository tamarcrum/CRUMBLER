#!/usr/bin/python

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
path_of_inputs = sys.argv[1] #can be path from output in previous step
path_of_outputs1 = 'unk_merged/' #can be a new directory, hard coded for par files
path_of_outputs2 = 'unk_eigenstrat/' # hard coded for par files, just has to be pre-made nothing from this script outputs here
plink_species_ID = sys.argv[2]
unknown_prefix = sys.argv[3]
mapfiles = sys.argv[4]

		
#Getting MAP file dict
with open(mapfiles) as f:
	mapfiledict = {}
	for line in f:
		k,v = line.split(':')
		v = v.rstrip('\n')
		mapfiledict[k] = v

#Making Output Directory
if not os.path.exists(path_of_outputs1):
    os.makedirs(path_of_outputs1)

if not os.path.exists(path_of_outputs2):
    os.makedirs(path_of_outputs2)

file_names_list = mylistdir(path_of_inputs)
merge_filename = path_of_outputs1 + 'merge_file_list_ref.txt'
merge_file_list = open(merge_filename, 'w')

ped_file_list = []
for i in file_names_list:
	if i.split('.')[-1] == 'ped':
		ped_file_list.append(i)

for x in ped_file_list:
	if x.split('.')[-2] != 'ped_filt_1':
		basename_parts = x.split('.')[:-1]
		basename = '.'.join(basename_parts)
		merge_file_list.write(path_of_inputs + x + " " + path_of_inputs + basename + ".map" + "\n")
	elif x.split('.')[-2] == 'ped_filt_1':
		first_file = '.'.join(x.split('.')[:-1])

merge_file_list.close()	 


if len(ped_file_list) > 2:
	plink_merge_mult_command = "plink --file " + path_of_inputs + first_file + " --merge-list " + path_of_outputs1 + "merge_file_list_ref.txt --recode --allow-no-sex --cow --out " + path_of_outputs1 + unknown_prefix
	os.system(plink_merge_mult_command)

elif len(ped_file_list) == 2:
	for x in ped_file_list: 
		if x.split('.')[-2] == 'ped_filt_2' and x.split('.')[-1] == 'ped':
			second_ped = x
			second_map = '.'.join(second_ped.split('.')[:-1]) + '.map'

	plink_merge_command = "plink --file " + path_of_inputs + first_file + " --merge " + path_of_inputs + second_ped + " " + path_of_inputs + second_map + " --recode --allow-no-sex --cow --out " + path_of_outputs1 + unknown_prefix
 	os.system(plink_merge_command)	

elif len(ped_file_list) < 2:
	plink_makebed_command = "plink --file " + path_of_inputs + first_file +  " --make-bed --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs1 + unknown_prefix
	os.system(plink_makebed_command)
	plink_recode_command = "plink --file " + path_of_inputs + first_file +  " --recode --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs1 + unknown_prefix
	os.system(plink_recode_command)
	
