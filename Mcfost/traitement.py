import numpy as np
import math
import cv2
import re
import scipy
from skimage.transform import warp_polar
from skimage.util import img_as_float
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

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

    return xmin[2],xmax[2],xmin[1],xmax[1],xmin[0],xmax[0]

def traitement(filename,inclinaison=40.9,PA=60,radius=200):
    """
    Traitement d'une image au format .ascii et ressort l'image originale, l'image transformée et la projection polaire.

    Parameters
    ----------
    filename : str
        Nom du fichier (au format 'folder/file').
    inclinaison : float
        Angle d'inclinaison du disque en degrés.
    PA : float
        Angle de position du disque en degrés.
    radius : int
        Rayon de projection polaire.

    Returns
    -------
    Arrays de l'image originale, l'image transformée, la projection polaire et les arguments d'intensité.

    """    
    # Importation du fichier
    image_original = np.loadtxt(filename,skiprows=9)
    # Récupère les données de l'image
    xmin,xmax,ymin,ymax,vmin,vmax = read_header(filename)
    # Transformation spatiale
    # PA déprojetée
    img2=scipy.ndimage.rotate(image_original,angle=PA)
    
    # Inclination déprojetée
    coef=1/np.cos(math.radians(inclinaison))
    rows, cols = np.shape(img2)
    image_transformed = cv2.resize(img2, (int(rows*coef), cols),interpolation = cv2.INTER_NEAREST)
    
    # Polaire
    image = img_as_float(image_transformed)
    image_polar = warp_polar(image, radius=radius) #, channel_axis=1)
    
    '''
    #Brouillon
    
    
    taille=np.shape(img2)[0]
    a = np.zeros((taille,taille))
    np.fill_diagonal(a,1/np.cos(math.radians(inclinaison)))
    
    coef=1/np.cos(math.radians(40.9))
    decalage=200*coef
    src=img2
    srcTri = np.array( [[0, 0], [src.shape[1]-1, 0], [0, src.shape[0] - 1]] ).astype(np.float32)
    dstTri = np.array( [[0, 0], [src.shape[1]*coef, 0], [0, src.shape[0] - 1]] ).astype(np.float32)
    warp_mat = cv2.getAffineTransform(srcTri, dstTri)
    
    
    quarter_height, quarter_width = 0, -decalage
    T = np.float32([[1, 0, quarter_width], [0, 1, quarter_height]])
    
    img3 = cv2.warpAffine(src, warp_mat, (src.shape[1], src.shape[0]))
    #img3=scipy.ndimage.affine_transform(img2,warp_mat)
    
    
    img4 = cv2.warpAffine(img3, T, (src.shape[1], src.shape[0]))

    
    d=np.sqrt((800*np.sin(math.radians(60))*coef)**2+(800*np.cos(math.radians(60)))**2)
    
    
    lx,ly=np.shape(img4)
    conversion=d/700
    
    dy=np.sqrt((800*np.cos(math.radians(60))*coef)**2+(800*np.sin(math.radians(60)))**2)
    conversiony=dy/700
    xmin=-lx/2*conversion
    xmax=lx/2*conversion
    
    ymin=-ly/2*conversiony
    ymax=ly/2*conversiony
    '''
    
    return(image_original,image_transformed,image_polar,xmin,xmax,ymin,ymax,vmin,vmax,coef)


def traitement_png(filename,vmin,vmax,inclinaison=40.9,PA=60,radius=200):
    """
    Traitement d'une image au format .ascii et ressort l'image originale, l'image transformée et la projection polaire.

    Parameters
    ----------
    filename : str
        Nom du fichier (au format 'folder/file').
    vmin : float
        Intensité minimale de l'image originale.
    vmax : float 
        Intensité maximale de l'image originale.
    inclinaison : float
        Angle d'inclinaison du disque en degrés.
    PA : float
        Angle de position du disque en degrés.
    radius : int
        Rayon de projection polaire.

    Returns
    -------
    Arrays de l'image originale, l'image transformée, la projection polaire et les arguments d'intensité.

    """    
    # Importation du fichier
    #image_original = np.loadtxt(filename)
    # Transformation spatiale
    # PA déprojetée
    img2=scipy.ndimage.rotate(filename,angle=PA)
    
    # Inclination déprojetée
    coef=1/np.cos(math.radians(inclinaison))
    rows, cols = np.shape(img2)
    image_transformed = cv2.resize(img2, (int(rows*coef), cols),interpolation = cv2.INTER_NEAREST)
    
    plt.figure(2)
    plt.imshow(image_transformed,
               cmap='inferno',
               vmin=vmin,
               vmax=vmax,
               origin='lower')
    plt.show()
    center=plt.ginput(1)
    # Polaire
    image = img_as_float(image_transformed)
    image_polar = warp_polar(image, radius=radius,center=(center[0][1],center[0][0])) #, channel_axis=1)
    
    
    return(image_transformed,image_polar,center,radius)

def maxima_locaux(polar_arr,image_polar,Nmaxmaxima=6):
    """
    
    Génère une liste contenant les maxima locaux de l'image.

    Parameters
    ----------
    polar_arr : array
        Array contenant la valeur des angles en degré.
    image_polar : array
        Image à traiter.
    Nmaxmaxima : int, optional
        Nombre de maxima à retourner. The default is 6.

    Returns
    -------
    Array contenant les maximas, avec shape=(360,6).

    """
    points_spirales=[]
    
    
    for theta in polar_arr:
        max_locaux=argrelextrema(image_polar[theta],np.greater,order=3)[0][:Nmaxmaxima]
        
        if np.shape(max_locaux)[0]==0:
            max_locaux=np.array([200],dtype=int)
        if np.shape(max_locaux)[0]<Nmaxmaxima:
            l=Nmaxmaxima-np.shape(max_locaux)[0]
            liste=np.zeros(l)
            
            max_locaux=np.hstack((max_locaux,liste))
        max_locaux=max_locaux.astype(int)
        points_spirales.append(max_locaux.tolist())
    
    psarrbis=np.array(points_spirales)
    
    psarrbis=np.where(psarrbis==0,np.nan,psarrbis)
    return(psarrbis)

def bordures(image_polar,polar_arr,vmin,var,epsilon=0.2):
    polar=np.copy(image_polar)
    bordures=[[],[]]
    for theta in polar_arr:
        # angle_rad=np.radians(theta)
        # polar[theta]=polar[theta]*1/np.sqrt(np.cos(angle_rad)**2*var**2+np.sin(angle_rad)**2)
        liste=np.where(polar[theta,:300]>vmin+epsilon)[0]
        bordure_interne=liste[0]
        bordure_externe=liste[-1]
        bordures[0].append(bordure_interne)
        bordures[1].append(bordure_externe)
    return(bordures)
    