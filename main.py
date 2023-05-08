import os
import landsat
from landsat import LandsatAPI

# Site's coord (EPSG:4326)
latitude = "5.48333"
longitude = "-75.0667"

# USGS website
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# chromedriver path
chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
geojson_path = os.getenv("GEOJSON_PATH")

# Download folder
downloads_dir = os.getenv("DOWNLOADS_DIR")

footprint = landsat.get_footprint(latitude, longitude, geojson_path)

# Download imagen Landsat 8
api = LandsatAPI(username, password, chromedriver_path, downloads_dir)
api.query(chromedriver_path, downloads_dir, footprint, 15)
