#!/bin/bash

# Read the parameter sets from textfile parameter.txt into the array ParameterSets

WORKING_DIR=$PWD
RUNS_DIR=$WORKING_DIR/multiple_models

echo "The working directory is $WORKING_DIR "

ParameterSets=() # create an empty array

while IFS= read -r line; do # reading file in row mode, insert each line into array
	ParameterSets+=("$line") # append
	
done < parameter_sets.txt

N=$((${#ParameterSets[@]})) #calculates number of parameter sets in parameter_sets.txt 
echo "We have $N parameter sets"

i=0 # 'i' is for going through dataNumDepthLayers array

echo "Writing the local parameters into the namelist..."
for (( d=1; d<=$N; d++ )); do # 'd' is for going through the run directories
	mkdir -p $RUNS_DIR/model_${d} #create model directories
	mkdir -p $RUNS_DIR/all_outputs/model_output_S{d} #create directories for model outputs 
	
	cp -a $WORKING_DIR/SLAMS2.0_modelfiles/. $RUNS_DIR/model_${d} 
	RUN_ID=$RUNS_DIR/model_${d}
	cd $RUN_ID; pwd
	cp namelist_template namelist.input #makes a new file 'namelist.inputs' with contents of 'namelis_template'
	
	# unpack the parameter set into individual parameters
	Parameters=()
	for j in ${ParameterSets[$i]}; do
		Parameters+=("$j");
	done
	
	# update 14 parameters on namelist.input with new values:
	sed_fractal=s/fractal_dimension_agg=.*/fractal_dimension_agg=${Parameters[0]}/  
	sed -i "$sed_fractal" namelist.input
	
	sed_Si2C_diat=s/Si2C_diat=.*/Si2C_diat=${Parameters[1]}/  
	sed -i "$sed_Si2C_diat" namelist.input
	
	sed_Calc2C_cocco=s/Calc2C_cocco=.*/Calc2C_cocco=${Parameters[2]}/  
	sed -i "$sed_Calc2C_cocco" namelist.input
	
	sed_k_NO3_diat=s/k_NO3_diat=.*/k_NO3_diat=${Parameters[3]}/  
	sed -i "$sed_k_NO3_diat" namelist.input

	sed_k_NO3_cocco=s/k_NO3_cocco=.*/k_NO3_cocco=${Parameters[4]}/  
	sed -i "$sed_k_NO3_cocco" namelist.input

	sed_phyto_exudation_frac=s/phyto_exudation_frac=.*/phyto_exudation_frac=${Parameters[5]}/  
	sed -i "$sed_phyto_exudation_frac" namelist.input

	sed_poc_to_zoo=s/poc_to_zoo=.*/poc_to_zoo=${Parameters[6]}/  
	sed -i "$sed_poc_to_zoo" namelist.input
	
	sed_poc_to_zoo_night_dvmdepth=s/poc_to_zoo_night_dvmdepth=.*/poc_to_zoo_night_dvmdepth=${Parameters[7]}/  
	sed -i "$sed_poc_to_zoo_night_dvmdepth" namelist.input
	
	sed_resp_rate_max_mesozoo=s/resp_rate_max_mesozoo=.*/resp_rate_max_mesozoo=${Parameters[8]}/  
	sed -i "$sed_resp_rate_max_mesozoo" namelist.input
	
	sed_resp_rate_max_bact=s/resp_rate_max_bact=.*/resp_rate_max_bact=${Parameters[9]}/  
	sed -i "$sed_resp_rate_max_bact" namelist.input
	
	sed_dissol_timescale_calc=s/dissol_timescale_calc=.*/dissol_timescale_calc=${Parameters[10]}/  
	sed -i "$sed_dissol_timescale_calc" namelist.input
	
	let i++
done
echo "... done."
