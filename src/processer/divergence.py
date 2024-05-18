from os.path import join
import imageio
import numpy as np
import matplotlib.pyplot as plt

def manageKwargs(kwargs_dict):
    DEP = kwargs_dict.get('DEP',0)
    UXNORM = kwargs_dict.get('UXNORM',0)
    UYNORM = kwargs_dict.get('UYNORM',0)
    SHEAR = kwargs_dict.get('SHEAR',0)
    SECONDINV = kwargs_dict.get('SECONDINV',0)
    CURL = kwargs_dict.get('CURL',0)
    DIVERGENCE = kwargs_dict.get('DIVERGENCE',0)
    ONOFF = kwargs_dict.get('ONOFF',0)
    ZONE = kwargs_dict.get('ZONE',1)
    return DEP , UXNORM , UYNORM , SHEAR , SECONDINV , CURL , DIVERGENCE , ONOFF , ZONE


def computeFramesDivergence(frame_numbers,source_directory_path, show=False, **kwargs):
    for frame_number in frame_numbers:
        computeFrameDivergence(frame_number,source_directory_path, show,**kwargs)


def processDEFINENAME(UxZoom,UyZoom,AxisXZ,AxisYZ,dx,dy):
    dUxdx = np.zeros_like(UxZoom)
    dUxdy = np.zeros_like(UxZoom)

    for r in range(1, AxisXZ.shape[0] - 1):
        dUxdx[:, r] = (UxZoom[:, r + 1] - UxZoom[:, r - 1]) / (2 * dx)

    for i in range(1, AxisYZ.shape[0] - 1):
        dUxdy[i, :] = (UxZoom[i + 1, :] - UxZoom[i - 1, :]) / (2 * dy)

    dUydy = np.zeros_like(UyZoom)
    dUydx = np.zeros_like(UyZoom)

    for r in range(1, AxisYZ.shape[0] - 1):
        dUydy[r, :] = (UyZoom[r + 1, :] - UyZoom[r - 1, :]) / (2 * dy)

    for i in range(1, AxisXZ.shape[0] - 1):
        dUydx[:, i] = (UyZoom[:, i + 1] - UyZoom[:, i - 1]) / (2 * dx)
    return dUxdx , dUxdy , dUydy , dUydx


def processDEFINENAME2(frame_directory_path,zoom):
    Ux = imageio.imread(join(frame_directory_path, 'Px1_Num6_DeZoom1_LeChantier.tif'))
    Uy = imageio.imread(join(frame_directory_path, 'Px2_Num6_DeZoom1_LeChantier.tif'))

    PXL = 4.35
    Ux /= PXL
    Uy /= PXL

    nx = Ux.shape[1]
    ny = Uy.shape[0]

    AxisX = np.arange(1, nx + 1) / PXL
    AxisY = np.arange(1, ny + 1) / PXL

    if zoom:
        ymin_mm = AxisY[0]
        ymax_mm = AxisY[-1]
        xmin_mm = AxisX[0]
        xmax_mm = AxisX[-1]

    ymin_mm_idx = np.argmin(np.abs(AxisY - ymin_mm))
    ymax_mm_idx = np.argmin(np.abs(AxisY - ymax_mm))
    xmin_mm_idx = np.argmin(np.abs(AxisX - xmin_mm))
    xmax_mm_idx = np.argmin(np.abs(AxisX - xmax_mm))

    dx = AxisX[1] - AxisX[0]
    dy = AxisY[1] - AxisY[0]

    AxisXZ = AxisX[xmin_mm_idx:xmax_mm_idx]
    AxisYZ = AxisY[ymin_mm_idx:ymax_mm_idx]

    UxZoom = Ux[ymin_mm_idx:ymax_mm_idx, xmin_mm_idx:xmax_mm_idx]
    UyZoom = Uy[ymin_mm_idx:ymax_mm_idx, xmin_mm_idx:xmax_mm_idx]

    return UxZoom , UyZoom , AxisXZ , AxisYZ , dx , dy


def computeFrameDivergence(frame_number,source_directory_path, show=False,**kwargs):
    DEP , UXNORM , UYNORM , SHEAR , SECONDINV , CURL , DIVERGENCE , ONOFF , ZONE = manageKwargs(kwargs)
    FRAME_DIRECTORY_PATH = join(source_directory_path,f"frame{frame_number}")

    min_limit = 0
    max_limit = 0.55
    ymin_mm = 410
    ymax_mm = 510
    xmin_mm = 750
    xmax_mm = 950

    UxZoom , UyZoom , AxisXZ , AxisYZ , dx , dy = processDEFINENAME2(FRAME_DIRECTORY_PATH,ZONE)

    matrixes = {}

    if SHEAR or SECONDINV or CURL or DIVERGENCE:
        dUxdx, dUxdy, dUydy, dUydx = processDEFINENAME(UxZoom,UyZoom,AxisXZ,AxisYZ,dx,dy)

    if DEP:
        label_type = 'Displacement'
        DeplZ = np.sqrt(UxZoom**2 + UyZoom**2)
        matrixes['Displacement'] = DeplZ
        if show:
            plotHeatmap(DeplZ, label_type, xmin_mm, xmax_mm, ymin_mm, ymax_mm)

    if UXNORM:
        label_type = 'Fault-parallel'
        UxNorma = (UxZoom * 100) / 0.5
        matrixes['Fault-parallel'] = UxNorma
        if show:
            plotHeatmap(UxNorma, label_type, xmin_mm, xmax_mm, ymin_mm, ymax_mm, min_limit, max_limit)

    if UYNORM:
        label_type = 'Fault-normal'
        UyNorma = ((UyZoom + 0.07) * 100) / 0.1482
        matrixes['Fault-normal'] = UyNorma
        min_limit = -0.1
        max_limit = 0.1
        if show:
            plotHeatmap(UyNorma, label_type, xmin_mm, xmax_mm, ymin_mm, ymax_mm, min_limit, max_limit)

    if SECONDINV:
        label_type = 'SecondInvariant'
        inv2 = -(dUxdx * dUydy) + (1/2 * (dUxdy + dUydx))**2
        matrixes['SecondInvariant'] = inv2
        min_limit = 0
        max_limit = 0.008
        if show:
            plotHeatmap(inv2, label_type, xmin_mm, xmax_mm, ymin_mm, ymax_mm, min_limit, max_limit)

    if ONOFF:
        label_type = 'On-off-fault'
        DeplZ = np.sqrt(UxZoom**2 + UyZoom**2)
        dDepldy = np.zeros_like(DeplZ)

        for r in range(1, AxisYZ.shape[0] - 1):
            dDepldy[r, :] = (DeplZ[r + 1, :] - DeplZ[r - 1, :]) / (2 * dy)

        OOf = dDepldy
        matrixes['On-off-fault'] = OOf
        min_limit = 0
        max_limit = 0.2
        if show:
            plotHeatmap(OOf, label_type, xmin_mm, xmax_mm, ymin_mm, ymax_mm, min_limit, max_limit)

    if SHEAR:
        label_type = 'Shear'
        shear_xy = 1/2 * (dUxdy + dUydx)
        matrixes['Shear'] = shear_xy
        min_limit = -0.05
        max_limit = 0.05
        if show:
            plotHeatmap(shear_xy, label_type, xmin_mm, xmax_mm, ymin_mm, ymax_mm, min_limit, max_limit)

    if CURL:
        label_type = 'Curl'
        curl_df = dUydx - dUxdy
        matrixes['Curl'] = curl_df
        min_limit = -0.3
        max_limit = 0.1
        if show:
            plotHeatmap(curl_df, label_type, xmin_mm, xmax_mm, ymin_mm, ymax_mm, min_limit, max_limit)

    if DIVERGENCE:
        label_type = 'Divergence'
        div = dUxdx + dUydy
        matrixes['Divergence'] = div
        min_limit = -0.02
        max_limit = 0.02
        if show:
            plotHeatmap(div, label_type, xmin_mm, xmax_mm, ymin_mm, ymax_mm, min_limit, max_limit)

    return matrixes


def plotHeatmap(data, label_type, xmin_mm, xmax_mm, ymin_mm, ymax_mm, vmin=None, vmax=None):
    plt.figure()
    if vmin is None or vmax is None:
        plt.imshow(data, cmap='coolwarm', extent=[xmin_mm, xmax_mm, ymin_mm, ymax_mm])
    else:
        plt.imshow(data, cmap='coolwarm', extent=[xmin_mm, xmax_mm, ymin_mm, ymax_mm], vmin=vmin, vmax=vmax)
    plt.colorbar(label=label_type)
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
