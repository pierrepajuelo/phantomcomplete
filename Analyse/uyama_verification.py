# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 17:44:58 2022

@author: Pierre P.

Programme de vérification des données de Uyama à partir de l'algorithme conçu
"""
# Importation des modules
import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from skimage.transform import warp_polar
from scipy.optimize import curve_fit
# Modules personnels
from traitement import traitement 
from fit import conditions_initiales_loga, loga
# Définitions des fonctions 

# Programme principal 

if __name__=='__main__':
    path = 'D:/Downloads/Donnees_Uyama'
    files = os.listdir(path)
    for file in files:
        filename = path + '/' + file
        im = Image.open(filename)
        image = np.array(im)
        # Sélectionner le centre de l'image
        # plt.close('all')
        plt.figure()
        plt.imshow(
                    image[:,:,0]
                    #origin='lower'
                    )
        plt.title("Image déprojetée d'après Uyama et al., 2020")
        #%% Sélection du centre de l'image
        # center = plt.ginput(1)[0]
        center = (338.63336663336656, 330.42640692640686) # Valeur pas trop mal
        
        image_polar = warp_polar(
                                image[:,:,0],
                                radius = 500,
                                center = center[::-1])
        # %% Affiche de la polaire
        plt.close('all')
        plt.figure()
        plt.imshow(
                    image_polar.T,
                    origin='lower')
        plt.title("Image polaire d'après Uyama et al., 2020")
        
        # Récupération des données pour la spirale S1a (Uyama)
        data_s1 = plt.ginput(5)
        # data_s1 = [(285.6831250510496, 211.4986931307686),
         # (288.13350485992, 217.2162460181328),
         # (292.2174712080373, 224.5673854447439),
         # (297.93502409540156, 235.1856979498489),
         # (302.01899044351876, 246.6208037245773)] #Données sympa pour S1a
         
        y = np.radians([data_s1[i][0] for i in range(5)])
        x = np.array([data_s1[i][1] for i in range(5)])
        param, covariance = curve_fit(loga, y, x, p0=conditions_initiales_loga(x,y),maxfev=100000)
        lldeg = np.degrees(y)
        plt.plot(lldeg,
                 loga(y, *param),
                 linestyle='-',
                 c = 'red',
                 label=r'Fit loga, $r_0$=%s, k=%s, $\phi$=%s$^{\circ}$'%(param[0].round(decimals=2),param[1].round(decimals=2),-np.degrees(np.arctan(param[1].round(decimals=2)).round(decimals=2)).round(decimals=2)))
        plt.legend()
        
        
        
        
        
        
