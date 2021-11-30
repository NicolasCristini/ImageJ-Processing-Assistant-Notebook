# ImageJ-Processing-Assistant-Notebook
-under development-

ImageJ-Processing-Assistant-Notebook (IPAN) consist of a series of ready-to-use Jupyter Notebooks for performing image analysis. This repository includes analytic pipelines to carry on some of the most requested tasks in the biomedical research field. 

For carrying out image analysis we are using the ImageJ software as a library from the Jupyter Notebook coded with Python. This notebook follows the guideline of PyImageJ [here](https://github.com/imagej/pyimagej). 

The main advantages of this working method are:
- performing all analysis on one single platform,
- standardize the analysis workflow
- combine the ImageJ functionalities with Python tools and packages

Examples for the installation and initialization of ImageJ are already available 
[here](https://github.com/imagej/pyimagej/tree/master/doc).

The IPAN project is divided into multiple notebooks. 
* 01-Working with ImageJ pt.1.ipynb:
     * how to open an image (different options and purposes)
     * how to run an ImageJ Macro from JN 
     * how to save results/pictures from the Macro
 
* 02-Working with ImageJ pt.2.ipynb:
     * how to run a ImageJ plug-in from JN 
     * how to build generalize functions
     * how to process an image in steps

* 03-Working with IPAN module.ipynb:
     * perform image analysis with imported functions

To run the .ipynb files install the required packages and software. 
Below is the basic procedure to install Jupyter Notebook [documentation here](https://jupyter.org/install),

#### Conda and Packages

1. Install Anaconda [download here](https://docs.continuum.io/anaconda/install/hashes/all/).
2. Install PyimageJ [documentation here](https://github.com/imagej/pyimagej/blob/master/doc/Install.md). Pyimage allows the interaction between Python and ImageJ
   
   `$ conda create -n pyimagej pyimagej openjdk=8`
3. Activate the environment before proceeding with the other installations.
   
   `$ conda activate pyimagej`
4. Install JPipe [documentation here](https://jpype.readthedocs.io/en/latest/install.html). JPype is a Python module to provide full access to Java from within Python.
   
   `$ conda install -c conda-forge jpype1`
   
#### Open the Jupyter Notebook

5. Clone the IPAN repository [download here](https://github.com/NicolasCristini/ImageJ-Processing-Assistant-Notebook/archive/refs/heads/main.zip)
5. Open a terminal console and move to the cloned directory.
6. Lunch the jupyter notebook in a web browser window.
   
   `$ jupyter notebook`
7. Click on the '##-NOTEBOOK.ipynb' to open it.

#### Libraries

Install the libraries that will be imported in the notebook:
* 00-Working with ImageJ pt.1:
    * skimage [here](https://scikit-image.org/docs/dev/install.html) used to import/show images
    
    `$ conda install scikit-image`
    * IPython.display [here](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html) (should be already installed)
    * scyjava [here](https://pypi.org/project/scyjava/) {optional}  Used to set maximum memory pool. The installation of this package requires pip.
    
    `$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
    
    `$ python3 get-pip.py`
    
    `$ pip install scyjava`
    
* 01-Working with ImageJ pt.2:
    * tiffile

     `conda install -c conda-forge tifffile`

```
(home) ~/
├─ IPAN-project/
│  ├─ FIGURES/
│  │  ├─ F01-Install_PyImageJ.png
│  ├─ IMAGES/
│  │  ├─ Image-test.tif
│  │  ├─ image-test1.tif
│  │  ├─ image-test2.tif
│  │  ├─ image-test3.tif
│  ├─ SupportingFunction.py
│  ├─ ProcessingFunction.py
│  ├─ 00-Working with ImageJ pt.1.ipynb
│  ├─ 01-Working with ImageJ pt.2.ipynb
│  ├─ 02-Working with ImageJ pt.3.ipynb
```

### Example Notebooks
On the official GitHub of ImageJ, there are many available notebooks written in ScyJAVA by CurtisReuden [here](https://github.com/imagej/tutorials) written using the SkyJava kernel in Jupyter Notebook. On the web, there are not many notebooks that use PyImageJ with python. Python allows the possibility to use tools like NumPy, SciPy, scikit-image, CellProfiler, OpenCV, ITK, etc. It is not possible to this tool from Jython, this is a reason more to combine the ImageJ functionalities with Python. Below some examples of Pyimagej notebooks:
   * Workshop material of the 2020 ImageJ conference [here](https://github.com/imagej/i2k-2020-pyimagej)
   * ImageJ with Python Kernel [here](https://nbviewer.org/github/imagej/tutorials/blob/master/notebooks/1-Using-ImageJ/6-ImageJ-with-Python-Kernel.ipynb)
   * Running a plugin that uses ImageJ1 windows¶ [here](https://github.com/uw-loci/Notebooks/blob/9ed90842f06c93b1c206d36fef2b13555e7273d9/PyImageJ/Rigid%20registration%20with%20pyimagej.ipynb)
   * IJ macro test example [here](https://github.com/uw-loci/Notebooks/blob/9ed90842f06c93b1c206d36fef2b13555e7273d9/PyImageJ/IJ%20macro%20test.ipynb)

Useful links: 
* It is possible to consult the "Developer discussion for PyImageJ" [here](https://gitter.im/imagej/pyimagej)
