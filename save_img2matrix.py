import time
import tarfile
import rasterio
import numpy as np
from numba import jit
from copy import deepcopy


def create_rgb(chanel, green=False, min_g=0):
    """
    This function create rgb image and highlights some chanels
    :param chanel: array chanel
    :param green: if highlights some chanel
    :param min_g: if highlights some chanel
    :return: processed chanel
    """
    for i in range(chanel.shape[0]):
        for j in range(chanel.shape[1]):
            if np.isnan(chanel[i, j]):
                chanel[i, j] = 1

    if not green:
        chanel_norm = (255 * (chanel - np.min(chanel)) / np.ptp(chanel)).astype(int)
    else:
        chanel_norm = (255 * (chanel - min_g) / np.ptp(chanel)).astype(int)

    return chanel_norm


@jit(nopython=True)
def iter_band(deforestation, forest_data):
    """
    this function compare threshold of ndvi
    Args:
        deforestation: numpy array with NDVI calculate
        forest_data:  numpy array empty with same shape of calculate

    Returns:

    """
    for i in range(deforestation.shape[0]):
        for j in range(deforestation.shape[1]):
            if deforestation[i, j] > 0:
                deforestation[i, j] = 0.65
            elif deforestation[i, j] > 1:
                deforestation[i, j] = 1
            elif deforestation[i, j] >= 0.7:
                forest_data[i, j] = 0.65

    return deforestation, forest_data


@jit(nopython=True)
def ndvi_matrix(infra_chanel, reed_chanel, matrix):
    """
    this function calculate ndvi from green and infra satelital chanel
    Args:
        infra_chanel: numpy array with infra chanel from satellite
        reed_chanel: numpy array with green chanel from satellite
        matrix: numpy array empty with same shape of calculate

    Returns:

    """
    for i in range(infra_chanel.shape[1]):
        for j in range(infra_chanel.shape[2]):
            num = round(infra_chanel[0][i, j] - reed_chanel[0][i, j], 2)
            den = round(infra_chanel[0][i, j] + reed_chanel[0][i, j], 2)
            if den > np.float64(0):
                ndvi = np.float32(num / den)
            else:
                ndvi = 0.0
            matrix[i, j] = np.float64(ndvi)

    return matrix


class ImgPrepare:

    def __init__(self, file_name):
        """
        this function prepare image to send IPFS
        :param file_name: path to image process
        """
        file = tarfile.open(f"img_input/{file_name}")
        self.folder_name = file_name.split(".")[0]
        self.file_path = f'bands_folder/{self.folder_name}'
        file.extractall(self.file_path)
        # time.sleep(30)
        file.close()

    def prepare(self):
        """
        this function return data from save
        Returns: resume dict, hist_data list, deforestation array

        """
        with rasterio.open(f"bands_folder/{self.folder_name}/{self.folder_name}_SR_B4.TIF") as src:
            img_b4 = src.read()

        with rasterio.open(f"bands_folder/{self.folder_name}/{self.folder_name}_SR_B1.TIF") as src:
            img_b1 = src.read()

        matrix = np.zeros((img_b4.shape[1], img_b4.shape[2]), dtype=np.float64)

        ndvi_mat = ndvi_matrix(infra_chanel=img_b4,
                               reed_chanel=img_b1,
                               matrix=matrix)

        forest_data = np.zeros((img_b4.shape[1], img_b4.shape[2]), dtype=np.float64)

        deforestation, forest_data = iter_band(deforestation=deepcopy(ndvi_mat),
                                               forest_data=forest_data)

        area_pixels = deforestation.shape[0] * deforestation.shape[1]
        area_forest = forest_data.sum()

        resume = {"mean": deforestation.mean(),
                  "total_px": area_pixels,
                  "deforestation": area_pixels - area_forest,
                  "percentage": round((1 - (area_forest / area_pixels)) * 100, 2)}

        hist_data = deforestation.flatten()

        return resume, hist_data, deforestation

    def rgb(self):
        """
        this function create a rgb image from coordinates
        Returns: rgb_img numpy array

        """
        with rasterio.open(f"{self.file_path}_SR_B1.TIF") as src:
            red = src.read()

        with rasterio.open(f"{self.file_path}_SR_B2.TIF") as src:
            green = src.read()

        with rasterio.open(f"{self.file_path}_SR_B2.TIF") as src:
            blue = src.read()

        red_norm = create_rgb(red)
        green_norm = create_rgb(green, green=True, min_g=75)
        blue_norm = create_rgb(blue)

        rgb_img = np.dstack((blue_norm, green_norm, red_norm)).astype(np.uint8)

        return rgb_img
