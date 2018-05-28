# QUANTORXS : QUANTification of ORganics by X-ray Spectrosocopy

QUANTORXS is an opensource program to automatically analyze X-ray spectroscopy spectra of Carbon, Nitrogen and Oxygen K-edges edges to quantify the concentration of functional groups and the elemental ratios N/C and O/C using a novel quantification method that will soon be pusblished in a peer-reviewed scientific article.

QUANTORXS performs the following tasks automatically:

* Load the data from the file(s)
* Remove background
* Normalize the spectral
* Generate a model of the fine structure a fit it to the experimental data
* Calculate the functional groups abundances and elemental rations from the results of the fit
* Generate an Excel file and multiple figures with the results and normalised spectra files.

This is illustrated in model detail in the following diagram.

![Alt text](/Images/Program_sequence.jpg "Sequence of operations performed by the program")

QUANTORXS is designed to work without any user input other than the experimental spectra. However, users willing to modify the details of the model can download the code [GitHub](https://github.com/CorentinLG/Xanes-Quant)

The code was initially written by [Corentin Le Guillou](http://umet.univ-lille1.fr/detailscomplets.php?id=505&lang=fr). [Francisco de la Peña](http://umet.univ-lille1.fr/detailscomplets.php?id=614&lang=fr) created the CLI and GUI.

## Installing QUANTORXS.

QUANTORXS is written in the Python programming languague and is available from pypi. If you are new to Python we reccomend you to install the opensource and free [Anaconda Python distribution](https://www.anaconda.com/download/) for your platform first.

To QUANTORXS execute the following in a terminal (e.g. the Anaconda Prompt  in Windows):

```bash
pip install quantorxs
```

### Detailed instructions for Windows users

* From the start menu, open "anaconda prompt" and type (the directory does not matter):

![Alt text](/Images/Anaconda_prompt.jpg "where to find anaconda prompt")

![Alt text](/Images/Install_command_line.jpg "The install command line")



## Starting the QUANTORXS Graphical User Interface

To start the graphical interface execute the ``quantorxs_gui`` e.g. a terminal. Alternatively, Windows users can start it by  searching for the executable file “quantorxs_gui” in the ``Start Menu`` and launching it as shown in the image below.

![Alt text](/Images/Start_quantorxs.jpg "where to find quantorxs")



## How to use the graphical interface

The program is designed to process several spectra at once. All source spectra should be assembled in one folder.
QUANTORXS reads only the format produced by [aXis2000](http://unicorn.mcmaster.ca/aXis2000.html)

* Click on “choose data directory” and select the folder containing the source spectra.
* Type in an output folder name to store the results of the analysis. The default is storing the results in a ``QUANTORXS result`` folder in the data directory selected in the preceding step.
* Make sure that the "demo" box is not checked. If checked, it uses default files as input to produce an example of the output files.
* Select the format of the figure output (the default is SVG)
* Set the ``offset`` if required to compensate from any energy misalignment (e.g. from poorly calibrated monochromator) *common to all spectra*.
* Click the ``Run`` button and wait until the analysis is completed (usually a few secondes per spectrum).

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
