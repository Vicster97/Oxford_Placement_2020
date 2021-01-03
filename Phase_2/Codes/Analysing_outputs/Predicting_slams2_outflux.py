#import requied packages and model files 
from deepemulator.diags import getdiagnostic
import numpy as np
import scipy as sp
import pickle
import time

#to allow argument input from cmd pannel 
import argparse


#define the function that calculates huber loss
def huber(x,y):
    err = np.abs(x - y)
    sqmask = 1.0 * (err < 1)
    return 0.5 * err*err * sqmask + (err - 0.5) * (1.0 - sqmask)

# load the diagnostic/simulation details and the model
otherml_name = "ExtraTreesRegressor"
model_file_name = "results-oml/trained-objects/"
weights = "slams2-ExtraTreesRegressor.pkl"

#take arguments from cmd 
parser = argparse.ArgumentParser()
parser.add_argument("frac_dim_agg")
parser.add_argument("Si2C_diat")
parser.add_argument("Calc2C_cocco")
parser.add_argument("k_NO3_diat")
parser.add_argument("k_NO3_cocco")
parser.add_argument("phyto_exu_frac")
parser.add_argument("poc_to_zoo")
parser.add_argument("poc_to_zoo_night")
parser.add_argument("resp_rate_max_mesozoo")
parser.add_argument("resp_rate_max_bact")
parser.add_argument("dissol_timescale_calc")
parser.add_argument("npp")
parser.add_argument("SiOH4")
parser.add_argument("TempC")
args = parser.parse_args()

#apply exceptions if the input parameters are out of range
if (float(args.frac_dim_agg) <1.3) or (float(args.frac_dim_agg) >2.3):
    raise Exception("The input value of the frac_dim_agg parameter is out of range. Try "
                    "choosing a value between 1.3 and 2.3")
else:
    frac_dim_agg = float(args.frac_dim_agg) #otherwise accept the parameters 

if (float(args.Si2C_diat) <0.030) or (float(args.Si2C_diat) >0.65):
    raise Exception("The input value of the Si2C_diat parameter is out of range. Try "
                    "choosing a value between 0.030 and 0.65.")
else:
    Si2C_diat = float(args.Si2C_diat) #otherwise accept the parameters 
    
if (float(args.Calc2C_cocco) <0.5) or (float(args.Calc2C_cocco) >2.5):
    raise Exception("The input value of the Calc2C_cocco parameter is out of range. Try "
                    "choosing a value between 0.5 and 2.5.")
else:
    Calc2C_cocco = float(args.Calc2C_cocco) #otherwise accept the parameters 
    
if (float(args.k_NO3_diat) <0.1) or (float(args.k_NO3_diat) >3.0):
    raise Exception("The input value of the k_NO3_diat parameter is out of range. Try "
                    "choosing a value between 0.1 and 3.0.")
else:
    k_NO3_diat = float(args.k_NO3_diat) #otherwise accept the parameters 

if (float(args.k_NO3_cocco) <0.1) or (float(args.k_NO3_cocco) >1):
    raise Exception("The input value of the k_NO3_cocco parameter is out of range. Try "
                    "choosing a value between 0.1 and 1.")
else:
    k_NO3_cocco = float(args.k_NO3_cocco) #otherwise accept the parameters 
    
if (float(args.phyto_exu_frac) <0.02) or (float(args.phyto_exu_frac) >0.6):
    raise Exception("The input value of the phyto_exu_frac parameter is out of range. Try "
                    "choosing a value between 0.02 and 0.6.")
else:
    phyto_exu_frac = float(args.phyto_exu_frac) #otherwise accept the parameters 

if (float(args.poc_to_zoo) <2) or (float(args.poc_to_zoo) >10):
    raise Exception("The input value of the poc_to_zoo parameter is out of range. Try "
                    "choosing a value between 2 and 10.")
else:
    poc_to_zoo = float(args.poc_to_zoo) #otherwise accept the parameters 
    
if (float(args.poc_to_zoo_night) <0.2) or (float(args.poc_to_zoo_night) >1):
    raise Exception("The input value of the poc_to_zoo_night parameter is out of range. Try "
                    "choosing a value between 0.2 and 1.")
else:
    poc_to_zoo_night = float(args.poc_to_zoo_night) #otherwise accept the parameters 
    
if (float(args.resp_rate_max_mesozoo) <0.03) or (float(args.resp_rate_max_mesozoo) >0.25):
    raise Exception("The input value of the resp_rate_max_mesozoo parameter is out of range. Try "
                    "choosing a value between 0.03 and 0.25.")
else:
    resp_rate_max_mesozoo = float(args.resp_rate_max_mesozoo) #otherwise accept the parameters 
    
if (float(args.resp_rate_max_bact) <0.01) or (float(args.resp_rate_max_bact) >0.5):
    raise Exception("The input value of the resp_rate_max_bact parameter is out of range. Try "
                    "choosing a value between 0.01 and 0.5.")
else:
    resp_rate_max_bact = float(args.resp_rate_max_bact) #otherwise accept the parameters 
    
if (float(args.dissol_timescale_calc) <1) or (float(args.dissol_timescale_calc) >7):
    raise Exception("The input value of the dissol_timescale_calc parameter is out of range. Try "
                    "choosing a value between 1 and 7.")
else:
    dissol_timescale_calc = float(args.dissol_timescale_calc) #otherwise accept the parameters 
    
if (float(args.npp) <2e-8) or (float(args.npp) >4e-6):
    raise Exception("The input value of the npp parameter is out of range. Try "
                    "choosing a value between 2*10^{-8} and 4*10^{-6}.")
else:
    npp = float(args.npp) #otherwise accept the parameters 
    
if (float(args.SiOH4) <0.1) or (float(args.SiOH4) >180):
    raise Exception("The input value of the SiOH4 parameter is out of range. Try "
                    "choosing a value between 0.1 and 180.")
else:
    SiOH4 = float(args.SiOH4)
    
if (float(args.TempC) <1) or (float(args.TempC) >30):
    raise Exception("The input value of the TempC parameter is out of range. Try "
                    "choosing a value between 1 and 30.")
else:
    TempC = float(args.TempC)
    
input_params = np.array([frac_dim_agg, Si2C_diat, Calc2C_cocco, k_NO3_diat, k_NO3_cocco, phyto_exu_frac, poc_to_zoo, poc_to_zoo_night, resp_rate_max_mesozoo, resp_rate_max_bact, dissol_timescale_calc, npp, SiOH4, TempC])
print(input_params.shape)

diag = getdiagnostic("slams2_outflux")

#loads the trained ExtraTreesRegressor 
with open(model_file_name + weights, "rb") as fb:
    reg = pickle.load(fb)

prof = np.array(diag.out_model_to_display(torch.Tensor(reg.predict(input_params)))).reshape(1,3*31*12)

np.savetxt("predicted_outflux.txt", prof)
print("Outputs saved.")

