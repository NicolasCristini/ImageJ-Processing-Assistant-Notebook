run("Close All");
print("\\Clear")
setBatchMode(true);


//Macro Info
scripttitle="Fluorescent Intensity Measuring Script";
version="1.0";
versiondate="08/11/2021";
description="Details: <br>This script takes fluorescent images and get the signal intensity of the area covered by cells and the bakgrounf intensity. <br><br>"
+"The CTCF is computed starting from this values and displayed in a bar plot at the end of the analysis"


print("FIJI Macro: "+scripttitle);								// Prints general information
print("Version: "+version+" ("+versiondate+")");
print("UU: Utrecht University - Applied Data Science Profile");
print("By Nicolas Cristini (2021) n.cristini@students.uu.nl")

start = getTime();	
print("");


// 1 ASK FOR THE SOURCE DIRECTORY

directory = getDirectory("Choose Source Directory");
result_directory = directory + "Results";
File.makeDirectory(result_directory);

summaryFile = File.open(result_directory + "/Data.csv");		//Creates a results file named Data.csv
print(summaryFile,"Filename"+","+"Nuclei"+","+"Signal-Area"+","+"Signal-Intensity"+","+"IntDen"+","+"Background-Area"+","+"Background-Intensity");

// 2 DEFINE THE MACRO FUNCTION

function intensityROI(dir, filename, cycle){
	print("Cycle: ",cycle+1);									// Log output, to keep track of the cycle
	run("Clear Results");
	roiManager("reset");										// Reset the ROI magager at the beggining of each cycle
	
	open(dir+filename);											// Open image
	title = File.getNameWithoutExtension(dir+filename);			// Get the tile
	selectWindow(filename);

	
	run("Split Channels");										// Split channels
	selectWindow("C2-" + filename);								// Select blue channel
	id_nuclei = getImageID();
	run("Duplicate...", "title=Nuclei.jpg");
	id_nuclei2 = getImageID();
	
	selectWindow("C1-" + filename); 							// Select green channel
	id_original = getImageID();
	run("Duplicate...", "title=Combine-ROIs.jpg");
	
	id_1 = getImageID();										// Make duplicates to run the multiple steps of the analysis
	run("Duplicate...", "title=Signal-intensity.jpg");
	id_2 = getImageID();
	run("Duplicate...", "title=Background-intensity.jpg");
	id_3 = getImageID();	

	//COUNT THE NUMBER OF CELLS/NUCLEI
	selectImage(id_nuclei);
	setAutoThreshold("Li dark");
	setOption("BlackBackground", false);
	run("Convert to Mask");
	run("Watershed");
	
	run("Set Measurements...", "decimal=3");					// Count the nuclei
	run("Analyze Particles...", "size=50-Infinity circularity=0.10-1.00 show=Outlines display clear summarize add");
	
	selectImage(id_nuclei2);									// Paste the nucei outline and save the image
	roiManager("Show All");
	roiManager("Set Color", "white");							// Sets ROIs lines to be the colour white																						
	roiManager("Set Line Width", 1);							// Sets ROIs line width to be 1									// Displays all ROIs onto the image window																						
	run("Flatten");
	saveAs("png", result_directory + "/" + title +"-Nuclei.png");
	
	NNuclei = getValue("results.count");						// Get the number of nuclei for the Data.csv file
	
	//SELECT THE TOTAL AREA COVERED BY CELLS
	selectImage(id_1);
	run("Median...", "radius=2");
	setAutoThreshold("Otsu dark");
	run("Analyze Particles...", "  show=Outlines add");
	num = roiManager("count");									// Get the number of single ROIs for the following step
	run("Close");

	//COMBINE THE ROIs AND SELECT THE SAME AREA ON THE ORIGINAL IMAGE																											
	selectImage(id_2);
	
	selectedRois=newArray(num);									// Create the array with the numbers of all the ROIs from 0 to #totROis
	for (indI = 0; indI < num; indI++){
		selectedRois[indI]=indI;
		}
	roiManager("Select", selectedRois);							// Select all the ROIs present in the manager
						
	roiManager("Combine");										// Combine (OR). Union of the all the ROIs
	roiManager("Deselect");                                		
	roiManager("Delete");										// Delete them from the ROIs
	roiManager("Add");											// Add the ROI that combines all the others

	//MEASUREMENTS OF THE INTEGRATED DENSITY ON ALL THE COMBINED ROIs
	run("Set Measurements...", "area mean integrated redirect=None decimal=3");
	run("Measure");																								
	Signal_Area = getResult("Area");							// Get these variable to save it in the final Data.csv file
	Signal_Intensity = getResult("Mean");      																					
	Integrated_Density = getResult("IntDen");
	
	roiManager("Set Color", "white");							// Sets ROIs lines to be the colour white																						
	roiManager("Set Line Width", 1);							 																				
 	run("Flatten");												// Paste the nucei outline and save the image
	saveAs("png", result_directory + "/" + title +"-ROI.png");

	//MEASURE BACKGROUND INTENSITY
	selectImage(id_3);
	roiManager("Select", 0);
	run("Make Inverse");										// In this way we measure the mean value of	the background.	
	run("Enlarge...", "enlarge=-5");							//  We can shrink the selection to avoid the region close to the object
	run("Set Measurements...", "area mean integrated redirect=None decimal=3");													
	run("Measure");			 									
	Background_Intensity = getResult("Mean");					// Get the values for the final Data.csv file
	Background_Area = getResult("Area");																							 	
	
	//PRINT pre-SELECTED OUTPUT
	print(summaryFile, title+","+NNuclei+","+ Signal_Area + "," + Signal_Intensity +","+ Integrated_Density +"," + Background_Area + "," + Background_Intensity);
	print("");
	run("Close All");
}

// 3 RUN THE FUNCTION IN THE CYCLE

list = getFileList(directory);

for (i = 0; i < list.length;i++){
if (endsWith(list[i], ".tif")){	
	intensityROI(directory, list[i], i);
}}

// 4 SAVE OUTPUT
print("");
print("Batch Completed");
print("Total Runtime was:");print((getTime()-start)/1000); 

selectWindow("Log");																																			//Selects the log window
saveAs("Text", result_directory+ "/Log.txt");	


//End of Script