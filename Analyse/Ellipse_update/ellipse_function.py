# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 13:28:37 2022

@author: pierr
"""
# Importation des librairies 
import numpy as np
from ellipse import LsqEllipse
# Définitions des fonctions
def ellipse_center(file,path,seuil=-0.1):
    '''
    
    Parameters
    ----------
    file : string
        Name of the file.
    path : string
        Path of the file.
    seuil : float, optional
        Seuil de détection de l'ellipse. The default is -0.1.

    Returns
    -------
    Coordinates of the center of the ellipse.

    '''

    # Chargement de l'image
    image_originale = np.loadtxt(path+'/'+file)
    # Finding coordinates 
    points = np.where(image_originale>seuil)
    X = points[0]
    Y = points[1]
    # Finding the ellipse
    data = np.array(list(zip(Y, X)))
    reg = LsqEllipse().fit(data)
    center, width, height, phi = reg.as_parameters()
    return(center)
# Programme principal

if __name__=='__main__':
    pass
