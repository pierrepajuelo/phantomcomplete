#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Routine pour générer une batterie de codes de simulation
@author = Pierre Pajuelo
V 3.0
"""
# Importations des librairies
import os 
import numpy as np
import sys
import getopt
import subprocess
import time

# Définition des fonctions
def scriptphantom(simulation,eccentricity,inclination,proc=32):
    """
    
    Génère une copie de script phantom à exécuter sur un terminal du PSMN (qsub command).

    Parameters
    ----------
    simulation : int
        Numéro de référence de la simulation.
    eccentricity : float
        Indication sur l'excentricité de l'orbite de la planète test.
    inclination : float
        Indication sur l'inclinaison de l'orbite de la planète test.
    proc : int, optional
        Nombre de coeurs utilisés pour effectuer le calcul. Values possible : 8,16,32. The default is 32.

    Returns
    -------
    Name of the output file with the script inside. Executes some commands on Linux.

    """
    # Create the name of the new script for phantom
    if type(eccentricity.item())==float:
        eccname=int(eccentricity*10**(len(str(eccentricity).split(".")[1])))
    elif type(eccentricity.item())==int:
        eccname=eccentricity
    if type(inclination.item())==float:
        incname=int(inclination*10**(len(str(inclination).split(".")[1])))
    elif type(inclination.item())==int:
        incname=inclination
    name='sp%se%si%s'%(simulation,eccname,incname)
    namesimu='S%se%si%s'%(simulation,eccname,incname)
    # Make a list of all files, including hidden ones
    liste = subprocess.run(['ls', '-a'], stdout=subprocess.PIPE).stdout.decode('utf-8').split("\n")
    # Search in the list if the file already exists
    indicator=0
    for file in liste:
        if file==name:
            print('Phantom script already exists !')
            indicator+=1
    # If the file doesn't exist
    if indicator==0:
        # Make a copy of the file
        cmdcopy='cp %s %s'%(spref,name)    
        os.system(cmdcopy)
        #Modification of the name of the simulation
        cmdmodifyname='sed -i "s/-N\ .*$/-N\ %s/" %s'%(namesimu,name)
        os.system(cmdmodifyname)
        #Modification of the core number
        systemname='openmp%s\ %s'%(proc,proc)
        cmdmodifycorenumber='sed -i "s/#$\ -pe\ .*$/#$\ -pe\ %s/" %s'%(systemname,name)
        os.system(cmdmodifycorenumber)
        #Modification of the .in name file
        filein='%s\.in'%(namesimu)
        beginphantomline='.\/phantom .*.in '
        modifyphantomline='.\/phantom\ %s\ '%(filein)
        cmdmodifyphantomin="sed -i 's/%s/%s/' %s"%(beginphantomline,modifyphantomline,name)
        os.system(cmdmodifyphantomin)
        beginline='export outfile=`grep logfile ".*.in" '
        modifyline='export\ outfile=\`grep\ logfile\ \"%s\"\ '%(filein)
        cmdmodifylogfilein="sed -i 's/%s/%s/' %s"%(beginline,modifyline,name)
        os.system(cmdmodifylogfilein)
        
        #Vérifier le nombre de modifications faites dans le fichier
        cmdverify='diff -U 0 %s %s | grep -c ^@ > tmp'%(name,spref)
        os.system(cmdverify)
        if open('tmp','r').read() == 3 :
            print('Fichier %s créé avec succès'%(name))
        os.remove('tmp')
    return(name)

def phantom_config(simulation,eccentricity,inclination,planetmass=50,particules=1000000,Norbits=51):
    """
    
    Génère une copie de configuration phantom en ne changeant que certains paramètres d'orbite de la planète.
    
    Parameters
    ----------
    simulation : int
        Numéro de référence de la simulation.
    eccentricity : float
        Indication sur l'excentricité de l'orbite de la planète test.
    inclination : float
        Indication sur l'inclinaison de l'orbite de la planète test.
    planetmass : float, optional
        Masse de la planète en masse de Jupiter. The default is 50.
    particules : int, optional
        Nombre de particules SPH dans la simulation. The default is 1000000.
    Norbits : int, optional
        Nombre d'orbites de la planète. The default is 51.

    Returns
    -------
    Name of the output file with the config inside (without extension .setup). Executes some commands on Linux.
    
    """
    # Create the name of the new config file
    if type(eccentricity.item())==float:
        eccname=int(eccentricity*10**(len(str(eccentricity).split(".")[1])))
    elif type(eccentricity.item())==int:
        eccname=eccentricity
    if type(inclination.item())==float:
        incname=int(inclination*10**(len(str(inclination).split(".")[1])))
    elif type(inclination.item())==int:
        incname=inclination
    name='S%se%si%s'%(simulation,eccname,incname)
    configname='%s.setup'%(name)
    liste = subprocess.run(['ls', '-a'], stdout=subprocess.PIPE).stdout.decode('utf-8').split("\n")
    # Search in the list if the file already exists
    indicator=0
    for file in liste:
        if file==configname:
            print('Phantom config file already exists !')
            a1=input('Re-write ? (O/N) :')
            if a1=='O':
                break
            if a1=='N':
                indicator+=1
                break
    # If the file doesn't exist
    if indicator==0:
        cmdcopy='cp %s %s'%(phantomref,configname)    
        os.system(cmdcopy)
        #Modification of the number of particles
        cmdmodifynumber='sed -i "s/np\ =\s.*\s\!/np\ =\     %s\   \!/" %s'%(particules,configname)
        os.system(cmdmodifynumber)
        #Modification of the planet eccentricity
        cmdmodifyeccentricity='sed -i "s/binary_e\ =\s.*\s\!/binary_e\ =\       %s\   \!/" %s'%(eccentricity,configname)
        os.system(cmdmodifyeccentricity)
        #Modification of the planet inclination
        cmdmodifyinclination='sed -i "s/binary_i\ =\s.*\s\!/binary_i\ =\       %s\   \!/" %s'%(inclination,configname)
        os.system(cmdmodifyinclination)
        #Modification of the planet mass
        planetmasssolar=round(planetmass*9.5*10**(-4),3) #Conversion
        cmdmodifyinclination='sed -i "s/m2\ =\s.*\s\!/m2\ =\       %s\   \!/" %s'%(planetmasssolar,configname)
        os.system(cmdmodifyinclination)
        #Modification of the number of orbits
        cmdmodifyorbits='sed -i "s/norbits\ =\s.*\s\!/norbits\ =\          %s\    \!/" %s'%(Norbits,configname)
        os.system(cmdmodifyorbits)
        
        #Vérifier le nombre de modifications faites dans le fichier
        cmdverify='diff -U 0 %s %s | grep -c ^@ > tmpp'%(configname,phantomref)
        os.system(cmdverify)
        nbmodif=open('tmpp','r').read()
        os.remove('tmpp')
        print('Fichier %s créé avec succès avec %s modifications !'%(configname,str(int(nbmodif)+1)))
        
    return(name)

def lancement_simulation(nameconfig,namesp):
    """
    

    Parameters
    ----------
    nameconfig : str
        Nom du fichier de configuration phantom.
    namesp : str
        Nom du fichier de script phantom.

    Returns
    -------
    Nothin', just tipping some Linux commands.

    """
    configname='%s.setup'%(nameconfig)
    
    # Vérifier que les deux fichiers existent !
    liste = subprocess.run(['ls', '-a'], stdout=subprocess.PIPE).stdout.decode('utf-8').split("\n")
    # Search in the list if the file already exists
    indicator=0
    for file in liste:
        if file==configname:
            print('Phantom config file exists !')
            indicator+=1
        if file==namesp:
            print('Phantom script file exists !')
            indicator+=1
    # If the file doesn't exist
    if indicator==0:
        print("Attention ! Les fichiers n'existent pas !")
    if indicator==1:
        print("Attention ! Il manque un fichier !")
    if indicator==2:
        cmdphantomsetup='%s %s'%(phantomsetup,nameconfig)
        os.system(cmdphantomsetup)
        time.sleep(10)
        cmdqsub='qsub %s > tmpq'%(namesp)
        os.system(cmdqsub)
        ok=open('tmpq','r').read()
        print(ok)
        os.remove('tmpq')
# Programme principal


if __name__=='__main__':
    # On se place dans le bon répertoire
    
    # Change the current working directory
    #os.chdir('~/Run/SCRIPT')
    
    '''
    # Print the current working directory
    print("Current working directory: {0}".format(os.getcwd()))

    
    
    # Print the current working directory
    print("Current working directory: {0}".format(os.getcwd()))
    '''
    
    # Reference file for Script phantom 
    spref='sp'
    phantomref='S2e1i1.setup'
    phantomsetup='./phantomsetup'
    
    # Récupération des informations sur les simulations à lancer
    
    # Valeurs par défaut
    
    nombreparticule=1000000
    planetmass=50
    inclinationstart=""
    inclinationend=""
    inclinationstep=""
    inclinationtype=float
    eccentricitystart=""
    eccentricityend=""
    eccentricitystep=""
    eccentricitytype=float
    simulationnumber=""
    nombrecoeurs=32
    
    argv = sys.argv[1:]
    
    try:
        options, args = getopt.getopt(argv, "n:p:s:e:a:t:d:f:l:y:z:c:",
                                   ["nombreparticule =",
                                    "planetmass =",
                                    "inclinationstart =",
                                    "inclinationend =",
                                    "inclinationstep =",
                                    "inclinationtype =",
                                    "eccentricitystart =",
                                    "eccentricityend =",
                                    "eccentricitystep =",
                                    "eccentricitytype =",
                                    "simulationnumber =",
                                    "nombrecoeurs ="])
    except:
        print("Il y a un problème ...")
     
    for name, value in options:
        if name in ['-n', '--nombreparticule']:
            nombreparticule = int(value)
        elif name in ['-p', '--planetmass']:
            planetmass = float(value)
        elif name in ['-s', '--inclinationstart']:
            inclinationstart = float(value)
        elif name in ['-e', '--inclinationend']:
            inclinationend = float(value)
        elif name in ['-a', '--inclinationstep']:
            inclinationstep = int(value)
        elif name in ['-t', '--inclinationtype']:
            inclinationtype = value
        elif name in ['-d', '--eccentricitystart']:
            eccentricitystart = float(value)
        elif name in ['-f', '--eccentricityend']:
            eccentricityend = float(value)
        elif name in ['-l', '--eccentricitystep']:
            eccentricitystep = int(value)
        elif name in ['-y', '--eccentricitytype']:
            eccentricitytype = value
        elif name in ['-z', '--simulationnumber']:
            simulationnumber = int(value)
        elif name in ['-c', '--nombrecoeurs']:
            nombrecoeurs = int(value)
    # print(inclinationstart,inclinationend,inclinationstep,inclinationtype)
    # print(eccentricitystart,eccentricityend,eccentricitystep,eccentricitytype)
    ils=np.linspace(inclinationstart,inclinationend,inclinationstep,dtype=inclinationtype)
    els=np.linspace(eccentricitystart,eccentricityend,eccentricitystep,dtype=eccentricitytype)
    
    # Vérifier que l'utilisation est ok sur les listes 
    print('Liste parcouru pour les inclinaisons :\n',ils)
    answer1=input('Est-ce correct ? (O/N) :')
    if answer1=='O':
        print('Liste parcouru pour les excentricités :\n',els)
        answer2=input('Est-ce correct ? (O/N) :')
        if answer2=='O':
            for i in ils:
                for e in els:
                    namesp=scriptphantom(simulationnumber,e,i,nombrecoeurs)
                    nameconfig=phantom_config(simulationnumber,e,i,planetmass,nombreparticule,Norbits=51)
                    lancement_simulation(nameconfig,namesp)
        else:
            raise ValueError('Veuillez recommencer')
            
    else:
        raise ValueError('Veuillez recommencer')
    
