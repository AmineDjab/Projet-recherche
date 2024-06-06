# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from ripser import ripser, lower_star_img
from persim import plot_diagrams
import PIL
import numpy as np

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
    plot_diagrams(dgms, show=False, lifetime=True)

    # Tracer la droite y = x en rouge en pointillés
    plt.plot([0, max_birth], [0, max_birth], 'r--', label='y = x')

    # Ajouter des labels et une légende
    plt.xlabel('Birth')
    plt.ylabel('Death')
    plt.legend()


def plotImagePersistenceDiagram(image):
    """
    Computes and plots the persistence diagram of a given image
    """
    dgm = lower_star_img(-image)

    plt.figure(figsize=(6, 6))
    plot_diagrams(dgm, lifetime=True)
