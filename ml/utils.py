import numpy as np
import rasterio


def calculate_additional_features(red, green, blue, nir):
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
