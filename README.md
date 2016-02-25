# EbirdToLaTex Checklist Generator #
eBirdToLaTex Checklist Generator is a short Python script which generates a customisable bird checklist based on a specific eBird dataset

## Motivation ##
Visit the page on [my website](http://zoziologie.raphaelnussbaumer.com/ebirdtolatex/) which explain more why I belive checklist are still important.

## How to use it ? ##
In this new version, internet connection is required to download updated bird taxonomy list, language traduction as well as location barchart data. This result in a very simple script to run. 

Everything is in the ```Script_Python.py```. You only need the ```Template_default.tex```, on which the script will write the new tex file. 

The script only create a .tex (LaTeX file), you will need to use your own tex compileur to create the pdf. Online tex editor and compilor exist. [ShareLaTeX](https://www.sharelatex.com/) is my favorite.


## How it work ##
### Load eBird barchart: ###
1. Define Project name : ```project_name``` (string )
2. Choose a location: ```code_loc``` (see [eBird API](https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-HotSpotsByRegion) for possibility)
3. Choose language : ```lang``` (list of language code, see python code for possibility)
4. Define date of interest : ```byear```, ```eyear```, ```bmonth```, ```emonth``` (begining and end month and year)

Then ```bird_creator``` fonction will return eBird barchar in a bird list format ```bird_list```.

### Create Table: ###

1. Define the columns you want to see in your checklist. Here are your possibilities (please, have a look at the code to better understand how to choose each column, the order of input will also be the order in the checklist):
  1. language (English, French, Latin…), 
  2. frequency (as a percentage per month, seasons or year), 
  3. notes (empty space for comments) and 
  4. space (“__” ) to write the number of birds seen or boxes to be ticked.
2. The checklist can create two distinct zones in the checklist: the regular list and the rare list. According to a chosen criteria (e.g: frequency under 1%, does not contain “hybrid”…etc ) birds are displayed either under “regular” (```condition_tableau```), “rare” (```condition_rare```)or none of the lists. The rare list only provides one language and one symbol for each bird. 

Finally, ```write_to_latex``` will create the tex file using ```Template_default.tex```

## Work to do ##
I'm currently working on a javascript adaptation of this script with a web interface to create the tex or even the pdf ! This would be great for non-geek birder ! I'm currently blocked at getting the barchart data as in order to get it, you need to be listed in the [cross-domain policy file](http://ebird.org/crossdomain.xml). The best solution would be to make this data available in the [eBird API](https://confluence.cornell.edu/display/CLOISAPI/eBirdAPIs). Any idea how to get that ?

## Contact ##
Don't hesitate to contact me for any question ! And visit by webiste (if you have some spare time !)
[Raphael Nussbaumer](rafnuss@gmail.com) 
[zoziologie.raphaelnussbaumer.comm](http://zoziologie.raphaelnussbaumer.com/)
