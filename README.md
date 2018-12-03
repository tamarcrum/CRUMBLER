# CRUMBLER
A tool for the prediction of ancestry in cattle.

- Updates 12/3/2018: -
  * Added an avenue for data that plink does not have a "species ID" for.  In this case users, will specify "NA" as the plink_species_ID in their input file.  It is now required to specify chromosome number for the data in the input.
  * Updated the delimiter for file names.  User can now use either an underscore or a period when creating file names.
  * In order to avoid an eigenstrat error when a marker is missing for ALL samples.  There is now a filter in the merge scripts that removes any marker with a genotype rate of less than 1%.
  * CRUMBLER has now been successfully ran in Pigs, following these updates.

- Updates 11/1/2018 - 
  * Updated marker list to exclude any non-autosomal markers (for cow analysis based on reference population in CRUMBLER manuscript)
  * Updated snpwts.reference to be based on the new autosomal marker list (for cow analysis based on referenece population in CRUMBLER manuscript)
  
  - Prior Updates - 
  * Individual updates specified in the commits...  Will try to track any updates in this readme from now on.
