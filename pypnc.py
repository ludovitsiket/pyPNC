#!/usr/bin/python
# pyPNC, program na zalohovanie, branch ftps
import sys
import os
import zipfile
from time import gmtime, strftime
from ftplib import FTP_TLS 
meno=[]
ps=[]
my_list=[]
def chyba():
    print "Nezadal si vsetky potrebne parametre programu."
    print "Syntax: python pypnc.py cesta_k_zdroj_zlozke cesta_k_ciel_zlozke meno_suboru"
    print "cesta_k_zdroj_zlozke = cesta k zlozke ktora sa ma komprimovat \ncesta_k_ciel_zlozke = cesta k zlozke kam ma byt presunuty komprimovany subor \nmeno_suboru.zip = nazov pod ktorym sa komprimovany subor ulozi. Pripona .zip bude pridana automaticky.\n"

def chyba2(): #este do programu zakomponovat
    print "Programu naozaj stacia 3 parametre...\n"
print "Cakajte prosim, program robi co moze. Naozaj sa snazi."

odkial=sys.argv[1]
kam=sys.argv[2]
meno=sys.argv[3]
source=odkial
cas=strftime("_%Y-%m-%d_%H:%M:%S", gmtime())
subor=meno+cas+".zip"
zip=zipfile.ZipFile(subor, 'w',zipfile.ZIP_DEFLATED) # nezipuje velke subory (treba zip64 extension)!
rootlen=len(source)+1
for base,dirs,files in os.walk(source):
    for file in files:
        fn=os.path.join(base,file)
        zip.write(fn,fn[rootlen:])
print "[OK]\nSubor sa nachadza v urcenom adresary",kam
if len(sys.argv)<=3: #program vyzaduje 3 parametre
   chyba()
else:
    with open('/home/peter/pwd','r') as infile:
        data=infile.read()
    my_list=data.splitlines()
    meno=my_list[0]
    ps=my_list[1]
    ftp=FTP_TLS("localhost",meno,ps) 
    ftp.prot_p()
    ftp.retrlines("LIST")
    ftp.storbinary("STORE"+subor, open(file, 'rb'))
#    ftp.storlines('STOR'+subor, open(subor, 'rb'))
    ftp.close()
