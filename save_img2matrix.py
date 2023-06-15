import rasterio
import numpy as np


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


class ImgPrepare:

    def __init__(self, file_path):
        """
        this function prepare image to send IPFS
        :param file_path: path to image process
        """
        self.file_path = file_path

    def prepare(self):
        """
        this function read TIF file and extract NDVI chanel, clouds and basic statistic
        :return: NDV image
        """
        with rasterio.open(f"{self.file_path}") as src:
            org_img = src.read()

        deforestation = np.array(org_img[4])

        forest_data = np.zeros((org_img.shape[1], org_img.shape[2]), dtype=np.int8)

        for i in range(org_img.shape[1]):
            for j in range(org_img.shape[2]):
                if np.isnan(deforestation[i, j]):
                    deforestation[i, j] = 0.65
                elif deforestation[i, j] > 1:
                    deforestation[i, j] = 1
                elif deforestation[i, j] >= 0.7:
                    forest_data[i, j] = 0.65

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
        this function create normal image
        :return: RGB image
        """
        with rasterio.open(f"{self.file_path}") as src:
            red = src.read(1)
            green = src.read(2)
            blue = src.read(3)

        red_norm = create_rgb(red)
        green_norm = create_rgb(green, green=True, min_g=75)
        blue_norm = create_rgb(blue)

        rgb_img = np.dstack((blue_norm, green_norm, red_norm)).astype(np.uint8)

        return rgb_img