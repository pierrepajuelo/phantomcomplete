# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 08:55:25 2022

@author: pierr
"""
#Importation des librairies 
import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import math
from skimage.measure import EllipseModel
from matplotlib.patches import Ellipse
from scipy.signal import argrelextrema
from PIL import Image

#Définition des fonctions

def sep_gas_sinks(data):
    if type(data.type.values[0]) != str:
        gas = data[data.type==1]
        sinks=data[data.type==3]
    if type(data.type.values[0]) == str:
        gas = data[data.type=='1']
        sinks=data[data.type=='3']
    return(gas,sinks)
def z_rotation(vector,theta):
    """Rotates 3-D vector around z-axis"""
    R = np.array([[np.cos(theta), -np.sin(theta),0],[np.sin(theta), np.cos(theta),0],[0,0,1]])
    return np.dot(R,vector)
def y_rotation(vector,theta):
    """Rotates 3-D vector around y-axis"""
    R = np.array([[np.cos(theta),0,np.sin(theta)],[0,1,0],[-np.sin(theta), 0, np.cos(theta)]])
    return np.dot(R,vector)
def x_rotation(vector,theta):
    """Rotates 3-D vector around x-axis"""
    R = np.array([[1,0,0],[0,np.cos(theta),-np.sin(theta)],[0, np.sin(theta), np.cos(theta)]])
    return np.dot(R,vector)

#Programme principal 

#Chargement des fichiers
files=os.listdir('D:/Stage/PSMN/Bras')
#Création des listes utiles
files_data = [i for i in files if i.endswith('.ascii')]
files_tif = [i for i in files if i.endswith('.png')]
filetif=files_tif[0]
for file in files_data:
    header = ['x', 'y', 'z', 'm', 'h', 'rho','vx', 'vy', 'vz', 'divv', 'dt', 'type']
    data = pd.read_csv('D:/Stage/PSMN/Bras/'+file, delim_whitespace=True, skiprows=14, header=None, names=header)
    timeline = np.loadtxt('D:/Stage/PSMN/Bras/'+file, skiprows=3, max_rows=1, usecols=(1,2), comments='&')
    time = int(timeline[0] * timeline[1])
    r = np.sqrt(data.x*data.x + data.y*data.y)
    data.loc[:,"r"] = r
    
    #%%
    # Déprojection de la densité
    # PA deprojected
    
    
    vector=z_rotation(np.array([data.x,data.y,data.z]),math.radians(-60))
    data.loc[:,"py"]=vector[1]
    data.loc[:,"px"]=vector[0]
    data.loc[:,"pz"]=vector[2]
    # gas,sinks=sep_gas_sinks(data)
    # plt.figure(2)
    
    
    # plt.scatter(gas.px,gas.py,c=gas.rho,cmap='jet',s=gas.h, norm=LogNorm(vmin=10e-18,vmax=10e-15))
    # plt.scatter(sinks.px,sinks.py,c='red',marker=(5, 2))
    # plt.xlabel('x (ua)')
    # plt.ylabel('y (ua)')
    # #plt.xlim((-2000,2000))
    # #plt.ylim((-500,500))
    # cbar = plt.colorbar(norm=LogNorm(vmin=10e-18,vmax=10e-14))
    # cbar.ax.set_title(r'Log Density (g/cm$^{2}$)')
    # plt.title('Carte de densité du disque PA dep.')
    
    #Inclinaison 
    vector2=y_rotation(np.array([data.px,data.py,data.pz]),math.radians(-40.9))
    data.loc[:,"py"]=vector2[1]
    data.loc[:,"px"]=vector2[0]
    data.loc[:,"pz"]=vector2[2]
    # gas,sinks=sep_gas_sinks(data)
    # plt.figure(3)
    
    
    # plt.scatter(gas.px,gas.py,c=gas.rho,cmap='jet',s=gas.h, norm=LogNorm(vmin=10e-18,vmax=10e-15))
    # plt.scatter(sinks.px,sinks.py,c='red',marker=(5, 2))
    # plt.xlabel('x (ua)')
    # plt.ylabel('y (ua)')
    # #plt.xlim((-2000,2000))
    # #plt.ylim((-500,500))
    # cbar = plt.colorbar(norm=LogNorm(vmin=10e-18,vmax=10e-14))
    # cbar.ax.set_title(r'Log Density (g/cm$^{2}$)')
    # plt.title('Carte de densité du disque dep.')
        
    #%%
    #Affichage de la densité
    # gas,sinks=sep_gas_sinks(data)
    # Si jamais ça marche pas :
    gas=data
    sinks=data
    plt.close('all')
    plt.figure(1)
    # im = Image.open(filetif)
    # plt.imshow(im,extent=[-600,750,-550,550])
    # datacopy=data[data.rho>0.5*10e-16]
    datacopy=data[data.rho>7*10e-17]
    plt.scatter(datacopy.px,datacopy.py,c=datacopy.rho,cmap='inferno',norm=LogNorm(vmin=10e-17,vmax=10e-15))
    cbar = plt.colorbar(cmap='inferno',norm=LogNorm(vmin=10e-17,vmax=10e-15))
    plt.xlabel('x (ua)')
    plt.ylabel('y (ua)')
    plt.xlim((-400,400))
    plt.ylim((-400,400))
    plt.title('Carte de densité du disque')
    plt.figure(2)
    up=datacopy[datacopy.pz>0]
    below=datacopy[datacopy.pz<0]
    plt.scatter(up.px,up.py,c='red',s=up.h)#,c=gas.rho, cmap='jet',norm=LogNorm(vmin=10e-17,vmax=10e-15))
    plt.scatter(below.px,below.py,c='blue',s=below.h)
    # cbar = plt.colorbar(cmap='inferno',norm=LogNorm(vmin=10e-17,vmax=10e-15))
    
    #plt.scatter(gas.x,gas.y,c=gas.rho,s=gas.h)
    # cbar = plt.colorbar(norm=LogNorm(vmin=10e-17,vmax=10e-15))
    # plt.scatter(sinks.x,sinks.y,c='red',marker=(5, 2))
    plt.xlabel('x (ua)')
    plt.ylabel('y (ua)')
    plt.xlim((-400,400))
    plt.ylim((-400,400))
    # plt.legend()
    # cbar.ax.set_title(r'Log Density (g/cm$^{2}$)')
    plt.title('Carte de densité du disque Up et Down')
    
    
    #%%
    # Rapport
    fig, ax = plt.subplots()
    a_points=np.array([data.px,data.py]).T
    ell = EllipseModel()
    ell.estimate(a_points)
    xc, yc, a, b, theta = ell.params
    ell_patch = Ellipse((xc, yc), 2*a, 2*b, theta*180/np.pi, edgecolor='red', facecolor='none')
    ax.add_patch(p=ell_patch)
    #%%
    gas,sinks=sep_gas_sinks(data)
    py = data.y/np.cos(math.radians(60))
    px = data.x/np.sin(math.radians(60))
    data.loc[:,"py"]=py
    data.loc[:,"px"]=px
    
    #plt.close('all')
    plt.figure(2)
    plt.scatter(data.px,data.py,c=data.rho,cmap='jet',s=data.h, norm=LogNorm(vmin=10e-18,vmax=10e-15))
    plt.scatter(sinks.x,sinks.y,c='red',marker=(5, 2))
    plt.xlabel('x (ua)')
    plt.ylabel('y (ua)')
    #plt.xlim((-2000,2000))
    #plt.ylim((-2000,2000))
    cbar = plt.colorbar(norm=LogNorm(vmin=10e-18,vmax=10e-14))
    cbar.ax.set_title(r'Log Density (g/cm$^{2}$)')
    plt.title('Carte de densité du disque PA dep.')
    
    #%%
    #Plot radial
    #Default value
    rbins=200
    vazmin=15
    zbins=15

    rindex, bins_r = pd.cut(data.r, rbins, retbins=True)
    zindex = pd.cut(data.z, np.linspace(-vazmin, vazmin, num=zbins))
    gas.loc[:,"rindex"]  = rindex
    gas.loc[:,"zindex"]  = zindex
    
    bin_r = gas.groupby("rindex").r.mean().values
    pro_rhog_r    = gas.groupby("rindex").rho.mean().values
    pro_rhog_z     = gas.groupby("zindex").rho.mean().values
    
    dict_r = {"r": bin_r,
          "rhog": pro_rhog_r}
    profiles_r    = pd.DataFrame(data=dict_r)
    profiles_r.plot("r","rhog")
    
    
    #%%
    #Projection sur le plan xy
    # Coordonnées sphériques
    rp = np.sqrt(data.x*data.x + data.y*data.y + data.z*data.z)
    data.loc[:,"rp"] = rp
    theta = np.arccos(data.z/data.rp)
    phi = np.arctan(data.y/data.x)
    data.loc[:,"theta"] = theta
    data.loc[:,"phi"] = phi
    # Projection suivant z
    px = data.x/np.sin(theta)
    py = data.y/np.sin(theta)
    data.loc[:,"px"] = px
    data.loc[:,"py"] = py
    
    gas = data[data.type==1]
    sinks=data[data.type==3]
    
    
    #%%
    #Affichage de la densité projetée

    #plt.close('all')
    plt.figure(2)
    plt.scatter(gas.px,gas.py,c=gas.rho,cmap='jet',s=gas.h, norm=LogNorm(vmin=10e-18,vmax=10e-15))
    plt.scatter(sinks.x,sinks.y,c='red',marker=(5, 2))
    plt.xlabel('x projeté (ua)')
    plt.ylabel('y projeté (ua)')
    cbar = plt.colorbar(norm=LogNorm(vmin=10e-18,vmax=10e-14))
    cbar.ax.set_title(r'Log Density (g/cm$^{2}$)')
    plt.title('Carte de densité du disque projeté')
    
    #%% 
    #Affichage d'une polaire radiale
    plt.close('all')
    plt.figure(3)
    plt.scatter(gas.phi,gas.rp,c=gas.rho,cmap='jet',s=gas.h, norm=LogNorm(vmin=10e-18,vmax=10e-15))
    plt.scatter(sinks.phi,sinks.rp,c='red',marker=(5, 2))
    plt.ylabel('r (ua)')
    plt.xlabel('phi (rad)')
    cbar = plt.colorbar(norm=LogNorm(vmin=10e-18,vmax=10e-14))
    cbar.ax.set_title(r'Log Density (g/cm$^{2}$)')
    plt.title('Carte de densité du disque radiale')
    
    #%%
    #Bin along phi
    rp = np.sqrt(data.px*data.px + data.py*data.py + data.pz*data.pz)
    data.loc[:,"rp"] = rp
    phi = np.arctan(data.py/data.px)
    data.loc[:,"phi"] = phi
    
    phibins=100
    phiindex, bins_phi = pd.cut(data.phi, phibins, retbins=True)
    data.loc[:,"phiindex"]  = phiindex
    rbins=100
    rindex, bins_r = pd.cut(data.r, rbins, retbins=True)
    #gas.loc[:,"rindex"]  = rindex
    
    bin_phi = data.groupby("phiindex").phi.mean().values
    bin_r = gas.groupby("rindex").r.mean().values
    
    liste=[]
    for i in range(100000):
        liste.append(data.phiindex.values[i].mid)
    liste_arr=np.array(liste)
    
    data["phin"]=liste_arr.tolist()
    
    
    #%%
    #Affichage du bin 
    
    gas,sinks=sep_gas_sinks(data)
    plt.close('all')
    plt.figure(3)
    plt.scatter(gas.phin,gas.rp,c=gas.rho,cmap='jet',s=gas.h, norm=LogNorm(vmin=10e-18,vmax=10e-15))
    plt.scatter(sinks.phi,sinks.rp,c='red',marker=(5, 2))
    plt.ylabel('r (ua)')
    plt.xlabel('phi (rad)')
    cbar = plt.colorbar(norm=LogNorm(vmin=10e-18,vmax=10e-14))
    cbar.ax.set_title(r'Log Density (g/cm$^{2}$)')
    plt.title('Carte de densité du disque radiale binned')
    
    #%%
    #Example of radial profile density
    plt.figure(54)
    #Example 
    data_r=data[data.phin==data.phin.values[0]]
    plt.scatter(data_r.rp, data_r.rho,s=data_r.h)
    plt.xlabel('r (ua)')
    plt.ylabel(r'$\rho$ (g/cm$^2$)')
    
    
    
    #%%
    #Triche avec hexbin
    
    test=data.plot.hexbin(x='phi',y='rp',C='rho',gridsize=(100,30),cmap='jet',bins='log',norm=LogNorm(vmin=10e-18,vmax=10e-15))
    
    
    #%%
    # Maxima locaux
    N=data.shape[0]
    for i in range(N):
        df=data[data.phin==data.phin.values[i]]
        n = 5 # number of points to be checked before and after
        df['max'] = df.iloc[argrelextrema(df.rho.values, np.greater_equal,order=n)[0]]['rho']
    #%%
    
    
    grouped = data.groupby('phiindex')

    #data.sort_values("phiindex")
    #gas,sinks=sep_gas_sinks(data)
    
    
    #Affichage d'une polaire radiale
    plt.close('all')
    plt.figure(26)
    plt.scatter(grouped.get_group()['phi'],grouped.get_group()['rp'],c=data.rho,cmap='jet',s=data.h, norm=LogNorm(vmin=10e-18,vmax=10e-15))
    plt.scatter(sinks.phiindex,sinks.rp,c='red',marker=(5, 2))
    plt.ylabel('r (ua)')
    plt.xlabel('phi bin (rad)')
    cbar = plt.colorbar(norm=LogNorm(vmin=10e-18,vmax=10e-14))
    cbar.ax.set_title(r'Log Density (g/cm$^{2}$)')
    plt.title('Carte de densité du disque radiale')
    
    
    #%%
    
    phibins=200
    phiindex, bins_phi = pd.cut(data.phi, phibins, retbins=True)
    data.loc[:,"phiindex"]  = phiindex
    
    data.set_index("phi", inplace=True)
    plt.close('all')
    #plt.figure(24)
    #data.groupby("phiindex")['rho'].plot(legend=True) #.head(1)
    plotradial=data.groupby("phiindex")['rp'].head(5)
    
    rbins=200
    rindex, bins_r = pd.cut(data.r, rbins, retbins=True)
    data.loc[:,"rindex"]  = rindex
    
    bin_r = data.groupby("rindex").rp.mean().values
    pro_phi_r    = data.groupby("phiindex").rho.mean().values
    dict_r = {"r": bin_r,
          "phig": pro_phi_r}
    profiles_r    = pd.DataFrame(data=dict_r)
    profiles_r.plot("r","phig")
    #plotr=pd.DataFrame(gas.phi,rhor)
    