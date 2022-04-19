# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:17:50 2017

@author: RO-AUROCH
"""

import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import yaml
import getopt
from os import chdir
from glob import glob
import sys

class correo:
        def __init__(self,yamlfile):
                print("Correo")
                print(yamlfile)
                with open (yamlfile, 'r')as file:
                        self.variables=yaml.full_load(file)
                src=self.variables["src"]
                if (src is not None):
                        chdir(src)    
                        self.adjuntos = [file for file in glob('*.{}'.format(ext))]
                        #self.adjuntos = [file for file in glob('*.*')]
                else:
                        self.adjuntos=None
                        self.src=''
                        self.ext=''
                return
        
        def get_variables(self):
               print("Get variables")
               print("FUENTE: "+self.src)
               print("EXTECION: "+self.ext)
               print("IP: "+self.variables["ip"])
               print("MENSAJE: "+self.variables["mensaje"])
               print("ADJUNTOS: "+str(self.adjuntos))
               print("TITULO: "+ self.variables["titulo"])
               print("ORIGEN: "+self.variables["origen"])
               print("DESTINO: "+ str(self.variables["destino"]))
                        

        def enviar_correo(self):
                #mensaje=self.get_cuerpo_correo()
                #print(ip)
                ip=self.variables["ip"]
                mensaje=self.variables["mensaje"]
                adjuntos=self.adjuntos
                titulo=self.variables["titulo"]
                origen=self.variables["origen"]
                destino=self.variables["destino"]
                
                COMMASPACE = ', '
                msg = MIMEMultipart()
                msg['Subject'] =titulo #self.variables["titulo"]
                msg['From'] =origen #self.variables["origen"]
                msg['To'] = COMMASPACE.join(destino)
        
                fp=open(mensaje)
                msg.attach(MIMEText(fp.read()))
                fp.close()
                #print(msg)  
                s = smtplib.SMTP(ip)
                #adjuntos=self.variables["adjuntos"]
                if (adjuntos is not None):
                        for f in adjuntos or []:
                                with open(f, "rb") as fill:
                                        part=MIMEApplication(fill.read(), Name=basename(f))
                                        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                                        msg.attach(part)
                else:
                        pass
                s.sendmail(origen, destino, msg.as_string())
                s.quit()
                return
def get_ops():
    try:
        opt,args=getopt.getopt(sys.argv[1:], 'x', ['yaml='])
    except getopt.GetoptError as err:
        print(err)
    u_args=[]
    yaml_=None
    for o, a in opt:
        if o=="--yaml":
            yaml_=a  
        else:
            print("Opción no reconocida")
    u_args.append(yaml_)
    return u_args

if __name__== '__main__':
        ops=get_ops()
        yaml_=ops[0]
        correo_=correo(yaml_)        
        correo_.get_variables()
        correo_.enviar_correo()
        
        
        #path_='correo_conf.yaml'
        #correo_=correo(path_)
        #correo_.get_variables()
        #correo_.enviar_correo()
        
