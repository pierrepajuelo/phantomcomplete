#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 13:32:50 2022

MCFOST routine for PSMN

@author: Pierre PAJUELO
"""
# Importation des librairies 
import os
import pandas as pd
import sys
import getopt
import traceback

# Définitions des fonctions

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
   # print(dump)
   # print(data.type)
    if type(data.type.values[0]) != str:
        data_sinks=data[data.type==3]
    if type(data.type.values[0]) == str:
        data_sinks=data[data.type=='3']
    xsink=data_sinks.x.iloc[0]
    ysink=data_sinks.y.iloc[0]
    zsink=data_sinks.z.iloc[0]
    xplanet=data_sinks.x.iloc[1]
    yplanet=data_sinks.y.iloc[1]
    zplanet=data_sinks.z.iloc[1]
    return(xsink,ysink,zsink,xplanet,yplanet,zplanet)

def mcfost(file,file_para='ref3.0.para',longueurdonde=1.229):
    xsink,ysink,zsink,xplanet,yplanet,zplanet=position_sink(file)
    repository='rendering%s'%(file)
    
# repository_img='renderingimg%s'%(file)
# cmd_clean='rm -rf data_%s'%(longueurdonde)
# cmd_clean_th='rm -rf data_th'
# os.system(cmd_clean)
# os.system(cmd_clean_th)

    # Modify the parameter file
    lines=open(file_para,'r').readlines()
    line_star = '  5900.0    6.5    5.3    %s    %s    %s    T Temp, radius (solar radius), M (solar mass), x,y,z (AU), automatic spectrum ?\n'%(xsink,ysink,zsink)
    line_planet = '  252.0    0.01    0.048    %s    %s    %s    T Temp, radius (solar radius), M (solar mass), x,y,z (AU), automatic spectrum ?\n'%(xplanet,yplanet,zplanet)
    lines[-3]=line_planet
    lines[-6]=line_star
    file_para_sim='transfert_radiatif.para'
    cmd_copy = 'cp %s %s'%(file_para,file_para_sim)
    os.system(cmd_copy)
    open('transfert_radiatif.para','w').writelines(lines)
    
    # MCFOST Commands
    cmd_mcfost='mcfost %s -phantom %s -root_dir %s -fix_star -old_PA'%(file_para_sim,file,repository)
    os.system(cmd_mcfost)
    cmd_mcfost_img='mcfost %s -phantom %s -img %s -root_dir %s -fix_star -old_PA'%(file_para_sim,file,longueurdonde,repository)
    os.system(cmd_mcfost_img)
    

# Programme principal

if __name__=='__main__':
    # Récupérer le(s) fichier(s) à analyser

    simulationfile=''
    folder=''
    argv=sys.argv[1:]
    try:
        options, args = getopt.getopt(argv,"s:f:",["simulationname =","folder ="])
    except:
        print('Problem in arguments')
    for name,value in options:
        if name in ['-s','--simulationname']:
            simulationfile = value
        if name in ['-f','--folder']:
            folder = value
            
    # Analyser un dossier ou un fichier + Séquence analyse
    if len(simulationfile)!=0:
        file_dump=simulationfile
        try: 
            mcfost(file_dump)
        except:
            print('Erreur avec la simulation %s'%(file_dump))
            print(traceback.format_exc())
    if len(folder)!=0:
        files=os.listdir()
        files_dump=[i for i in files if i.startswith('%s_'%(folder)) and not i.endswith('.ascii')]
        for file in files_dump:
            try :
                if os.path.exists('rendering%s_ta'%(file)):
                    print('Transfert radiatif déjà calculé pour %s !'%(file))
                else:
                    mcfost(file)
            except:
                print('Erreur avec le fichier %s ...'%(file))
                print(traceback.format_exc())
                
    # !!! Brouillon !!!
    # print(files_dump)
    # x,y=position_sink(files_dump[2])
    # print(x,y,'Ca fonctionne pourtant !')
    # print(files_dump)
    # files_para=[i for i in files if i.endswith('.para')]
    

    
            
