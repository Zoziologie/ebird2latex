#!/usr/bin/env python
import os
import e2L
import sys
import urllib.parse
import unidecode


projet_name = "Sweden"
print('Start Project: '+ projet_name)
filename = unidecode.unidecode(projet_name).replace(' ','_').replace("'",'').replace('.','')

#1. Create the Bird List loading data from eBird
code_loc = 'SE' # See possible country code here : https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-HotSpotsByRegion + region code for each region ? where ?
lang = ['en_UK','FR'] # a single language, or list of several language en,en_US,de,en_AE,en_AU,en_IN,en_NZ,en_UK,en_ZA,es,es_AR,es_CL,es_CU, es_DO,es_ES,es_MX,es_PA,es_PR,fi,fr,fr_HT,ht_HT,in,is,pt_BR,pt_PT,tr,zh http://help.ebird.org/customer/portal/articles/1596582-common-name-translations-in-ebird
cat = ['species'] # domestic,form,hybrid,intergrade,issf,slash,species,spuh
byear = 1900
eyear = 2015
bmonth = 9
emonth = 10
info, bird_list = e2L.bird_creator(code_loc, lang, cat, byear, eyear, bmonth, emonth)
format='a4paper,margin=.3in'
family = 'true'


#2. Define column et Condition
# col.append(TableInput(type,option1,option1,option2,option3))
# type     option1                 option 2
# checkbox   number of checkbox
# tiret     number of tiret             length (eg: '8ex')
# lang   language code only those computed in the birdlist. 'EN' and 'LA' is always available
# freq     'Year', 'Season', 'month', 'week'    index (1:4 season, 1:12 month 1:... week)
# note     leength (eg. : 4cm)
print('define column and condition')
col = []
col.append(e2L.TableInput(info,'checkbox',1))
#col.append(TableInput(info,'Tiret',5,'8ex')) # number of tiret , length
col.append(e2L.TableInput(info,'lang','EN','0'))
#col.append(e2L.TableInput(info,'language','FR'))
#col.append(e2L.TableInput(info,'language','LA'))
#col.append(e2L.TableInput(info,'Freq','Year',0))
#col.append(e2L.TableInput(info,'freq','season',4,))
#col.append(e2L.TableInput(info,'Freq','Season',1))
#col.append(e2L.TableInput(info,'Freq','Season',2))
#col.append(e2L.TableInput(info,'Freq','Season',3))
#col.append(e2L.TableInput(info,'freq','month',10))
#col.append(e2L.TableInput(info,'Note','4cm')) # lenght of note


condition_tableau = ['Main table display only non-hybrid birds with occurence >1\\%.'," ( bird['freq']['year'] >= 0.01)"]
condition_rare = ['\\footnotesize{>.1\\%}'," (bird['freq']['year'] < .01) and (bird['freq']['year'] > 0.001)"]


## Write To LateX
#print('Write to latex')
e2L.write_to_latex(projet_name,filename,bird_list,col,condition_tableau, condition_rare, family, format, spacing, info)
#os.chdir('Latex'); os.system(projet_name+'.tex');os.chdir('..')


## Run Latex
#print('Run pdflatex and open')
#os.chdir('Latex')
#os.system('"pdflatex '+ Projet_name + '.tex"')
#os.system('"start '+ Projet_name + '.pdf"')
#os.chdir('..')
