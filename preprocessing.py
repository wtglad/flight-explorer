import pandas as pd

'''
Flight origin & destination survey data available at https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FHK&QO_fu146_anzr=b4vtv0%20n0q%20Qr56v0n6v10%20f748rB
Parent page w/ additional information: https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EFI&Yv0x=D
HOWEVER THIS IS ONLY US DATA

'''

# Get origins and destinations (this data represents Q2 2023)
df = pd.read_csv('data/T_DB1B_MARKET.csv')
df = df.groupby(['ORIGIN', 'DEST']).size().reset_index()
df.columns = ['origin', 'destination', 'num_flights']

# Require at least 50 flights in quarter, although this should potentially be adjusted or deduplicated (currently only doing origin -> destination, could also consider destination -> origin)
df = df[df['num_flights'] >= 50]

# Airport location data https://github.com/ip2location/ip2location-iata-icao/blob/master/iata-icao.csv
locs = pd.read_csv('data/iata-icao.csv')

# Merge origin/destination with location data 
df = df.merge(locs, left_on='origin', right_on='iata', how='left')
df = df.merge(locs, left_on='destination', right_on='iata', how='left', suffixes=('', '_destination'))

# Rename columns to consistently specify origin vs. destination
df.columns = ['origin',
             'destination',
             'num_flights',
             'country_code_origin',
             'region_name_origin',
             'iata_origin',
             'icao_origin',
             'airport_origin',
             'latitude_origin',
             'longitude_origin',
             'country_code_destination',
             'region_name_destination',
             'iata_destination',
             'icao_destination',
             'airport_destination',
             'latitude_destination',
             'longitude_destination']

# Create searchable airport
df['search_airport'] = df['iata_origin'] + ' - ' + df['airport_origin']

# Save cleaned data
df.to_csv('data/clean_flight_data.csv', index=False)