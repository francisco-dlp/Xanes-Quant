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
conda install quantorxs
```

![Alt text](/Images/Anaconda_prompt.jpg "where to find anaconda prompt")

![Alt text](/Images/Install_command_line.jpg "The install command line")

* Quantorxs is automatically installed in the anaconda environment, and you can look for the executable file “quantorxs_gui” in the start menu and launch it…(and create a shortcut for later?)

![Alt text](/Images/Start_quantorxs.jpg "where to find quantorxs")


# Running the program:
## Sequence of operation performed by the program

Basically, it opens, normalize, fit, quantifies and export the results for each spectrum.
The user interface is designed to be as simple as possible. In order to keep the quantification reproducible, there is no possibility to play with the fitting parameters. 
However, users willing to modify the code can find it here: https://github.com/CorentinLG/Xanes-Quant

![Alt text](/Images/Program_sequence.jpg "Sequence of operations performed by the program")

## How to use the graphical interface

The program is designed to process several spectra at once. All source spectra should be assembled in one folder.
QUANTORXS reads only the format produced by aXis200: http://unicorn.mcmaster.ca/aXis2000.html

* Click on “choose data directory”. It is the folder containing the source spectra.
* Type in an output folder name (default is “QUANTORXS result” and it is created in the folder from which the data are taken)
* Uncheck the "demo" box. If checked, it uses default files as input to produce an example of the output files. 
* Select the format of the figure output (default: *.svg)
* There is an "offset" box to allow offsetting all spectra at once (if monochromator was not perfectly calibrated, it happens...)
* click on “Run” and wait (should take a few secondes per spectrum)

![Alt text](/Images/Quantorxs_gui.jpg "The graphical user interface")

## Description of the output files

The output folder will be created in the folder from which the data have been taken.
An .xls result file and two different sub-folders are created:

### a .xls file contains several sheets:
* The fitting parameters 
* The quantified data (aromatic, ketones, aliphatics, carboxylics; as well as N/C and O/C ratios) and some related plots
* The spectra at the C-K edge normalized by the area ratio method
* The spectra at the N-K edge normalized by the area ratio method
* The spectra at the O-K edge normalized by the area ratio method
* The fitted heights of the Gaussians for the area-based normalization at the C-K edge
* The fitted heights of the Gaussians for the area-based normalization at the N-K edge
* The fitted heights of the Gaussians for the area-based normalization at the O-K edge

![Alt text](/Images/excel_Tab1.jpg "Analysis parameters")

![Alt text](/Images/excel_Tab2.jpg "Quantified data")

![Alt text](/Images/excel_Tab3.jpg "normalized spectra")

![Alt text](/Images/excel_Tab4.jpg "fitted gaussians")

### A folder containing the .txt files of each normalized spectrum

### A folder with figures displaying:

* The cross-section fit
* The normalized spectra
* The deconvolution (all gaussians included)
 
