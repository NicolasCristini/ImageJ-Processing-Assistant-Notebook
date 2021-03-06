
## IMPORT PACKAGES
print("---------------------------------------------------")
print("Importing packages:\n")
import os                         # Used to manipulate and create directory with python.
print("os loaded")
import tifffile                   # Save .tif files from numpy arrays
print("tiffle loaded")
from skimage import io
print("io loaded")
import matplotlib.pyplot as plt
from matplotlib import cm
print("matplotlib loaded")
import numpy as np
print("numpy loaded")
from pathlib import Path
print("pathlib loaded")
print("\n")

## IMPORT IMAGEJ in the module
print("---------------------------------------------------")
print("Importing ImageJ:\n")
if not __name__ == "__main__":
    import imagej
    ij = imagej.init(['sc.fiji:fiji:2.0.0-pre-10', 'net.imagej:imagej-legacy'])
    print("\nThe actual version of ImageJ is:", ij.getApp().getInfo(True))
    print("\nLegacy state: Is active?", ij.legacy.isActive())


## IMAGING PROCESSING functions:

def Open(INPUT_filename = "", path_in = "", path_out = "", process = False):

# 1 - CREATE path for input/outputt
    # FOR SPECIFIED path_in representing for the absolute path of the single file in the EXPERIMENT FOLDER.
    if len(INPUT_filename) == 0:
        INPUT_filename = path_in.rsplit('/', 1)[1]
        path_in = path_in.rsplit('/', 1)[0] + "/"
        if len(path_out) == 0:
            path_out = path_in + "Results/"
            path_image_out = path_in + "Images/"
            try:
                os.mkdir(path_out)
                os.mkdir(path_image_out)
                print("Output directories created")
            except FileExistsError:
                print("Output directories already exist.")
                print("\n")

    #FOR SPECIFIED INPUT_filename in IMAGE folder (located in the same directory of the notebook)
    cwd = os.getcwd() #Get current directory
    if len(path_in) == 0:
        path_in = cwd + "/IMAGES/"
    if len(path_out) == 0:
        path_out = cwd + "/RESULTS/"
        path_image_out = path_out + "resulted_images/"
        try:
            os.mkdir(path_out)
            print("Output directory (RESULTS) created")
        except FileExistsError:
            print("Output directory (RESULTS) already exist.")
            print("\n")

        try:
            os.mkdir(path_image_out)
            print("Output directory (RESULTS/resulted_images/) created")
        except FileExistsError:
            print("Output directory (RESULTS/resulted_images/) already exist.")
            print("\n")

    # INITIALIZE dictionary with arguments
    args_IO = {
    'dir_in' :f"{path_in}",
    'filename_in' : f"{INPUT_filename}"}

    macro_Open = """
    #@ String dir_in
    #@ String filename_in

    // OPEN IMAGE
    open(dir_in + filename_in)
    """
    # RUN the Macro
    macro_results = ij.py.run_macro(macro_Open, args_IO)

    # GET the results
    INPUT_path = path_in + INPUT_filename
    opened_image = ij.py.active_image_plus()

    # PRINT the output
    if not process:
        ij.py.show(opened_image, cmap = "gray")
        print("\nIMAGE ??????")
        print("\nImage path:", f"{INPUT_path}")

    # MAKE variables available for following steps
    global filename, base_dir, results_dir, images_dir
    filename = INPUT_filename           # to pass to other function the input filename
    base_dir = path_in                  # to pass to other function the input directory
    results_dir = path_out              # to save the plots and data resulted from the processes
    images_dir = path_image_out         # to save the images resulted from intermediated processes

def Profile(path_out= "", process = False):
    global filename, base_dir, results_dir
    # If no image is open, a message is printed out that explain how to use this function.
    # Create output filename
    OUTPUT_filename = filename.rsplit('.', 1)[0] + "_profile.png" # create OUTPUT_filename

    # 2 - ImageJ macro
    # Initialize dictionary with arguments
    args_IO = {
    'dir_in' :f"{base_dir}",
    'dir_out' : f'{results_dir}',
    'filename_in' : f'{filename}',
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

    # RUN the Macro on the image left active from the Open function
    open_images = ij.window().getOpenWindows()

    if not len(open_images) == 0:
        macro_results = ij.py.run_macro(macro_Profile, args_IO)
        #GET the results from the macro for checking
        INPUT_path = macro_results.getOutput("in")
        OUTPUT_path = macro_results.getOutput("out")

        #PRINT file/folder and output
        if not process:
            PrintOutput(filename, OUTPUT_filename, base_dir, results_dir)

            profile = io.imread(f"{OUTPUT_path}")
            ij.py.show(profile, cmap = "gray")
            print("IMAGE PROFILE ??????")

    else:
        print("""
        There are no images open.\n
        To use the Profile() function, firstly call the Open() function""")

def Filter(process = False):
    global filename, base_dir, results_dir, images_dir
# This functions apply the mean filter plug-in with default radius = 2 pixels.
# the resulted filtered image will be shown to screen and saved to the IMAGES folder.

    #a) The image is left activated by the previous function, filename is a global variable.
    INPUT_filename = filename
    OUTPUT_filename = INPUT_filename.rsplit('.', 1)[0] + "_filtered.tif"
    path_image_out = images_dir + OUTPUT_filename

    # 2 - RUN the plugin
    plugin = 'Mean'
    args_mean = {
    'block_radius_x': 4,
    'block_radius_y': 4}

    ij.py.run_plugin(plugin, args_mean)

    # ACTIVATE resulted image
    filtered = ij.py.active_image_plus()

    # SAVE resulted filename by modifying the global variable
    filename = OUTPUT_filename

    if not process:
        #PRINT file/folder and output
        PrintOutput(INPUT_filename, OUTPUT_filename, base_dir, results_dir)

        #SAVE the resulted filtered image
        numpy_filtered = ij.py.from_java(filtered)
        tifffile.imwrite(path_image_out, numpy_filtered, imagej=True)

        #SHOW the resulted filtered image to screen
        ij.py.show(filtered, cmap = "gray")
        print("\nIMAGE ??????")

def SubtractBackground(process = False):
    global filename, base_dir, results_dir, images_dir
# This functions apply a ImageJ macro to use the rolling subtract background plug in with default 50 pixel diameter.
# the resulted subtracted image will be shown to screen and saved to the IMAGES folder.

# 1 - Multiple working situations:
    #a) The image is left activated by the previous function, filename is a global variable.
    INPUT_filename = filename
    OUTPUT_filename = INPUT_filename.rsplit('_', 1)[0] + "_subtracted.tif"
    path_image_out = images_dir + OUTPUT_filename

# 2 - ImageJ macro subtract background text
    # INITIALIZE dictionary with arguments

    macro_SubtractBackground = """

// macro commands
run("Enhance Contrast...", "saturated=0.35");               // Run the default contract
run("Subtract Background...", "rolling=50 disable");        // Run the default contract
"""
    ij.py.run_macro(macro_SubtractBackground)

    #ACTIVATE subtracted image
    subtracted = ij.py.active_image_plus()

    # SAVE resulted filename
    filename = OUTPUT_filename

    if not process:
        PrintOutput(INPUT_filename, OUTPUT_filename, base_dir, results_dir)

        #SAVE the resulted subtracted image
        numpy_subtracted = ij.py.from_java(subtracted)
        tifffile.imwrite(path_image_out, numpy_subtracted, imagej=True)

        #SHOW the results to screen
        ij.py.show(subtracted, cmap = "gray")
        print("\nIMAGE ??????")

def Threshold(process = False):
    global filename, base_dir, results_dir, images_dir
# This functions apply a ImageJ macro to applly the Threshold. Now setted as Li.
# the resulted thresholded image will be shown to screen and saved to the IMAGES folder.
# In the following macro, I had to save the image from the macro-text becuase the method used before gave an ERROR

# 1 - Multiple working situations:
    #a) The image is left activated by the previous function, filename is a global variable.
    INPUT_filename = filename
    OUTPUT_filename = INPUT_filename.rsplit('_', 1)[0] + "_thresholded.tif"
    path_image_out = images_dir + OUTPUT_filename

    args_IO = {
    'path_out' : f'{path_image_out}',
    }

    macro_Threshold = """
//DEFINE IO
#@ String path_out

// RUN threshold
setAutoThreshold("Default dark");
setOption("BlackBackground", true);
run("Convert to Mask");
run("Watershed");
saveAs("tiff", path_out);  //In this case the image must be saved within the macro
"""
    ij.py.run_macro(macro_Threshold, args_IO)

    thresholded = ij.py.active_image_plus()

    # SAVE resulted filename
    filename = OUTPUT_filename

    # ACTIVATE resulted image

    if not process:
        # PRINT file/folder AND output
        PrintOutput(INPUT_filename, OUTPUT_filename, base_dir, results_dir)

        #PRINT the results
        imp_thresholded = io.imread(path_image_out)
        ij.py.show(imp_thresholded, cmap = "gray")
        print("\nIMAGE ??????")

def Count(process = False):
    global filename, base_dir, results_dir, images_dir
# This functions use the *Analyse Particles* in a ImageJ macro to applly to count the number of objects in the picture.
# the Result table will show the feature selected in *Set Measurements* In this case we are going to analysis:
# area, circularity, AR ratio. The resulted table will be saved in the RESULTS folder.
# Besides that, the table will be displayed by using pandas.


# 1 - Multiple working situations:
    #a) The image is left activated by the previous function, filename is a global variable.

    INPUT_filename = filename
    OUTPUT_filename = INPUT_filename.rsplit('_', 1)[0] + "_data.csv"
    path_data_out = results_dir + OUTPUT_filename

    args_IO = {
    'path_out' : f'{path_data_out}',
    }

    macro_Count = """
// DEFINE IO
#@ String path_out

// RUN THE MEASUREMENTS
title = getTitle()

run("Set Measurements...", "area shape display redirect=None decimal=3");
run("Analyze Particles...", "size=20-Infinity pixel circularity=0.10-1.00 show=Outlines display clear summarize in_situ");
saveAs("Results", path_out);
"""

    ij.py.run_macro(macro_Count, args_IO)

    if not process:
        PrintOutput(INPUT_filename, OUTPUT_filename, base_dir, results_dir)
        print("\nThe data are saved as:\n", path_data_out)

    #PRINT the results
    return path_data_out

def MacroRun(filepath= "", macro_title = "", process = False):
    global macros
# This function run any kind of Macro of your choise by just giving in input the Macro macro_text
# The macros are collected in a dictionary and called to the SpecialRun() with their initialization name

    # Manafe IO
    if len(filepath) == 0:
        print("Select input file by pasting the absolute file path")
    else:
        INPUT_filename = filepath.rsplit('/', 1)[1]
        OUTPUT_filename = INPUT_filename.rsplit('.', 1)[0] + "_MacroResult.tiff"
        path_in = filepath.rsplit('/', 1)[0] + "/"
        path_out = path_in + "Results/"
        try:
            os.mkdir(path_out)
        except FileExistsError:
            print("Output directory already exist.")
            print("\n")


    # ImageJ macro arguments
    macro_args = {
        'dir_in' :f"{path_in}",
        'dir_out' : f'{path_out}',
        'filename_in' : f'{INPUT_filename}',
        'filename_out' : f'{OUTPUT_filename}'
        }

    # ImageJ macro commands
    macro_args_text = """
//DEFINE IO
#@ String dir_in
#@ String dir_out
#@ String filename_in
#@ String filename_out
"""

    macro_text = macro_args_text + "\n" + macros[macro_title]
    macro_results = ij.py.run_macro(macro_text, macro_args)
    print("The results are saved in:\n\n", path_out+OUTPUT_filename)


## ACCESSORIES funtions:
def AddMacro(title = "", text = ""):
    global macros
    macros = {}
    macros[title] = text

def Profile3D(INPUT_path):
    #Set input/outout
    filename_title = INPUT_path.rsplit('/', 1)[1].rsplit('.',1)[0] + "_profile3D"
    filename_path = INPUT_path.rsplit('/', 1)[0]

    path_out = filename_path + "/Results/"
    try:
        os.mkdir(path_out)
        print("Output directories created.\n")
    except FileExistsError:
        print("Output directories already exist.\n")

    filename_pathout = path_out + filename_title + ".tif"

    #Open image
    image = io.imread(INPUT_path)
    print("\nThe computer see the image as a matrix of values.")
    print(image)

    print("\nThe human eye see the image as a change in light intensity.")
    print("\nThe image can also be as a 3D representation of the pixel intensity:\n")

    #Show image
    plt.imshow(image, cmap = "gray")

    #Create data to plot
    dimensions = np.shape(image)
    X = np.arange(0, dimensions[0])
    Y = np.arange(0, dimensions[1])
    X, Y = np.meshgrid(X, Y)
    Z = image

    # Plot the surface.
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize = (12,12))
    surf = ax.plot_surface(X, -Y, Z, cmap=cm.viridis, linewidth=0, antialiased=True)

    # Customize the z axis.
    ax.set_zlim(0, 255)

    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.3, aspect=10)
    plt.title(filename_title)

    plt.show()

    fig.savefig(filename_pathout, dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)


## SUPPORTING functions:
def PrintOutput(I_file, O_file, I_path, O_path):
    print("---------------------------------------------------")
    print("\n")
    print("The images are imported from: ", I_path)
    print("INPUT_filename:", I_file)
    print("\n")
    print("The results are exported in: ", O_path)
    print("OUTPUT_filename:", O_file)
    print("\n")
    print("---------------------------------------------------")

def CloseAll():
    macro_close_text = """
close("*");
run("Close All");
"""
    ij.py.run_macro(macro_close_text)
    print("\nAll windows are closed")

def FolderTree(folder_path): #credits to [https://stackoverflow.com/users/2479038/abstrus
    class DisplayablePath(object):
        display_filename_prefix_middle = '?????????'
        display_filename_prefix_last = '?????????'
        display_parent_prefix_middle = '    '
        display_parent_prefix_last = '???   '

        def __init__(self, path, parent_path, is_last):
            self.path = Path(str(path))
            self.parent = parent_path
            self.is_last = is_last
            if self.parent:
                self.depth = self.parent.depth + 1
            else:
                self.depth = 0

        @property
        def displayname(self):
            if self.path.is_dir():
                return self.path.name + '/'
            return self.path.name

        @classmethod
        def make_tree(cls, root, parent=None, is_last=False, criteria=None):
            root = Path(str(root))
            criteria = criteria or cls._default_criteria

            displayable_root = cls(root, parent, is_last)
            yield displayable_root

            children = sorted(list(path
                                   for path in root.iterdir()
                                   if criteria(path)),
                              key=lambda s: str(s).lower())
            count = 1
            for path in children:
                is_last = count == len(children)
                if path.is_dir():
                    yield from cls.make_tree(path,
                                             parent=displayable_root,
                                             is_last=is_last,
                                             criteria=criteria)
                else:
                    yield cls(path, displayable_root, is_last)
                count += 1

        @classmethod
        def _default_criteria(cls, path):
            return True

        @property
        def displayname(self):
            if self.path.is_dir():
                return self.path.name + '/'
            return self.path.name

        def displayable(self):
            if self.parent is None:
                return self.displayname

            _filename_prefix = (self.display_filename_prefix_last
                                if self.is_last
                                else self.display_filename_prefix_middle)

            parts = ['{!s} {!s}'.format(_filename_prefix,
                                        self.displayname)]

            parent = self.parent
            while parent and parent.parent is not None:
                parts.append(self.display_parent_prefix_middle
                             if parent.is_last
                             else self.display_parent_prefix_last)
                parent = parent.parent

            return ''.join(reversed(parts))

    paths = DisplayablePath.make_tree(Path(folder_path))
    for path in paths:
        print(path.displayable())



print("---------------------------------------------------")
print("\nIPAN module loaded\n")
print("---------------------------------------------------")
