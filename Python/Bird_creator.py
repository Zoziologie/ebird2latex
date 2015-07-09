def Read_BarChart_file(filename):
    f = open(filename, 'r')
    Birdlist=[]
    info=dict()
    u=0
    for line in f:
        if line=='\n' or line=="\r\n":
            pass
        elif "Frequency of observations in the selected location(s).:"  in line:
            # print(line)
            # Don't know that it's is ???
            pass
        elif "Number of taxa" in line:
            # Line with the number of taxa in the list
            info['NbTaxa']=int(line.replace("Number of taxa: ",""))
        elif "Jan				Feb" in line:
            pass
        elif "Sample Size" in line:
            info['SampleSize']=[int(float(i)) for i in line.replace("Sample Size:","").split()]
            info['SampleSize_month'], info['SampleSize_season'], info['SampleSize_year'] = WeekToElse(info['SampleSize'])
        elif " sp. " in line:
            pass
        else:
            #line=line.replace('<em class="sci">','')
            #line=line.replace('</em>','')
            BirdNameEN,line=line.split(' (<em class="sci">',1)
            BirdNameLA,line=line.split('</em>)',1)
            BirdFreq=[float(i) for i in line.split()]
            assert len(BirdFreq)==48,"Number of bird frequency is not equal to 48" 
            Birdlist.append(Bird(BirdNameEN,BirdNameLA,BirdFreq))
        u +=1
        if u==10000:
            return Birdlist
            break
    f.close()
    return (Birdlist, info)

class Bird():
    def __init__(self,Name_EN,Name_LA,Freq):
        self.Name_En=Name_EN
        self.Name_La=Name_LA
        self.Name_Fr=None
        self.Freq_week=Freq
        self.Freq_month, self.Freq_season, self.Freq_year = WeekToElse(self.Freq_week)
        self.taxon=None
        self.family=None
        
    def __str__(self):
        string="Name: " + self.Name_En + "\t" + self.Name_La
        if self.Name_Fr:
            string += "\t" + self.Name_Fr
        string += "\t" + str(self.Freq_year)
        string += "\t" + str(self.taxon)
        string += "\t" + self.family
        return string
    
    def __comp__(self,other):
        if self.taxon < other.taxon : return -1
        elif self.taxon > other.taxon : return 1
        else: return 0
    def __lt__(self, other):
        return self.taxon < other.taxon
    def __gt__(self, other):
        return self.taxon > other.taxon
    def __eq__(self, other):
            return self.taxon == other.taxon
    def __le__(self, other):
         return self.taxon <= other.taxon
    def __ge__(self, other):
        return self.taxon >= other.taxon
    def __ne__(self, other):
        return self.taxon != other.taxon
        
        
    def addLang(self,lang,name):
        if name:
            name=name[0][0]
        if lang=='French' or lang=='French_modif':
            self.Name_Fr = name
        elif lang=="Scientific_name" or lang=="Scientific_name_modif":
            self.Name_La = name
        
    def addinfo(self, taxon, family):
        if taxon:
            taxon=taxon[0][0]
        if family:
            family=family[0][0]
        self.taxon=float(taxon.replace(',','.'))
        self.family=family

def WeekToElse(week):
    t_m = []
    month=[]
    for i in range(0,len(week)):
        t_m.append(week[i])
        if i%4==3:
            month.append(sum(b for b in t_m) / len(t_m))
            t_m=[]
    assert len(month)==12,'Month Frequency is not equal to 12'
    #Season
    season=[]
    season.append(sum(b for b in month[2:5]) / 3)
    season.append(sum(b for b in month[5:8]) / 3)
    season.append(sum(b for b in month[8:11]) / 3)
    season.append(sum(b for b in month[0:2]+ [month[11]]) / 3)
    #Year
    year = sum(b for b in week) / len(week)
    return (month,season,year)

def AddLanguage(Birdlist,filename,lang):
    import csv
    import sqlite3

    db = sqlite3.connect(':memory:')

    def init_db(cur):
        cur.execute('''CREATE TABLE Multilangue (
            Scientific_name TEXT,
            Scientific_name_modif TEXT,
            English TEXT,
            Chinese TEXT,
            Chinese_Traditional TEXT,
            Czech TEXT,
            Danish TEXT,
            Dutch TEXT,
            Estonian TEXT,
            Finnish TEXT,
            French TEXT,
            French_modif TEXT,
            German TEXT,
            Hungarian TEXT,
            Italian TEXT,
            Japanese TEXT,
            Lithuanian TEXT,
            Norwegian TEXT,
            Polish TEXT,
            Portuguese TEXT,
            Russian TEXT,
            Slovak TEXT,
            Spanish TEXT,
            Swedish TEXT)''')

    def populate_db(cur, csv_fp):
        rdr = csv.reader(csv_fp)
        cur.executemany('''
            INSERT INTO Multilangue (Scientific_name,Scientific_name_modif,English,Chinese,Chinese_Traditional,Czech,Danish,Dutch,Estonian,Finnish,French,French_modif,German,Hungarian,Italian,Japanese,Lithuanian,Norwegian,Polish,Portuguese,Russian,Slovak,Spanish,Swedish)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', rdr)

    cur = db.cursor()
    init_db(cur)
    populate_db(cur, open(filename))
    db.commit()

    for bird in Birdlist:
        t=tuple([bird.Name_La],)
        cur.execute('SELECT '+lang+' FROM Multilangue WHERE Scientific_name=?', t)
        bird.addLang(lang,cur.fetchall())

    db.close()

def AddInfo(Birdlist,filename):
    import csv
    import sqlite3

    db = sqlite3.connect(':memory:')

    def init_db(cur):
        cur.execute('''CREATE TABLE Taxonomy (
           TAXON_ORDER TEXT,
           CATEGORY TEXT,
           SPECIES_CODE TEXT,
           SCI_NAME TEXT,
           PRIMARY_COM_NAME TEXT,
           ORDER1 TEXT,
           FAMILY TEXT,
           SPECIES_GROUP TEXT,
           REPORT_AS TEXT)''')

    def populate_db(cur, csv_fp):
        rdr = csv.reader(csv_fp)
        cur.executemany('''
            INSERT INTO Taxonomy (TAXON_ORDER,CATEGORY,SPECIES_CODE,SCI_NAME,PRIMARY_COM_NAME,ORDER1,FAMILY,SPECIES_GROUP,REPORT_AS)
            VALUES (?,?,?,?,?,?,?,?,?)''', rdr)

    cur = db.cursor()
    init_db(cur)
    populate_db(cur, open(filename))
    db.commit()


    for bird in Birdlist:
        t=tuple([bird.Name_La],)
        cur.execute('SELECT TAXON_ORDER FROM Taxonomy WHERE SCI_NAME=?', t)
        taxon=cur.fetchall()
        cur.execute('SELECT FAMILY FROM Taxonomy WHERE SCI_NAME=?', t)
        family=cur.fetchall()
        bird.addinfo(taxon, family)

    db.close()


