import numpy as np
import pkg_resources


### open the F2 files and fills arrays with their values.
def openf2 (source_file):
    path = pkg_resources.resource_filename("quantorxs", source_file)
    f = open(path,'r')
    header1 = f.readline()
    header2 = f.readline()
    header3 = f.readline()
    header4 = f.readline()
    header5 = f.readline()
    numline = int(851) 		               #    Reads the number of datapoints in the source file
    E_f2 = np.ndarray(numline, float)
    OD_f2 = np.ndarray(numline, float)
    k=0
    for line in f:						#Reads the line/column of the source file and fills the arrays
        line = line.strip()
        columns = line.split()
        E_f2[k] = float(columns[0])
        OD_f2[k] = float(columns[2])
        k=k+1
    f.close()
    return E_f2, OD_f2

#Open and reads the spectra from the directory
def openfile(spectrum_path):
    E, OD = np.loadtxt(spectrum_path, skiprows=4).T
    return E, OD
