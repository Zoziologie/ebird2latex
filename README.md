# EbirdToLaTex Checklist Generator #
eBirdToLaTex Checklist Generator is a short Python script which generates a customisable bird checklist based on a specific dataset downloaded from [eBird](http://ebird.org/). There is also a web version of the generator available on my [my website](http://zoziologie.raphaelnussbaumer.com/ebirdtolatex/) with some explanation of the importance of checklist.

## How to use the python version ? ##
If you have python3 (python2 won't work with ```urllib```) and LaTeX, take the ```e2L.py``` module with the ```script_e2L.py``` and ```Template_default```. Internet connection is required to download updated bird taxonomy list, language traduction as well as location barchart data.  

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

## How to use the web-version ? ##
For the web version, just follow the instruction on [the website](http://zoziologie.raphaelnussbaumer.com/ebirdtolatex/), you won't need any special knowledge. Please let me know if you have any problem or beug! 

If you wish to dive into my code, I'm using Nodejs, python3 and javascript. Javascript get the input for the checklist and send a the info to Nodejs which run the python script on my server and return a link to the pdf generated. 

## GIF
![Exemple](https://raw.githubusercontent.com/Zoziologie/e2L/master/e2l.gif)

## Contact ##
Don't hesitate to contact me for any question ! And visit by webiste (if you have some spare time !)
[Raphael Nussbaumer](rafnuss@gmail.com) 
[zoziologie.raphaelnussbaumer.comm](http://zoziologie.raphaelnussbaumer.com/)
