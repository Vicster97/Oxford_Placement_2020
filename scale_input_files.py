# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 10:59:47 2020

@author: veronika ulanova
"""

#to allow argument input from cmd pannel 
import argparse

#to write onto binary files 
import struct


#take arguments from cmd 
parser = argparse.ArgumentParser()
parser.add_argument("npp_scaler")
parser.add_argument("SiOH4_scaler")
parser.add_argument("TempC_scaler")
args = parser.parse_args()

#apply exceptions if the input parameters are out of range
if (float(args.npp_scaler) <2e-8) or (float(args.npp_scaler) >4e-6):
    raise Exception("The input value of the npp_scaler parameter is out of range. Try "
                    "choosing a value between 2*10^{-8} and 4*10^{-6}.")
else:
    npp_scaler = float(args.npp_scaler) #otherwise accept the parameters 
    
if (float(args.SiOH4_scaler) <0.1) or (float(args.SiOH4_scaler) >180):
    raise Exception("The input value of the SiOH4_scaler parameter is out of range. Try "
                    "choosing a value between 0.1 and 180.")
else:
    SiOH4_scaler = float(args.SiOH4_scaler)
    
if (float(args.TempC_scaler) <1) or (float(args.TempC_scaler) >30):
    raise Exception("The input value of the TempC_scaler parameter is out of range. Try "
                    "choosing a value between 1 and 30.")
else:
    TempC_scaler = float(args.TempC_scaler)
    
#scailing the NPP
npp = np.fromfile("dataNPPvgpm.bin", dtype='>f8')
maximum_val = max(npp)
scaled_npp = npp_scaler*(npp/maximum_val)

#output NPP
packed_scaled_npp = struct.pack('>'+str(len(scaled_npp)) + 'd', *scaled_npp)

with open("dataNPPvgpmScaled.bin", 'br+') as f1:
    f1.write(packed_scaled_npp)
f1.close()

#scailing the SiOH4 
SiOH4 = np.fromfile("dataSiOH4.bin", dtype='>f8')
maximum_SiOH4 = max(SiOH4)
scaled_SiOH4 = SiOH4_scaler*(SiOH4/maximum_SiOH4)

#output SiOH4
packed_scaled_SiOH4 = struct.pack('>'+str(len(scaled_SiOH4)) + 'd', *scaled_SiOH4)

with open("dataSiOH4Scaled.bin", 'br+') as f2:
    f2.write(packed_scaled_SiOH4)
f2.close()

#scailing the SiOH4 
TempC = np.fromfile("dataTempC.bin", dtype='>f8')
maximum_TempC = max(TempC)
scaled_TempC = TempC_scaler*(TempC/maximum_TempC)

#output TempC
packed_scaled_TempC = struct.pack('>'+str(len(scaled_TempC)) + 'd', *scaled_TempC)

with open("dataTempCScaled.bin", 'br+') as f3:
    f3.write(packed_scaled_TempC)
f3.close()
