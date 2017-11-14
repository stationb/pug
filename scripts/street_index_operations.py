import json
from rtree.index import Index
from shapely.geometry import asShape

STREETS_FILE = '../../datasets/oakland/out/streets.jsonlines'
BUILDINGS_FILE = '../../datasets/oakland/out/buildings.jsonlines'
NQUADS_FILE = '../data/nquads.txt'


class StreetIndex(object):
    def __init__(self, streets_file):
        self.idx = Index()
        with open(streets_file) as f:
            for line in f.readlines():
                street = json.loads(line)
                street_id = street['properties']['id']
                street_shape = asShape(street['geometry'])
                self.idx.insert(int(street_id), list(street_shape.bounds))

    def find_nearest_street(self, building):
        building_shape = asShape(building['geometry'])
        building_centroid = (
            float(building_shape.centroid.coords.xy[0][0]),
            float(building_shape.centroid.coords.xy[1][0])
        )
        street_id = list(self.idx.nearest(building_centroid))[0]
        return str(street_id)

    def find_connected_street(self, street):
        street_id = int(street['properties']['id'])
        street_shape = asShape(street['geometry'])
        street_bounds = street_shape.bounds
        street_ids = list(self.idx.intersection(street_bounds))
        if street_id in street_ids:
            street_ids.remove(street_id)
        return street_ids


if __name__ == '__main__':
    street_idx = StreetIndex(STREETS_FILE)
    with open(NQUADS_FILE, 'w') as outfile:
        with open(BUILDINGS_FILE, 'r') as infile:
            for line in infile.readlines():
                building = json.loads(line)
                building_id = 'pug://building/%s' % building['properties']['id']
                street_id = 'pug://street/%s' % street_idx.find_nearest_street(building)
                outfile.write('<%s> <pug://rel/on> <%s> .' % (building_id, street_id))
                outfile.write('\n')
                outfile.write('<%s> <pug://rel/connects_to> <%s> .' % (street_id, building_id))
                outfile.write('\n')
        with open(STREETS_FILE, 'r') as infile:
            for line in infile.readlines():
                street = json.loads(line)
                street_id = 'pug://street/%s' % street['properties']['id']
                connected_street_ids = street_idx.find_connected_street(street)
                for csid in connected_street_ids:
                    csid = 'pug://street/%s' % csid
                    outfile.write('<%s> <pug://rel/connects_to> <%s> .' % (street_id, csid))
                    outfile.write('\n')
                    outfile.write('<%s> <pug://rel/connects_to> <%s> .' % (csid, street_id))
                    outfile.write('\n')
