#!/usr/bin/env python
import os
import e2L
import sys
import urllib.parse
import unidecode

print(sys.argv[1])

print('1. Read the url, transform it to dict and adapt it for our purpuse')
urld = dict(urllib.parse.parse_qs(urllib.parse.unquote(sys.argv[1])))
print(urld)

# Adapt the dict structure:
for idx,val in enumerate(urld['col']):
    urld['col'][idx] = val.split(',')

projet_name = urld['project_name'][0]
filename = unidecode.unidecode(projet_name).replace(' ','_').replace("'",'').replace('.','')

code_loc = urld['code_loc'][0] # See possible country code here : https://confluence.cornell.edu/display/CLOISAPI/eBird-1.1-HotSpotsByRegion + region code for each region ? where ?
lang = [col[1] for col in urld['col'] if col[0]=='lang'] # a single language, or list of several language en,en_US,de,en_AE,en_AU,en_IN,en_NZ,en_UK,en_ZA,es,es_AR,es_CL,es_CU, es_DO,es_ES,es_MX,es_PA,es_PR,fi,fr,fr_HT,ht_HT,in,is,pt_BR,pt_PT,tr,zh http://help.ebird.org/customer/portal/articles/1596582-common-name-translations-in-ebird
cat = urld['cat'] # domestic,form,hybrid,intergrade,issf,slash,species,spuh
byear = int(urld['byear'][0])
eyear = int(urld['eyear'][0])
bmonth = int(urld['bmonth'][0])
emonth = int(urld['emonth'][0])
cond_rare = urld['condition'][0]
cond_tableau = urld['condition'][1]
format = urld['format'][0]
family = urld['family'][0]

print('2. Create the Bird List from eBird.org')
info, bird_list = e2L.bird_creator(code_loc, lang, cat, byear, eyear, bmonth, emonth)


print('3. Define column and condition')
# col.append(TableInput(type,option1,option1,option2,option3))
# type     option1                 option 2
# checkbox   number of checkbox
# tiret     number of tiret             length (eg: '8ex')
# language   language code only those computed in the birdlist. 'EN' and 'LA' is always available
# freq     'Year', 'Season', 'month', 'week'    index (1:4 season, 1:12 month 1:... week)
# note     leength (eg. : 4cm)
col = []
print(info['samples_size'])
for urld_col in urld['col']:
    col.append(e2L.TableInput(info,urld_col[0],urld_col[1],urld_col[2]))


condition_tableau = ['Main table display only non-hybrid birds with occurence >1\\%.'," ( bird['freq']['year'] >= "+cond_rare+")"]
condition_rare = ['\\footnotesize{<.1\\%}'," (bird['freq']['year'] < "+cond_rare+") and (bird['freq']['year'] > "+cond_tableau+")"]
print(condition_tableau)
print(condition_rare)

## Write To LateX
print('4. Write to latex')
e2L.write_to_latex(projet_name,filename,bird_list,col,condition_tableau, condition_rare, family, format, info)
# os.system('cp temp.tex  ./latex/'+ projet_name + '.tex' )


## Run Latex
print('5. Run Pdflatex and Open')
os.chdir('latex')
os.system('pdflatex '+ filename + '.tex')
#os.system('"start '+ projet_name + '.pdf"')
os.chdir('..')

urlf = 'http://zoziologie.raphaelnussbaumer.com/wp-content/plugins/e2L/latex/'+ filename + '.pdf'
print('<a href="'+urlf+'">'+urlf+'</a>')
print(urlf)

