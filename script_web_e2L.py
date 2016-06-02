#!/usr/bin/env python

import e2L
import sys
import urllib.parse

urld = dict(urllib.parse.parse_qs(urllib.parse.unquote(sys.argv[1])))

print(urld)
#print(urld)
#projet_name = "Sweden"
#print('Start Project: '+ projet_name)

sys.exit()

#1. Create the Bird List loading data from eBird
code_loc = 'SE' # See possible country code here : https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-HotSpotsByRegion + region code for each region ? where ?
lang = ['EN_UK','FR'] # a single language, or list of several language en,en_US,de,en_AE,en_AU,en_IN,en_NZ,en_UK,en_ZA,es,es_AR,es_CL,es_CU, es_DO,es_ES,es_MX,es_PA,es_PR,fi,fr,fr_HT,ht_HT,in,is,pt_BR,pt_PT,tr,zh http://help.ebird.org/customer/portal/articles/1596582-common-name-translations-in-ebird
cat = 'species' # domestic,form,hybrid,intergrade,issf,slash,species,spuh
byear = 1900
eyear = 2015
bmonth = 9
emonth = 10
info, bird_list = e2L.bird_creator(code_loc, lang, cat, byear, eyear, bmonth, emonth)



#2. Define column et Condition
# col.append(TableInput(type,option1,option1,option2,option3))
# type     option1                 option 2
# checkbox   number of checkbox
# tiret     number of tiret             length (eg: '8ex')
# language   language code only those computed in the birdlist. 'EN' and 'LA' is always available
# freq     'Year', 'Season', 'month', 'week'    index (1:4 season, 1:12 month 1:... week)
# note     leength (eg. : 4cm)
print('define column and condition')
col = []
col.append(e2L.TableInput('checkbox',1))
#col.append(TableInput('Tiret',5,'8ex')) # number of tiret , length
col.append(e2L.TableInput('language','EN_UK'))
col.append(e2L.TableInput('language','FR'))
col.append(e2L.TableInput('language','LA'))
#col.append(e2L.TableInput('Freq','Year',0,info))
col.append(e2L.TableInput('freq','season',4,info))
#col.append(e2L.TableInput('Freq','Season',1,info))
#col.append(e2L.TableInput('Freq','Season',2,info))
#col.append(e2L.TableInput('Freq','Season',3,info))
col.append(e2L.TableInput('freq','month',10,info))
#col.append(e2L.TableInput('Note','4cm')) # lenght of note


condition_tableau = ['Main table display only non-hybrid birds with occurence >1\\%.'," ( bird['freq']['year'] >= 0.01)"]
condition_rare = ['\\footnotesize{>.1\\%}'," (bird['freq']['year'] < .01) and (bird['freq']['year'] > 0.001)"]


## Write To LateX
#print('Write to latex')
e2L.write_to_latex(projet_name,bird_list,col,condition_tableau,condition_rare, info)

#os.chdir('Latex'); os.system(projet_name+'.tex');os.chdir('..')


## Run Latex
#print('Run pdflatex and open')
#os.chdir('Latex')
#os.system('"pdflatex '+ Projet_name + '.tex"')
#os.system('"start '+ Projet_name + '.pdf"')
#os.chdir('..')

