#!/usr/bin/env python
import os
import sys
import urllib.parse
import subprocess

# debug
#import importlib
#spec = importlib.util.spec_from_file_location("module.name", "./e2L.py")
#e2L = importlib.util.module_from_spec(spec)
#spec.loader.exec_module(e2L)

import e2L
import importlib
importlib.reload(e2L)

# create project metadata
projet_name = "Puerto Rico"
filename = projet_name.replace(' ','_').replace("'",'').replace('.','')

# 1. Authentify
# Sesssion is required to download barchart data
session = e2L.auth('rafnuss','12468935')

#1. Create the Bird List loading data from eBird
code_loc = 'PR' # See possible country code here : https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-HotSpotsByRegion + region code for each region ? where ?
lang = ['EN'] # a single language, or list of several language en,en_US,de,en_AE,en_AU,en_IN,en_NZ,en_UK,en_ZA,es,es_AR,es_CL,es_CU, es_DO,es_ES,es_MX,es_PA,es_PR,fi,fr,fr_HT,ht_HT,in,is,pt_BR,pt_PT,tr,zh https://support.ebird.org/en/support/solutions/articles/48000804865-bird-names-in-ebird
cat = ['species'] # domestic,form,hybrid,intergrade,issf,slash,species,spuh
byear = 1900
eyear = 2050
bmonth = 1
emonth = 12
info, bird_list = e2L.bird_creator(session, code_loc, lang, cat, byear, eyear, bmonth, emonth)

#3. Add Status
# status can be any of the following: target (year/life - per region/world), endemic, introduced
target_loc = "world" # or any codeLoc
target_time = "life" # "year" "life" 
# bird_list = e2L.statusInTarget(session,bird_list,code_loc,target_loc,target_time,bmonth,emonth)
bird_list = e2L.statusInList('target-world',bird_list,session,target_loc,target_time)
target_loc = code_loc
bird_list = e2L.statusInList('target-PR',bird_list,session,target_loc,target_time)

# 4. Add endemic & Introduced
bird_list = e2L.statusAvibase(['endemic-PR','introduce-PR'],bird_list, code_loc)

#2. Define column et Condition
# col.append(TableInput(type,option1,option1,option2,option3))
# type     option1                 option 2
# checkbox   number of checkbox
# tiret     number of tiret             length (eg: '8ex')
# lang   language code only those computed in the birdlist. 'EN' and 'LA' is always available
# freq     'Year', 'Season', 'month', 'week'    index (1:4 season, 1:12 month 1:... week)
# note     leength (eg. : 4cm)
col = []
col.append(e2L.TableInput(info,'checkbox',1))
#col.append(TableInput(info,'Tiret',5,'8ex')) # number of tiret , length
statusTable = [['endemic-PR','bold'], ['introduce-PR','color-violet'],['target-world','sym-*']]
# bold, italic, underline, color-... (see), sym-*
col.append(e2L.TableInput(info,'lang','EN',statusTable))
# col.append(e2L.TableInput(info,'lang','LA'))
#col.append(e2L.TableInput(info,'freq','year',0))
#col.append(e2L.TableInput(info,'freq','season',0))
col.append(e2L.TableInput(info,'freq','month',0))
#col.append(e2L.TableInput(info,'Note','4cm')) # lenght of note

format='letterpaper,margin=.3in,twocolumn' #'a4paper,margin=15mm,twocolumn'
family = False
spacing = '.95'
condition_tableau = ['Main table display only non-hybrid birds with occurence >0.1\\%.'," ( bird['freq']['year'] >= 0.001)"]
# condition_rare = ['\\footnotesize{>.1\\%}'," (bird['freq']['year'] < .01) and (bird['freq']['year'] > 0.001)"]
condition_rare = ['\\footnotesize{>.1\\%}'," (bird['freq']['year'] < .00) and (bird['freq']['year'] > 0.001)"]


## Write To LateX
#print('Write to latex')
e2L.write_to_latex(projet_name,filename,bird_list,col,condition_tableau, condition_rare, family, format, spacing, info)
#os.chdir('latex'); os.system(projet_name+'.tex');os.chdir('..')


## Run Latex
#print('Run pdflatex and open')
os.system('pdflatex -output-directory=./latex/ ./latex/'+ filename + '.tex ')
# os.system('pdflatex -output-directory=./latex/ ./latex/'+ filename + '.tex > /dev/null 2>&1')
# os.system('"start '+ filename + '.pdf"')
#os.chdir('..')
