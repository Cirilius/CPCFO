import pandas as pd
import rasterio

from ml.utils import calculate_additional_features


def process_csv(csv_data):
    """
    process_csv(csv_data)

    This function processes the input CSV data by calculating the mean values of the last 10 rows (excluding the first column).

    Parameters:
        csv_data (pd.DataFrame):
            A pandas DataFrame containing the CSV data to be processed. The first column is excluded from processing, and only the last 10 rows of the remaining columns are considered.

    Returns:
        pd.Series:
            A pandas Series containing the mean values of the last 10 rows for each feature (excluding the first column). If there is no data, the mean values will be NaN.
    """
    # Read the CSV file
    # Take only the last 10 rows
    last_10_rows = csv_data.iloc[:, 1:].tail(10)
    # Calculate the mean for each feature
    mean_values = last_10_rows.mean()
    # If there's no data, the mean will be NaN
    return mean_values


# In your main processing function:
def load_and_preprocess_tiff(file_path, r_band, g_band, b_band, ik_band, mask_band):
    """
    load_and_preprocess_tiff(file_path, r_band, g_band, b_band, ik_band, mask_band)

    This function loads a multi-band TIFF image, extracts specified bands, calculates additional remote sensing features, and returns a DataFrame containing pixel-level information for further analysis.

    Parameters:
        file_path (str):
            The file path to the input TIFF image.
        r_band (int):
            The index of the red band in the TIFF image.
        g_band (int):
            The index of the green band in the TIFF image.
        b_band (int):
            The index of the blue band in the TIFF image.
        ik_band (int):
            The index of the near-infrared (NIR) band in the TIFF image.
        mask_band (int):
            The index of the mask band in the TIFF image (currently commented out in the function).

    Returns:
        pd.DataFrame:
            A DataFrame where each row corresponds to a pixel from the TIFF image and each column represents the values of the red, green, blue, NIR, and additional calculated features (e.g., NDVI, EVI, SAVI, NDWI, SR, GNDVI) for that pixel.

    Function Workflow:
        1. Opens the TIFF image using `rasterio` and extracts the specified bands (red, green, blue, and NIR).
        2. Calculates additional vegetation and water indices, such as NDVI, EVI, SAVI, and NDWI, as well as spectral ratios.
        3. Flattens the band data and derived features to create a tabular format.
        4. Returns a pandas DataFrame with the extracted and calculated features for each pixel.
    """
    with rasterio.open(file_path) as src:
        red = src.read(r_band)
        green = src.read(g_band)
        blue = src.read(b_band)
        nir = src.read(ik_band)
        # mask = src.read(mask_band)

    ndvi, evi, savi, ndwi, sr, gndvi, entropy_red, entropy_nir = (
        calculate_additional_features(red, green, blue, nir)
    )

    # Create a DataFrame with pixel-level information
    pixel_data = pd.DataFrame(
        {
            "red": red.flatten(),
            "green": green.flatten(),
            "blue": blue.flatten(),
            "nir": nir.flatten(),
            "ndvi": ndvi.flatten(),
            "evi": evi.flatten(),
            "savi": savi.flatten(),
            "ndwi": ndwi.flatten(),
            "sr": sr.flatten(),
            "gndvi": gndvi.flatten(),
            #'entropy_red': entropy_red.flatten(),
            #'entropy_nir': entropy_nir.flatten(),
            #'mask': mask.flatten()
        }
    )

    return pixel_data
