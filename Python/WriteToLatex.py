from TableInput import *
def WriteToLatex(projname,Birdlist,filename,Col,condition_tableau,condition_rare, info):
    family_current=''

    # Start Writing
    f = open(filename, 'w')
    
    # Import preformatted text
    f2 = open('Latex/Template_default.tex', 'r')
    for line in f2:
        if 'newcommand{\maxnum}' in line:
            line = line[:-1]+'100.00}\n'
        if 'newcommand{\SampleSize}' in line:
            line = line[:-1]+ str(round(info['SampleSize_year']))+' checklists ('+str(info['NbTaxa'])+' differents species)} '
        elif '_condition_' in line:
            line= condition_tableau[0]+'\n'
        elif '_projectname_' in line:
            line = '\\LARGE{'+projname+' Bird Checklist}\\\\'
        elif '_noteline_' in line:
            line=3*'\\newnoteline'
        elif 'begin{tabularx' in line:
            line=line[:-1]
            for col in Col: # write column width
                line += col.wid
            line+='}'
        elif '_columntitle_' in line:
            line=''
            for col in Col[:-1]: # write title
                line +='\\textsc{ \\large{'+col.title+'}} \t & '
            line +='\\textsc{ \\large{ '+Col[-1].title+'}}\\\\'
        elif '_content_' in line:
            line=''
            for bird in Birdlist: #write Content
                if eval(condition_tableau[1]): # condition to display or not a bird
                    if bird.family != family_current: # family name
                        f.write('\n\\\\\n\\multicolumn{'+str(len(Col))+'}{c}{\\textbf{'+bird.family+'}} \\\\ \n')
                        f.write('\\hline\n')
                        family_current=bird.family

                    for col in Col[:-1]:
                        f.write(col.get_content(bird) + ' \t & ') # Content of the cell
                    f.write(Col[-1].get_content(bird)+' \\\\') # end of line
        elif '_rare_' in line:
            line=''
            # Table Rare
            n_rare_col=3
            Col_r = TableInput('Language','EN')
            Birdlist_r=[]
            for bird in Birdlist:
                if eval(condition_rare[1]):
                    Birdlist_r.append(Col_r.get_content(bird))
                   
            u=len(Birdlist_r)
            
            if u != 0: # check if there are rare bird
                while u-n_rare_col*round(u/n_rare_col)!=0:
                    Birdlist_r.append('\\underline{\\hfill}')
                    u=len(Birdlist_r)
                c=round(u/n_rare_col)
                f.write('\\begin{tabularx}{\\textwidth}{')
                for x in range(0,n_rare_col):
                    f.write('cX')
                f.write('} \n')
                f.write('\\hline\n\\\\\n')
                f.write('\\multicolumn{'+str(2*n_rare_col)+'}{c}{\\textsc{ \\Large{Rare'+condition_rare[0]+'}}} \\\\ \n')
                f.write('\\\\\n\\hline\n')
                for cc in range(0,c):
                    for c_r in range(0,n_rare_col-1):
                        f.write('\\underline{\\hspace{3ex}} \t &' + Birdlist_r[cc+c*c_r] +' \t &')
                    f.write('\\underline{\\hspace{3ex}} \t &' + Birdlist_r[cc+c*(n_rare_col-1)]+' \\\\ \n')
                f.write('\\hline\n')
                f.write('\\end{tabularx} ')
        
        f.write(line)
    f2.close()
