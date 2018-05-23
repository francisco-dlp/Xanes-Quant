# QUANTORXS : QUANTification of ORganics by X-ray Spectrosocopy

This program analyze Carbon and Nitrogen K-edge spectra (and Oxygen) and retrieves the functional group concentrations and the elemental ratio (N/C, O/C).

A published article describes the methods which are based on a empirical calibrations.
It automatically performs background subtraction, normalization to the total carbon content and spectra deconvolution. 
Figures are automatically plotted for direct data visualization and data output are gathered in an excel file.

## Installing QUANTORXS.

* Inexperienced python users should first install the latest Anaconda distribution (a suite of python packages and an environment to install further options: https://anaconda.org/anaconda/python. 
Download the appropriate setup file (windows, Mac, linux) and execute it...

* From the start menu, open "anaconda prompt" and type (the directory does not matter):

```bash
conda install quantorxs -c
```

![Alt text] (https://github.com/CorentinLG/Xanes-Quant/Images/Anaconda_prompt.jpeg "where to find anaconda prompt")
![Alt text] (https://github.com/CorentinLG/Xanes-Quant/Images/Install_command_line.jpeg "The install command line")

* Quantorxs is automatically installed in the anaconda environment, and you can look for the executable file “Quantorxs_gui” in the start menu and launch it…(and create a shortcut for later?)

![Alt text] (https://github.com/CorentinLG/Xanes-Quant/Images/Start_quantorxs.jpeg "where to find quantorxs")


# Running the program:
## Sequence of operation performed by the program

Basically, it opens, normalize, fit, quantifies and export the results for each spectrum.
The user interface is designed to be as simple as possible. In order to keep the quantification reproducible, there is no possibility to play with the fitting parameters. 
However, users willing to modify the code can find it here: https://github.com/CorentinLG/Xanes-Quant

![Alt text] (https://github.com/CorentinLG/Xanes-Quant/Images/Program_sequence.jpeg "Sequence of operations performed by the program")

## How to use the graphical interface

The program is designed to process several spectra at once. All source spectra should be assembled in one folder.
QUANTORXS reads only the format produced by aXis200: http://unicorn.mcmaster.ca/aXis2000.html

* Click on “choose data directory”. It is the folder containing the source spectra.
* Type in an output folder name (default is “QuantORXS result” and appears in the folder from which the data are taken)
* Select the format of the figure output (default: *.svg)
* There is an "offset" box to allow offsetting all spectra at once (if monochromator was not perfectly calibrated, it happens...)
* click on “Run” and wait (should take a few secondes per spectrum)

![Alt text] (https://github.com/CorentinLG/Xanes-Quant/Images/Quantorxs_gui.jpeg "The graphical user interface")

## Description of the output files

The output folder will be created in the folder from which the data have been taken.
An .xls result file and two different sub-folders are created:

### a .xls file contains several sheets:
* The fitting parameters 
* The quantified data (aromatic, ketones, aliphatics, carboxylics) and some related plots
* The spectra at the C-K edge normalized by the area ratio method
* The spectra at the N-K edge normalized by the area ratio method
* The spectra at the O-K edge normalized by the area ratio method
* The fitted heights of the Gaussians for the area-based normalization at the C-K edge
* The fitted heights of the Gaussians for the area-based normalization at the N-K edge
* The fitted heights of the Gaussians for the area-based normalization at the O-K edge

![Alt text] (https://github.com/CorentinLG/Xanes-Quant/Images/excel_Tab1.jpeg "Analysis parameters")
![Alt text] (https://github.com/CorentinLG/Xanes-Quant/Images/excel_Tab2.jpeg "Quantified data")
![Alt text] (https://github.com/CorentinLG/Xanes-Quant/Images/excel_Tab3.jpeg "normalized spectra")
![Alt text] (https://github.com/CorentinLG/Xanes-Quant/Images/excel_Tab4.jpeg "fitted gaussians")


### A folder containing the .txt files of each normalized spectrum

### A folder with figures displaying:

* The cross-section fit
* The normalized spectra
* The deconvolution (all gaussians included)
 
