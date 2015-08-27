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
file_to_zip=""
def chyba():
    print "Nezadali ste vsetky potrebne parametre programu."
    print "Syntax: python pypnc.py cesta_k_zdroj_zlozke cesta_k_ciel_zlozke meno_suboru timestamp (time pre ulozenie casu do mena suboru, no pre vynechanie timestampu)"
    print "cesta_k_zdroj_zlozke = cesta k zlozke ktora sa ma komprimovat \ncesta_k_ciel_zlozke = cesta k zlozke kam ma byt presunuty komprimovany subor \nmeno_suboru.zip = nazov pod ktorym sa komprimovany subor ulozi. Pripona .zip bude pridana automaticky.\n"

if len(sys.argv)<=3: #program vyzaduje 3 parametre
   chyba()
else:
    print "Cakajte prosim, program vytvara .zip subor. V zavislosti od velkosti to moze trvat niekolko minut." 
    odkial=sys.argv[1]
    kam=sys.argv[2]
    meno=sys.argv[3]
    timestamp=sys.argv[4]
    if timestamp == "time":
        cas=strftime("_%Y-%m-%d_%H:%M:%S", gmtime()) 
    elif timestamp =="no" : cas=""
    else: None
    source=odkial
    subor=meno+cas+".zip" 
    zip=zipfile.ZipFile(subor, 'w',zipfile.ZIP_DEFLATED,"allowZip64=True") 
    rootlen=len(source)+1
    for base,dirs,files in os.walk(source):
        for file in files:
            fn=os.path.join(base,file)
            file_to_zip=zip.write(fn,fn[rootlen:]) #file_to_zip je hotovy zazipovany subor
            suborik=str(file_to_zip) #string premennej file_to_zip
    print "[OK]\nSubor sa nachadza v urcenom adresary",kam
    with open('/home/peter/pwd','r') as infile:
        data=infile.read()
    my_list=data.splitlines()
    meno2=my_list[0]
    ps=my_list[1]
    path=my_list[2]
    server=my_list[3]
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,"*.zip"):
            file_to_send=str(file) 
    velkost_local=os.path.getsize(file_to_send)
    ftp=FTP_TLS(server,meno2,ps)   
    ftp.prot_p()
    ftp.cwd(my_list[2]) 
    ftp.retrlines("LIST")
    print "Posielam subor. Cakajte prosim."
    ftp.storbinary('STOR '+file_to_send, open(file_to_send, 'rb'),)
    print "[OK]"
    size_ftp=ftp.nlst()
    velkost_ftp_subor=size_ftp[0] #berie len prvy subor zo zoznamu
    ftp.sendcmd("TYPE i")
    velkost_ftp=ftp.size(velkost_ftp_subor)
    ftp.close()
    if velkost_local==velkost_ftp:
       print "Meno a velkost preneseneho suboru sa zhoduju."
    else: print "Velkosti suborov sa lisia, pravdepodobne doslo k chybe."
    print "Spojenie ukoncene."
