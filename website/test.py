import pandas 


test = pandas.read_csv('../data/area_locations.csv')
test

test['lon'].loc[test['area'] == 'Bath'].item()
