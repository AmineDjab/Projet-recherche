# -*- coding: utf-8 -*-

from os.path import dirname, join
import matplotlib.pyplot as plt
from processer.processer import plotPersistenceDiagram, plotImagePersistenceDiagram
from analyser.analyser import processImage, computeMNS_1
from processer.divergence import computeFrameDivergence

__PROJECT_ROOT_DIR = dirname(dirname(__file__))
__PROJECT_DATA_DIR = join(__PROJECT_ROOT_DIR,'data')

computeMNS_1(join(__PROJECT_DATA_DIR,'dsm'))
plotImagePersistenceDiagram(processImage(join(__PROJECT_DATA_DIR,'dsm'),30)[0])
matrixes = computeFrameDivergence(40, join(__PROJECT_DATA_DIR,'correlation'),DIVERGENCE=1,CURL=1)
for matrix_name, matrix in matrixes.items():
    plotPersistenceDiagram(matrix)
plt.show()
