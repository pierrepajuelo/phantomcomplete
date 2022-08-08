# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 16:24:58 2022

@author: Pierre
"""

# Importation des librairies
import numpy as np 
import os 
import matplotlib.pyplot as plt

from ellipse import LsqEllipse
from matplotlib.patches import Ellipse
# For read_header
import re 

# Définition des fonctions
def read_header( file ):
    """
      read the x, y and v plot limits from the .pix header lines
    """
    pat = re.compile(r'.*min\s*=\s+(\S+)\s+max\s*=\s+(\S+)')
    fh = open(file, 'r')
    count = 0
    got = 0
    xmin = np.full((3),0.)
    xmax = np.full((3),1.)
    while (count < 10):
       count += 1

       # Get next line from file
       line = fh.readline()

       # if line is empty
       # end of file is reached
       if not line:
          break

       # otherwise match lines like "min = 0.000 max = 1.000"
       if (pat.match(line)):
          [m] = pat.findall(line)
          xmin[got] = m[0]
          xmax[got] = m[1]
          got += 1

    return (xmin[2],xmax[2],xmin[1],xmax[1],xmin[0],xmax[0])

# Programme principal


if __name__=='__main__':
    # Filename
    path = 'C:/Users/pierr/Documents/STAGE_L3'
    files = os.listdir(path)
    files_dump = [i for i in files if i.endswith('.pix')]
    for dump in files_dump:
        # Chargement des données
        image_originale = np.loadtxt(path+'/'+dump)
        # Lecture des données concernant l'image
        xmin,xmax,ymin,ymax,vmin,vmax = read_header(path+'/'+dump)
        # Affichage de l'image originale
        plt.close('all')
        plt.figure()
        plt.imshow(image_originale,
                vmin=vmin,
                vmax=vmax,
                cmap='inferno', 
                origin='lower')
        cbar = plt.colorbar(cmap='inferno')
        cbar.set_label('Echelle de densité')
        plt.title('Image originale')

        # Finding coordinates 
        list_test = np.where(image_originale>-0.1)
        X = list_test[0]
        Y = list_test[1]
        plt.plot(Y,X,'+',ms=1,label='Marqueurs')
        plt.legend()
        # print('Coordonnées : ',list_test)
        
        # Finding the ellipse
        data = np.array(list(zip(Y, X)))
        reg = LsqEllipse().fit(data)
        center, width, height, phi = reg.as_parameters()

        print(f'center: {center[0]:.3f}, {center[1]:.3f}')
        print(f'width: {width:.3f}')
        print(f'height: {height:.3f}')
        print(f'phi: {phi:.3f}')

        fig = plt.figure(figsize=(6,6))
        ax = plt.subplot()
        ax.axis('equal')
        
        ax.imshow(image_originale,
                vmin=vmin,
                vmax=vmax,
                cmap='inferno', 
                origin='lower')
        #cbar = fig.colorbar(ax=ax,cmap='inferno')
        #cbar.set_label('Echelle de densité')

        ellipse = Ellipse(
        xy=center, width=2*width, height=2*height, angle=np.rad2deg(phi),
        edgecolor='b', fc='None', lw=2, label='Ellipse ajustée', zorder=2
        )
        ax.add_patch(ellipse)
        plt.legend()
        plt.title('Détection d une ellipse')
        
        
    