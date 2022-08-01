#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 15:07:08 2022

Affichage des orbites sélectionnées

@author: Pierre PAJUELO
"""
# Importation des librairies
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
# Définition des fonctions 

def adjustFigAspect(fig,aspect=1):
    '''
    Adjust the subplot parameters so that the figure has the correct
    aspect ratio.
    '''
    xsize,ysize = fig.get_size_inches()
    minsize = min(xsize,ysize)
    xlim = .4*minsize/xsize
    ylim = .4*minsize/ysize
    if aspect < 1:
        xlim *= aspect
    else:
        ylim /= aspect
    fig.subplots_adjust(left=.5-xlim,
                        right=.5+xlim,
                        bottom=.5-ylim,
                        top=.5+ylim)

def orbite(X,Y,Z,PA,Inclination):
    """
    

    Parameters
    ----------
    X : array
        Array contenant les valeurs selon l'axe X.
    Y : array
        Array contenant les valeurs selon l'axe Y.
    Z : array
        Array contenant les valeurs selon l'axe Z.
    PA : float
        Valeur de l'angle de position en radians.
    Inclination : float
        Valeur de l'angle d'inclinaison en radians.

    Returns
    -------
    Les trois arrays après transformation.

    """
    Xnew = np.cos(Inclination)*X + Z*np.sin(Inclination)
    Ynew = Y
    Znew = -np.sin(Inclination)*X + Z*np.cos(Inclination)
    
    Xnnew = np.cos(PA)*Xnew - np.sin(PA)*Ynew
    Ynnew = np.sin(PA)*Xnew + np.cos(PA)*Ynew
    Znnew = Znew
    return(Xnnew,Ynnew,Znnew)

def planet(phi,a=135,e=0.9):
    """
    
    Calcule l'orbite elliptique d'une planète.

    Parameters
    ----------
    phi : float
        Angle de position en degrés.
    a : float, optional
        Demi grand-axe de l'orbite. The default is 135.
    e : float, optional
        Excentricité de l'orbite. The default is 0.9.

    Returns
    -------
    Arrays X,Y,Z correspondant à l'orbite de la planète.

    """
    aplanet = a
    eplanet = e
    cplanet = eplanet*aplanet
    bplanet = np.sqrt(aplanet**2-cplanet**2)
    pplanet = bplanet**2/aplanet
    
    phiplanet = math.radians(phi)
    Rplanet = pplanet/(1+eplanet*np.cos(Theta+phiplanet))
    Xplanet = Rplanet*np.cos(Theta)
    Yplanet = Rplanet*np.sin(Theta)
    Zplanet = np.zeros(100)
    return(Xplanet,Yplanet,Zplanet)

# Programme principal
if __name__=='__main__':
    # Construction of the disk
    R = np.linspace(170,400,100) # Uyama et al.,2020
    Theta = np.radians(np.linspace(0,360,100))
    Disk_PA = math.radians(-60) # Uyama et al.,2020
    Disk_Inclination = math.radians(40.9) # Uyama et al.,2020
    X = R[:,None]*np.cos(Theta)
    Y = R[:,None]*np.sin(Theta)
    Z = np.zeros((100,100))
    
    # Rplanet = aplanet*(1-eplanet*np.cos(Theta))
    # phiplanet = math.radians(-155.95)
    # phiplanet = math.radians(33.62)
    
    
    
    
    # phiplanet2 = math.radians(0)
    # Rplanet2 = pplanet/(1+eplanet*np.cos(Theta+phiplanet2))
    # Xplanet2 = Rplanet2*np.cos(Theta)
    # Yplanet2 = Rplanet2*np.sin(Theta)
    # Zplanet2 = np.zeros(100)
    
  
    Xnnew,Ynnew,Znnew=orbite(X,Y,Z,Disk_PA,Disk_Inclination)
    # !!! Angles en radians !!!
   
    X2,Y2,Z2=planet(phi=0,a=135,e=0.9)
    Xplanetnew2,Yplanetnew2,Zplanetnew2=orbite(X2,Y2,Z2,PA = math.radians(0),Inclination = math.radians(40))
    
    # plt.close('all')
    # plt.figure()
    # plt.plot(Xplanet,Yplanet)
    
    # Plotting
    
    plt.close('all')
    # plt.figure()
    # for inclination in range(0,90,10):
    #     Xplanetnew,Yplanetnew,Zplanetnew=orbite(Xplanet,Yplanet,Zplanet,PA = PAplanet ,Inclination = math.radians(inclination))
    #     plt.plot(Xplanetnew,Yplanetnew,label=r'Inclinaison = %s$^{\circ}$'%(inclination))
    # plt.legend()
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(Xnnew,
                            Ynnew,
                            Znnew,
                            # cmap=cm.coolwarm,
                            # linewidth=0,
                            antialiased=False,
                            alpha=0.2)
    for phi in range(0,90,10):
        X1,Y1,Z1=planet(-90-56.38,a=135,e=0.9)
        PAplanet = math.radians(-phi+90)
        Xplanetnew,Yplanetnew,Zplanetnew=orbite(X1,Y1,Z1,PA = PAplanet,Inclination = math.radians(-30))
        ax.plot(Xplanetnew,Yplanetnew,Zplanetnew,label='Orbite planète, $PA = %s^{\circ}$'%(phi))
    ax.plot(Xplanetnew2,Yplanetnew2,Zplanetnew2,label=r'Orbite planète, $e=0.9$, $i=40^{\circ}$')
    ax.scatter(0,0,marker=(5,2))
    ax.legend(ncol=2)
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_xlabel('X (ua.)')
    ax.set_ylabel('Y (ua.)')
    ax.set_zlabel('Z (ua.)')
    ax.set_xlim(-400,400)
    ax.set_ylim(-400,400)
    ax.set_zlim(-400,400)
    ax.elev = 27
    ax.azim = 68
    ax.dist = 10
    plt.show()
    
    
    
