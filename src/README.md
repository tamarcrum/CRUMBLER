Source code for CRUMBLER

Files:

sw_filt.py
 - Filters input genotype files for specified marker/SNP list
 - Handles the additional manipulation of AB genotypes for input into EIGENSTRAT
 
sw_ref_merge.py
  - Merges genotypes files following filtering for reference individuals
  
sw_unk_merge.py
  - Merges genotypes files following filtering for unknown (target) individuals
   
sw_edit_output.py
  - Edits SNPweights output "output_table.txt" to user specified name
  - Adds in a column header for population identification
  - Adds sample IDs to rows for animal identification
  - Removes PC columns
  - Adds 2 columns for reference panel identification (snpwts file name) and marker list identification
