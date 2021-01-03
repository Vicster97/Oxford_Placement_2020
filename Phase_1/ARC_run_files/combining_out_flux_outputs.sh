#!/bin/bash

#combining all out_flux and out_flux_seafloor files from their directories into a singles txt file

WORKING_DIR=$PWD
RUNS_DIR=$WORKING_DIR/multiple_models

ParameterSets=() # create an empty array

while IFS= read -r line; do # reading file in row mode, insert each line into array
	ParameterSets+=("$line") # append
	
done < parameter_sets_main.txt

N=$((${#ParameterSets[@]})) #calculates number of parameter sets in parameter_sets.txt 
echo "We have $N models"

i=0 # 'i' is for going through ParameterSets array

echo "Applying combining_out_flux.py and moving the flux.txt files..."
for (( d=0; d<$N; d++ )); do # 'd' is for going through the run directories
	RUN_ID=$RUNS_DIR/all_outputs/model_output_${d}
	cd $RUN_ID; pwd
	python combining_out_flux.py ${d}
	cp -a flux_${d}.txt $RUNS_DIR/all_outputs/all_out_flux_files
done

echo " ... all flux.txt files moved. Now merging into one txt..."
cd $RUNS_DIR/all_outputs/all_out_flux_files
cat * > merged_flux.txt

echo "...done"
