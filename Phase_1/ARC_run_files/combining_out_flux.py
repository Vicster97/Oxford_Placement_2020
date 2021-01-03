#file for combining the SLAMS2.0 out_flux and out_flux_seafloor files into one array

# load usual python packages
import numpy as np

#to allow argument input from cmd pannel 
import argparse

#take arguments from cmd 
parser = argparse.ArgumentParser()
parser.add_argument("model_num")
args = parser.parse_args()

#loading output files 
out_control = np.fromfile("out_control.bin", dtype='>i4')
nTimeStepsPassed, lastpos, nTimesFlux, nSedTrapDeployDepth, nImagingDeployDepth,\
nTimesAvgAtt, nTimesStats, nTimesAux = out_control

out_flux_seafloor = np.fromfile(file_path + "out_flux_seafloor.bin", dtype='>f8').reshape(
    (6,1,nTimesFlux),order='F')[:5,:,-12:]

out_flux = np.fromfile(file_path + "out_flux.bin",dtype='>f8').reshape(
    (6,nSedTrapDeployDepth,nTimesFlux),order='F')[:5,:,-12:]    

flux_all = np.concatenate((out_flux, out_flux_seafloor), axis=1)

poc, tepc, calcite, aragonite, opal = flux_all 

poc_new = poc + tepc
pic = calcite + aragonite

all_flux = np.concatenate((poc_new.reshape(1,31,12), pic.reshape(1,31,12),opal.reshape(1,31,12)))

np.savetxt('flux_'+ str(args.model_num) + '.txt',all_flux.reshape(1,3*31*12))

