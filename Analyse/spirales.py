import numpy as np

def spirales(data,polar_arr,direction,N,epsilonpos=6,epsilontheta=5,Taillemin=20):
    """
    
    Construction des spirales
    
    Parameters
    ----------
    data : array
        de taille (360,N) où N est le nombre de maximaux par direction azimutales, contient la position des maximaux.
    polar_arr : array
       contient les angles parcourus.
    direction : str
      "Bas" ou "Haut", choisit la direction radiales des spirales lors de la construction.
    N : int
        Nombre de maxima.
    epsilonpos : int, optional
        Tolérance radiale. The default is 6.
    epsilontheta :  int, optional
        Tolérance azimutale. The default is 5.
    Taillemin : int, optional
        Taille minimale des spirales. The default is 20.
        
    Returns
    -------
    None.

    """
    data=np.reshape(data,(360,N))
    spirales=np.zeros((1000,360,2))
    
    i=0 #On initialise le numéro de notre branche
    for theta in polar_arr: #On parcourt les différents angles
        if theta<np.shape(data)[0]: #On s'assure qu'on puisse atteindre theta
            for position in data[theta]: #On parcourt la direction radiale
                # Initialisation de la position
                position0=position
                # Initialisation de l'angle
                theta0=theta
                
                # On l'ajoute à la liste finale
                spirales[i,0,0]=position
                spirales[i,0,1]=theta
                
                # On retire de la liste la position initiale
                data[theta,np.where(data[theta]==position)]=np.nan
                #data=np.delete(data,np.where(data[theta]==position),axis=1)
                
                #On initialise notre branche
                j=1
                
                #On recherche la suite de la spirale
                thetap=1
                
                while theta0+thetap<np.shape(data)[0]: #On s'assure qu'on puisse parcourir
                    #print(theta0+thetap)
                    candidats=[] #On crée une liste des candidats potentiels pour la suite de la branche
                    #print(np.shape(data))
                    #print(data)
                    #print(data[theta0+thetap])
                    #print(np.shape(data[theta0+thetap]))
                    
                    
                    for positionsuiv in data[theta0+thetap]: #On parcourt la direction azimutale suivante
                        if np.abs(positionsuiv-position0)<epsilonpos:
                            candidats.append(positionsuiv) #On note les valeurs possibles
                    
                    #Dans le cas où il y en a 
                    if len(candidats)!=0:
                        #On choisit notre nouveau départ
                        if direction=='Bas':
                            nouveau=min(candidats)
                        if direction=='Haut':
                            nouveau=max(candidats)
                        
                        
                        
                        #On l'ajoute à la liste finale
                        spirales[i,j,0]=nouveau
                        spirales[i,j,1]=theta0+thetap
                        
                        # On retire de la liste la position finale
                        #data=np.delete(data,np.where(data[theta0+thetap]==nouveau),axis=1)
                        data[theta0+thetap,np.where(data[theta0+thetap]==nouveau)]=np.nan
                        
                        # On initialise la nouvelle position
                        position0=nouveau
                        theta0+=thetap
                        thetap=1
                        
                        # On continue notre branche
                        j+=1     
                    if len(candidats)==0: # Si jamais pas de candidats à thetap+theta0
                        if theta0+thetap+1<np.shape(data)[0]: # Si jamais on peut
                            if thetap<epsilontheta: #On met un angle limite de séparation
                                thetap+=1 #On parcourt la suite
                                continue   
                            else:
                                break
                        # Si jamais on peut pas continuer
                        else:
                            break
                if j>Taillemin:
                    #On crée une nouvelle branche
                    i+=1
    return(spirales)
