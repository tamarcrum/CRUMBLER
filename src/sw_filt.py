## Update 12/3/2018

#!/usr/bin/python

#Packages
import sys
import os
import re
from collections import defaultdict
import pandas as pd
import csv

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
plink_marker_action = sys.argv[4]
plink_species_ID = sys.argv[5]
mapfiles = sys.argv[6]


		
#Getting MAP file dict
with open(mapfiles) as f:
	mapfiledict = {}
	for line in f:
		k,v = line.split(':')
		v = v.strip()
		mapfiledict[k] = v

def remove_duplicates(snp_names):
	output = []
	seen = set()
	for snp_id in snp_names:
		if snp_id not in seen:
			output.append(snp_id)
			seen.add(snp_id)
	return output

def plink_AB_command():
	for k,v in mapfiledict.items():
		if k == assay:
			PLINK_map = v

#Edit map files for duplicate snp IDs which will not work with reference allele specification			
			v_filename_only = v.split('/')[-1]
			map_file_table = pd.read_table(PLINK_map, sep='\t', header=None, index_col=False)
			map_file_table.columns = ['chr', 'snp_id', 'g_dis', 'bpos']
			map_file_table['dup'] = map_file_table['snp_id'].duplicated().astype(int).astype(str)
			map_file_table.loc[map_file_table.dup == '1', 'bpos'] = '-1'
			map_file_table2 = map_file_table.drop('dup', 1)
			map_file_table2.sort_index(inplace=True)
			name_of_output_map = path_of_outputs + v_filename_only
			map_file_table2.to_csv(name_of_output_map, sep='\t', header=False, index=False)

#Create reference allele specification file			
			ref_allele_filename = path_of_outputs + 'ref_allele_' + assay + '.txt'
			ref_allele = open(ref_allele_filename, 'w')
			snp_names = [n[1] for n in csv.reader(open(PLINK_map, 'r'), delimiter = '\t')]
			snp_names_2 = remove_duplicates(snp_names)
 			for s in snp_names_2:
				ref_allele.write(s + " A" + "\n")
			ref_allele.close()

#Plink command to filter markers and set reference allele
			if plink_marker_action == "S":			
				plink_filter_markers_command = "plink --ped " + path_of_inputs + x + " --map " + name_of_output_map + " --extract " + marker_list + " --reference-allele " + path_of_outputs + "ref_allele_" + assay + ".txt  --recode 12 --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs + x + "_filt_" + str(counter)
				os.system(plink_filter_markers_command)
			elif plink_marker_action == "R":
				plink_filter_markers_command = "plink --ped " + path_of_inputs + x + " --map " + name_of_output_map + " --extract " + marker_list + " --range --reference-allele " + path_of_outputs + "ref_allele_" + assay + ".txt  --recode 12 --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs + x + "_filt_" + str(counter)
				os.system(plink_filter_markers_command)

			 	
		elif len(mapfiledict) <= 1:
			k,v = mapfiledict.items()[0]
			PLINK_map = v
#Edit map file for duplicate snp IDs which will not work with reference allele specification			
			v_filename_only = v.split('/')[-1]
			map_file_table = pd.read_table(PLINK_map, sep='\t', header=None, index_col=False)
			map_file_table.columns = ['chr', 'snp_id', 'g_dis', 'bpos']
			map_file_table['dup'] = map_file_table['snp_id'].duplicated().astype(int).astype(str)
			map_file_table.loc[map_file_table.dup == '1', 'bpos'] = '-1'
			map_file_table2 = map_file_table.drop('dup', 1)
			map_file_table2.sort_index(inplace=True)
			name_of_output_map = path_of_outputs + v_filename_only
			map_file_table2.to_csv(name_of_output_map, sep='\t', header=False, index=False)

#Create reference allele specification file			
			ref_allele_filename = path_of_outputs + 'ref_allele_' + assay + '.txt'
			ref_allele = open(ref_allele_filename, 'w')
			snp_names = [n[1] for n in csv.reader(open(PLINK_map, 'r'), delimiter = '\t')]
			snp_names_2 = remove_duplicates(snp_names)
 			for s in snp_names_2:
				ref_allele.write(s + " A" + "\n")
			ref_allele.close()

#Plink command to filter markers and set reference allele			
			if plink_marker_action == "S":			
				plink_filter_markers_command = "plink --ped " + path_of_inputs + x + " --map " + name_of_output_map + " --extract " + marker_list + " --reference-allele " + path_of_outputs + "ref_allele_" + assay + ".txt  --recode 12 --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs + x + "_filt_" + str(counter)
				os.system(plink_filter_markers_command)
			elif plink_marker_action == "R":
				plink_filter_markers_command = "plink --ped " + path_of_inputs + x + " --map " + name_of_output_map + " --extract " + marker_list + " --range --reference-allele " + path_of_outputs + "ref_allele_" + assay + ".txt  --recode 12 --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs + x + "_filt_" + str(counter)
				os.system(plink_filter_markers_command)
	
def plink_12_command():
	for k,v in mapfiledict.items():
		if k == assay:
			PLINK_map = v
			if plink_marker_action == "S":			
				plink_filter_markers_command = "plink --ped " + path_of_inputs + x + " --map " + PLINK_map + " --extract " + marker_list + " --recode --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs + x + "_filt_" + str(counter)
				os.system(plink_filter_markers_command)
			elif plink_marker_action == "R":
				plink_filter_markers_command = "plink --ped " + path_of_inputs + x + " --map " + PLINK_map + " --extract " + marker_list + " --range --recode --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs + x + "_filt_" + str(counter)
				os.system(plink_filter_markers_command)
		elif len(mapfiledict) <= 1:
			k,v = mapfiledict.items()[0]
			PLINK_map = v
			if plink_marker_action == "S":			
				plink_filter_markers_command = "plink --ped " + path_of_inputs + x + " --map " + PLINK_map + " --extract " + marker_list + " --recode --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs + x + "_filt_" + str(counter)
				os.system(plink_filter_markers_command)
			elif plink_marker_action == "R":
				plink_filter_markers_command = "plink --ped " + path_of_inputs + x + " --map " + PLINK_map + " --extract " + marker_list + " --range --recode --allow-no-sex --" + plink_species_ID + " --out " + path_of_outputs + x + "_filt_" + str(counter)
				os.system(plink_filter_markers_command)


#Making Output Directory
if not os.path.exists(path_of_outputs):
    os.makedirs(path_of_outputs)

file_names_list = mylistdir(path_of_inputs)
ped_file_list = []
for b in file_names_list:
	if b.split('.')[-1] == "ped":   
		ped_file_list.append(b)

nonempty_genotype_files = []
for c in ped_file_list:
	path_file_name = path_of_inputs + c
	if os.path.getsize(path_file_name) > 0:
		nonempty_genotype_files.append(c)


	

counter = 0
for x in nonempty_genotype_files:	
	counter +=1
	assay = x.replace('_', '.').split('.')[-2]
	#assay = x.split('.')[-2]
	genotype_file_name = path_of_inputs + x
	with open(genotype_file_name) as f:
		first_line = f.readline().strip()
		if 'BB' in first_line:
			plink_AB_command()
                elif 'B' in first_line:
                        plink_AB_command()
		elif 'C' in first_line: 
			sys.exit('Genotypes are not in AB or 12 format.')
		elif 'T' in first_line: 
			sys.exit('Genotypes are not in AB or 12 format.')
		else:
			plink_12_command()
