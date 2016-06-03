#!/usr/bin/env python
import os
import e2L
import sys
import urllib.parse

urld = dict(urllib.parse.parse_qs(urllib.parse.unquote(sys.argv[1])))
print(urld)

# Adapt the dict structure:
keycol = sorted([item for item in urld.keys() if item.startswith('col')])
urld['col']=[]
for idx,val in enumerate(keycol):
    urld['col'].append(urld[val])	
    del urld[val]

#print(urld)
projet_name = urld['project_name'][0]
print('Start Project: '+ projet_name)


#1. Create the Bird List loading data from eBird
code_loc = urld['code_loc'][0] # See possible country code here : https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-HotSpotsByRegion + region code for each region ? where ?
lang = [col[1] for col in urld['col'] if col[0]=='lang'] # a single language, or list of several language en,en_US,de,en_AE,en_AU,en_IN,en_NZ,en_UK,en_ZA,es,es_AR,es_CL,es_CU, es_DO,es_ES,es_MX,es_PA,es_PR,fi,fr,fr_HT,ht_HT,in,is,pt_BR,pt_PT,tr,zh http://help.ebird.org/customer/portal/articles/1596582-common-name-translations-in-ebird
cat = urld['cat[]'] # I DONT KNOW WHERE [] IS COMING FROM...# domestic,form,hybrid,intergrade,issf,slash,species,spuh
byear = int(urld['byear'][0])
eyear = int(urld['eyear'][0])
bmonth = int(urld['bmonth'][0])
emonth = int(urld['emonth'][0])
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

for i in urld['col']:
        col.append(e2L.TableInput(i[0],i[1],i[2],info))

condition_tableau = ['Main table display only non-hybrid birds with occurence >1\\%.'," ( bird['freq']['year'] >= 0.01)"]
condition_rare = ['\\footnotesize{>.1\\%}'," (bird['freq']['year'] < .01) and (bird['freq']['year'] > 0.001)"]


## Write To LateX
print('Write to latex')
e2L.write_to_latex(projet_name,bird_list,col,condition_tableau,condition_rare, info)
# os.system('cp temp.tex  ./latex/'+ projet_name + '.tex' )


## Run Latex
print('Run pdflatex and open')
os.chdir('latex')
os.system('pdflatex '+ projet_name + '.tex')
#os.system('"start '+ projet_name + '.pdf"')
os.chdir('..')

print('http://zoziologie.raphaelnussbaumer.com/wp-content/plugins/e2L/latex/'+ projet_name + '.pdf')


