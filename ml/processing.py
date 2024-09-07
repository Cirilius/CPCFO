import pandas as pd
import rasterio

from ml.utils import calculate_additional_features


def process_csv(csv_data):
    # Read the CSV file
    # Take only the last 10 rows
    last_10_rows = csv_data.iloc[:, 1:].tail(10)
    # Calculate the mean for each feature
    mean_values = last_10_rows.mean()
    # If there's no data, the mean will be NaN
    return mean_values


# In your main processing function:
def load_and_preprocess_tiff(file_path, r_band, g_band, b_band, ik_band, mask_band):
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
