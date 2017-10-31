import json
from rtree.index import Index
from shapely.geometry import asShape

STREETS_FILE = '../../datasets/oakland/streets.geojson.jsonlines'
BUILDINGS_FILE = '../../datasets/oakland/buildings.geojson.jsonlines'
NQUADS_FILE = '../data/nquads.txt'


class StreetIndex(object):
    def __init__(self, streets_file):
        self.idx = Index()
        self.metadata = {}
        with open(streets_file) as f:
            for line in f.readlines():
                street = json.loads(line)
                street_id = street['properties']['objectid']
                self.metadata[street_id] = street['properties']
                street_shape = asShape(street['geometry'])
                self.idx.insert(int(street_id), list(street_shape.bounds))

    def find_nearest_street(self, building):
        shapely_building = asShape(building['geometry'])
        coordinate_tuple = (
            float(shapely_building.centroid.coords.xy[0][0]),
            float(shapely_building.centroid.coords.xy[1][0])
        )
        street_id = list(self.idx.nearest(coordinate_tuple))[0]
        return str(street_id)


if __name__ == '__main__':
    street_idx = StreetIndex(STREETS_FILE)
    with open(BUILDINGS_FILE, 'r') as infile:
        with open(NQUADS_FILE, 'w') as outfile:
            for line in infile.readlines():
                building = json.loads(line)
                building_id = '/building/%s' % building['properties']['objectid']
                street_id = '/street/%s' % street_idx.find_nearest_street(building)
                outfile.write('"%s" "near" "%s" .' % (building_id, street_id))
                outfile.write('\n')
