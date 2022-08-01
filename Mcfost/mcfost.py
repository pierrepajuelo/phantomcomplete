# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 09:27:34 2022

Affichage des images en diffusion CO

@author: Pierre PAJUELO
"""
# Importation des librairies
import matplotlib.pyplot as plt
import pymcfost as mcfost
import os
import pandas as pd
import numpy as np

# Definition des fonctions
def position_sink(dump):
    """
    

    Parameters
    ----------
    dump : str
        Name of the full dump to analyse.

    Returns
    -------
    Position of the central sink.

    """
    # Dossier de travail
    cwd = os.getcwd()
    # On transforme le dump en fichier ascii
    if os.path.exists('%s/%s.ascii'%(cwd,dump)):
        pass
    else:
        cmd_ascii='splash to ascii %s'%(dump)
        os.system(cmd_ascii)
    file_ascii='%s.ascii'%(dump)
    
    
    header = ['x', 'y', 'z', 'm', 'h', 'rho','vx', 'vy', 'vz', 'divv', 'dt', 'type']
    data = pd.read_csv('%s/%s'%(cwd,file_ascii), delim_whitespace=True, skiprows=14, header=None, names=header)
    
    if type(data.type.values[0]) != str:
        data_sinks=data[data.type==3]
    if type(data.type.values[0]) == str:
        data_sinks=data[data.type=='3']
    xsink=data_sinks.x.iloc[0]
    ysink=data_sinks.y.iloc[0]
    return(xsink,ysink)

# Programme principal

if __name__=="__main__":
    files=os.listdir()
    files_dump=[i for i in files if i.startswith('S2e9i40_') and not i.endswith('.ascii')]
    # print(files_dump)
    files_para=[i for i in files if i.endswith('.para')]
    file_para=files_para[0]
    longueurdonde=1.229
    for file in files_dump:
        xsink,ysink=position_sink(file)
        cmd_clean='rm -rf data_%s'%(longueurdonde)
        cmd_clean_th='rm -rf data_th'
        os.system(cmd_clean)
        os.system(cmd_clean_th)
        cmd_mcfost='mcfost %s -phantom %s'%(file_para,file)
        os.system(cmd_mcfost)
        cmd_mcfost_img='mcfost %s -phantom %s -img %s'%(file_para,file,longueurdonde)
        os.system(cmd_mcfost_img)
        image_1mum = mcfost.Image("./data_%s/"%(longueurdonde))
        fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15,4))
        cbar = True
        no_ylabel = False
        shift_dx=xsink
        shift_dy=ysink
        image_1mum.plot(0, ax=axes,vmin=1e-17, vmax=1e-15, shift_dx=shift_dx, shift_dy=shift_dy,colorbar=cbar, no_ylabel=no_ylabel)
        # for i in range(3):
        #     if i==2:
        #         cbar=True
        #     if i>0:
        #         no_ylabel=True
        #     image_1mum.plot(i, ax=axes[i],vmin=1e-18, vmax=1e-14, colorbar=cbar, no_ylabel=no_ylabel)
        plt.savefig('Rendering_%s.png'%(file))
