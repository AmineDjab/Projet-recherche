import imageio
from os.path import join
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import median_filter

MNS_1 = None
RESOLUTION  = 0.14

def computeMNS_1(source_directory_path):
    global MNS_1
    MNS_1 = imageio.imread(join(source_directory_path,'DSC_1','dsm.tif'))


def processImages(source_directory_path,image_numbers):
    computeMNS_1(source_directory_path)
    for image_number in image_numbers:
        processImage(source_directory_path,image_number)


def processImage(source_directory_path,image_number):
    global MNS_1
    DSC = f'DSC_{image_number}'
    MNS = imageio.imread(join(source_directory_path,DSC,"dsm.tif"))
    MNS1 = imageio.imread(join(source_directory_path,DSC,"dsm.tif"))
    MNS = MNS - MNS_1
    MNS = MNS * 1e3
    MNS = np.transpose(MNS)

    axeY = np.arange(1, MNS.shape[0] + 1) * RESOLUTION
    axeX = np.arange(1, MNS.shape[1] + 1) * RESOLUTION

    ymin_m = 320  # axeY[0]
    ymax_m = 560  # axeY[ny - 1]
    xmin_m = 350  # axeX[0]
    xmax_m = 900  # axeX[nx - 1]

    ymin = np.argmin(np.abs(axeY - ymin_m))+1
    ymax = np.argmin(np.abs(axeY - ymax_m))+1
    xmin = np.argmin(np.abs(axeX - xmin_m))+1
    xmax = np.argmin(np.abs(axeX - xmax_m))+1


    MNS_F = median_filter(MNS[ymin:ymax, xmin:xmax], size=(10,10))
    #plotHeatmap(MNS_F,xmin_m,xmax_m,ymin_m,ymax_m)
    return MNS_F, MNS1


def plotHeatmap(MNS_F,xmin_m,xmax_m,ymin_m,ymax_m,show=True,save=False,save_path=".",save_name="autosave.png"):
    fig, ax = plt.subplots()
    img = ax.imshow(MNS_F,cmap='coolwarm', extent=[xmin_m, xmax_m, ymin_m, ymax_m])
    plt.colorbar(img, ax=ax, label='Vertical [mm]')
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_xlim([xmin_m, xmax_m])
    ax.set_ylim([ymin_m, ymax_m])
    ax.invert_xaxis()
    if show:
        plt.show()
    if save:
        plt.savefig(join(save_path,save_name), dpi=400)
