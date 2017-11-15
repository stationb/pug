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
                for i in range(len(street_shape.geoms)):
                    seg_id = self.encode_seg_id(i, street_id)
                    self.idx.insert(seg_id, street_shape.geoms[i].coords[0])
                    self.idx.insert(-seg_id, street_shape.geoms[i].coords[-1])

        self.bb_idx = Index()
        with open(streets_file) as f:
            for line in f.readlines():
                street = json.loads(line)
                street_id = int(street['properties']['id'])
                street_shape = asShape(street['geometry'])
                self.bb_idx.insert(street_id, list(street_shape.bounds))

    def encode_seg_id(self, i, street_id):
        return i * 1000000 + int(street_id)

    def decode_seg_id(self, seg_id):
        i = abs(seg_id) / 1000000
        return abs(seg_id) - i

    def find_nearest_street(self, building):
        building_shape = asShape(building['geometry'])
        building_centroid = (
            float(building_shape.centroid.coords.xy[0][0]),
            float(building_shape.centroid.coords.xy[1][0])
        )
        street_id = list(self.bb_idx.nearest(building_centroid))[0]
        return str(street_id)

    def find_connected_street(self, street):
        street_id = int(street['properties']['id'])
        street_shape = asShape(street['geometry'])
        street_start = street_shape.geoms[0].coords[0]
        street_end = street_shape.geoms[-1].coords[-1]
        seg_ids = list(self.idx.intersection(street_start))
        seg_ids += list(self.idx.intersection(street_end))
        street_ids = set(map(self.decode_seg_id, seg_ids))
        if street_id in street_ids:
            street_ids.remove(street_id)
        return street_ids


if __name__ == '__main__':
    street_idx = StreetIndex(STREETS_FILE)
    with open(NQUADS_FILE, 'w') as outfile:
        with open(BUILDINGS_FILE, 'r') as infile:
            for line in infile.readlines():
                building = json.loads(line)
                building_id = 'pug://building/%s' % building['properties']['id'].replace(' ', '_')
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
                    outfile.write('<%s> <pug://rel/intersects> <%s> .' % (street_id, csid))
                    outfile.write('\n')
                    outfile.write('<%s> <pug://rel/intersects> <%s> .' % (csid, street_id))
                    outfile.write('\n')
