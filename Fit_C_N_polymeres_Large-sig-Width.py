from scipy import optimize
import xlsxwriter
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.integrate import simps
import glob
import os.path
from numpy import ndarray #, array
from math import*

"""
import xlrd
from scipy.integrate import quad
from scipy import stats
import scipy
"""

#Description of all parameters used for further analysis of the spectra

Emin = 270              # Lower energy of the range used for the raw spectrum _ 270
Emax_C = 700            # Higher end of the energy range used for the raw spectrum
dE = 0.1			    # Energy step used for the discretization of the spectrum

Estop_C = 282           # Energy up to which the pre-edge background fitting is performed _ 282
Enorm_C = 291.5         # Energy up to which the area normalization is calculated _ 291.5
Efit_C = 305            # Energy up to which the gaussian fitting is performed _ 305
EpeMin_C = 355          # Energy from which the fitting of the carbon step function is considered for fitting the post-edge _ 355
w_C = 0.2               # Half Width at Half Maximum of the fitted gaussians _ 0.2

Emin_N = 370            # Energy at which the Nitrogen edge analysis begins _ 370
Estop_N = 395           # Energy up to which the pre-edge background fitting is performed _ 397
Enorm_N = 406.5         # Energy up to which the area normalization is calculated _ 406.5
Efit_N = 420            # Energy up to which the gaussian fitting is performed _ 420
EpeMin_N = 430          # Energy from which the fitting of the Nitrogen step function is considered for fitting the post edge _ 430
Emax_N = 449            # Energy up to which the fitting of the post edge is performed _ 449
w_N = 0.3               # Half Width at Half Maximum used for the fitted gaussians _ 0.3

Emin_O = 470            # Energy at which the Oxygen edge analysis begins _ 470
Estop_O = 527.5         # Energy up to which the pre-edge background fitting is performed _ 527.5
Enorm_O = 540           # Energy up to which the area normalization is calculated _ 540
EpeMin_O = 600          # Energy from which the fitting of the Oxygen step function is considered for fitting the post edge _ 600
Emax_O = 680            # Energy up to which the fitting of the Oxygen step function is considered for fitting the post edge _ 680

shift = 0             # If energy axis needs calibration, the spectra can be directly shifted here.

### Values issued from the calibration used to quantify the functional groups
Aro_pente = 524.864
Aro_ordo = -2.587
Aro_s1 = 4.5
Keton_pente = 283.011	
Keton_ordo = -2.851
Keton_s1 = 2.4
Ali_pente = 699.038	
Ali_ordo = -22.241
Ali_s1 = 11.1
Carbo_pente = 40.801	
Carbo_ordo = -4.001
Carbo_s1 = 7.2

#Creates lists of the functional groups used for the gaussian deconvolutions
List_Func_Group_C = ('284.1', '284.4', '284.7', '285', '285.4', '285.8', '286.2', '286.5', '286.8', '287.2', '287.5', '287.8', '288.2', '288.5', '288.9', '289.4', '289.9', '290.3', '290.8', '291.2', '291.5', '292.1', '292.7', '293.3', '294', '295', '297.1', '297.5', '299.7', '300', '302.5', '305', '307.5', '310', '312.5', 'Normalization constant', 'Fit Er (Min. sq.)')
Func_Group_C = (284.1, 284.4, 284.7, 285, 285.4, 285.8, 286.2, 286.5, 286.8, 287.2, 287.5, 287.8, 288.2, 288.5, 288.9, 289.4, 289.9, 290.3, 290.8, 291.2, 291.5, 292.1, 292.7, 293.3, 294, 295, 297.1, 297.5, 299.7, 300, 302.5, 305, 307.5, 310, 312.5)
tab_Func_Group_C = ndarray (len(Func_Group_C), float)

List_Func_Group_N = ('398.7', '398.9', '399.3', '399.6', '400', '400.6', '401', '401.1', '401.4', '401.6', '402', '402.5', '403', '403.4', '403.8', '404.4', '405', '405.4', '406', '406.4', '406.7', '407', '407.3', '407.6', '408', '408.5', '411', '413.7', '416', '420', 'Normalization constant', 'Fit Er (Min. sq.)')
Func_Group_N = (398.7, 398.9, 399.3, 399.6, 400, 400.6, 401, 401.1, 401.4, 401.6, 402, 402.5, 403, 403.4, 403.8, 404.4, 405, 405.4, 406, 406.4, 406.7, 407, 407.3, 407.6, 408, 408.5, 411, 413.7, 416, 420)
tab_Func_Group_N = ndarray (len(Func_Group_N), float)

# Opens the source file repertory, creates a list of them, and shorten their name (repoertory and extension) for printing purposes.
repertoire = 'Raw Axis Spectra'
def listdirectory(repertoire):
    liste_fichier=[]
    l = glob.glob(repertoire+'\\*')
    for i in l:
        if os.path.isdir(i): liste_fichier.extend(listdirectory(i))
        else: liste_fichier.append(i)
    return liste_fichier
liste_fichier = listdirectory(repertoire)
i=0
for f in liste_fichier:
    liste_fichier[i] = liste_fichier[i][len('Raw Axis Spectra\\'):len(liste_fichier[i])-len('.txt')]
    i=i+1

#Fills a table with all gaussian positions
i=0
for elt in Func_Group_C:
    tab_Func_Group_C [i] = elt
    i=i+1

i=0
for elt in Func_Group_N:
    tab_Func_Group_N [i] = elt
    i=i+1

### open the F2 files and fills arrays with their values.
def openf2 (source_file):
    f = open(source_file,'r')
    header1 = f.readline()				
    header2 = f.readline()
    header3 = f.readline()
    header4 = f.readline()
    header5 = f.readline()
    numline = int(851) 		               #    Reads the number of datapoints in the source file
    E_f2 = ndarray(numline, float)		   
    OD_f2 = ndarray(numline, float)
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
def openfile(spectre):
    f = open(repertoire+"/"+spectre,'r')
    
    header1 = f.readline()				#Lit une a un les header pour commencer à lire les données réelles apres
    header2 = f.readline()
    header3 = f.readline()
    header4 = f.readline()
    numline = int(header3[1:1000]) 		#Renvoie le nombre de ligne depuis la source
    E = ndarray(numline, float)			#Défini les dimensions et la classe de variable du tableau
    OD = ndarray(numline, float)

    k=0
    for line in f:						#Lit les lignes une a une et délimite les colonnes
        line = line.strip()
        columns = line.split()
        E[k] = float(columns[0])
        OD[k] = float(columns[1])
        k=k+1
    f.close()
    return E, OD

# Interpolate the data to discretize them and have arrays of data of similar dimensions
def discretize (E, ODlb, Einf, Esup):
    numE = ((Esup-Einf)/dE)+1
    Ei = np.linspace(Einf, Esup, num=numE, endpoint=True)							# Creates a linear space of discretized E values
    In = interpolate.interp1d(E, ODlb, bounds_error=False, fill_value=0)		    # Defines the interpolation function
    ODi = In(Ei)																	# Applies the function
    return Ei, ODi

# Substract a power law background from a spectrum
def powerlaw_Bgd (E, OD, Emin, Estop):
    if max(E) <= 400:
        Emin = np.ceil(min(E))
    Ei, ODi = discretize (E, OD, Emin, np.ceil(max(E))) 
    def powerlaw (x, amp, index):
        return amp * (x**index)
    
    E_bcg = ndarray(int((Estop-Emin)/dE), float)
    OD_bcg = ndarray(int((Estop-Emin)/dE), float)

    for i in range (0, int((Estop-Emin)/dE)):
        E_bcg[i] = Ei[i]
        OD_bcg[i] = ODi[i]
    
    B = 0    
    amp = 1
    index = 1
    param = np.array([B, amp, index])
    errfunc = lambda param, x, y: ((param[0] + powerlaw(x, param[1], param[2])) - y)**2
    guess = param
    param, success = optimize.leastsq(errfunc, guess[:], args = (E_bcg, OD_bcg))
    
    OD_lb_powlaw = OD-(param[0] + powerlaw(E, param[1], param[2]))
    return OD_lb_powlaw

# Normalize the spectrum by fitting the f2 scattering over a range of pre-edge and post-edge energies then plot
def normalize_f2(OD, f):
    Ei, ODi = discretize (E, OD, Emin, max(E))
    Ei_C_f2, ODi_C_f2 = discretize (E_Cf2, OD_Cf2, Emin, max(E))   
    #Ei_K_f2, ODi_K_f2 = discretize (E_Nf2, OD_Nf2, Emin, max(E))
    #Ei_Ca_f2, ODi_Ca_f2 = discretize (E_Nf2, OD_Nf2, Emin, max(E))
    Ei_N_f2, ODi_N_f2 = discretize (E_Nf2, OD_Nf2, Emin, max(E))
    Ei_O_f2, ODi_O_f2 = discretize (E_Of2, OD_Of2, Emin, max(E))
    
    Kc = 0      # list of the parameters which are going to be fitted, including absorption coefft and power law parameters
    Kn = 0
    Ko = 0
    B = 0
    amp1 = 0
    index1 = 1
    amp2 = 0
    index2 = 1
    amp3 = 0
    index3 = 1   
    
    # The fit is performed only on specific pre and post edge energies ranges which are defined below with specific variables.
    if max(E) >= Emax_O:
        Ei_fit = ndarray((int((Estop_C-Emin)/dE) + int((Estop_N-EpeMin_C)/dE) + int((Estop_O-Emin_O)/dE) + int((Emax_O-EpeMin_O)/dE)), float)
        ODi_fit = ndarray((int((Estop_C-Emin)/dE) + int((Estop_N-EpeMin_C)/dE) + int((Estop_O-Emin_O)/dE) + int((Emax_O-EpeMin_O)/dE)), float)			#Défini les dimensions et la classe de variable du tableau
        ODi_f2_fitC = ndarray((int((Estop_C-Emin)/dE) + int((Estop_N-EpeMin_C)/dE) + int((Estop_O-Emin_O)/dE) + int((Emax_O-EpeMin_O)/dE)), float)			#Défini les dimensions et la classe de variable du tableau
        ODi_f2_fitN = ndarray((int((Estop_C-Emin)/dE) + int((Estop_N-EpeMin_C)/dE) + int((Estop_O-Emin_O)/dE) + int((Emax_O-EpeMin_O)/dE)), float)			#Défini les dimensions et la classe de variable du tableau
        ODi_f2_fitO = ndarray((int((Estop_C-Emin)/dE) + int((Estop_N-EpeMin_C)/dE) + int((Estop_O-Emin_O)/dE) + int((Emax_O-EpeMin_O)/dE)), float)			#Défini les dimensions et la classe de variable du tableau
        
        k=0
        for i in range (0, int((Estop_C-Emin)/dE)):
            Ei_fit[k] = Ei[i]
            ODi_fit[k] = ODi[i]
            ODi_f2_fitO[k] = ODi_O_f2[i]
            ODi_f2_fitC[k] =  ODi_C_f2[i]
            ODi_f2_fitN[k] = ODi_N_f2[i]
            k=k+1
        for i in range (int((EpeMin_C-Emin)/dE), int((Estop_N-Emin)/dE)):
            Ei_fit[k] = Ei[i]
            ODi_fit[k] = ODi[i]
            ODi_f2_fitO[k] = ODi_O_f2[i]
            ODi_f2_fitC[k] =  ODi_C_f2[i]
            ODi_f2_fitN[k] = ODi_N_f2[i]
            k=k+1        
        for i in range (int((Emin_O-Emin)/dE), int((Estop_O-Emin)/dE)):
            Ei_fit[k] = Ei[i]
            ODi_fit[k] = ODi[i]
            ODi_f2_fitO[k] = ODi_O_f2[i]
            ODi_f2_fitC[k] =  ODi_C_f2[i]
            ODi_f2_fitN[k] = ODi_N_f2[i]
            k=k+1
        for i in range (int((EpeMin_O-Emin)/dE), int((Emax_O-Emin)/dE)):
            Ei_fit[k] = Ei[i]
            ODi_fit[k] = ODi[i]
            ODi_f2_fitO[k] = ODi_O_f2[i]
            ODi_f2_fitC[k] =  ODi_C_f2[i]
            ODi_f2_fitN[k] = ODi_N_f2[i]
            k=k+1
        
        # Defines the parameters to fit and the function to optimize
        param = np.array([B, Kc, Kn, Ko, amp1, index1, amp2, index2, amp3, index3])  
        errfunc = lambda param, x, y: ((param[0] + param[1]*ODi_f2_fitC + param[2]*ODi_f2_fitN + param[3]*ODi_f2_fitO + param[4]*(x**param[5]) + param[6]*(x**param[7]) + param[8]*(x**param[9])) - y)**2
        guess = param
        param, success = optimize.leastsq(errfunc, guess[:], args = (Ei_fit, ODi_fit))
        (B, Kc, Kn, Ko, amp1, index1, amp2, index2, amp3, index3) = (param[0], param[1], param[2], param[3], param[4], param[5], param[6], param[7], param[8], param[9]) 

    elif max(E) >= Emax_N:        
        Ei_fit = ndarray((int((Estop_C-Emin)/dE) + int((Estop_N-EpeMin_C)/dE) + int((Emax_N-EpeMin_N)/dE))) 
        ODi_fit = ndarray((int((Estop_C-Emin)/dE) + int((Estop_N-EpeMin_C)/dE) + int((Emax_N-EpeMin_N)/dE)))
        ODi_f2_fitC = ndarray((int((Estop_C-Emin)/dE) + int((Estop_N-EpeMin_C)/dE) + int((Emax_N-EpeMin_N)/dE)))
        ODi_f2_fitN = ndarray((int((Estop_C-Emin)/dE) + int((Estop_N-EpeMin_C)/dE) + int((Emax_N-EpeMin_N)/dE)))
        
        k=0
        for i in range (0, int((Estop_C-Emin)/dE)):
            Ei_fit[k] = Ei[i]
            ODi_fit[k] = ODi[i]
            ODi_f2_fitC[k] =  ODi_C_f2[i]
            ODi_f2_fitN[k] = ODi_N_f2[i]
            k=k+1
        for i in range (int((EpeMin_C-Emin)/dE), int((Estop_N-Emin)/dE)):
            Ei_fit[k] = Ei[i]
            ODi_fit[k] = ODi[i]
            ODi_f2_fitC[k] =  ODi_C_f2[i]
            ODi_f2_fitN[k] = ODi_N_f2[i]
            k=k+1
        for i in range (int((EpeMin_N-Emin)/dE), int((Emax_N-Emin)/dE)):
            Ei_fit[k] = Ei[i]
            ODi_fit[k] = ODi[i]
            ODi_f2_fitC[k] =  ODi_C_f2[i]
            ODi_f2_fitN[k] = ODi_N_f2[i]
            k=k+1

        param = np.array([B, Kc, Kn, amp1, index1, amp2, index2])  
        errfunc = lambda param, x, y: ((param[0] + param[1]*ODi_f2_fitC + param[2]*ODi_f2_fitN + param[3]*(x**param[4]) + param[5]*(x**param[6])) - y)**2
        guess = param
        param, success = optimize.leastsq(errfunc, guess[:], args = (Ei_fit, ODi_fit))
        (B, Kc, Kn, Ko, amp1, index1, amp2, index2, amp3, index3) = (param[0], param[1], param[2], 0, param[3], param[4], param[5], param[6], 0, 0) 

    elif max(E) >= 395:
        Ei_fit = ndarray((int((Estop_C-Emin)/dE) + int((395-EpeMin_C)/dE))) 
        ODi_fit = ndarray((int((Estop_C-Emin)/dE) + int((395-EpeMin_C)/dE)))
        ODi_f2_fitC = ndarray((int((Estop_C-Emin)/dE) + int((395-EpeMin_C)/dE)))
        
        k=0
        for i in range (0, int((Estop_C-Emin)/dE)):
            Ei_fit[k] = Ei[i]
            ODi_fit[k] = ODi[i]
            ODi_f2_fitC[k] =  ODi_C_f2[i]
            k=k+1
        for i in range (int((EpeMin_C-Emin)/dE), int((395-Emin)/dE)):
            Ei_fit[k] = Ei[i]
            ODi_fit[k] = ODi[i]
            ODi_f2_fitC[k] =  ODi_C_f2[i]
            k=k+1

        param = np.array([B, Kc, amp1, index1])  
        errfunc = lambda param, x, y: ((param[0] + param[1]*ODi_f2_fitC + param[2] * (x**param[3])) - y)**2
        guess = param
        param, success = optimize.leastsq(errfunc, guess[:], args = (Ei_fit, ODi_fit))
        (B, Kc, Kn, Ko, amp1, index1, amp2, index2, amp3, index3) = (param[0], param[1], 0, 0, param[2], param[3], 0, 0, 0, 0) 
        
    # Plots the raw spectrum as well as the fitted F2 absorption cross section functions
    plt.legend([f])
    plt.xlabel('Energy')
    plt.ylabel('O.D.')
    plt.plot(Ei, ODi, Ei, B + Kc*ODi_C_f2 + Kn*ODi_N_f2 + Ko*ODi_O_f2 + amp1*(Ei**index1) + amp2*(Ei**index2) + amp3*(Ei**index3))
    plt.savefig('Normalized Spectra/'+f+'F2_fitted.pdf')
    plt.clf()

    return Kc, Kn, Ko
    
# Normalize the spectrum by the value of the integrated area
def normalize (Ei, ODi, Estop, Enorm):
    Enorm1 = Ei >= Estop				# Creates local variable corresponding to the spectrum energy range between Estop and Enorm
    Ei1 = Ei[Enorm1]
    Enorm2 = Ei1 <= Enorm				
    Eint = Ei1[Enorm2]
    ODint1 = ODi [Enorm1]
    ODint = ODint1 [Enorm2]
    A = simps (ODint, Eint)			    # Integraetd the spectrum to get the area over the specific energy range
    ODnorm = ODi/A                      # New spectrum, OD values are diveided by the initial area.
    return ODnorm, A

# Defines the gaussians and their sum with their positions and width fixed.
def gaussian (x, height, c, w):
    return np.absolute(height*np.exp(-(x - c)**2/(2*w**2)))

# Sum of all gaussians which will be fitted to the spectrum. While width and positions are defined, height will be the free parameter to fit.
def all_gaussians_C(x, w, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16 , h17, h18, h19, h20, h21,\
                  h22, h23, h24, h25, h26, h27, h28, h29, h30, h31, h32, h33, h34, h35):
    fit_C = (gaussian(x, h1, 284.1, w) + gaussian(x, h2, 284.4, w) + gaussian (x, h3, 284.7, w) + gaussian(x, h4, 285, w) \
             + gaussian(x, h5, 285.4, w) + gaussian(x, h6, 285.8, w) + gaussian(x, h7, 286.2, w) \
             + gaussian(x, h8, 286.5, w) + gaussian(x, h9, 286.8, w) + gaussian(x, h10, 287.2, w) \
             + gaussian(x, h11, 287.5, w) + + gaussian(x, h12, 287.8, w) + gaussian(x, h13, 288.2, w) + gaussian(x, h14, 288.5, w) \
             + gaussian(x, h15, 288.9, w) + gaussian(x, h16, 289.4, w) + gaussian(x, h17, 289.9, w) \
             + gaussian(x, h18, 290.3, w) + gaussian(x, h19, 290.8, w) + gaussian(x, h20, 291.2, w) \
             + gaussian(x, h21, 291.5, w) + gaussian(x, h22, 292.1, 1.3) + gaussian(x, h23, 292.7, 1.3) \
             + gaussian(x, h24, 293.3, 1.3) + gaussian(x, h25, 294, 1.3) + gaussian(x, h26, 295, 1.5) \
             + gaussian(x, h27, 297.1, 0.4) + gaussian(x, h28, 297.5, 2) + gaussian(x, h29, 299.7, 0.4)\
             + gaussian(x, h30, 300, 2) + gaussian(x, h31, 302.5, 2) + gaussian(x, h32, 305, 2) \
             + gaussian(x, 0, 307.5, 2) + gaussian(x, 0, 310, 2) + gaussian (x, 0, 312.5, 2))
    return fit_C    

def all_gaussians_N(x, w, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16 , h17, h18, h19, h20, h21, \
                  h22, h23, h24, h25, h26, h27, h28, h29, h30):
    fit_N = (gaussian (x, h1, 398.7, w_N) + gaussian (x, h2, 398.9, w_N) + gaussian(x, h3, 399.3, w_N) + gaussian(x, h4, 399.6, w_N) \
           + gaussian (x, h5, 400, w_N) + gaussian(x, h6, 400.6, w_N) + gaussian(x, h7, 401, w_N) + gaussian(x, h8, 401.1, w_N)\
           + gaussian(x, h9, 401.4, w_N) + gaussian(x, h10, 401.6, w_N) + gaussian(x, h11, 402, w_N) + gaussian(x, h12, 402.5, w_N)\
           + gaussian(x, h13, 403, w_N) + gaussian(x, h14, 403.4, w_N) + gaussian(x, h15, 403.8, w_N) \
           + gaussian(x, h16, 404.4, w_N) + gaussian(x, h17, 405, w_N)+ gaussian(x, h18, 405.4, w_N) + gaussian(x, h19, 406, w_N) \
           + gaussian(x, h20, 406.4, w_N)+ gaussian(x, h21, 406.7, w_N) + gaussian(x, h22, 407, 0.4)+ gaussian(x, h23, 407.3, 0.4)\
           + gaussian(x, h24, 407.6, 0.4)+ gaussian(x, h25, 408, 1) + gaussian(x, h26, 408.5, 1)  + gaussian(x, h27, 411, 1) \
           + gaussian(x, h28, 413.7, 1) + gaussian(x, h29, 416, 2) + gaussian(x, h30,  420, 2))
    return fit_N

# Calculate the residual between the fit and the spectrum using R2
def ErFit (Ei, ODnorm, w, optim, Enorm):
    k = 0
    er = Ei <= Enorm
    ER = Ei[er]
    if Enorm == Enorm_C :
        for i in ER:
            ER[k] = sqrt(np.absolute((all_gaussians_C(Ei[k], w, *optim))**2-((ODnorm[k])**2)))
            k = k+1
    if Enorm == Enorm_N :
        for i in ER:
            ER [k] = np.sqrt(np.absolute((all_gaussians_N(Ei[k], w, *optim))**2-((ODnorm[k])**2)))
            k = k+1
    Er = sum (ER)
    return Er

# Plot each Carbon or Nitrogen edge spectrum individually and save it
def fig_spectre (Ei, ODnorm, spectre):
    plt.plot(Ei, ODnorm)
    plt.legend([spectre[:len(spectre)-len('.txt')]])
    plt.xlabel('Energy')
    plt.ylabel('O.D.')
    if Enorm_C <= max(Ei) <= Emin_N:
        plt.savefig('Normalized Spectra/'+spectre[:len(spectre)-len('.txt')]+'_C.pdf')
    if max(Ei) >= Enorm_N:
        plt.savefig('Normalized Spectra/'+spectre[:len(spectre)-len('.txt')]+'_N.pdf')
    plt.clf()

#plot all fitted gaussians together with data and total fit
def plotgaussians_C (Eifit, optim, spectre, w):
    k = 0
    for i in tab_Func_Group_C [0:20]:
        plt.plot (Eifit, gaussian(Eifit, optim[k], tab_Func_Group_C [k], w))
        k = k+1
    plt.plot (Eifit, gaussian(Eifit, optim[21], 292.1, 1.3))
    plt.plot (Eifit, gaussian(Eifit, optim[22], 292.7, 1.3))
    plt.plot (Eifit, gaussian(Eifit, optim[23], 293.3, 1.3))
    plt.plot (Eifit, gaussian(Eifit, optim[24], 294, 1.3))
    plt.plot (Eifit, gaussian(Eifit, optim[25], 295, 1.5))
    plt.plot (Eifit, gaussian(Eifit, optim[26], 297.1, 0.4))
    plt.plot (Eifit, gaussian(Eifit, optim[27], 297.5, 2))
    plt.plot (Eifit, gaussian(Eifit, optim[28], 299.7, 0.4))
    plt.plot (Eifit, gaussian(Eifit, optim[29], 300, 2))
    plt.plot (Eifit, gaussian(Eifit, optim[30], 302.5, 2))
    plt.plot (Eifit, gaussian(Eifit, optim[31], 305, 2))
    plt.plot (Eifit, gaussian(Eifit, optim[32], 307.5, 2))
    plt.plot (Eifit, gaussian(Eifit, optim[33], 310,2))
    plt.plot (Eifit, gaussian(Eifit, optim[34], 312.5, 2))
    plt.plot(Eifit, all_gaussians_C(Eifit, w, *optim))
    plt.plot(Eifit, ODfit_C)
    plt.legend([spectre[:len(spectre)-len('.txt')]])
    plt.xlabel('Energy')
    plt.ylabel('O.D.')
    plt.savefig('Normalized Spectra/'+spectre[:len(spectre)-len('.txt')]+'_C_fitted.pdf')
    plt.clf()

#plot all individual fitted gaussians together with data and total fit
def plotgaussians_N (Eifit, optim, spectre, w):
    k=0
    for i in tab_Func_Group_N [0:20]:
        plt.plot (Eifit, gaussian(Eifit, optim[k], tab_Func_Group_N [k], w))
        k=k+1
    plt.plot (Eifit, gaussian(Eifit, optim[21], 407, 0.4))
    plt.plot (Eifit, gaussian(Eifit, optim[22], 407.3, 0.4))
    plt.plot (Eifit, gaussian(Eifit, optim[23], 407.6, 0.4))
    plt.plot (Eifit, gaussian(Eifit, optim[24], 408, 1))
    plt.plot (Eifit, gaussian(Eifit, optim[25], 408.5, 1))
    plt.plot (Eifit, gaussian(Eifit, optim[26], 411, 1))
    plt.plot (Eifit, gaussian(Eifit, optim[27], 413.7, 1))
    plt.plot (Eifit, gaussian(Eifit, optim[28], 416, 2))
    plt.plot (Eifit, gaussian(Eifit, optim[29], 420, 2))
    plt.plot(Eifit, all_gaussians_N (Eifit, w, *optim))
    plt.plot(Eifit, ODfit_N)
    plt.legend([spectre[:len(spectre)-len('.txt')]])
    plt.xlabel('Energy')
    plt.ylabel('O.D.')
    plt.savefig('Normalized Spectra/'+spectre[:len(spectre)-len('.txt')]+'_N_fitted.pdf')
    plt.clf()

######################################################################
######################################################################
### Apply all operation on the full list of files in the directory ###

# Defines all lists and variable used later to store the data
E_Cf2, OD_Cf2 = openf2 ('Carbonf2.f1f2')            # Opens the file of the F2 step function of the absorption cross section
E_Nf2, OD_Nf2 = openf2 ('Nitrogenf2.f1f2')          
E_Kf2, OD_Kf2 = openf2 ('Potassiumf2.f1f2')
E_Caf2, OD_Caf2 = openf2 ('Calciumf2.f1f2')
E_Of2, OD_Of2 = openf2('Oxygenf2.f1f2')

file_nb = len(os.listdir(repertoire))                       # Number of files in the source folder
size_C = ((Emax_C-Emin)/dE)+1                               # Size of the array for the energy axis       
size_N = ((Emax_N-Emin_N)/dE)+1
size_O = ((Emax_O-Emin_O)/dE)+1

tab_C = np.zeros ((int(file_nb), len(Func_Group_C)))        # Heights of the gaussian after fit for C 
tab_N = np.zeros ((int(file_nb), len(Func_Group_N)))        # Heights of the gaussian after fit for N
tab_C_f2 = np.zeros((int(file_nb), len(Func_Group_C)))      # Heights of the gaussian with F2 normalization after fit for C
tab_N_f2 = np.zeros((int(file_nb), len(Func_Group_N)))      # Heights of the gaussian with F2 normalization after fit for C

tab_norm_sp_C = np.zeros((int(file_nb),size_C))             # Opt. Densities after area normalization
tab_norm_sp_N = np.zeros((int(file_nb),size_N))
tab_norm_sp_O = np.zeros((int(file_nb),size_O))
tab_norm_sp_C_f2 = np.zeros((int(file_nb),size_C))          # Opt. Densities after F2 normalization
tab_norm_sp_N_f2 = np.zeros((int(file_nb),int(size_N)))

#tab_E = np.zeros((int(file_nb),((Emax_C-Emin)/dE)+1))
#tab_full_sp_C = np.zeros((int(file_nb),((Emax_C-Emin)/dE)+1))

tabA_C = np.zeros(int(file_nb), float)                      # Area normalization constants
tabA_N = np.zeros(int(file_nb), float)
tabA_O = np.zeros(int(file_nb), float)
tab_f2_N = np.zeros(int(file_nb), float)
tab_f2_C = np.zeros(int(file_nb), float)

tab_NC = np.zeros(int(file_nb), float)                      # Nitrogen to carbon ratio based on area normalization
tab_NC_f2 = np.zeros(int(file_nb), float)                   # Nitrogen to carbon ratio based on F2 normalization
tab_OC = np.zeros(int(file_nb), float)                      # Oxygen to carbon ratio based on area normalization
tab_OC_f2 = np.zeros(int(file_nb), float)                   # Oxygen to carbon ratio based on F2 normalization

tab_Erfit_C = np.zeros(int(file_nb), float)                 # Values of the fit error for the C edge (Area Norm)
tab_Erfit_N = np.zeros(int(file_nb), float)                 # Values of the fit error for the N edge (Area Norm)
tab_Erfit_C_f2 = np.zeros(int(file_nb), float)              # Values of the fit error for the C edge (F2 Norm)
tab_Erfit_N_f2 = np.zeros(int(file_nb), float)              # Values of the fit error for the N edge (F2 Norm)

tabQuant_group = np.zeros((int(file_nb), 4))                # Table containing the quantified values of the various functional groups
tabQuant_group_list = ('Aromatics-olefinics', 'Ketones-Phenols-Nitrile', 'Aliphatics', 'Carboxylics', '' , 'N/C_area', 'O/C_Area', 'N/C F2', 'O/C F2')

# Execute all the different operation on all spectra one after each other 
        # If the spectrum stop before the Nitrogen edge, then only the carbon edge is treated/fitted.
        # It is done first for a F2 Normalization, then for a integrated-area normalization
        # Quantification is performed only for area normalization
i=0
for f in os.listdir(repertoire):
    E, OD = openfile(f)
    a=0
    for p in range (0, len(E)):
        E[a] = E[a] + shift
        a = a+1
    ODb_C = powerlaw_Bgd (E, OD, Emin, Estop_C)
    Ei_C, ODi_C = discretize (E, ODb_C, Emin, Emax_C)
   
    ODnorm_C, A_C = normalize (Ei_C, ODi_C, Emin, Enorm_C)
    tabA_C[i] = A_C
    tab_norm_sp_C [i,:] = ODnorm_C
    
    Eifit_C = Ei_C[(Estop_C-Emin)/dE:(Efit_C-Emin)/dE]      # Defines the sub energy region over which the fit is performed
    ODfit_C = ODnorm_C[(Estop_C-Emin)/dE:(Efit_C-Emin)/dE]
    errfunc = lambda p, x, y: (all_gaussians_C (x, w_C, *p) - y)**2
    guess = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    optim_C, success = optimize.leastsq(errfunc, guess [:], args=(Eifit_C, ODfit_C))
    tab_C[i,:] = abs(optim_C)
    tab_Erfit_C[i] = ErFit (Eifit_C, ODfit_C, w_C, abs(optim_C), Enorm_C)    
    
    fig_spectre (Eifit_C, ODfit_C, f)
    plotgaussians_C (Eifit_C, optim_C, f, w_C)
    tabQuant_group[i, :] = (((optim_C [1] + optim_C [2] + optim_C [3] + optim_C [4]) / 4 * Aro_pente + Aro_ordo), ((optim_C [6] + optim_C [7] + optim_C [8]) / 3 * Keton_pente + Keton_ordo), ((optim_C[10] + optim_C[11]) / 2 * Ali_pente + Ali_ordo), ((optim_C[13]) * Carbo_pente - Carbo_ordo))
    
    # If the spectrum is acquired up to Estop_N (397.5 eV), the the F2 normalization is performed as well
    if max(E) >= 395:
        Kc1, Kn, Ko = normalize_f2 (OD, f)
        OD_Normf2_C = ODi_C/Kc1    
        tab_f2_C [i] = Kc1
        tab_norm_sp_C_f2[i,:] = OD_Normf2_C

        ODfit_C = OD_Normf2_C[(Estop_C-Emin)/dE:(Efit_C-Emin)/dE]
        errfunc = lambda p, x, y: (all_gaussians_C (x, w_C, *p) - y)**2
        guess = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        optim_C_f2, success = optimize.leastsq(errfunc, guess [:], args=(Eifit_C, ODfit_C))
        tab_C_f2[i,:] = abs(optim_C_f2)
        tab_Erfit_C_f2[i] = ErFit (Eifit_C, ODfit_C, w_C, abs(optim_C_f2), Enorm_C)
        
    f_C = open('Normalized Spectra/txt files/'+f[:len(f)-len('.txt')]+'_C.txt', 'w')
    l=0
    for j in Ei_C:
        f_C.write(str(np.around(Ei_C[l], decimals = 4))+'    ')
        f_C.write(str(np.around(ODnorm_C[l], decimals = 4))+'\n')
        l=l+1
    f_C.close()
        
    #if the spectrum is acquired at energies above Enorm_N (406.5 eV), then the Area-normalization and the deconvolution are performed
    if max(E) >= Enorm_N:
        ODb_N = powerlaw_Bgd (E, OD, Emin_N, Estop_N)
        Ei_N, ODi_N = discretize (E, ODb_N, Emin_N, Emax_N)
        
        ODnorm_N, A_N = normalize (Ei_N, ODi_N, Estop_N, Enorm_N)
        tab_norm_sp_N[i,:] = ODnorm_N
        tabA_N[i] = A_N
        tab_NC[i]=(A_N/A_C)*(3.672/3.81)
        
        Eifit_N = Ei_N[(Estop_N-Emin_N)/dE:(Efit_N-Emin_N)/dE]
        ODfit_N = ODnorm_N [(Estop_N-Emin_N)/dE:(Efit_N-Emin_N)/dE]
        errfunc = lambda p, x, y: (all_gaussians_N (x, w_N, *p) - y)**2
        guess = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        optim_N, success = optimize.leastsq(errfunc, guess [:], args=(Eifit_N, ODfit_N))
        tab_N[i,:] = abs(optim_N)
        tab_Erfit_N[i] = ErFit (Eifit_N, ODfit_N, w_N, abs(optim_N), Enorm_N)
    
        fig_spectre (Eifit_N, ODfit_N, f)
        plotgaussians_N (Eifit_N, optim_N, f, w_N)
        
        #If the spectrum is acquired above Emax_N (450 eV), F2-normalization and fit are performed
        if max(E) >= Emax_N:
            Kc2, Kn, Ko = normalize_f2 (OD, f) 
            OD_Normf2_N = ODi_N/Kn
            tab_norm_sp_N_f2 [i,:] = OD_Normf2_N
            tab_f2_N [i] = Kn
            tab_NC_f2 [i] = Kn/Kc2
            
            ODfit_N = OD_Normf2_N [(Estop_N-Emin_N)/dE:(Efit_N-Emin_N)/dE]
            errfunc = lambda p, x, y: (all_gaussians_N (x, w_N, *p) - y)**2
            guess = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            optim_N_f2, success = optimize.leastsq(errfunc, guess [:], args=(Eifit_N, ODfit_N))
            tab_N_f2[i,:] = abs(optim_N_f2)
            tab_Erfit_N_f2[i] = ErFit (Eifit_N, ODfit_N, w_N, abs(optim_N_f2), Enorm_N)
    
        f_N = open('Normalized Spectra/txt files/'+f[:len(f)-len('.txt')]+'_N.txt', 'w')
        l=0
        for j in Ei_N:
            f_N.write(str(np.around(Ei_N[l], decimals = 4))+'    ')
            f_N.write(str(np.around(ODnorm_N[l], decimals = 4))+'\n')
            l=l+1
        f_N.close()
    
    #If the spectrum goes beyond Enorm_O (546.5 eV) eV ,then the Oxygen edge is treated (O/C ratio, normalization and plot)
    if max(E) >= Enorm_O:
        ODb_O = powerlaw_Bgd (E, OD, Emin_O, Estop_O)
        Ei_O, ODi_O = discretize (E, ODb_O, Emin_O, Emax_O)
        ODnorm_O, A_O = normalize (Ei_O, ODi_O, Emin_O, Enorm_O)
        tab_norm_sp_O[i,:] = ODnorm_O 
        tabA_O[i] = A_O
        tab_OC[i]=(A_O/A_C)*(3.6/4.12)
        
        #If the spectrum is acquired above Emax_O (680 eV), F2-normalization and fit are performed
        if max(E) >= Emax_O:
            Kc3, Kn2, Ko = normalize_f2 (OD, f)
            OD_Normf2_O = ODi_O/Ko
#           tab_norm_sp_O_f2 [i,:] = OD_Normf2_O
#           tab_f2_O [i] = Ko
            tab_OC_f2 [i] = Ko/Kc3    
        
        f_O = open('Normalized Spectra/txt files/'+f[:len(f)-len('.txt')]+'_O.txt', 'w')
        l=0
        for j in Ei_O:
            f_O.write(str(np.around(Ei_O[l], decimals = 4)) + '    ')
            f_O.write(str(np.around(ODnorm_O[l], decimals = 4)) + '\n')
            l=l+1
        f_O.close()
    i=i+1
    
#Plot the last spectrum of the list and the fit
plt.plot(Eifit_C, all_gaussians_C (Eifit_C, w_C, *optim_C), lw=3, c='b', label='fit of all Gaussians')
plt.plot (Ei_C, ODnorm_C, lw = 1, c='r', label = 'data')

######################################################################################################
### Export in an excel file the fitted functional groups heights for C and N as well as normalized spectra data and plots
#Creates the Excel file and its different tabs
cell_nb = str (file_nb+2)
workbook = xlsxwriter.Workbook('Data/data.xlsx')
worksheet_param = workbook.add_worksheet(name = 'Analysis parameters')
worksheet_data = workbook.add_worksheet(name = 'Quantified data')
worksheet_spNorm_C = workbook.add_worksheet(name = 'C spectra Area_Norm')
worksheet_spNorm_N = workbook.add_worksheet(name = 'N spectra Area_Norm')
worksheet_spNorm_O = workbook.add_worksheet(name = 'O spectra Area_Norm')
worksheet_rawspectra = workbook.add_worksheet(name = 'Raw spectra')
worksheet_C = workbook.add_worksheet(name = 'C fits Area_Norm')
worksheet_N = workbook.add_worksheet(name = 'N fits Area_Norm')
worksheet_spNorm_C_f2 = workbook.add_worksheet(name = 'C spectra F2_Norm')
worksheet_spNorm_N_f2 = workbook.add_worksheet(name = 'N spectra F2_Norm')
worksheet_C_f2 = workbook.add_worksheet(name = 'C fit_param f2')
worksheet_N_f2 = workbook.add_worksheet(name = 'N fit_param f2')

# Fill the worksheet with the various parameters used to normalize, fit and deconvolve the spectra
worksheet_param.write('A1', 'Emin = '+str(Emin)+'               Lower energy of the range used for the raw spectrum(default = 270)')
worksheet_param.write('A2', 'Emax_C = '+str(Emax_C)+'           Higher end of the energy range used for the raw spectrum (default = 700)')
worksheet_param.write('A3', 'dE = '+str(dE)+'                   Energy step used for the discretization of the spectrum (default = 0.1)')
worksheet_param.write('A4', 'Estop_C = '+str(Estop_C)+'         Energy up to which the pre-edge background fitting is performed (default = 282)')
worksheet_param.write('A5', 'Enorm_C = '+str(Enorm_C)+'         Energy up to which the area normalization is calculated (default = 291.5)')
worksheet_param.write('A6', 'Efit_C = '+str(Efit_C)+'           Energy up to which the gaussian fitting is performed (default = 310)')
worksheet_param.write('A7', 'EpeMin_C = '+str(EpeMin_C)+'       Energy from which the fitting of the carbon step function is considered for fitting the post-edge (default = 355)')
worksheet_param.write('A8', 'w_C = '+str(w_C)+'                 Half Width at Half Maximum of the fitted gaussians (default = 0.2)')
worksheet_param.write('A10', 'Emin_N = '+str(Emin_N)+'          Energy at which the Nitrogen edge analysis begins(default = 370)')
worksheet_param.write('A11', 'Estop_N = '+str(Estop_N)+'        Energy up to which the pre-edge background fitting is performed (default = 397)')
worksheet_param.write('A12', 'Enorm_N = '+str(Enorm_N)+'        Energy up to which the area normalization is calculated (default = 406.5)')
worksheet_param.write('A13', 'EpeMin_N = '+str(EpeMin_N)+'      Energy from which the fitting of the Nitrogen step function is considered for fitting the post edge (default = 430)')
worksheet_param.write('A14', 'Emax_N = '+str(Emax_N)+'          Energy up to which the fitting of the post edge is performed (default = 449)')
worksheet_param.write('A15', 'w_N = '+str(w_N)+'                Half Width at Half Maximum used for the fitted gaussians (default = 0.3)')
worksheet_param.write('A17', 'Emin_O = '+str(Emin_O)+'          Energy at which the Oxygen edge analysis begins (default = 470)')
worksheet_param.write('A18', 'Estop_O = '+str(Estop_O)+'        Energy up to which the pre-edge background fitting is performed (default = 528)')
worksheet_param.write('A19', 'Enorm_O = '+str(Enorm_O)+'        Energy up to which the area normalization is calculated (default = 540)')
worksheet_param.write('A20', 'EpeMin_O = '+str(EpeMin_O)+'      Energy from which the fitting of the Oxygen step function is considered for fitting the post edge (default = 600)')
worksheet_param.write('A21', 'Emax_O = '+str(Emax_O)+'          Energy up to which the fitting of the Oxygen step function is considered for fitting the post edge (default = 680)')
worksheet_param.write('A23', 'shift = '+str(shift)+'            If energy axis needs calibration, the spectra can be directly shifted here. (default = 0)')

# Fill the worksheet of the quantified data summary
worksheet_data.write_column ('A3:', liste_fichier)
worksheet_data.write_row ('B1:', tabQuant_group_list)
worksheet_data.add_table('B2:E2'+ cell_nb, {'data': tabQuant_group})
worksheet_data.write_column ('G3:', tab_NC)
worksheet_data.write_column ('H3:', tab_OC)
worksheet_data.write_column ('I3:', tab_NC_f2)
worksheet_data.write_column ('J3:', tab_OC_f2)

    #Plot the quantified data in 3 was : aromatics vs. ketones, aromatics vs. aliphatics and a ternary diagram with aromatics/ketones and aliphatics
chart_data1 = workbook.add_chart({'type': 'scatter'})
chart_data1.add_series({
    'categories': ['Quantified data', 2, 1, len(liste_fichier)+1, 1],
    'values': ['Quantified data', 2, 2, len(liste_fichier)+1, 2], 
    'x_error_bars': {'type': 'fixed', 'value': Aro_s1}, 
    'y_error_bars': {'type': 'fixed', 'value': Keton_s1}})
chart_data1.set_x_axis({
    'name': '(Aromatic + Olefinic)_C / Total C (at.)',
    'name_font': {'size': 12, 'bold': False},
    'line': {'color': 'black', 'width': 0.75}})
chart_data1.set_y_axis({
    'name': '(Ketone + Phenol + Nitrile)_C / Total C (at.)',
    'name_font': {'size': 12, 'bold': False},
    'line': {'color': 'black','width': 0.75},
    'major_gridlines': {'visible': False}})
chart_data1.set_size({'width': 400, 'height': 320})
chart_data1.set_title({'none': True})
chart_data1.set_legend({'none': True})
worksheet_data.insert_chart('B11', chart_data1)

        #second plot
chart_data2 = workbook.add_chart({'type': 'scatter'})
chart_data2.add_series({
    'categories': ['Quantified data', 2, 1, len(liste_fichier)+1, 1],
    'values': ['Quantified data', 2, 3, len(liste_fichier)+1, 3], 
    'x_error_bars': {'type': 'fixed', 'value': Aro_s1},
    'y_error_bars': {'type': 'fixed', 'value': Ali_s1}})
chart_data2.set_x_axis({
    'name': '(Aromatic + Olefinic)_C / Total C (at.)',
    'name_font': {'size': 12, 'bold': False},
    'line': {'color': 'black', 'width': 0.75}})
chart_data2.set_y_axis({
    'name': 'Aliphatic_C / Total C (at.)',
    'name_font': {'size': 12, 'bold': False},
    'line': { 'color': 'black', 'width': 0.75},
    'major_gridlines': {'visible': False}})
chart_data2.set_size({'width': 400, 'height': 320})
chart_data2.set_title({'none': True})
chart_data2.set_legend({'none': True})
worksheet_data.insert_chart('J11', chart_data2)

        #Third plot: a ternary diagram using the quantified data
worksheet_data.write_column (1,11, ['Triangle x coord.', -0.5, -0.45, -0.4, -0.35, -0.3, -0.25, -0.2, -0.15, -0.1, -0.05, 0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50])
worksheet_data.write_column (1, 12, ['Triangle y coord.', 0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00, 0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10, 0.00])
Y_ternary = tabQuant_group[:, 0]/(tabQuant_group[:, 1] + tabQuant_group[:, 2] + tabQuant_group[:, 0])
X_ternary = -0.5*(1-Y_ternary) + tabQuant_group[:, 2]/(tabQuant_group[:, 1] + tabQuant_group[:, 2] + tabQuant_group[:, 0])
worksheet_data.write_column (2, 13, X_ternary)
worksheet_data.write_column (2, 14, Y_ternary)

chart_data3 = workbook.add_chart({'type': 'scatter', 'subtype' : 'straight_with_markers'})
chart_data3.add_series({
    'categories': ['Quantified data', 2, 11, 23, 11],
    'values':     ['Quantified data', 2, 12, 23, 12],
    'marker':     {'type': 'short_dash', 'size': 5, 'border': {'color': 'black'}, 'fill':   {'color': 'black'}},
    'line':       {'width' : 0.75, 'color': 'black'}})
chart_data3.add_series({
    'categories': ['Quantified data', 2, 13, len(liste_fichier)+1, 13],
    'values':     ['Quantified data', 2, 14, len(liste_fichier)+1, 14],
    'line':       {'none' : True},
    'x_error_bars': {'type': 'fixed', 'value': Ali_s1/100},
    'y_error_bars': {'type': 'fixed', 'value': Aro_s1/100}})
chart_data3.set_x_axis({
    'name': 'Ketones-Aliphatics',
    'name_font': {'size': 12, 'bold': False},
    'line': {'color': 'black', 'width': 0.75},
    'min' : -0.5, 
    'max' : 0.5,
    'major_gridlines': {'visible': False}})
chart_data3.set_y_axis({
    'max' : 1,
    'major_gridlines': {'visible': False},
    'visible': False})
chart_data3.set_title({
   'name': 'Aromatics',
   'name_font':  {'size': 12, 'bold': False}})
chart_data3.set_legend({'none': True})
chart_data3.set_size({'width': 500, 'height': 485})
worksheet_data.insert_chart('R4', chart_data3)

#Fills the worksheet containing the Carbon edge spectra normalized to their Area
norm_sp_C = tab_norm_sp_C.T
worksheet_spNorm_C.write_row (0,1, liste_fichier)
worksheet_spNorm_C.write_column (2,0, Ei_C)
worksheet_spNorm_C.add_table(1,1, len(Ei_C)+1, file_nb+1, {'data': norm_sp_C})
    #Plots the spectra of all files
chart_C = workbook.add_chart({'type': 'scatter', 'subtype' : 'smooth'})
i=0
for f in os.listdir(repertoire):
    chart_C.add_series({
        'categories': ['C spectra Area_Norm', 2, 0, int(((Emax_C-Emin)/dE)+2), 0],
        'values': ['C spectra Area_Norm', 2, i+1, int(((Emax_C-Emin)/dE)+2), i+1],
        'name':     liste_fichier[i], 
        'line':       {'width': 1.25}})
    i = i+1
chart_C.set_x_axis({
    'name': 'Energy (eV)',
    'name_font': {'size': 14, 'bold': True},
    'min': 282, 
    'max': 295,
    'major_unit': 1,
    'line': {'color': 'black', 'width': 1.25},
    'major_gridlines': {'visible': True, 'line': {'width': 0.5, 'dash_type': 'dash'}}})
chart_C.set_y_axis({
    'name': 'Normalized absorption (a.u)',
    'name_font': {'size': 14, 'bold': True},
    'min': 0,
    'major_gridlines': {'visible': False},
    'visible': False})
chart_C.set_title({'none': True})
chart_C.set_size({'width': 1000, 'height': 550})
worksheet_spNorm_C.insert_chart('D3', chart_C)

#Fills the worksheet containing the Nitrogen edge spectra normalized to their Area
norm_sp_N = tab_norm_sp_N.T
worksheet_spNorm_N.write_row (0,1, liste_fichier)
Ei_N = Ei_C[(Emin_N-Emin)/dE:(Emax_N-Emin)/dE]
k=0
for i in range (0, int((Emax_N-Emin_N)/dE)):
    Ei_N[k] = Emin_N + dE*k
    k=k+1
worksheet_spNorm_N.write_column (2,0, Ei_N)
worksheet_spNorm_N.add_table(1,1, len(Ei_N)+1, file_nb+1, {'data': norm_sp_N})
        
    #Plots the spectra of all files
chart_N = workbook.add_chart({'type': 'scatter', 'subtype' : 'smooth'})
i=0
for f in os.listdir(repertoire):
    chart_N.add_series({
        'categories': ['N spectra Area_Norm', 2, 0, int(((Emax_N-Emin_N)/dE)+2), 0],
        'values': ['N spectra Area_Norm', 2, i+1, int(((Emax_N-Emin_N)/dE)+2), i+1],
        'name':     liste_fichier[i], 
        'line':       {'width': 1.25}})
    i = i+1
chart_N.set_x_axis({
    'name': 'Energy (eV)',
    'name_font': {'size': 14, 'bold': True},
    'min': 395, 
    'max': 420,
    'major_unit': 1,
    'line': {'color': 'black', 'width': 1.25},
    'major_gridlines': {'visible': True, 'line': {'width': 0.5, 'dash_type': 'dash'}}})
chart_N.set_y_axis({
    'name': 'Normalized absorption (a.u)',
    'name_font': {'size': 14, 'bold': True},
    'min': 0,
    'major_gridlines': {'visible': False},
    'visible': False})
chart_N.set_title({'none': True})
chart_N.set_size({'width': 1000, 'height': 550})
worksheet_spNorm_N.insert_chart('D3', chart_N)

#Fills the worksheet containing the Oxygen edge spectra normalized to their Area
norm_sp_O = tab_norm_sp_O.T
worksheet_spNorm_O.write_row (0,1, liste_fichier)
Ei_O = Ei_C[(Emin_O-Emin)/dE:(Emax_O-Emin)/dE]
k=0
for i in range (0, int((Emax_O-Emin_O)/dE)):
    Ei_O[k] = Emin_O + dE*k
    k=k+1
worksheet_spNorm_O.write_column (2,0, Ei_O)
worksheet_spNorm_O.add_table(1,1, len(Ei_O)+1, file_nb+1, {'data': norm_sp_O})

    #Plots the spectra of all files
chart_O = workbook.add_chart({'type': 'scatter', 'subtype' : 'smooth'})
i=0
for f in os.listdir(repertoire):
    chart_O.add_series({
        'categories': ['O spectra Area_Norm', 2, 0, int(((Emax_O-Emin_O)/dE)+2), 0],
        'values': ['O spectra Area_Norm', 2, i+1, int(((Emax_O-Emin_O)/dE)+2), i+1],
        'name':     liste_fichier[i], 
        'line':       {'width': 1.25}})
    i = i+1
chart_O.set_x_axis({
    'name': 'Energy (eV)',
    'name_font': {'size': 14, 'bold': True},
    'min': 525, 
    'max': 555,
    'major_unit': 1,
    'line': {'color': 'black', 'width': 1.25},
    'major_gridlines': {'visible': True, 'line': {'width': 0.5, 'dash_type': 'dash'}}})
chart_O.set_y_axis({
    'name': 'Normalized absorption (a.u)',
    'name_font': {'size': 14, 'bold': True},
    'min': 0,
    'major_gridlines': {'visible': False},
    'visible' : False})
chart_O.set_title({'none': True})
chart_O.set_size({'width': 1000, 'height': 550})
worksheet_spNorm_O.insert_chart('D3', chart_O)

#Fills the worksheet containing all raw spectra
chart_rawspectra = workbook.add_chart({'type': 'scatter', 'subtype' : 'smooth'})

i=0
for f in os.listdir(repertoire):
    E, OD = openfile(f)
    worksheet_rawspectra.write_row (0, 2*i, [liste_fichier[i]])
    worksheet_rawspectra.write_column (1, 2*i, E)
    worksheet_rawspectra.write_column (1, 2*i+1, OD)
    chart_rawspectra.add_series({
        'categories':   ['Raw spectra', 1, 2*i, len(E)+1, 2*i],
        'values':       ['Raw spectra', 1, 2*i+1, len(OD)+1, 2*i+1],
        'name':         liste_fichier[i], 
        'line':       {'width': 1.25}})  
    i=i+1
chart_rawspectra.set_x_axis({
    'name':             'Energy (eV)',
    'name_font':        {'size': 14, 'bold': True},
    'min':              250,
    'line':             {'color': 'black', 'width': 1.25},
    'major_gridlines':  {'visible': False}})
chart_rawspectra.set_y_axis({
    'name':             'X-Ray absorption',
    'name_font':        {'size': 14, 'bold': True},
    'min':              0,
    'major_gridlines':  {'visible': False},
    'line':             {'color': 'black', 'width': 1.25}})
chart_rawspectra.set_title({'none': True})
chart_rawspectra.set_size({'width': 1000, 'height': 550})
worksheet_rawspectra.insert_chart('D3', chart_rawspectra)    
    
#Fills the worksheet containing the fitted parameters of the Carbone K-edge normalized to the area
worksheet_C.write_column ('A3:', liste_fichier)
worksheet_C.write_row ('B1:', List_Func_Group_C)
worksheet_C.add_table('B2:AJ'+ cell_nb, {'data': tab_C})
worksheet_C.write_column ('AK3:', tabA_C)
worksheet_C.write_column ('AL3:', tab_Erfit_C)

#Fills the worksheet containing the fitted parameters of the Nitrogen K-edge normalized to the area
worksheet_N.write_column ('A3:', liste_fichier)
worksheet_N.write_row ('B1:', List_Func_Group_N)
worksheet_N.add_table('B2:AE'+ cell_nb, {'data': tab_N})
worksheet_N.write_column ('AF3:', tabA_N)
worksheet_N.write_column ('AG3:', tab_Erfit_N)

#Fills the worksheet with all spectra at the C edge normalized using the F2 functions
norm_sp_C_f2 = tab_norm_sp_C_f2.T
worksheet_spNorm_C_f2.write_row (0,1, liste_fichier)
worksheet_spNorm_C_f2.write_column (2,0, Ei_C)
worksheet_spNorm_C_f2.add_table(1,1, len(Ei_C)+1, file_nb+1, {'data': norm_sp_C_f2})

#Creates a table with all spectra at the N edge over the specific energy range
norm_sp_N_f2 = tab_norm_sp_N_f2.T
worksheet_spNorm_N_f2.write_row (0,1, liste_fichier)
worksheet_spNorm_N_f2.write_column (2,0, Ei_N)
worksheet_spNorm_N_f2.add_table(1,1, len(Ei_N)+1, file_nb+1, {'data': norm_sp_N_f2})

#Fills the worksheet containing the fitted parameters of the Carbone K-edge normalized using the F2 functions
worksheet_C_f2.write_column ('A3:', liste_fichier)
worksheet_C_f2.write_row ('B1:', List_Func_Group_C)
worksheet_C_f2.add_table('B2:AJ'+ cell_nb, {'data': tab_C_f2})
worksheet_C_f2.write_column ('AK3:', tab_f2_C)
worksheet_C_f2.write_column ('AL3:', tab_Erfit_C_f2)

#Fills the worksheet containing the fitted parameters of the Nitrogen K-edge normalized using the F2 functions
worksheet_N_f2.write_column ('A3:', liste_fichier)
worksheet_N_f2.write_row ('B1:', List_Func_Group_N)
worksheet_N_f2.add_table('B2:AE'+ cell_nb, {'data': tab_N_f2})
worksheet_N_f2.write_column ('AF3:', tab_f2_N)
worksheet_N_f2.write_column ('AG3:', tab_Erfit_N_f2)

workbook.close()

  
"""
  # Perform linear background correction
def linBackground (E, OD, Emin, Estop):
    Estop1 = E >= Emin				    #Cherche toutes les valeurs de E < Estop en mode bouléen (renvoie du vrai ou faux)
    Es1 = E[Estop1]
    Estop2 = Es1 <= Estop
    Es2 = Es1[Estop2]						#Renvoie les valeurs de E inférieure à Estop
    ODs1 = OD[Estop1]
    ODs2 = ODs1[Estop2]
    slope, intercept, r_value, p_value, std_err = stats.linregress(Es2, ODs2)		#Effectue la régréssion linéaire sur Es, ODs
    a = slope
    b = intercept
    ODlb = OD-(a*E+b)					#Calcule le nouveau spectre avec régression lineaire
    return ODlb
    
    # perform linear regression for the post edge determination (Athena Style)
def postedge (Ei, ODi, EpeMin, EpeMax, Emin, Ec):
    ODPE = ODi [int((EpeMin-Emin)/dE):int((EpeMax+1-Emin)/dE)]
    Eipe = Ei[int((EpeMin-Emin)/dE):int((EpeMax+1-Emin)/dE)]
    slope, intercept, r_value, p_value, std_err = stats.linregress(Eipe, ODPE)		#Effectue la régréssion linéaire sur Es, ODs
    ape  = slope
    bpe = intercept
    c = ape*Ec + bpe
    ODAth = ODi/c
    return c, ODAth
    
def normalize_f2_OneByOne(OD):
    Ei, ODi = discretize (E, OD, Emin, max(E))
    Ei_O_f2, ODi_O_f2 = discretize (E_Of2, OD_Of2, Emin, max(E))
    Ei_C_f2, ODi_C_f2 = discretize (E_Cf2, OD_Cf2, Emin, max(E))
    #Ei_K_f2, ODi_K_f2 = discretize (E_Nf2, OD_Nf2, Emin, max(E))
    #Ei_Ca_f2, ODi_Ca_f2 = discretize (E_Nf2, OD_Nf2, Emin, max(E))
    Ei_N_f2, ODi_N_f2 = discretize (E_Nf2, OD_Nf2, Emin, max(E))
    
    Kc = 0
    Kn = 0
    Ko = 0
    
    Ei_fit = ndarray((int((Estop_C-Emin)/dE) + int((Estop_N-EpeMin_C)/dE))) 
    ODi_fit = ndarray((int((Estop_C-Emin)/dE) + int((Estop_N-EpeMin_C)/dE)))
    ODi_f2_fitC = ndarray((int((Estop_C-Emin)/dE) + int((Estop_N-EpeMin_C)/dE)))
    
    k=0
    for i in range (0, int((Estop_C-Emin)/dE)):
        Ei_fit[k] = Ei[i]
        ODi_fit[k] = ODi[i]
        ODi_f2_fitC[k] =  ODi_C_f2[i]
        k=k+1
    for i in range (int((EpeMin_C-Emin)/dE), int((Estop_N-Emin)/dE)):
        Ei_fit[k] = Ei[i]
        ODi_fit[k] = ODi[i]
        ODi_f2_fitC[k] =  ODi_C_f2[i]
        k=k+1

    B = 0
    Kc = 0.0
    amp = 1
    index = 1
    param = np.array([B, Kc, amp, index])  
    errfunc = lambda param, x, y: ((param[0] + param[1]*ODi_f2_fitC + param[2] * (x**param[3])) - y)**2
    guess = param
    param, success = optimize.leastsq(errfunc, guess[:], args = (Ei_fit, ODi_fit))
    Kc = param[1]
    
    if max(E) > 400:        
        Ei_fit = ndarray(int((Estop_N-EpeMin_C)/dE) + int((450-EpeMin_N)/dE)) 
        ODi_fit = ndarray(int((Estop_N-EpeMin_C)/dE) + int((450-EpeMin_N)/dE))
        ODi_f2_fitN = ndarray(int((Estop_N-EpeMin_C)/dE) + int((450-EpeMin_N)/dE))
        
        k=0
        for i in range (int((EpeMin_C-Emin)/dE), int((Estop_N-Emin)/dE)):
            Ei_fit[k] = Ei[i]
            ODi_fit[k] = ODi[i]
            ODi_f2_fitN[k] = ODi_N_f2[i]
            k=k+1
        for i in range (int((EpeMin_N-Emin)/dE), int((450-Emin)/dE)):
            Ei_fit[k] = Ei[i]
            ODi_fit[k] = ODi[i]
            ODi_f2_fitN[k] = ODi_N_f2[i]
            k=k+1
        
        B = 0
        Kn = 0.00
        amp = 1
        index = 1
        param = np.array([B, Kn, amp, index])  
        errfunc = lambda param, x, y: ((param[0] + param[1]*ODi_f2_fitN + param[2]*(x**param[3])) - y)**2
        guess = param
        param, success = optimize.leastsq(errfunc, guess[:], args = (Ei_fit, ODi_fit))
        Kn = param[1]

    if max(E) > 500:
        Ei_fit = ndarray((int((Estop_O-460)/dE) + int((Emax_O-EpeMin_O)/dE)), float)
        ODi_fit = ndarray((int((Estop_O-460)/dE) + int((Emax_O-EpeMin_O)/dE)), float)			#Défini les dimensions et la classe de variable du tableau
        ODi_f2_fitO = ndarray((int((Estop_O-460)/dE) + int((Emax_O-EpeMin_O)/dE)), float)			#Défini les dimensions et la classe de variable du tableau

        k=0
        for i in range (int((460-Emin)/dE), int((Estop_O-Emin)/dE)):
            Ei_fit[k] = Ei[i]
            ODi_fit[k] = ODi[i]
            ODi_f2_fitO[k] = ODi_O_f2[i]
            k=k+1
        for i in range (int((EpeMin_O-Emin)/dE), int((Emax_O-Emin)/dE)):
            Ei_fit[k] = Ei[i]
            ODi_fit[k] = ODi[i]
            ODi_f2_fitO[k] = ODi_O_f2[i]
            k=k+1
        
        B = 0
        Ko = 0.0
        amp = 1
        index = 1
            
        param = np.array([B, Ko, amp, index])  
        errfunc = lambda param, x, y: ((param[0] + param[1]*ODi_f2_fitO + param[2]*(x**param[3])) - y)**2
        guess = param
        param, success = optimize.leastsq(errfunc, guess[:], args = (Ei_fit, ODi_fit))

        Ko = param[1]
    return Kc, Kn, Ko    
    
# Calculate the area of the spectra over an energy range
def FG_SurfCal(borneInf, borneSup, Ei, ODnorm):   #Fonction de calcul de surface
    E_1 = Ei >= borneInf				                #Cherche toutes les valeurs de Ei>EQuiInf en mode bouléen (renvoie du vrai ou faux)
    E1 = Ei[E_1]
    OD1 = ODnorm[E_1]
    E_2 = Ei >= borneSup
    E2 = Ei[E_2]
    OD2 = ODnorm[E_2]
    Surf = simps (OD1, E1)- simps (OD2, E2)
    return Surf
    
    #Plot and save all normalized spectra within the same plot
for f in os.listdir(repertoire) :
    E, OD = openfile(f)
    ODlb = powerlaw_Bgd (E, OD, Emin, Estop_C)
    Ei, ODi = discretize (E, ODlb, Emin, Emax)
#    Kc = normalize_f2_C (OD, Emax_C)
#    OD_Normf2_C = ODi_C/Kc
    ODnorm, A = normalize (Ei, ODi, Estop_C, Enorm_C)
    plt.plot(Ei, ODnorm)
    plt.legend(['All_spectra_Normalized'])
    plt.xlabel('Energy') 
    plt.ylabel('O.D.')
    plt.savefig('Data/All_Spectra_Normalized.pdf')
plt.clf()
    
"""