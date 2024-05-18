import numpy as np
import matplotlib.pyplot as plt
from ripser import ripser
from persim import plot_diagrams

plt.rcParams.update({
    "text.usetex": False,
})

def plotPersistenceDiagram(matrix):
    """
    Computes and plots the persistence diagram of a given matrix
    """
    # Calculer les diagrammes de persistance
    dgms = ripser(matrix)['dgms']
    
    # Créer une nouvelle figure
    plt.figure(figsize=(8, 8))
    
    # Calculer les bornes des axes pour la droite y = x
    max_birth = max(dgms[0][:, 0]) if len(dgms[0]) > 0 else 1
    
    # Tracer les diagrammes de persistance
    plot_diagrams(dgms, show=False)

    # Tracer la droite y = x en rouge en pointillés
    plt.plot([0, max_birth], [0, max_birth], 'r--', label='y = x')
    
    # Créer un polygone pour remplir la partie inférieure à la droite en gris foncé
    polygon = np.array([[0, 0], [max_birth, max_birth], [max_birth, 0]])
    plt.fill(polygon[:, 0], polygon[:, 1], color='darkgray', alpha=0.5)

    # Ajouter des labels et une légende
    plt.xlabel('Birth')
    plt.ylabel('Death')
    plt.legend()
    
    # Afficher la figure
    plt.show()
