# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from ripser import ripser
from persim import plot_diagrams

def plotPersistenceDiagram(matrix):
    """
    Computes and plots the persistence diagram of a given matrix
    """
    dgms = ripser(matrix)['dgms']
    plot_diagrams(dgms, show=True)
    plt.show()
