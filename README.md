# ImageJ-Processing-Assistant-Notebook
-under development-

I.P.A.N. consist of a series of ready-to-use Jupyter Notebooks for performing image analysis. This repository includes analytic pipelines to carry on some of the most requested tasks in the biomedical research field. 

For carrying out image analysis we are using the ImageJ software as a library from the Jupyter Notebook coded with Python. This notebook follows the guideline of PyImageJ (https://github.com/imagej/pyimagej). 

Main advantages of this working method are:
- performing the all analysis on one single platform,
- standardize the analysis workflow
- combine the ImageJ functionalities with Python tools and packages

Examples for the installation and initialization of ImageJ are already available here: https://github.com/imagej/pyimagej/tree/master/doc.

The IPAN project is devided in multiple notebooks. 
The first one available is the "00 - introduction" that shows:
- how to open an image (different options and purposes)
- how to run a ImageJ Macro from JN 
- How to save results/pictures from the Macro

## Pre-requisites

#### Packages and lybraries
To properly run the .ipynb it is important to install the required packages and downloads the folders with the sample images used in the notebook.
1. Install PyimageJ [here](https://github.com/imagej/pyimagej/blob/master/doc/Install.md). For the installation, I suggest to run them with conda in a pre-created environment (ex: pyimagej).
2. Install JPipe [here](https://jpype.readthedocs.io/en/latest/install.html). JPype is a Python module to provide full access to Java from within Python.
```
conda install -c conda-forge jpype1
```
3. Install the lybraries that will be imported in the notebbok
    * scyjava [here](https://pypi.org/project/scyjava/)      {optional}   used to set maximum memory pool
    ```
    pip install scyjava
    ```
    * skimage [here](https://scikit-image.org/docs/dev/install.html)                  used to import/show images
    ```
    conda install scikit-image 
    ```
    * IPython.display [here](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html)          used to just display images (should be already installed)
    ```
    conda install -c anaconda ipython
    ```
    
    
#### Folders

For the purpose of showing how to import and export images/tables in jupyter notebook it is required to have a set of directory organized as specified below:
* Create a folder called "IPAN" in your home directory. The following code will do it for you.
* Download the "Images" folder available in this repository and save it in the "IPAN folder"
* Download the .ipynb notebook, place it in the "IPAN" folder 
* Activate the pyimagej environment, lunch the jupyter notebook and open the .ipynb file
