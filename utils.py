import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from shapely.geometry import Point
import matplotlib.pyplot as plt
import numpy as np
import requests
import gzip
import shutil
import os
import argparse
import glob



def create_geometry_dataframe(data):
    try :
        gdf = gpd.GeoDataFrame(
        data, geometry=gpd.GeoSeries.from_wkt(data['geometry']))
        return gdf
    except Exception as e: 
        print(f'Your df is not available for geometry convertion, Error : {str(e)}')


def filter_dataframe(data, latitude, longitude):
    df_filtered = data.loc[
    data['latitude'].between(latitude-0.02, latitude+0.02) & 
    data['longitude'].between(longitude-0.02, longitude+0.02)
    ]

    print(f'filtered dataframe size : {df_filtered.size}')
    return df_filtered


def calcul_distance(gdf, latitude, longitude) -> pd.DataFrame:
    return np.sqrt(((gdf['latitude'] - latitude)**2) + ((gdf['longitude'] - longitude)**2))


def create_geometry_data_point(data_row):
    point_geom = Point(data_row['longitude'], data_row['latitude'])
    point_closest = gpd.GeoDataFrame([data_row], geometry=[point_geom])
    return point_closest


def plot_closest(gdf, reference_point, closest_point):    
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(15, 10) )

    gdf.plot(ax=ax1, color='blue', label='buildings')
    gdf.plot(ax=ax2, color = 'blue', label = 'buildings')
    ax1.set_title("General view")

    reference_point = create_geometry_data_point(reference_point)
    closest_point = create_geometry_data_point(closest_point)

    ref_lon = float(reference_point['longitude'].iloc[0])
    ref_lat = float(reference_point['latitude'].iloc[0])

    ax2.set_xlim([ref_lon-0.001, ref_lon+0.001])  
    ax2.set_ylim([ref_lat-0.001, ref_lat+0.001]) 
    ax2.set_title("Accurate view") 

    reference_point.plot(ax=ax1, color='red',markersize=40, label='reference_point')
    reference_point.plot(ax=ax2, color='red',markersize=20, label='reference_point')
    closest_point.plot(ax=ax2, color='yellow', markersize=20, label='closest_building')

    ax1.legend()
    ax2.legend()

    plt.tight_layout()
    plt.savefig('output.png')
    print("Plot saved as output.png")


# def plot_gdf(gdf, reference_point):
#     fig, ax = plt.subplots(figsize = (10,10))
#     reference_point = create_geometry_data_point(reference_point)
#     gdf.plot(ax = ax, color='blue', label='buildings')
#     reference_point.plot(ax=ax, color='red',markersize=40, label='reference_point')

#     plt.show()


def extract_region_file(url, filename):
    print('start downloading region file')
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        with gzip.open(filename, "rb") as f_in:
            with open(filename[:-3], "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
                os.remove(filename)
        print(f"Downloaded : {filename}")


def get_lat_lon_url_parser():
    parser = argparse.ArgumentParser(description='Parse latitude and longitude')
    
    parser.add_argument("--ref_lat", type=float, required=True, help="reference latitude")
    parser.add_argument("--ref_lon", type=float, required=True, help="reference longitude")
    parser.add_argument("--url", type=str, required=True, help="region url" )
    args = parser.parse_args()
    lat = args.ref_lat
    lon = args.ref_lon
    url = args.url

    return lat, lon, url

def clean_repo(patterns):
    for pattern in patterns:
        files = glob.glob(pattern)  
        for file in files:
            os.remove(file)