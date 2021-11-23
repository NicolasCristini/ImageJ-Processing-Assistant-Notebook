#Import required Libraries:
print("---------------------------------------------------")
print("Importing packages:\n")

import os                         # Used to manipulate and create directory with python.
print("os loaded")
import tifffile                   # Save .tif files from numpy arrays
print("tiffle loaded")
from skimage import io
print("io loaded")

print("---------------------------------------------------")

#Import IMAGEJ in the module
import imagej
ij = imagej.init(['sc.fiji:fiji:2.0.0-pre-10', 'net.imagej:imagej-legacy'])

#Function:
def Open(INPUT_filename = "", path_in = ""):

# make variables  available to all functions and to name and save the following resulted images

# 1 - CREATE path for input/outputt

    # FOR SPECIFIED INPUT_filename in IMAGE folder - located in the directory of the notebook -
    if len(INPUT_filename) == 0:
        INPUT_filename = path_in.rsplit('/', 1)[1]
        path_in = path_in.rsplit('/', 1)[0] + "/"

    #FOR SPECIFIED INPUT_filename in IMAGE folder (located in the same directory of the notebook)
    cwd = os.getcwd() #Get current directory
    if len(path_in) == 0:
        path_in = cwd + "/IMAGES/"
        print("\n")
        print("The images are imported from: ", path_in)

# 2 - ImageJ macro text

    # INITIALIZE dictionary with arguments
    args_IO = {
    'dir_in' :f"{path_in}",
    'filename_in' : f"{INPUT_filename}"}

    macro_Open = """
    #@ String dir_in
    #@ String filename_in
    #@output String in

    // CREATE OUTPUT
    in = dir_in + filename_in

    // OPEN IMAGE
    open(in)
    """

    # RUN the Macro
    macro_results = ij.py.run_macro(macro_Open, args_IO)

    # GET the results
    INPUT_path = macro_results.getOutput("in")

    # PRINT the results
    opened_image = ij.py.active_image_plus()
    ij.py.show(opened_image, cmap = "gray")
    print("\nIMAGE ⬆︎")

    print("\nImage path:", f"{INPUT_path}")
    print("--> this image has been opened with the Open() function [IPAN-project]")

    # MAKE variables available for following steps
    global filename, image
    filename = INPUT_filename

def Profile(path_in = "", path_out= ""):
    # 1 - Multiple working situations:
    #a) The image is left activated by the the Open() function, filename is a global variable.

    INPUT_filename = filename
    OUTPUT_filename = INPUT_filename.rsplit('.', 1)[0] + "_profile.png" # create OUTPUT_filename

    #b) The profile is computed on a non open image. INPUT_filename of path_in is specified

    # MISSING (WORK WITH CLASSES TO IMPLEMENT THIS OPTION)

    cwd = os.getcwd() #Get current directory
    if len(path_in) == 0:
        path_in = cwd + "/IMAGES"
    if len(path_out) == 0:
        path_out = cwd + "/RESULTS"

    try:
        os.mkdir(path_out)
    except FileExistsError:
        print("The output directory already exist.")

    # PRINT file/folder info
    print("---------------------------------------------------")
    print("\n")
    print("The images are imported from: ", path_in)
    print("INPUT_filename:", INPUT_filename)

    print("\n")

    print("The results are exported in: ", path_out)
    print("OUTPUT_filename:", OUTPUT_filename)
    print("\n")
    print("---------------------------------------------------")

# 2 - ImageJ macro profile text

    # INITIALIZE dictionary with arguments
    args_IO = {
    'dir_in' :f"{path_in}",
    'dir_out' : f'{path_out}',
    'filename_in' : f'{INPUT_filename}',
    'filename_out' : f'{OUTPUT_filename}'
    }

    # ImageJ macro commands
    macro_Profile = """

//DEFINE IO
#@ String dir_in
#@ String dir_out
#@ String filename_in
#@ String filename_out
#@output String in
#@output String out

title = getTitle();

in = dir_in + "/" + filename_in
out = dir_out + "/" + filename_out

//MAKE AND SAVE PROFILE ON ORIGINAL IMAGE

H = getHeight();                            // get image size
W = getWidth();
makeLine(0, 0, W, H, 5);                    // make line with
run("Plot Profile");                        // make Profile
saveAs(".png", out);

// SELECT THE INPUT IMAGES AS LAST COMMAND FOR THE FOLLOWING STEPS
selectWindow(title);
"""

    #RUN the Macro
    macro_results = ij.py.run_macro(macro_Profile, args_IO)

    #GET the results
    INPUT_path = macro_results.getOutput("in")
    OUTPUT_path = macro_results.getOutput("out")
    results = (INPUT_path, OUTPUT_path)

    profile = io.imread(f"{OUTPUT_path}")
    ij.py.show(profile, cmap = "gray")
    print("IMAGE PROFILE ⬆︎")

    # Select the previous active image to reselect it at the end of the function for next steps!
    image = ij.py.active_image_plus()

def Filter(path_in = "", path_out = ""):
    global filename, image
# This functions apply the mean filter plug-in with default radius = 2 pixels.
# the resulted filtered image will be shown to screen and saved to the IMAGES folder.

# 1 - Multiple working situations:
    #a) The image is left activated by the previous function, filename is a global variable.

    INPUT_filename = filename
    OUTPUT_filename = INPUT_filename.rsplit('.', 1)[0] + "_filtered.tif"

    # get the IMAGES folder path to save the resulted image
    cwd = os.getcwd() # get current directory
    if len(path_in) == 0:
        path_in = cwd + "/IMAGES"
    path_image_out = path_in + "/" + OUTPUT_filename

    # PRINT file/folder info
    print("---------------------------------------------------")
    print("\n")
    print("The images are imported from: ", path_in)
    print("INPUT_filename:", INPUT_filename)

    print("\n")

    print("The results are exported in: ", path_image_out)
    print("OUTPUT_filename:", OUTPUT_filename)
    print("\n")
    print("---------------------------------------------------")


# 2 - RUN the plugin
    plugin = 'Mean'
    args_mean = {
    'block_radius_x': 4,
    'block_radius_y': 4}

    ij.py.run_plugin(plugin, args_mean)

    # SAVE the resulted filtered image
    filtered = ij.py.active_image_plus()
    numpy_filtered = ij.py.from_java(filtered)
    tifffile.imwrite(path_image_out, numpy_filtered, imagej=True)

    # PRINT the results
    ij.py.show(filtered, cmap = "gray")
    print("\nIMAGE ⬆︎")

    # ACTIVATE resulted image
    filtered = ij.py.active_image_plus()
    # SAVE resulted filename
    filename = OUTPUT_filename

def SubtractBackground(path_in = "", path_out = ""):
    global filename

# This functions apply a ImageJ macro to use the rolling subtract background plug in with default 50 pixel diameter.
# the resulted subtracted image will be shown to screen and saved to the IMAGES folder.

# 1 - Multiple working situations:
    #a) The image is left activated by the previous function, filename is a global variable.

    INPUT_filename = filename
    OUTPUT_filename = INPUT_filename.rsplit('_', 1)[0] + "_subtracted.tif"
    path_image_out = path_in + "/" + OUTPUT_filename

    # get the IMAGES folder path to save the resulted image
    cwd = os.getcwd() # get current directory
    if len(path_in) == 0:
        path_in = cwd + "/IMAGES"
    path_image_out = path_in + "/" + OUTPUT_filename

    # PRINT file/folder info
    print("---------------------------------------------------")
    print("\n")
    print("The images are imported from: ", path_in)
    print("INPUT_filename:", INPUT_filename)

    print("\n")

    print("The results are exported in: ", path_image_out)
    print("OUTPUT_filename:", OUTPUT_filename)
    print("\n")
    print("---------------------------------------------------")


# 2 - ImageJ macro subtract background text
    # INITIALIZE dictionary with arguments

    macro_SubtractBackground = """

// macro commands
run("Enhance Contrast...", "saturated=0.35");               // Run the default contract
run("Subtract Background...", "rolling=50 disable");        // Run the default contract
"""
    ij.py.run_macro(macro_SubtractBackground)

    #SAVE the resulted subtracted image
    subtracted = ij.py.active_image_plus()
    numpy_subtracted = ij.py.from_java(subtracted)
    tifffile.imwrite(path_image_out, numpy_subtracted, imagej=True)

    #PRINT the results
    ij.py.show(subtracted, cmap = "gray")
    print("\nIMAGE ⬆︎")

    # ACTIVATE resulted image
    subtracted = ij.py.active_image_plus()

    # SAVE resulted filename
    filename = OUTPUT_filename

def Threshold(path_in = "", path_out = ""):
    global filename
# This functions apply a ImageJ macro to applly the Threshold. Now setted as Li.
# the resulted thresholded image will be shown to screen and saved to the IMAGES folder.
# In the following macro, I had to save the image from the macro-text becuase the method used before gave an ERROR

# 1 - Multiple working situations:
    #a) The image is left activated by the previous function, filename is a global variable.

    INPUT_filename = filename
    OUTPUT_filename = INPUT_filename.rsplit('_', 1)[0] + "_thresholded.tif"
    path_image_out = path_in + "/" + OUTPUT_filename

    # get the IMAGES folder path to save the resulted image
    cwd = os.getcwd() # get current directory
    if len(path_in) == 0:
        path_in = cwd + "/IMAGES"
    path_image_out = path_in + "/" + OUTPUT_filename

    # PRINT file/folder info
    print("---------------------------------------------------")
    print("INPUT:")
    print("The images are imported from: ", path_in)
    print("INPUT_filename:", INPUT_filename)

    print("\n")
    print("OUTPUT:")
    print("The results are exported in: ", path_image_out)
    print("OUTPUT_filename:", OUTPUT_filename)
    print("---------------------------------------------------")

    args_IO = {
    'path_out' : f'{path_image_out}',
    }

    macro_Threshold = """
//DEFINE IO
#@ String path_out

// GET title
title = getTitle();

// RUN threshold
setAutoThreshold("Default dark");
setOption("BlackBackground", true);
run("Convert to Mask");
run("Watershed");

// SAVE image
selectWindow(title);
saveAs("tiff", path_out);
"""
    ij.py.run_macro(macro_Threshold, args_IO)

    #PRINT the results
    thresholded = io.imread(path_image_out)
    ij.py.show(thresholded, cmap = "gray")
    print("\nIMAGE ⬆︎")

    # ACTIVATE resulted image
    thresholded = ij.py.active_image_plus()

    # SAVE resulted filename
    filename = OUTPUT_filename

def Count(path_in = "", path_out = ""):
    global filename
# This functions use the *Analyse Particles* in a ImageJ macro to applly to count the number of objects in the picture.
# the Result table will show the feature selected in *Set Measurements* In this case we are going to analysis:
# area, circularity, AR ratio. The resulted table will be saved in the RESULTS folder.
# Besides that, the table will be displayed by using pandas.

# 1 - Multiple working situations:
    #a) The image is left activated by the previous function, filename is a global variable.

    INPUT_filename = filename
    OUTPUT_filename = INPUT_filename.rsplit('_', 1)[0] + "_data.csv"

    # get the IMAGES folder path to save the resulted image
    cwd = os.getcwd() # get current directory
    if len(path_in) == 0:
        path_in = cwd + "/IMAGES"
    if len(path_out) == 0:
        path_out = cwd + "/RESULTS"

    path_data_out = path_out + "/" + OUTPUT_filename

    # PRINT file/folder info
    print("---------------------------------------------------")
    print("INPUT:")
    print("The images are imported from: ", path_in)
    print("INPUT_filename:", INPUT_filename)

    print("\n")
    print("OUTPUT:")
    print("The results are exported in: ", path_out)
    print("OUTPUT_filename:", OUTPUT_filename)
    print("---------------------------------------------------")

    args_IO = {
    'path_out' : f'{path_data_out}',
    }

    macro_Count = """
// DEFINE IO
#@ String path_out

// RUN THE MEASUREMENTS
title = getTitle()

run("Set Measurements...", "area shape display redirect=None decimal=3");
run("Analyze Particles...", "size=20-Infinity pixel circularity=0.10-1.00 show=Outlines display exclude clear summarize in_situ");
saveAs("Results", path_out);
"""

    ij.py.run_macro(macro_Count, args_IO)
    print("\nThe data are saved as:\n", path_data_out)

    #PRINT the results
    return path_data_out

print("---------------------------------------------------")
#Outout:
print("\nThe actual version of ImageJ is:", ij.getApp().getInfo(True))
print("\nLegacy state: Is active?", ij.legacy.isActive())
print("\nProcessing Functions is loaded!")

print("---------------------------------------------------")
