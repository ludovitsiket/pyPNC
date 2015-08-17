#!/usr/bin/python
# pyPNC, program na zalohovanie
import sys
import os
import zipfile
def chyba():
    print "Nezadal si vsetky potrebne parametre programu."
    print "Syntax: python pypnc.py cesta_k_zdroj_zlozke cesta_k_ciel_zlozke meno_suboru"
    print "cesta_k_zdroj_zlozke = cesta k zlozke ktora sa ma komprimovat \ncesta_k_ciel_zlozke = cesta k zlozke kam ma byt presunuty komprimovany subor \nmeno_suboru = nazov pod ktorym sa komprimovany subor ulozi \n"

def prg ():
    odkial=sys.argv[1]
    kam=sys.argv[2]
    meno=sys.argv[3]
    print "odkial ",odkial
    print "kam ",kam
    print "meno suboru ",meno
    source=odkial
    zip=zipfile.ZipFile(kam+meno, 'w',zipfile.ZIP_DEFLATED)
    rootlen=len(source)+1
    for base,dirs,files in os.walk(source):
        for file in files:
            fn=os.path.join(base,file)
            zip.write(fn,fn[rootlen:])

if len(sys.argv)<=3: #program vyzaduje 3 parametre
    chyba()
else: prg()
#print sys.argv[1] #prvy parameter po nazve programu
