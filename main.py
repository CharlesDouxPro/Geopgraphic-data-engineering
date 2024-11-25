from utils import *
import pandas as pd
from datetime import datetime
import gc


def main():
    start = datetime.now()
    extract_region_file(url, filename)
    df = pd.read_csv(filename[:-3])
    data_filtered = filter_dataframe(df, reference_lat, reference_lon)
    gdf = create_geometry_dataframe(data_filtered) 
    del df, data_filtered
    gc.collect()

    gdf['distance'] = calcul_distance(gdf, reference_lat, reference_lon)
    reference_building = gdf.loc[gdf['distance'].idxmin()]
    gdf['distance_from_reference_building'] = calcul_distance(gdf, reference_building['latitude'], reference_building['longitude'])
    closest_from_reference_building = gdf.loc[gdf['distance_from_reference_building'][gdf['distance_from_reference_building'] > 0].idxmin()] #Avoid reference to call itself
    end = (datetime.now() - start)
    print(f'closest building PC : {closest_from_reference_building['full_plus_code']}, pipeline executed in {end} seconds')
    plot_closest(gdf, reference_building, closest_from_reference_building)
    del gdf
    gc.collect()

if __name__ == '__main__':
    clean_repo(patterns=['*.csv*','*.png*'])
    reference_lat, reference_lon, url = get_lat_lon_url_parser()
    filename = url.split('/')[-1]
    main()
    clean_repo(patterns=['*.csv*'])