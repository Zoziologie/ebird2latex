
class TableInput():
    def __init__(self,typ,option1=None,option2=None,option3=None):
        self.typ=typ
        self.title=None
        self.wid=None
        self.option1=option1
        self.option2=option2
        self.option3=option3
        if self.typ=='Language':
            self.wid='X'
            if self.option1 == 'EN':
                self.title='English'
            elif self.option1 == 'LA':
                self.title='Scientific'
            elif self.option1 == 'FR':
                self.title='Français'
        elif self.typ=='Freq':
            self.wid='c'
            if self.option1=='Year':
                self.title='Y'#ear'+'\\footnotesize{ (' +str(round(self.option3['SampleSize_year'])) +')} '
            elif self.option1 =='Season':
                season=['Sp','Sm','F','W']#['Spring','Summer','Fall','Winter']
                self.title=season[self.option2]# +'\\footnotesize{ (' +str(round(self.option3['SampleSize_season'][self.option2])) +')} '
            elif self.option1 == 'Month':
                month=['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'Jul', 'Aug', 'Sept.', 'Oct.', 'Nov.', 'Dec.']
                self.title=month[self.option2]+'\\footnotesize{ (' +str(round(self.option3['SampleSize_month'][self.option2])) +')} '
        elif self.typ=='Note':
            self.wid='X'
            self.title='Note'
        elif self.typ=='Tiret':
            self.wid='c'
            alphabet='A B C D E F G H'
            self.title='\\normalsize{'+self.get_content(None)+'}'
        elif self.typ=='Checkbox':
            self.wid='c'
            self.typ='Tiret' # put Tiret-like title
            self.title='\\normalsize{'+self.get_content(None)+'}'
            self.typ='Checkbox'
        
    def __str__(self):
        return str(self.title)
            
    def get_content(self,bird):
        if self.typ=='Language':
            if self.option1 == 'EN':
                return str(bird.Name_En)
            elif self.option1 == 'LA':
                return '\\textit{'+str(bird.Name_La)+'}'
            elif self.option1 == 'FR':
                if bird.Name_Fr:
                    return str(bird.Name_Fr)
                else:
                    return ''
        elif self.typ=='Freq':
            if self.option1=='Year':
                return  '\\databar{'+'{:.1f}'.format(bird.Freq_year*100) +'}'
            elif self.option1 =='Season':
                return '\\databar{'+'{:.1f}'.format(bird.Freq_season[self.option2]*100) +'}'
            elif self.option1 == 'Month':
                return '\\databar{'+'{:.1f}'.format(bird.Freq_month[self.option2]*100) +'}'
        elif self.typ=='Note':
            if not self.option1:
                self.option1='4cm'
            return '\\dotuline{\\hspace{'+self.option1+'}}'
        elif self.typ=='Tiret':
            if not self.option1:
                self.option1=3
            if not self.option2:
                self.option2='3ex'
            return self.option1*('\\underline{\\hspace{'+self.option2+'}}\\hspace{1ex}')
        elif self.typ=='Checkbox':
            if not self.option1:
                self.option1=3
            return self.option1*'$\\square$\\hspace{1ex} '
        
