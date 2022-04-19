# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:17:50 2017

@author: czalapa
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
        def __init__(self,yamlfile, src,ext):
                print("Correo")
                print(yamlfile)
                with open (yamlfile, 'r')as file:
                        self.variables=yaml.full_load(file)
                chdir(src)    
                self.adjuntos = [file for file in glob('*.{}'.format(ext))]
                #self.adjuntos = [file for file in glob('*.*')]                        
                return
        
        def get_variables(self):
               print("Get variables")
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
                s = smtplib.SMTP()
                s.connect(ip, '587')
                s.starttls()
                s.login('KEY', 'KEY')
                #adjuntos=self.variables["adjuntos"]

                """
                for f in adjuntos or []:
                        with open(f, "rb") as fill:
                                part=MIMEApplication(fill.read(), Name=basename(f))
                                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                                msg.attach(part)
                    
                        s.sendmail(origen, destino, msg.as_string())
                        s.quit()
                """

                s.sendmail(origen, destino, msg.as_string())
                s.quit()
                return
def get_ops():
    try:
        opt,args=getopt.getopt(sys.argv[1:], 'x', ['yaml=','src=', 'ext='])
    except getopt.GetoptError as err:
        print(err)
    u_args=[]
    yaml_=None
    src=None
    ext='csv'
    for o, a in opt:
        if o=="--yaml":
            yaml_=a
        elif o=='--src':
            src=a
        elif o=='--ext':
            ext=a    
        else:
            print("Opción no reconocida")
    u_args.append(yaml_)
    u_args.append(src)
    u_args.append(ext)
    return u_args

if __name__== '__main__':
        #ops=get_ops()
        #yaml_=ops[0]
        #src=ops[1]
        #ext=ops[2]
        #correo_=correo(yaml_,src, ext)        
        #correo_.get_variables()
        #correo_.enviar_correo()
        
        
        path_='correo_conf.yaml'
        correo_=correo(path_,'/OUTS','txt')
        correo_.get_variables()
        correo_.enviar_correo()
        
