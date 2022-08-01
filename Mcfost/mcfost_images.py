# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 13:42:35 2022

MCFOST routine for creating images

@author: Pierre PAJUELO
"""
# Importation des librairies
import matplotlib.pyplot as plt
import pymcfost
import os 
# import numpy as np
import importlib
importlib.reload(pymcfost)
# from skimage.transform import warp_polar, rotate, rescale
# from tqdm import tqdm
import sys
import getopt



# Importation des librairies personnelles
from mcfost_psmn import position_sink
# from traitement import traitement_png
# Définitions des fonctions 
def plot_mcfost(dossier,longueurdonde=1.229,d=356.5):
    # Récupérer les données des sinks
    file = dossier[9:]
    xsink,ysink,zsink,xplanet,yplanet,zplanet = position_sink(file)
    # rplanet
    # Converting into arcsec
    xsink = xsink/d
    ysink = ysink/d
    image = pymcfost.Image("./%s/data_%s/"%(dossier,longueurdonde))
    
    # PLOT
    cbar = True
    no_ylabel = False
    shift_dx=xsink
    shift_dy=ysink
    # axes_unit='au' # Converting into au (Not wanted here)
    # rescale_r2=True # Rescaling with R^2 (Not wanted here)
    # limits=[0.60,-0.70,-0.60,0.5] # Adapted limits
    plt.close('all') # Clean all figures
    plt.figure(1,figsize=(7,6))
    # vmin=2*1e-18
    # vmax=1e-16
    # Memory
    # vmin=5*1e-4
    # vmax=1e-2
    vmin = 7*1e-17
    vmax = 3*1e-18
    typeimg='I'
    image.plot(#axes_unit=axes_unit,
               shift_dx=-shift_dx, 
               shift_dy=-shift_dy, 
               vmin=vmin,
               vmax=vmax,
               colorbar=cbar, 
               no_ylabel=no_ylabel,
               plot_stars=True,
               # limits=limits,
               # rescale_r2=rescale_r2,
               type=typeimg
               )
    plt.savefig('Rendering_MCFOST_%s.png'%(dossier))
    
def plot_qphi_mcfost(dossier,longueurdonde=1.229,d=356.5):
    # Récupérer les données des sinks
    file = dossier[9:]
    xsink,ysink,zsink,xplanet,yplanet,zplanet = position_sink(file)
    # rplanet
    # Converting into arcsec
    xsink = xsink/d
    ysink = ysink/d
    image = pymcfost.Image("./%s/data_%s/"%(dossier,longueurdonde))
    # print("Taille de l'array image : ",image.image.shape[0])
    shift_dx=xsink
    shift_dy=ysink
    
    # PLOT
    plt.close('all') # Clean all figures
    plt.figure(1,figsize=(7,6))
    cbar = True
    no_ylabel = False
    image.plot(#axes_unit=axes_unit,
                    type="Qphi",
                    vmax=5*1e-18,
                    vmin=5*1e-21,
                    shift_dx=-shift_dx, 
                    shift_dy=-shift_dy, 
                    colorbar=cbar,
                    no_ylabel=no_ylabel,
                    plot_stars=True,
                    # pola_vector=True,
                    nbin=15)
    # plt.gca().invert_xaxis()
    plt.savefig('Rendering_MCFOST_Qphi_%s.png'%(dossier))
    
    
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
    
    if len(folder)!=0:
        files=os.listdir()
        files_rendering=[i for i in files if i.startswith('rendering%s'%(folder))] 
        for dossier in files_rendering:
            plot_mcfost(dossier)
            plot_qphi_mcfost(dossier)
    if len(simulationfile)!=0:
        plot_mcfost(simulationfile)
        # plot_qphi_mcfost(simulationfile)
    # !!! Brouillon !!!
    # and not i.endswith('pa')]
    # print('Liste des fichiers à traiter : ',files_rendering)
    # halfsize = np.asarray(image_1mum.image.shape[-2:]) /2 *image_1mum.pixelscale
    # plt.gca().invert_yaxis()
    
    # if dossier.endswith('pa'):
    #     plt.savefig('Rendering_%s_pa.png'%(file))
    # if dossier.endswith('ta'):
    #     plt.savefig('Rendering_%s_final.png'%(file))
    #     print('Saved !')
    # else:
    #     plt.savefig('Rendering_%s.png'%(file))
    

    # for dossier in tqdm(files_rendering):
    #     if dossier.endswith('pa'):
    #         # file=dossier[9:-3]
    #         continue
    #     if dossier.endswith('ta'):
    #         file=dossier[9:-3]
    #         if not file.endswith('153'):
    #             continue
    #     else:
    #         # file=dossier[9:]
    #         continue
        
    #     # print(dossier)
        
        
    #     e=0.9
    #     positionangle=np.degrees(np.arctan(yplanet/xplanet))
    #     print('Demi grand-axe : ',rplanet/(1+e))
    #     print('Angle de position : ',positionangle)
        
    # if dossier.endswith('pa'):
    #     plt.savefig('Renderingpolar_%s_pa.png'%(file))
    # else:
    #     plt.savefig('Renderingpolar_%s.png'%(file))
        
        
        
        
        
        
        # img=image_1mum.image[0, 0, 0, :, :]
        # vmin=2*1e-18
        # vmax=1e-16

        # plt.close('all')
        # image_transformed,image_polar,center,radius=traitement_png(img,
        #                                                            PA=50,
        #                                                            inclinaison=57,
        #                                                            vmin=vmin,
        #                                                            vmax=vmax)
        
        
        
        
        
        # plt.close('all')
        # plt.figure(1,figsize=(7,6))
        # # fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15,4))
        
        # cbar = True
        # no_ylabel = False
        # shift_dx=xsink
        # shift_dy=ysink
        # vmin=2*1e-18
        # vmax=1e-16
        # typeimg='I'
        # image_1mum.plot(
        #                 # ax=axes[0],
        #                 shift_dx=-shift_dx, 
        #                 shift_dy=-shift_dy, 
        #                 vmin=vmin,
        #                 vmax=vmax,
        #                 colorbar=cbar, 
        #                 no_ylabel=no_ylabel,
        #                 # plot_stars=True,
        #                 type=typeimg,
        #                 coronagraph=10
        #                 )
        
        # plt.figure(3,figsize=(9,6))
        # plt.imshow(image_transformed,
        #            origin='lower',
        #            cmap='inferno',
        #            vmin=vmin,
        #            vmax=vmax)
        # plt.colorbar(cmap='inferno')
        # plt.title('Transformed image')
        # plt.xlabel('x (pix.)')
        # plt.ylabel('y (pix.)')
        
        
        
        # plt.figure(4,figsize=(9,6))
        # plt.imshow(image_polar.T,
        #            origin='lower',
        #            cmap='inferno',
        #            vmin=vmin,
        #            vmax=vmax)
        
        # plt.colorbar(cmap='inferno')#,ax=axes[2]) im2,
        # plt.title('Polar plot of Radiative Transfer Image')
        # plt.xlabel(r'Angles $\theta$ (deg.)')
        # plt.ylabel('Distance au centre (pix.)')
        # plt.tight_layout()
        # # plt.xlim(0,360)
        # # plt.ylim(0,radius)
        
        # # im3=plt.imshow(img, 
        # #                cmap='inferno',
        # #                vmin=vmin,
        # #                vmax=vmax,
        # #                origin='lower')
        # # plt.colorbar(im1,cmap='inferno',ax=axes[2])
        # # plt.title('Original image')
        # # plt.xlabel('x (pix.)')
        # # plt.ylabel('y (pix.)')
    
        
        '''
        polar=warp_polar(img,radius=200)
        plt.close('all')
        plt.figure(n+200,figsize=(10,7))
        plt.imshow(img,origin='lower',cmap='inferno')#,vmin=vmin,vmax=vmax)#,extent=[xmin,xmax,ymin,ymax]
        # plt.xlim(0,2*np.pi)
        # plt.ylim(0,200)
        # plt.colorbar(cmap='inferno')
        plt.savefig('Renderingpolarpolar%s.png'%(file))
        #a=input('Ok ?')
        '''
    print('End of program !')