import landsat
from landsat import LandsatAPI

# Site's coord (EPSG:4326)
latitude = 000
longitude = 000

# USGS website
username = 'xxx'
password = 'xxx'

# chromedriver path
chromedriver_path = 'xxx'
geojson_path = "xxx"  #

# Download folder
downloads_dir = "xxx"

footprint = landsat.get_footprint(latitude, longitude, geojson_path)

# Download imagen Landsat 8
api = LandsatAPI(username, password, chromedriver_path, downloads_dir)
api.query(chromedriver_path, downloads_dir, footprint, 15)
