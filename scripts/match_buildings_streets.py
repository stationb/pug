import json
from rtree.index import Index
from shapely.geometry import asShape

from pprint import pprint


class StreetIndex(object):
    def __init__(self, street_file):
        self.idx = Index()
        self.metadata = {}
        with open(streets_file) as f:
            for i, line in enumerate(f.readlines()):
                street = json.loads(line)
                self.metadata[i] = street['properties']
                shapely_street = asShape(street['geometry'])
                self.idx.insert(i, list(shapely_street.bounds))

    def find_nearest_street(self, building):
        print building['properties']['bldgid3']
        shapely_building = asShape(building['geometry'])
        coordinate_tuple = (
            float(shapely_building.centroid.coords.xy[0][0]),
            float(shapely_building.centroid.coords.xy[1][0])
        )
        street_id = list(self.idx.nearest(coordinate_tuple))[0]
        return self.metadata[street_id]['name']


if __name__ == '__main__':
    streets_file = '../../datasets/oakland/streets.geojson.jsonlines'
    buildings_file = '../../datasets/oakland/buildings.geojson.jsonlines'
    street_idx = StreetIndex(streets_file)
    with open(buildings_file) as f:
        for i, line in enumerate(f.readlines()):
            building = json.loads(line)
            print street_idx.find_nearest_street(building)
            print
