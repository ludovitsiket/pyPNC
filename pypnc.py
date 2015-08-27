#!/usr/bin/python
# pyPNC, program na zalohovanie, branch ftps
import sys
import os
import zipfile
from time import gmtime, strftime
from ftplib import FTP_TLS 
import fnmatch
meno=[]
ps=[]
my_list=[]
souborek=""
def chyba():
    print "Nezadali ste vsetky potrebne parametre programu."
    print "Syntax: python pypnc.py cesta_k_zdroj_zlozke cesta_k_ciel_zlozke meno_suboru"
    print "cesta_k_zdroj_zlozke = cesta k zlozke ktora sa ma komprimovat \ncesta_k_ciel_zlozke = cesta k zlozke kam ma byt presunuty komprimovany subor \nmeno_suboru.zip = nazov pod ktorym sa komprimovany subor ulozi. Pripona .zip bude pridana automaticky.\n"

if len(sys.argv)<=3: #program vyzaduje 3 parametre
   chyba()
else:
    print "Cakajte prosim, program vytvara .zip subor. V zavislosti od velkosti to moze trvat niekolko minut." 
    odkial=sys.argv[1]
    kam=sys.argv[2]
    meno=sys.argv[3]
    source=odkial
    cas=strftime("_%Y-%m-%d_%H:%M:%S", gmtime())
    subor=meno+cas+".zip" #vysledne meno suboru
    zip=zipfile.ZipFile(subor, 'w',zipfile.ZIP_DEFLATED,"allowZip64=True") # nezipuje velke subory (treba zip64 extension)!
    rootlen=len(source)+1
    for base,dirs,files in os.walk(source):
        for file in files:
            fn=os.path.join(base,file)
            souborek=zip.write(fn,fn[rootlen:]) #souborek je hotovy zazipovany subor
            suborik=str(souborek) #string premennej souborek
    print "[OK]\nSubor sa nachadza v urcenom adresary",kam
    with open('/home/peter/pwd','r') as infile:
        data=infile.read()
    my_list=data.splitlines()
    meno2=my_list[0]
    ps=my_list[1]
    path=my_list[2]
    server=my_list[3]
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,"*.iso"):
            fajl=str(file) #tymto tu si do fajl ulozim meno hotoveho suboru na odoslanie; pouzita kniznica fnmatch
    ftp=FTP_TLS(server,meno2,ps)   #pripojenie k serveru atd. 
    ftp.prot_p()
    ftp.cwd(my_list[2]) #prepnutie do prislusneho adresara ftps serveru
    ftp.retrlines("LIST")
    print "Posielam subor. Cakajte..."
    ftp.storbinary('STOR '+fajl, open(fajl, 'rb'))
    ftp.close()
    print "[OK]\n"
    print "Spojenie ukoncene.\n"
