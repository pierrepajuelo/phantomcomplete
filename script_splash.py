#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Routine pour analyser une batterie de simulations
@author: Pierre Pajuelo
@version: 4.0
"""
# Importation des librairies
import os

# Not Necessary
import subprocess

import sys
import getopt

# Définitions des fonctions
def make_video(setup,rewrite):
    """
    Make video based on phantom dumps.

    Parameters
    ----------
    setup : str
        Name of the simulation.
    rewrite : str
        Option for rewriting a video. Option 'y' or 'n'.

    Returns
    -------
    Nothing, just run some commands.

    """
    # Affichage du nombre de fichiers traités 
    os.system('ls %s_* | wc -l > tmp'%(setup))
    nbmodif=open('tmp','r').read()
    os.remove('tmp')
    print('Nombre de dumps traités : %s'%(nbmodif))
    nameplot='plot%s/png'%(setup)
    namesetup='%s_*'%(setup)


    
    #!!! Début de la fonction !!!
    # Utilisation de subprocess, peut être adapté avec os.system
    # splash=subprocess.Popen('splash '+namesetup+' -x 1 -y 2 -r 6 -dev '+nameplot,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
    # print(str(splash.communicate()[0]))
    
    # Affichage des lignes en direct, ne fonctionne pas (écran noir à la fin)
    # for line in iter(splash.stdout.readline, b''):
    #   print(line)
    # splash.stdout.close()
    # splash.wait()
    
    # Utilisation de os.system
    os.system('splash '+namesetup+' -x 1 -y 2 -r 6 -dev '+nameplot)
    
    namepng='plot%s*.png'%(setup)
    
    # Utilisation de subprocess, peut être adapté avec os.system
    # move=subprocess.Popen('mv -v '+namepng+' ../Plot/.',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
    # print(str(move.communicate()[0]))
    
    # Utilisation de os.system
    os.system('mv -v '+namepng+' ../Plot/.')
    
    if rewrite=='y':
        nameplotplot='/home/ppajuelo/Run/Plot/plot%s'%(setup)
        namemovie='/home/ppajuelo/Run/Plot/movie%s'%(setup)
        # !!! Attention !!!
        # Fichier script 'movie.sh' modifié !
        os.system('/home/ppajuelo/Code/splash/scripts/movie.sh -y '+nameplotplot+' '+namemovie)
        
    if rewrite=='n':
        nameplotplot='/home/ppajuelo/Run/Plot/plot%s'%(setup)
        namemovie='/home/ppajuelo/Run/Plot/movie%s'%(setup)
        os.system('/home/ppajuelo/Code/splash/scripts/movie.sh '+nameplotplot+' '+namemovie)
        
# Programme principal 
if __name__=='__main__':
    # Interaction avec l'utilisateur : Numéro de la simulation à analyser
    simulationnumber=2
    argv = sys.argv[1:]
    specialsimulation=''
    try:
        options, args = getopt.getopt(argv, "n:s:",
                                   ["simulationnumber =",
                                    "simulationspecial ="])
    except:
        print("Il y a un problème ...")
     
    for name, value in options:
        if name in ['-n', '--simulationnumber']:
            simulationnumber = int(value)
        if name in ['-s','--simulationspecial']:
            specialsimulation = value
    
    if len(specialsimulation)!=0:
        make_video(specialsimulation,'y')
    else:
        # !!! Se placer dans le répertoire concerné avant de lancer le programme !!!
        # Faire une liste des simulations à transformer
        files=os.listdir() #Linux
        # Récupère les noms des simulations
        files_setup=[i.split(".")[0] for i in files if i.endswith('.setup') and i.startswith('S%s'%(simulationnumber))]
        # Récupère les fichiers .mp4
        files_Plot=os.listdir('/home/ppajuelo/Run/Plot') #Linux
        files_plot_mp4 = [i.split(".")[0][5:] for i in files_Plot if i.endswith('.mp4')]
        # On demande à l'utilisateur si on doit tout écraser 
        ecraser=input('Rewrite all ? (O/N) : ')
        if ecraser=='O':
            for setup in files_setup:
                analyzer=0
                for mp4 in files_plot_mp4:
                    if setup==mp4:
                        print('%s.mp4 already exists !'%(setup))
                        make_video(setup,'y')
                        analyzer+=1
                if analyzer==0:
                    make_video(setup,'n')
        if ecraser=='N':
            for setup in files_setup:
                analyzer=0
                for mp4 in files_plot_mp4:
                    if setup==mp4:
                        print('%s.mp4 already exists !'%(setup))
                        analyzer+=1
                if analyzer==0:
                    make_video(setup,'n')
        
    print('End of script !')
