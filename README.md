# QUANTORXS : QUANTification of ORganics by X-ray Spectrosocopy

This program analyze Carbon and Nitrogen K-edge spectra (and Oxygen) and retrieves the functional group concentrations and the elemental ratio (N/C, O/C).
It automatically performs background subtraction, normalization to the total carbon content and spectra deconvolution. It uses the empirical calibrations for the quantification as described in the article. 
Figures are automatically plotted for direct data visualization and data output are gathered in an excel file.

The user interface is designed to be as simple as possible. In order to keep the quantification reproducible, there is no possibility to play with the fitting parameters. 
However, users willing to modify the code can find it here: https://github.com/CorentinLG/Xanes-Quant


# How to install and run QUANTORXS.

## Installation sequence: 
* Install python (for instance using the anaconda distribution: https://anaconda.org/anaconda/python.
* Go to pipy.org/QUANTORXS and download the setup file
* Execute the setup
* Look for the executable file “Quantorxs_gui” and launch it…

## Run the program:

The program is designed to process several spectra at once. All source spectra should be assembled in one folder.
QUANTORXS reads only the format produced by aXis200: http://unicorn.mcmaster.ca/aXis2000.html

* Click on “choose data directory”. It is the folder containing the source spectra.
* Type in an output folder name (default is “QuantORXS result” and appears in the folder from which the data are taken)
* Select the format of the figure output (default: *.svg)
* There is an "offset" box to allow offsetting all spectra at once (if monochromator was not perfectly calibrated, it happens...)
* click on “Run” and wait (not long)

# Description of the output files

The output folder will be created in the folder from which the data have been taken.
An .xls result file and two different sub-folders are created:

## a .xls file contains several sheets:
* The fitting parameters 
* The quantified data (aromatic, ketones, aliphatics, carboxylics) and some related plots
* The spectra at the C-K edge normalized by the area ratio method
* The spectra at the N-K edge normalized by the area ratio method
* The spectra at the O-K edge normalized by the area ratio method
* The fitted heights of the Gaussians for the area-based normalization at the C-K edge
* The fitted heights of the Gaussians for the area-based normalization at the N-K edge
* The fitted heights of the Gaussians for the area-based normalization at the O-K edge


## A folder containing the .txt files of each normalized spectrum

## A folder with figures displaying:

* The cross-section fit
* The normalized spectra
* The deconvolution (all gaussians included)
 
![Alt text] (C:\Users\Corentin\Documents\Github\Xanes-Quant.Program_sequence.jpeg "Sequence of operations performed by the program")