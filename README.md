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

**OUTPUT:** running this script in the *ARC_run_files* folder will produce 
a) 1286 independent SLAMS 2.0 models, which can be found at *ARC_run_files/multiple_models/model_{d}*, and 
b) files for output of evry model created at *ARC_run_files/multiple_models/all_outputs/model_output_{d}*, where {d}- is the model number (unique model ID). 

2) *run_models.sh* - the script runs the models with chosen models id. (**NOTE:** this script is run through implementing the *send_jobs.sh* script, which is used to queue a job consisting of multiple model runs to the ARC computer. In order to use it you need to ammend the *send_jobs.sh* script for the number of independent model runs (*nRuns*) you want to have in a job. **DO NOT EXCEED 5000 number of runs** as this number of runs will not finish all at once and the job would be requed and you will most likely lose the progress on the unfinished model runs. **RECOMMENDED nRuns number is 100**, but even then some model instances can be unstable and not finish running in the allocated 24hrs wall time. Ignore these recommendations if you are using a machine different to ARC).

**OUTPUT:** The outputs of the model instances are saved into their individual *model_output_{d}* folders (see above) 

3) *combining_out_flux_outputs.sh* - this scripts pulls all out\_flux.txt files (which is one of the SLAMS2.0 output files) into one folder, *all_output/all_out_flux_files*, where those files are combined into one file named *merged_flux.txt*. This script can be used as a template for combining other SLAMS2.0 output files. Make sure you create a folder in *all_outputs/**yourfoldername*** and change the name of the output merged file. This script runs *combining_out_flux.py* which should be in *ARC_run_files* folder.

**OUTPUT:** The output is *merged_flux.txt* with shape N*M, where N is the number of independent model instances that you have run (i.e. the number of initial parameter sets) and M is the number representing how much information is stored in the output file you combined (e.g. out\_flux.txt has dimensions 3\*31\*12, where 3 is the number of physical properties presented in out\_flux.txt, 30 is the number of depth the three properties are measured at and 12 is the number of month the measurement has been taken, so in this case M = 3\*31\*12 = 1116). Since originally we chose 1500 different variations of the initial 14-parameter sets, N will be equal 1500, but only 1286 rows in merged\_flux.txt will have non-zero values. This is because the outputs from the model instances that were too unstable (and therefore were not completed) were replaced with a row of zeros. The rows of zeros are the models instance that have to be disgarded for further analysis along with the corresponding initial parameter sets, which is done at the end of **Analysing_SLAMS2.0_output_files.ipynb** file in **Preprocessing data for training** section. 

This jupyter notebook also contains code which is used to introduce redundancy into data (replicating it several times, set by **nmult** variable ), the values of mean, standard deviation, maximum and minimum and saves the data in bin format for ML algorithm training. Please refer to the comments in that notebook for further help.

**PHASE 2:**
	i) **Instructions on how to create a wrapper for training a deep emulator on your data:**
1) Once you have done the steps outlined above and have chosen a file (SLAMS2.0 output file or Y, in our case it is the combination of all *out\_flux.bin* files) that you want to use along with X, the file with sets of initial parameters for SLAMS2.0 (*parameter\_sets\_all.txt* which can be found in *Phase_1/Data_for_ML/* folder), you can begin building a wrapper for this data in order to integrate it into the deeep emulator model. You will need the **_params.bin_** and **_specs.bin_** that are produced by **Analysing_SLAMS2.0_output_files.ipynb** file (see PHASE 1 instructions). You will also need the information about the mean, standard deviation (std), maximum (max) and minimum (min) values of your data (e.g. the *merged\_flux\_stable.txt* data) which are also given in that notebook. 

2) **CREATE** a new python file in *Machine_Learning/Codes/deepemu2/deepemulator/diags/* folder and name it *slams2_**OutputFile**.py*. E.g. as we used out\_flux output file from SLAMS2.0, we named our file *slams2_outflux.py*. You can copy the general structure of slams2_outflux.py* into YOUR file and change the following:
	 - a) `class` name: replace *SLAMS2OutFluxDiagnostic* by YOUR name, e.g. *SLAMS2**XXXXX**Diagnostic** where XXXXX is the OutputFile from slams2.0
	 - b) `self.means` values by the mean values you have identified in **Analysing_SLAMS2.0_output_files.ipynb** 
	 - c) `self.stds` values by the mean values you have identified in **Analysing_SLAMS2.0_output_files.ipynb** 
	 - d) `self.nmult` value by the nmult value you used in **Analysing_SLAMS2.0_output_files.ipynb** + 1 (e.g. we used 3 in **Analysing_SLAMS2.0_output_files.ipynb**, so we need to use 4 here)
	 - e) `self.orig_shape` and `self.data_shape` by the shape of the output file you used, we used out\_flux.bin which had shape of 3,31,12 (**NOTE this is NOT the shape of the collection of merged out\_flux files, cause each 'row' in merged\_flux.txt is considered as a separate image**)
	 - f) the returns of the `handle` property 
	 - g) in `data_range` property we need to adjust the number we multiply by n in d = { "largest"}, we used nmult=4 so our total number of rows is 1286*4 = 5144, we want to use 50\% of that for training, so 0.5\*5144 = 2572, and 2572/4 = 643. and we want to use the bigger portion of the rest for testing and smallest for validation. in our example we use 25\% of 5144 (or 1286) for validation and the remaining 25\% for testing, so 2572+1286 = 3858 and 3858/4 = 964.5. do similar calculation based on total number of data rows in your dataset and replace 643 and 964.5 values by your values.
	 - h) `out_channel` property output by the number of 2d images you want ML algorithm to predict. In our example we have 3 physical quantities (PIC,POC and Opal) in out\_flux n=and so 3 images of data = 3 out channels
	 - i) `out_shape` property output, which is the dimenssions of your output images, which is in out case is 31 by 12, for 31 depths and 12 months
	 - j) `name` property output, change the string 
	 - k) `xlims` and `xlabel` properties outputs, dpending if your dimenssions of the images changed in `out_shape` property
	 - l) everything after `ylabel` property ca be deleted as it is not used for training
3) **GO** to *Machine_Learning/Codes/deepemu2/deepemulator/models/rpnas/* folder and **CREATE** a new python file with name *rpnas_2d_slams2_**OutputFile**.py* . Copy over the contents of *rpnas_2d_slams2_outflux.py* and change the following:
	 - a) `__all__ ` variable at the top, make it the same as the name of the file. **THIS IS GOING TO BE YOUR MODEL NAME**
	 - b) `class` name, same as in a)
	 - c) `self.nodes`, the last row has to have the output dimension as the same that you had in `out_shape` property in *deepemulator/diags/slams2_**OutputFile**.py* above. Also the nodes before the last one have to have smaller dimensions than your last node and increase from the first node to the last node. You can have repeats.
	 - d) lastly scroll all the way to the bottom and change the value of `dn` variable to match the name of the file. E.g. *rpnas_2d_slams2_outflux()* to *rpnas_2d_slams2_**OutputFile**()*. **DO NOT FORGET A SET OF CURLY BRACKETS AT THE END SINCE dn CALLS A THE CLASS THAT YOU JUST DEFINED IN THIS FILE**
3) **GO** back put to *Machine_Learning/Codes/deepemu2/deepemulator/models/* and **ADD** the model you have just created into the *factory.py* file. Specifically you need to add the following lines:
	 - a) `from deepemulator.models.rpnas.rpnas_2d_slams2_OUTPUTFILE import rpnas_2d_slams2_OUTPUTFILE` where capital letter are replaced by the name you gave your model
	 - b) inside the `getmodel` function add an extra line: `"rpnas_2d_slams2_OUTPUTFILE" : rpnas_2d_slams2_OUTPUTFILE`, where capital letters are placeholders for your name
save and close 
4) **NAVIGATE TO** *Machine_Learning/Codes/deepemu2/deepemulator/datasets/* and **CREATE** a folder for your data. E.g. we used out\_flux file in slams2.0, so the folder name for that data set is *slams2_outflux*, so use *slams2_OUTPUTFILE* format. Then **COPY OVER** your *params.bin* and *specs.bin* files to this folder.
5) **TRAIN** the model by navigating to the *Machine_Learning/Codes/deepemu2/deepemulator/trains/* folder and editing the *command.sh* file:
	 - a) 3rd item should be replaces by the `handle` property in your diag file in *Machine_Learning/Codes/deepemu2/deepemulator/diags/*. In our case this is *slams2_outflux*.
	 - b) item after `--model` feature should read the name of your model as given in your model file in *Machine_Learning/Codes/deepemu2/deepemulator/models/rpnas/*. In our case it is *rpnas_2d_slams2_outflux*
	 - c) the remaining feature are the initial parameters for ML algorithm training and can be changed as desired 
**SAVE and CLOSE**
6) before we can train the deep emulator we need to compile all the models. **NAVIGATE** to the *Machine_Learning/Codes/deepemu2/deepemulator/trains/* and **COMPLETE** the steps outlined in *README.md* file's *Getting started* section. Then **RUN** command.sh from terminal for model training according to steps outlined in the *Training* section.

**NOTE:** every python file created in deepemulator is accompanied by a pyc file with a similar name, which are created automatically after a model (command.sh) is run. There is no need to create pyc files, only the py files need to be created.

**OUTPUT:** At the end of the deepemulator training the wrapper produces a folder with the trained model outputs. **NAVIGATE** to *Machine_Learning/Codes/deepemu2/results/*. The most recent training would be the most recently produced folder named *XXXXXX-spv-slams2-rpnas_2d_slams2*, where XXXXXX is the id of the training (every time *command.sh* is executed and is finished properly it is assigned trainign id that goes into the file name). 

**USING TRAINED MODEL FOR PREDICTIONS:**
a) **NAVIGATE** to the last created folder in *Machine_Learning/Codes/deepemu2/results/* and **MOVE** the whole folder to  *Machine_Learning/Codes/Analysing_outputs/* . 
*to be continued soon...*

**PHASE 2:** ii) **Trainign other ML models:** 
*coming soon....*

**PHASE 3:**
**Using the trained ML to predict SLAMS2.0 output**
Please go to Phase 3 folder where you can find the code for implementing this phase and relevant comments in the **Analysing_out_flux.ipynb** notebook. 










REFERENCES:
[1] Jokulsdottir T, Archer D. A stochastic, Lagrangian model of sinking biogenic aggregates in the ocean (SLAMS 1.0): model formulation, validation and sensitivity. Geoscientific Model Development. 2016 Apr 19;9(4):1455-76.
[2] Blanco AR, Jokulsdottir T, May D, Barrett S, Khatiwala S. A 3-D Model of Lagrangian Marine Particles. InOcean Sciences Meeting 2020 2020 Feb 18. AGU.
