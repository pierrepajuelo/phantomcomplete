# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 17:20:08 2022

@author: pierr
"""
# Importation des librairies
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd
import math
# Ellipse Fitting
from skimage.measure import EllipseModel
from matplotlib.patches import Ellipse
import matplotlib
from scipy.signal import argrelextrema
import re
from PIL import Image
import scipy
import cv2
from skimage.transform import warp_polar, rotate, rescale
from skimage.util import img_as_float
import polarTransform
from scipy.interpolate import interp1d
import traceback

# Importation des librairies personnelles
from spirales import *
from traitement import *
from minima import *
from fit import *
from HD34700 import *
#Accélération de python
#from numba import jit
#@jit(nopython=True, parallel = True)

# Définition des fonctions
def radial_profile(data, center): #Non utilisé
    y, x = np.indices((data.shape))
    r = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    r = r.astype(np.int)

    tbin = np.bincount(r.ravel(), data.ravel())
    nr = np.bincount(r.ravel())
    radialprofile = tbin / nr
    return radialprofile 

def get_cmap(n, name='hsv'):
    '''
    Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.
    '''
    return plt.cm.get_cmap(name, n)
# Programme principal

"""
Caractérisation des spirales d'un disque
"""
if __name__=="__main__":
    #Chargement des fichiers
    Folder_name = 'D:/Stage/PSMN/Plot_Rapport'
    # files=os.listdir('D:/Stage/Analyse/spirales') #Windows
    files=os.listdir(Folder_name)
    #files=os.listdir('/mnt/d/Stage/PSMN/HD34700') #Linux
    # files=os.listdir('/mnt/d/Stage/Analyse/spirales')
    #Création des listes utiles
    files_data = [i for i in files if i.endswith('.ascii')]
    # files_data=files_data[0]
    precession = [i for i in files if i.endswith('.dat')][0]
    files_pix=[i for i in files if i.endswith('.pix')]
    files_png=[i for i in files if i.endswith('.png')]
    files_tif=[i for i in files if i.endswith('.tif')]
    # filetif=files_tif[0]
    # Rendering via Splash
    # file2=files_pix[2]
    Anglesspirales=[]
    Numerofichier=0
    Nombrefichiers=len(files_pix)
    #%%
    for file in files_tif:
        try:
            file = Folder_name +'/' +file
            
            im = Image.open(file)
            imarray=np.array(im)
            image_transformed=traitement_png(imarray[:,:,1],inclinaison=40.9,PA=-60,radius=600)
            plt.close('all')
            plt.figure()
            plt.imshow(image_transformed,
                       origin='lower',
                       cmap='inferno')
            cbar = plt.colorbar(cmap='inferno')
            cbar.set_label('Flux de luminosité')
            plt.title('Image observée déprojetée avec i=40.9°, PA=60°')
            polar=warp_polar(img_as_float(rotate(image_transformed,180)),
                             radius=400
                             # center=(center[0][1],center[0][0])
                             )
            plt.figure()
            plt.imshow(polar.T,
                       origin='lower',
                       cmap='inferno')
            cbar = plt.colorbar(cmap='inferno')
            cbar.set_label('Flux de luminosité')
            plt.title('Image polaire observée déprojetée avec i=40.9°, PA=60°')
            
            polar_arr=np.linspace(0,359,360,dtype=int)
            image_polar_crame=np.copy(polar)
            vmin=0
            vmax=1
            # image_polar_crame[image_polar_crame>0.9]=vmin
            # image_polar_crame[image_polar_crame<0.1]=vmin
            psarrbis=maxima_locaux(polar_arr,image_polar_crame,Nmaxmaxima=6)
           
            # psarrreel=maxima_locaux(polar_arr,image_polar_reel,Nmaxmaxima=3)
        
            psarrcopy=np.copy(psarrbis)
           
            # psarrreelcopy=np.copy(psarrreel)
            
            # Construction des spirales
            spiralesarr=spirales(psarrbis,polar_arr,direction="Haut",N=6,epsilonpos=6,epsilontheta=3,Taillemin=50)
            # spiralesarrreel=spirales(psarrreel,polar_arr,direction="Haut",N=3,epsilonpos=6,epsilontheta=3,Taillemin=50)
            # Mise en forme de l'array
            spiralesarr[spiralesarr==0]=np.nan
            spiralesarr[spiralesarr==400]=np.nan
            
            
            # spiralesarrreel=np.where(spiralesarrreel==0,np.nan,spiralesarrreel)
            # spiralesarrreel=np.where(spiralesarrreel==200,np.nan,spiralesarrreel)
            
            # Affichage des spirales
            fin=0
            #Initialisation de la polaire
            # image_polaire=traitement(filename,radius=400)[2]
            plt.figure()
            plt.imshow(polar.T,
                       vmin=vmin,
                       vmax=vmax,
                       cmap='inferno', 
                       origin='lower')
            cbar = plt.colorbar(cmap='inferno')
            cbar.set_label('Flux de luminosité')
            #plt.figure(1000)
            for i in range(100):
                for k in range(np.shape(spiralesarr)[1]):
                    if np.isnan(spiralesarr[i,k,0])==False:
                        
                        fin+=1
                        break
            rayon_limite=50
            # Fit des bras
            Out,Polar_arrays=fitting(spiralesarr,polar_arr,fin-1,fonction='Logarithme')
                
            for i in range(fin-1):
                plot='True'
                for rayon in spiralesarr[i,:,0]:
                    if rayon<rayon_limite:
                        plot='False'
                if plot=='True':
                    def get_cmap(n, name='hsv'):
                        '''
                        Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
                        RGB color; the keyword argument name must be a standard mpl colormap name.
                        '''
                        return plt.cm.get_cmap(name, n)
                    cmap = get_cmap(fin)
                    plt.plot(spiralesarr[i,:,1],spiralesarr[i,:,0],lw=2,c=cmap(i),label='Spirale %s'%i)
                    np.savetxt("obs_spirale_%s.csv"%i, np.sqrt(np.diag(Out[1][i])), delimiter=";")
                    # Anglesspirales.append([-np.degrees(np.arctan(param[1].round(decimals=2)).round(decimals=2)).round(decimals=2) for param in Out[0]])
                    # tt=np.linspace(np.min(x),np.max(x),100)
                    # ll=np.linspace(0,2*np.pi,200)
                    ll = Polar_arrays[i]
                    # lldeg=np.degrees(ll)
                    lldeg = np.degrees(Polar_arrays[i])
                    param=Out[0][i]
                    plt.plot(lldeg, loga(ll, *param), linestyle='-',c=cmap(i),label=r'Fit loga, $r_0$=%s, k=%s, $\phi$=%s$^{\circ}$'%(param[0].round(decimals=2),param[1].round(decimals=2),-np.degrees(np.arctan(param[1].round(decimals=2)).round(decimals=2)).round(decimals=2)))
                    # for param in Out[0]:
                        #plt.plot(ll, archimede(ll, *param), color='darkgreen', linestyle='--',label='Fit archi, a=%s, b=%s, n=%s'%(param[0].round(decimals=2),param[1].round(decimals=2),param[2].round(decimals=2)))
                        # 
            plt.legend(loc='upper center',
                       bbox_to_anchor=(-0.4, 0.8),
                       ncol=1,
                       fancybox=True,
                       shadow=True)
            plt.ylim(0,400)
            
            plt.title('Image déprojetée avec PA = %s°, i = %s°'%(round(60,ndigits=2),round(40.9,ndigits=2)))
            # plt.savefig(Folder_name+'/spirales_observee_test.png')
            '''
            # ,image_polar,center,radius
            # Reshape
            image_resize = cv2.resize(image_transformed, (1066,782),interpolation = cv2.INTER_NEAREST)
            plt.close('all')
            plt.figure()
            plt.imshow(image_resize,origin='lower',cmap='inferno')
            plt.colorbar()
            
            
            plt.close('all')
            plt.figure()
            plt.imshow(rotate(image_resize,180),origin='lower',cmap='inferno')
            # center=plt.ginput(1)
            
        
            plt.close('all')
            plt.figure()
            polar=warp_polar(img_as_float(rotate(image_resize,180)),
                             radius=400
                             # center=(center[0][1],center[0][0])
                             )
            plt.imshow(polar.T,origin='lower',cmap='inferno')
            '''
        except Exception as e: 
            print(traceback.format_exc())
    #%%
    Numerofichier=0
    for nfile,file in enumerate(files_pix):
        try:
            # if nfile==1:
                # continue
            # filename='D:/Stage/Analyse/spirales/'+file #Windows
            filename = Folder_name+'/'+file
            # precession_data = open(Folder_name+'/precession.dat', 'r')
            if nfile==0:
                precession_data = open(Folder_name+'/precession.dat', 'r')
            if nfile==1:
                precession_data = open(Folder_name+'/precession-S5.dat', 'r')
            for n,line in enumerate(precession_data):
                line = line.strip()
                columns = line.split()
                if n==2:
                    PA_real = columns[5]
                    Inclinaison_real = columns[4]
                    print(PA_real)
                    print(Inclinaison_real)
            # filename='/mnt/d/Stage/PSMN/HD34700/'+file
            #filename='/mnt/d/Stage/Analyse/spirales/'+file
            print('Fichier numéro %s/%s'%(Numerofichier,Nombrefichiers))
            Numerofichier+=1
            
            # Image réelle
            # im = Image.open(filetif)
            # imarray=np.array(im)
            
            #image_transformed,image_polar_reel=traitement_png(imarray[:,:,0],inclinaison=40.9,PA=-60,radius=600)

            # Image simulation
            # PA_image = 60
            PA_image = float(PA_real)
            # Inclinaison_Image = 40.9
            Inclinaison_Image = float(Inclinaison_real)
            img,img4,image_polar,xmin,xmax,ymin,ymax,vmin,vmax,coef=traitement(filename,radius=400,PA=PA_image,inclinaison=Inclinaison_Image)
            
            
            # Affichage des plots
            plt.close('all')
            plt.figure()
            plt.imshow(img,
                       vmin=vmin,
                       vmax=vmax,
                       cmap='inferno', 
                       origin='lower')
            plt.colorbar(cmap='inferno')
            plt.title('Image originale')
            
            plt.figure()
            plt.imshow(img4,
                       vmin=vmin,
                       vmax=vmax,
                       cmap='inferno', 
                       origin='lower')
            cbar = plt.colorbar(cmap='inferno')
            plt.title('Image déprojetée avec PA = %s°, i = %s°'%(round(PA_image,ndigits=2),round(Inclinaison_Image,ndigits=2)))
            # plt.savefig(Folder_name+'/img_modified_flyby.png')
            cbar.set_label('Densité de colonne logarithmique')
            
            # Construction de la liste des maxima
            polar_arr=np.linspace(0,359,360,dtype=int)
            image_polar_crame=np.copy(image_polar)
            if nfile==0:
                image_polar_crame[image_polar_crame>vmax*0.9]=vmin
                image_polar_crame[image_polar_crame<vmin*0.6]=vmin
            if nfile==1:
                image_polar_crame[image_polar_crame>vmax*0.7]=vmax
                image_polar_crame[image_polar_crame<vmin*0.6]=vmin
            psarrbis=maxima_locaux(polar_arr,image_polar_crame,Nmaxmaxima=6)
           
            # psarrreel=maxima_locaux(polar_arr,image_polar_reel,Nmaxmaxima=3)
        
            psarrcopy=np.copy(psarrbis)
           
            # psarrreelcopy=np.copy(psarrreel)
            
            # Construction des spirales
            spiralesarr=spirales(psarrbis,polar_arr,direction="Haut",N=6,epsilonpos=6,epsilontheta=3,Taillemin=20)
            # spiralesarrreel=spirales(psarrreel,polar_arr,direction="Haut",N=3,epsilonpos=6,epsilontheta=3,Taillemin=50)
            # Mise en forme de l'array
            spiralesarr[spiralesarr==0]=np.nan
            spiralesarr[spiralesarr==400]=np.nan
    
            # spiralesarrreel=np.where(spiralesarrreel==0,np.nan,spiralesarrreel)
            # spiralesarrreel=np.where(spiralesarrreel==200,np.nan,spiralesarrreel)
            
            # Affichage des spirales
            fin=0
            #Initialisation de la polaire
            # image_polaire=traitement(filename,radius=400)[2]
            plt.figure()
            plt.imshow(image_polar.T,
                       vmin=vmin,
                       vmax=vmax,
                       cmap='inferno', 
                       origin='lower')
            cbar = plt.colorbar(cmap='inferno')
            cbar.set_label('Densité de colonne logarithmique')
            #plt.figure(1000)
            for i in range(100):
                for k in range(np.shape(spiralesarr)[1]):
                    if np.isnan(spiralesarr[i,k,0])==False:
                        
                        fin+=1
                        break
            rayon_limite=50
            # Fit des bras
            Out,Polar_arrays=fitting(spiralesarr,polar_arr,fin-1,fonction='Logarithme')
            for i in range(fin-1):
                plot='True'
                for rayon in spiralesarr[i,:,0]:
                    if rayon<rayon_limite:
                        plot='False'
                if plot=='True':
                    
                    cmap = get_cmap(fin)
                    plt.plot(spiralesarr[i,:,1],spiralesarr[i,:,0],lw=2,c=cmap(i),label='Spirale %s'%i)
                    np.savetxt("file%s_spirale_%s.csv"%(Numerofichier,i), np.sqrt(np.diag(Out[1][i])), delimiter=";")
                    # Anglesspirales.append([-np.degrees(np.arctan(param[1].round(decimals=2)).round(decimals=2)).round(decimals=2) for param in Out[0]])
                    # tt=np.linspace(np.min(x),np.max(x),100)
                    # ll=np.linspace(0,2*np.pi,200)
                    ll = Polar_arrays[i]
                    # lldeg=np.degrees(ll)
                    # Pour n'avoir que les spirales à l'endroit des datas
                    lldeg = np.degrees(Polar_arrays[i])
                    param=Out[0][i]
                    plt.plot(lldeg, loga(ll, *param), linestyle='-',c=cmap(i),label=r'Fit loga, $r_0$=%s, k=%s, $\phi$=%s$^{\circ}$'%(param[0].round(decimals=2),param[1].round(decimals=2),-np.degrees(np.arctan(param[1].round(decimals=2)).round(decimals=2)).round(decimals=2)))
            # for param in Out[0]:
                #plt.plot(ll, archimede(ll, *param), color='darkgreen', linestyle='--',label='Fit archi, a=%s, b=%s, n=%s'%(param[0].round(decimals=2),param[1].round(decimals=2),param[2].round(decimals=2)))
                         
            plt.legend(loc='upper center',
                       bbox_to_anchor=(-0.4, 0.9),
                       ncol=1,
                       fancybox=True,
                       shadow=True)
            plt.ylim(0,400)
            
            plt.title('Image déprojetée avec PA = %s°, i = %s°'%(round(PA_image,ndigits=2),round(Inclinaison_Image,ndigits=2)))
            # plt.savefig(Folder_name+'/spirales_flyby.png')
            # fin2=0  
            # for i in range(100):
                # for k in range(np.shape(spiralesarrreel)[1]):
                    # if np.isnan(spiralesarrreel[i,k,0])==False:
                        # plt.plot(spiralesarr[i,:,1],spiralesarr[i,:,0],lw=2,label='spirale %s'%i)
                        # fin2+=1
                        # break
                    
            print('Fichier numéro %s/%s traité !'%(Numerofichier,Nombrefichiers))
        except Exception as e: 
            print(traceback.format_exc())
            Anglesspirales.append([np.nan])
            print(Numerofichier,' : Erreur !')
            pass
    
    print('End of program !')
    
    
        