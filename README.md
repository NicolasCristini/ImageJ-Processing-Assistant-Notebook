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

1. Install Anaconda[download here](https://docs.continuum.io/anaconda/install/hashes/all/).
2. Install PyimageJ [documentation here](https://github.com/imagej/pyimagej/blob/master/doc/Install.md). Pyimage allows the interaction between Python and ImageJ
   `conda create -n pyimagej pyimagej openjdk=8`
3. Activate the environment before procedding with the other installations.
   `conda activate pyimagej`
4. Install JPipe [documentation here](https://jpype.readthedocs.io/en/latest/install.html). JPype is a Python module to provide full access to Java from within Python.
   `conda install -c conda-forge jpype1`
   
   
#### Lybraries

Install the lybraries that will be imported in the notebbok
    * scyjava [here](https://pypi.org/project/scyjava/) {optional} used to set maximum memory pool
    `pip install scyjava`
    * skimage [here](https://scikit-image.org/docs/dev/install.html) used to import/show images
    `conda install scikit-image`
    * IPython.display [here](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html) (should be already installed)
    
#### Open the Jupyter Notebook

5. Clone the IPAN repository [download here](https://github.com/NicolasCristini/ImageJ-Processing-Assistant-Notebook/archive/refs/heads/main.zip)
5. Open a terminal console and move to the cloned directory.
6. Lunch the jupyter notebook in a web browser window.
   `jupyter notebook`
7. Click on the `00-Introduction.ipynb` notebook to open it.


```
(home) ~/
├─ IPAN-project/
│  ├─ IMAGES/
│  │  ├─ Image-test.tif
│  │  ├─ image-test1.tif
│  │  ├─ image-test2.tif
│  ├─ SupportingFunction.py
│  ├─ 00-Introduction.ipynb
```
