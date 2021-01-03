# Oxford_Placement_2020

**Short Abstract of the Project.**

This folder cointains the code produced as part of the summer 2020 Data Science placement at Oxford. This project aims at training an ML algorithm that can accurately replicate the outputs of the Stochastic, Lagrangian model of sinking biogenic aggregates in the ocean (SLAMS 1.0) originally put together by Jokulsdottir et al 2016 [1] and then revised by Anna Rufas during her P.h.D at Oxford University (SLAMS 2.0) [2]. We chose to vary 14 parameters to test the sensitivity of SLAMS 2.0 outputs and therefore use those 14 parameters as inputs (X) and the SLAMS 2.0 outputs (Y) for ML training (namely the out\_flux.txt). We use the Latin-Hyper-Sampling (LHS) to produce 1286 independent sets of 14 input parameters. The description of the 14 parameters as well as the ranges used for the LHS can be found in *selection\_params\_sensitivity.xlsx* . **NOTE: during the initial runs of the SLAMS2.0 on the ARC network only 1286 put of 1500 instances were able to be completed in full dur to the constraints of ARC wall time. Therefore the 204 unfinished model instances (also reffered to as unstable model instances) were not used for further analysis (i.e. past phase 1 of this project)**

After trying several algorithms for predictions of out\_flux, we found the Extra Trees Regressor model to be the most successful at understanding the relationship between the input parameters and out\_flux.txt outputs (as this model produced the lelast huber-loss, criteria that we chose to evaluate model predictions). We used the outputs of Extra Trees Regressor (ETR) model, i.e. predicted out\_flux, to test the sensitivity of SLAMS 2.0 to the chosen 14 input parameters.
We found that our ML predictions replicate the overall pattern of the out\_flux data well, however the individual values of physical quantities covered by out\_flux (e.g. PIC, POC and Opal quantities) wary greatly from their expected values. We also found that POC and Opal predicted profiles were the most successfully replicated by our algorithm, reinforcing the anticipated uncertain nature of the PIC signal.

This project had 3 phases:
1) Creating a collection of data from running the SLAMS2.0 model N number of times with N set of initial parameters. The outputs of the model produced 18 files with data, we picked 1 in this project to use for a proof of concept.
2) Writing additional model files for the deep emulator and other ML models to enable those algorithms to learn our dataset. This includes: *put includded file names here* 
3) Training the models and evaluating which models performed best at learning the statistically significant signal that i spresented in out data set (i.e. the connection between the set of 14-input paraneters and the SLAMS2.0 output files). 


**PHASE 1:**
- **File Description**
1) *create_ocean_models.sh* - creates 1286 unique ocean models (versions of SLAMS 2.0 ) with the 1286 LHS-led 14-paramter sets (the parameter sets can be found in *parameter_sets_main.txt* and *scailing_factors_for_bin.txt*, where the first file has the first 10 parameters from the *selection_params_sensitivity.xlsx* and the last file cointains the other 4). This script runs a *scale_input_files.py* which has to be **INCLUDED INTO THE** *SLAMS2.0_modelfiles* folder as the last 4 parameter inputs are not individual values but arrays of values (profiles) that have to be scaled against a chosen value (e.g. temperature profile). 
**OUTPUT:** running this script in the *ARC_run_files* folder will produce a) 1286 independent SLAMS 2.0 models, which can be found at *ARC_run_files/multiple_models/model_{d}*, and b) files for output of evry model created at *ARC_run_files/multiple_models/all_outputs/model_output_{d}*, where {d}- is the model number (unique model ID). 
2) *run_models.sh* - the script runs the models with chosen models id (**NOTE:** this script is run through implementing the *send_jobs.sh* script, which is used to queue a job consisting of multiple model runs to the ARC computer. In order to use it you need to ammend the *send_jobs.sh* script for the number of independent model runs (*nRuns*) you want to have in a job. **DO NOT EXCEED 5000 number of runs** as this number of runs will not finish all at once and the job would be requed and you will most likely lose the progress on the unfinished model runs. **RECOMMENDED nRuns number is 100**, but even then some model instances can be unstable and not finish running in the allocated 24hrs wall time. Ignore these recommendations if you are using a machine different to ARC).
**OUTPUT:** The outputs of the model instances are saved into their individual *model_output_{d}* folders (see above) 
3) *combining_out_flux_outputs.sh* - this scripts pulls all out\_flux.txt files (which is one of the SLAMS2.0 output files) into one folder, *all_output/all_out_flux_files*, where those files are combined into one file named *merged_flux.txt*. This script can be used as a template for combining other SLAMS2.0 output files. Make sure you create a folder in *all_outputs/**yourfoldername*** and change the name of the output merged file. This script runs *combining_out_flux.py* which should be in *ARC_run_files* folder.
**OUTPUT:** The output is *merged_flux.txt* with shape N*M, where N is the number of independent model instances that you have run (i.e. the number of initial parameter sets) and M is the number representing how much information is stored in the output file you combined (e.g. out\_flux.txt has dimensions 3\*30\*12, where 3 is the number of physical properties presented in out\_flux.txt, 30 is the number of depth the three properties are measured at and 12 is the number of month the measurement has been taken, so in this case M = 3\*30\*12 = 1080). Since originally we chose 1500 different variations of the initial 14-parameter sets, N will be equal 1500, but only 1286 rows in merged\_flux.txt will have non-zero values. This is because the outputs from the model instances that were too unstable (and therefore were not completed) were replaced with a row of zeros. The rows of zeros are the models instance that have to be disgarded t=for further analysis along with the corresponding initial parameter sets, which is done in **PUT FILE THAT DPES THIS HERE**. 










REFERENCES:
[1] Jokulsdottir T, Archer D. A stochastic, Lagrangian model of sinking biogenic aggregates in the ocean (SLAMS 1.0): model formulation, validation and sensitivity. Geoscientific Model Development. 2016 Apr 19;9(4):1455-76.
[2] Blanco AR, Jokulsdottir T, May D, Barrett S, Khatiwala S. A 3-D Model of Lagrangian Marine Particles. InOcean Sciences Meeting 2020 2020 Feb 18. AGU.
