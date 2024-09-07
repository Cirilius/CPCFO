import numpy as np
import rasterio


def calculate_additional_features(red, green, blue, nir):
    """
    calculate_additional_features(red, green, blue, nir)

    This function calculates various vegetation and water indices, as well as texture features, from multi-spectral image data. These indices are useful in remote sensing applications for analyzing vegetation health, water content, and other environmental features.

    Parameters:
        red (np.array):
            The red band data from the image.
        green (np.array):
            The green band data from the image.
        blue (np.array):
            The blue band data from the image.
        nir (np.array):
            The near-infrared (NIR) band data from the image.

    Returns:
        tuple:
            A tuple of calculated indices and features, including:
            - NDVI (Normalized Difference Vegetation Index)
            - EVI (Enhanced Vegetation Index)
            - SAVI (Soil Adjusted Vegetation Index)
            - NDWI (Normalized Difference Water Index)
            - SR (Simple Ratio)
            - GNDVI (Green Normalized Difference Vegetation Index)
            - entropy_red (Texture feature based on local entropy for the red band)
            - entropy_nir (Texture feature based on local entropy for the NIR band)
    """
    # Existing NDVI calculation
    ndvi = (nir - red) / (1e-3 + nir + red)

    # Enhanced Vegetation Index (EVI)
    evi = 2.5 * (nir - red) / (1e-3 + nir + 6 * red - 7.5 * blue + 1)

    # Soil Adjusted Vegetation Index (SAVI)
    savi = ((nir - red) / (nir + red + 0.5)) * 1.5

    # Normalized Difference Water Index (NDWI)
    ndwi = (green - nir) / (1e-3 + green + nir)

    # Simple Ratio (SR)
    sr = nir / (1e-3 + red)

    # Green Normalized Difference Vegetation Index (GNDVI)
    gndvi = (nir - green) / (1e-3 + nir + green)

    # Texture features (example: local entropy)
    def entropy(values):
        values = values.flatten()
        h, _ = np.histogram(values, bins=20)
        h = h / h.sum()
        return -np.sum(h * np.log2(h + (h == 0)))

    entropy_red = 0  # generic_filter(red, entropy, size=5)
    entropy_nir = 0  # generic_filter(nir, entropy, size=5)

    return ndvi, evi, savi, ndwi, sr, gndvi, entropy_red, entropy_nir


def pixel_to_coord(row, col, transform):
    x, y = rasterio.transform.xy(transform, row, col)
    return x, y
