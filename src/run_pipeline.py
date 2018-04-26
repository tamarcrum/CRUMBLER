#!/usr/bin/python

#Run breed composition pipeline using a par file for inputs


import os
import sys

#Arguments
base_script = sys.argv[0]
par_file = sys.argv[1]

#Get Path of src code if there is one
path_of_source_code = '/'.join(base_script.split('/')[:-1])

#Reading Par File and gathering information
with open(par_file) as p:
	par_dict = {}
	for line in p:
		key, value = line.split(':')
		value = value.rstrip('\n')
		value = value.strip()
			
		if key in par_dict:
			par_dict.update({key:value})
		else:
			par_dict[key] = value
			

if par_dict.has_key('genotypes') and par_dict['genotypes']!= '':
	path_of_inputs_1 = par_dict['genotypes']
	
else: 
	#print 'No genotype input file path specified.'
	sys.exit('No genotype input file specified.')

if par_dict.has_key('marker_list') and par_dict['marker_list'] != '':
	marker_list = par_dict['marker_list']
else:
	# marker_list_answer = raw_input("Do you want to use a SNP list for marker filtering (Y/N): ")
# 	if marker_list_answer == 'N':
# 		filter_plink_call_rate == 'Y'
# 	elif marker_list_answer == 'Y': 
# 		#print 'No marker list file specified.'
# 		sys.exit('Please specify your SNP list in the parameter file.')
	sys.exit('Please specify your SNP list in the parameter file.')
	
if par_dict.has_key('plink_species_ID') and par_dict['plink_species_ID'] != '':
	plink_species_ID = par_dict['plink_species_ID']
else: 
	#print 'No plink species ID specified.'
	sys.exit('No PLINK species ID was specified.')

if par_dict.has_key('reference_set') and par_dict['reference_set'] != '':
	run_reference = par_dict['reference_set']
else:
	reference_set_answer = raw_input('Does SNP weights need to be calculated for these genotypes?  Is this a set of reference population samples? (Y/N): ')
	run_reference = reference_set_answer
	#print 'Is this a reference set and does it need to be calculated?'

if run_reference == 'N':
	if par_dict.has_key('output_table_name') and par_dict['output_table_name'] != '':
		final_table_name = par_dict['output_table_name']
		
	else: 
		sys.exit('An output table name needs to be specified.')

if run_reference == 'Y':
	if par_dict.has_key('number_ref_populations') and par_dict['number_ref_populations'] != '':
		user_k = par_dict['number_ref_populations']
		
	else:
		k_pop_answer = raw_input('How many reference populations are in this analysis? (enter # or U if unknown): ')
 		if k_pop_answer != 'U':
 			user_K = k_pop_answer
 		else:
			sys.exit('Please figure out how many reference populations there are and insert into parameter file.')

if par_dict.has_key('snpweights_filename') and par_dict['snpweights_filename'] != '':
	snpweights_filename = par_dict['snpweights_filename']
else:
	#print 'Specify a name for the snpweights reference file.'
	sys.exit('A SNP weights file name needs to be specified.')

if par_dict.has_key('eig_par_file_directory_path') and par_dict['eig_par_file_directory_path'] != '':
	eig_par_file_directory_path = par_dict['eig_par_file_directory_path']
else:
	#print 'What is the path for the directory containing all the EIGENSOFT par files?'
	sys.exit('Please specify a path to the EIGENSOFT par file directory.')

if par_dict.has_key('SNPweights_software_path') and par_dict['SNPweights_software_path'] != '':
	SNPweights_software_path = par_dict['SNPweights_software_path']
else:
	sys.exit('Please specify a path to where the SNPweights software is located.')	
	
if par_dict.has_key('EIGENSOFT_software_path') and par_dict['EIGENSOFT_software_path'] != '':
	EIGENSOFT_software_path = par_dict['EIGENSOFT_software_path']
else:
	sys.exit('Please specify a path to where the EIGENSOFT software is located.')	

if par_dict.has_key('number_of_chrom') and par_dict['number_of_chrom'] != '':
	number_of_chromosomes = par_dict['number_of_chrom']
 
else:	
	number_of_chrom_answer = raw_input('Please specify the number of chromosomes (autosomes) for the species. The X is assumed to be num+1 and the Y is numchrom+2.(enter # or U if unknown): ')	
 	if number_of_chrom_answer != 'U':
 		user_chrom = number_of_chrom_answer
	else:
		sys.exit('Please figure out the number of chromosomes (autosomes) for the species and specify in the parameter file. The X is assumed to be num+1 and the Y is numchrom+2.')	

if par_dict.has_key('assay_plink_map_files') and par_dict['assay_plink_map_files'] != '':
	map_files = par_dict['assay_plink_map_files']
	
else: 
	sys.exit('Please specify file name containing the list of PLINK compatible map file(s) for the assays in this analysis.')

#If Reference set is YES, need to specify a snpweights filename
if run_reference == "Y":	
##Edit EIGENSOFT par files based on inputs
##Edit reference EIGENSTRAT file for # of chromosomes
	par_reference_eigenstrat = eig_par_file_directory_path + 'par.reference.PED.EIGENSTRAT'
	with open(par_reference_eigenstrat) as e:
		par_reference_EIGENSTRAT_dict = {}
		for line in e:
			k,v = line.split(':')
			v = v.rstrip('\n')
			par_reference_EIGENSTRAT_dict[k] = v
	
	for key, value in par_reference_EIGENSTRAT_dict.items():
		par_reference_EIGENSTRAT_dict['numchrom'] = number_of_chromosomes
		
	par_reference_EIGENSTRAT_new = eig_par_file_directory_path + 'par.reference.PED.EIGENSTRAT'
	eopen = open(par_reference_EIGENSTRAT_new, 'w')
	
	for k,v in par_reference_EIGENSTRAT_dict.items():
		eopen.write(str(k) + ': ' + str(v) + '\n')
	eopen.close()	
	
##Edit SMARTPCA par file for # of chromsomes and K
	par_reference_smartpca = eig_par_file_directory_path + 'par.reference.smartpca'
	with open(par_reference_smartpca) as s:
		par_reference_smartpca_dict = {}
		for line in s:
			k,v = line.split(':')
			v = v.rstrip('\n')
			par_reference_smartpca_dict[k] = v
	
	for key, value in par_reference_smartpca_dict.items():
		par_reference_smartpca_dict['numchrom'] = number_of_chromosomes
		par_reference_smartpca_dict['numoutevec'] = user_k
		
	par_reference_smartpca_new = eig_par_file_directory_path + 'par.reference.smartpca'
	sopen = open(par_reference_smartpca_new, 'w')
	
	for k,v in par_reference_smartpca_dict.items():
		sopen.write(str(k) + ': ' + str(v) + '\n')
	sopen.close()
	
##Edit calculate SNPweights par file for SNP weights file name
	par_reference_calc_snpwt = eig_par_file_directory_path + 'par.reference.calc_snpwt'
	with open(par_reference_calc_snpwt) as c:
		par_reference_calc_snpwt_dict = {}
		for line in c:
			k,v = line.split(':')
			v = v.rstrip('\n')
			par_reference_calc_snpwt_dict[k] = v

	for key, value in par_reference_calc_snpwt_dict.items():
		par_reference_calc_snpwt_dict['snpwtoutput'] = snpweights_filename

	par_reference_calc_snpwt_new = eig_par_file_directory_path + 'par.reference.calc_snpwt'
	copen = open(par_reference_calc_snpwt_new, 'w')

	for k,v in par_reference_calc_snpwt_dict.items():
		copen.write(str(k) + ': ' + str(v) + '\n')
	copen.close()

##Inferancestry par file with SNP weights file name specified in input
	par_inferancestry = eig_par_file_directory_path + 'par.inferancestry'
	with open(par_inferancestry) as i:
		par_inferancestry_dict = {}
		for line in i:
			k,v = line.split(':')
			v = v.rstrip('\n')
			par_inferancestry_dict[k] = v

	for key, value in par_inferancestry_dict.items():
		par_inferancestry_dict['snpwt'] = snpweights_filename

	par_inferancestry_new = eig_par_file_directory_path + 'par.inferancestry'
	iopen = open(par_inferancestry_new, 'w')

	for k,v in par_inferancestry_dict.items():
		iopen.write(str(k) + ': ' + str(v) + '\n')
	iopen.close()

elif run_reference == "N":
##Unknown EIGENSTRAT CONVERTF par file edits for # of chromosomes
	par_unknown_eigenstrat = eig_par_file_directory_path + 'par.unknown.PED.EIGENSTRAT'	
	with open(par_unknown_eigenstrat) as e:
		par_unknown_EIGENSTRAT_dict = {}
		for line in e:
			k,v = line.split(':')
			v = v.rstrip('\n')
			par_unknown_EIGENSTRAT_dict[k] = v
	
	for key, value in par_unknown_EIGENSTRAT_dict.items():
		par_unknown_EIGENSTRAT_dict['numchrom'] = number_of_chromosomes
		
	par_unknown_EIGENSTRAT_new = eig_par_file_directory_path + 'par.unknown.PED.EIGENSTRAT'
	eopen = open(par_unknown_EIGENSTRAT_new, 'w')
	
	for k,v in par_unknown_EIGENSTRAT_dict.items():
		eopen.write(str(k) + ': ' + str(v) + '\n')
	eopen.close()
		
##Inferancestry par file
	par_inferancestry = eig_par_file_directory_path + 'par.inferancestry'
	with open(par_inferancestry) as i:
		par_inferancestry_dict = {}
		for line in i:
			k,v = line.split(':')
			v = v.rstrip('\n')
			par_inferancestry_dict[k] = v

	for key, value in par_inferancestry_dict.items():
		par_inferancestry_dict['snpwt'] = snpweights_filename

	par_inferancestry_new = eig_par_file_directory_path + 'par.inferancestry'
	iopen = open(par_inferancestry_new, 'w')

	for k,v in par_inferancestry_dict.items():
		iopen.write(str(k) + ': ' + str(v) + '\n')
	iopen.close()



##Code to run if reference calculations need to be made and the genotypes are in plink format
if run_reference == "Y":
	#Filter Reference Genotype Files to Smaller Set of Markers Using Plink
	path_of_outputs_ref_2 = 'ref_filtered/'

	filter_commandline_ref= "python " + path_of_source_code +  "/sw_filt.py " + path_of_inputs_1 + " " + path_of_outputs_ref_2 + " " + marker_list + " " + plink_species_ID + " " + map_files #+ " " + filter_plink_call_rate
	os.system(filter_commandline_ref)

	#Merge Reference Genotype Files Together
	path_of_inputs_ref_3 = 'ref_filtered/'
	reference_prefix = 'ref_input'

	merge_commandline_ref = "python " + path_of_source_code +  "/sw_ref_merge.py " + path_of_inputs_ref_3 + ' ' + plink_species_ID + ' ' + reference_prefix + " " + map_files
	os.system(merge_commandline_ref)
	

	#Change .fam File extension for use in covertf
	change_famfile_extension = 'cp ref_merged/ref_input.fam ref_merged/ref_input.pedind'
	os.system(change_famfile_extension)


	#Convert to EIGENSTRAT format
	par_file_ref_EIG = eig_par_file_directory_path + 'par.reference.PED.EIGENSTRAT'

	convert_eigenstrat_command = EIGENSOFT_software_path + 'bin/convertf -p ' + par_file_ref_EIG
	os.system(convert_eigenstrat_command)


	#Run SmartPCA with Reference Samples
	par_file_ref_SmartPCA = eig_par_file_directory_path + 'par.reference.smartpca'
	smartpca_command = EIGENSOFT_software_path + 'src/eigensrc/smartpca -p ' + par_file_ref_SmartPCA + ' > ref_eigenstrat/ref.log'
	os.system(smartpca_command)


	#Run SNPweight calculator
	par_file_ref_calc_snpwt = eig_par_file_directory_path + 'par.reference.calc_snpwt'
	calc_snpwts_command = 'python ' + SNPweights_software_path + 'calc_snpwt.py --par ' + par_file_ref_calc_snpwt
	os.system(calc_snpwts_command)


##Code to run if genotypes are unknown genotypes
elif run_reference == "N":
	#Filter Unknown Genotype Files to Smaller Set of Markers Using Plink
	path_of_outputs_unk_2 = 'unk_filtered/'

	filter_commandline_unk = "python " + path_of_source_code +  "/sw_filt.py " + path_of_inputs_1 + " " + path_of_outputs_unk_2 + " " + marker_list + " " + plink_species_ID + " " + map_files
	os.system(filter_commandline_unk)


	#Merge Unknown Genotype Files Together
	path_of_inputs_unk_3 = 'unk_filtered/'
	unknown_prefix = 'unk_input'

	merge_commandline_unk = "python " + path_of_source_code +  "/sw_unk_merge.py " + path_of_inputs_unk_3 + ' ' + plink_species_ID + ' ' + unknown_prefix + " " + map_files
	os.system(merge_commandline_unk)


	#Change .fam File extension for use in covertf
	change_famfile_extension = 'cp unk_merged/unk_input.fam unk_merged/unk_input.pedind'
	os.system(change_famfile_extension)


	#Convert to EIGENSTRAT format
	par_file_unk_EIG = eig_par_file_directory_path + 'par.unknown.PED.EIGENSTRAT'
	convert_eigenstrat_command = EIGENSOFT_software_path + 'bin/convertf -p ' + par_file_unk_EIG
	os.system(convert_eigenstrat_command)


	#Inferancestry
	par_file_inferan = eig_par_file_directory_path + 'par.inferancestry'
	inferancestry_command = SNPweights_software_path + 'bin/inferanc -p ' + par_file_inferan
	os.system(inferancestry_command)


	#Edit Output
	output_table_command = "python " + path_of_source_code +  "/sw_edit_snpwt_output.py " + marker_list + " " + final_table_name + " " + snpweights_filename
	os.system(output_table_command)
