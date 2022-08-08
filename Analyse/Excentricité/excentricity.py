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

# Définition des fonctions

# Programme principal
if __name__=='__main__':
    path = 'C:/Users/pierr/Documents/GitHub/phantomcomplete/Analyse/Excentricité/DATA'
    files = os.listdir(path)
    files_data = [i for i in files if i.startswith('sinks')]
    # files_ascii = [i for i in files if i.endswith('.ascii')]
    for sinks_file in files_data:
        header = ['Time','Rad(sph)','Tilt_sink','Twist_sink','Tilt_ID','Tilt_OD','Twist_ID','Twist_OD','Lin/Lp','Lout/Lp','Rel._misali','Sink-ID','Sink-OD','e','r']
        data = pd.read_csv(path+'/'+sinks_file, delim_whitespace=True,skiprows=1, header=None, names=header)  
        eccentricity_time = data['e'].tolist()
        time = data['Time'].tolist()
        # Study of eccentricity over time
        # print('The list extracted from the table is : ', eccentricity_time)
        plt.figure()
        plt.plot(time,eccentricity_time)
        plt.title("Evolution de l'excentricité au cours du temps")
        plt.xlabel('Temps')
        plt.ylabel('Excentricité')
        plt.ylim(0,1)
        plt.savefig(path+'/'+'ploteccentricty_%s.png'%(sinks_file))
        
        # Study of radius over time
        radius_time = data['r'].tolist()
        plt.figure()
        plt.plot(time,radius_time)
        plt.title("Evolution du rayon au cours du temps")
        plt.xlabel('Temps')
        plt.ylabel('Rayon')
        plt.savefig(path+'/'+'plotradius_%s.png'%(sinks_file))


        # Show flyby passage
        if sinks_file.endswith('1'):
            time_arr = np.array(time)
            radius_time_arr = np.array(radius_time)
            radius_criterium = 800
            
            time_interest = time_arr[radius_time_arr<radius_criterium]
            # print("Zone d'intérêt : ",time_interest)
        if sinks_file.endswith('2'):
            fig, ax = plt.subplots()
            ax.plot(time,eccentricity_time)
            eccentricity_time_arr = np.array(eccentricity_time)
            eccentricity_interest = eccentricity_time_arr[radius_time_arr<radius_criterium]
            ax.fill_between(time_interest, 0, eccentricity_interest, facecolor='green', alpha=0.5,label='Flyby')
            plt.legend()
            plt.xlabel('Temps')
            plt.ylabel('Excentricité')
            plt.xlim(0,50000)
            plt.savefig(path+'/'+'radiusstudy_%s.png'%(sinks_file))
    print('End of program !')
    plt.close('all')