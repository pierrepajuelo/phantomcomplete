# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 08:36:42 2022

@author: pierr
"""

# Importation des librairies
from scipy.optimize import curve_fit
import numpy as np

# Définitions des fonctions

def conditions_initiales(x,y):
    """
    Génère des conditions initiales pour un set de données

    Parameters
    ----------
    x : Array
        Array Input.
    y : Array
        Array Output.

    Returns
    -------
    Paramètres de la fonction de fit.
    """
    a=125
    b=-10
    n=1
    return [a,b,n]

def archimede(theta,a,b,n):
    """
    

    Parameters
    ----------
    theta : array
        Valeur de l'angle.
    a : float
        Paramètre a de l'équation.
    b : float
        Paramètre b de l'équation.
    n : float
        Exposant de theta dans l'équation.

    Returns
    -------
    TYPE
        Equation générale d'une spirale d'Archimède en coordonnées polaires.

    """
    return (a+b*theta**n)

def loga(theta,r0,k):
    """
    

    Parameters
    ----------
    theta : array
        Valeur de l'angle.
    r0 : float
        Paramètre r0 de l'équation.
    k : float
        Paramètre k de l'équation.

    Returns
    -------
    array.
        Equation d'une spirale logarithmique.
        
    """
    return r0*np.exp(k*theta)

def conditions_initiales_loga(x,y):
    """
    Génère des conditions initiales pour un set de données

    Parameters
    ----------
    x : Array
        Array Input.
    y : Array
        Array Output.

    Returns
    -------
    Paramètres de la fonction de fit.
    """
    r0=1000
    k=-1.2
    return [r0,k]

def fitting(spirales,polar_arr,fin,fonction='Archimede'):
    '''
    
    Renvoie les paramètres de fit pour les équations générales d'Archimède et de spirale logarithmique

    Parameters
    ----------
    spirales : array
        Entrée de format (fin,360,2) avec k=0 : r et k=1 : theta.
    polar_arr : array
        Array contenant les valeurs de theta.
    fin : int
        Nombre de spirales.
    fonction : str, optional
        Fonction de référence pour le fit, à choisir entre 'Archimede', 'Logarithme'. The default is 'Archimede'.

    Returns
    -------
    Out : TYPE
        DESCRIPTION.

    '''
    # Iteration de toutes les spirales
    
    # !!! Pas de modification des spirales !!!
    #x=newspirale[numero,1:Pointscourbure[0][0],0]
    # Liste des paramètres donnés en sortie
    Out = [[],[]]
    Polar = []
    for numero in range(fin):
        #On ne fit que les données
        nnandebut=-1
        for n,info in enumerate(spirales[numero,:,0]):
            if np.isnan(info)==False:
                if nnandebut==-1:
                    nnandebut=n
                if n+1<360:
                    if np.isnan(spirales[numero,n+1,0])==True:
                        nnanfin=n+1
                        break
                if n==359:
                    nnanfin=n
        if np.isnan(spirales[numero,nnandebut,1])==False:
            theta0=int(spirales[numero,nnandebut,1])
        else:
            theta0=int(spirales[numero,nnandebut+1,1])

        #print(spirales[numero,nnandebut:nnanfin,1])    
        x=spirales[numero,nnandebut:nnanfin,0]
        Nlongueur=int(nnanfin-nnandebut)
        y=np.radians(polar_arr[theta0:Nlongueur+theta0])
        Polar.append(y)
        #y=newspirale[numero,1:Pointscourbure[0][0],1]
       
        if fonction=='Archimede':
            param, covariance = curve_fit(archimede, y, x, p0=conditions_initiales(x,y),maxfev=100000)
            Out[0].append(param)
            Out[1].append(covariance)
            
        if fonction=='Logarithme':
            param2, covariance2 = curve_fit(loga, y, x, p0=conditions_initiales_loga(x,y),maxfev=100000)
            Out[0].append(param2)
            Out[1].append(covariance2)
    return Out,Polar
        
        