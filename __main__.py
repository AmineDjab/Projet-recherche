# -*- coding: utf-8 -*-

from processer.processer import plotPersistenceDiagram
from analyser.analyser import processImage
from processer.divergence import computeFramesDivergence

plotPersistenceDiagram(processImage("C:/Users/djab-/OneDrive/Bureau/Projet recherche/E494/dsm",30)[0])
matrixes = computeFramesDivergence([40,41],"C:/Users/djab-/OneDrive/Bureau/Projet recherche/E494/correlation",DIVERGENCE=1)
for matrix_name, matrix in matrixes.items():
    plotPersistenceDiagram(matrix)
