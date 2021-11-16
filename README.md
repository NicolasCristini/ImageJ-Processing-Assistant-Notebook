# ImageJ-Processing-Assistant-Notebook
-under development-

ImageJ-Processing-Assistant-Notebook (IPAN) consist of a series of ready-to-use Jupyter Notebooks for performing image analysis. This repository includes analytic pipelines to carry on some of the most requested tasks in the biomedical research field. 

For carrying out image analysis we are using the ImageJ software as a library from the Jupyter Notebook coded with Python. This notebook follows the guideline of PyImageJ [here](https://github.com/imagej/pyimagej). 

Main advantages of this working method are:
- performing the all analysis on one single platform,
- standardize the analysis workflow
- combine the ImageJ functionalities with Python tools and packages

Examples for the installation and initialization of ImageJ are already available 
here: https://github.com/imagej/pyimagej/tree/master/doc.

The IPAN project is devided in multiple notebooks. 
The first one available is the "00 - introduction" that shows:
- how to open an image (different options and purposes)
- how to run a ImageJ Macro from JN 
- How to save results/pictures from the Macro


To  run the .ipynb files install the required packages and software. 
Below the basic procedure to install Jupyter Notebook [documentation here](https://jupyter.org/install),

#### Conda and Packages

1. Install Anaconda [download here](https://docs.continuum.io/anaconda/install/hashes/all/).
2. Install PyimageJ [documentation here](https://github.com/imagej/pyimagej/blob/master/doc/Install.md). Pyimage allows the interaction between Python and ImageJ
   
   `$ conda create -n pyimagej pyimagej openjdk=8`
3. Activate the environment before procedding with the other installations.
   
   `$ conda activate pyimagej`
4. Install JPipe [documentation here](https://jpype.readthedocs.io/en/latest/install.html). JPype is a Python module to provide full access to Java from within Python.
   
   `$ conda install -c conda-forge jpype1`
   
   
#### Libraries

Install the lybraries that will be imported in the noteboos:
* 00-Introduction:
    * skimage [here](https://scikit-image.org/docs/dev/install.html) used to import/show images
    
    `$ conda install scikit-image`
    * IPython.display [here](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html) (should be already installed)
    * scyjava [here](https://pypi.org/project/scyjava/) {optional}  Used to set maximum memory pool. The installation of this package requires pip.
    
    `$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
    
    `$ python3 get-pip.py`
    
    `$ pip install scyjava`
    
#### Open the Jupyter Notebook

5. Clone the IPAN repository [download here](https://github.com/NicolasCristini/ImageJ-Processing-Assistant-Notebook/archive/refs/heads/main.zip)
5. Open a terminal console and move to the cloned directory.
6. Lunch the jupyter notebook in a web browser window.
   
   `$ jupyter notebook`
7. Click on the '00-Introduction.ipynb' notebook to open it.


```
(home) ~/
├─ IPAN-project/
│  ├─ FIGURES/
│  │  ├─ F01-Install_PyImageJ.png
│  ├─ IMAGES/
│  │  ├─ Image-test.tif
│  │  ├─ image-test1.tif
│  │  ├─ image-test2.tif
│  ├─ SupportingFunction.py
│  ├─ 00-Introduction.ipynb
```

### Example Notebooks
On the official GitHub of ImageJ there are many available notebook written in ScyJAVA by CurtisReuden [here](https://github.com/imagej/tutorials) written using the SkyJava kernel in Jupyter Notebook. In the web there are not many notebook that use PyImageJ with python. Python allows the possibility to use tools like NumPy, SciPy, scikit-image, CellProfiler, OpenCV, ITK, etc. It is not possible to this tool from Jython, this is a reason more to combine the ImageJ functionalities with Python. Below some example of Pyimagej notebooks:
   * ImageJ with Python Kernel [here](https://nbviewer.org/github/imagej/tutorials/blob/master/notebooks/1-Using-ImageJ/6-ImageJ-with-Python-Kernel.ipynb)
   * Running a plugin that uses ImageJ1 windows¶ [here](https://github.com/uw-loci/Notebooks/blob/9ed90842f06c93b1c206d36fef2b13555e7273d9/PyImageJ/Rigid%20registration%20with%20pyimagej.ipynb)
   * IJ macro test example [here](https://github.com/uw-loci/Notebooks/blob/9ed90842f06c93b1c206d36fef2b13555e7273d9/PyImageJ/IJ%20macro%20test.ipynb)

Useful links: 
* It is possible to consult the "Developer discussion for PyImageJ" [here](https://gitter.im/imagej/pyimagej)
