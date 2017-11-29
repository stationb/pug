import json
import os
import sys


IRI_TEMPLATE = '<pug://%s>'
V_TEMPLATE = '"%s"'
TV_TEMPLATE = '"%s"^^http://www.w3.org/2001/XMLSchema#%s'


def _type_mapping(types):
    tm = {}
    for type_ in types:
        t, v = type_.split('=', 1)
        tm[t] = v
    return tm


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python %s <NODE_TYPE> <JSONLINES_FILE> [TYPE_MAPPING...]' % sys.argv[0])
        sys.exit(255)
    node_type = sys.argv[1]
    node_type_iri = IRI_TEMPLATE % ('type/%s' % node_type)
    fn = os.path.abspath(sys.argv[2])
    type_mapping = _type_mapping(sys.argv[3:])

    with open(fn) as f:
        for line in f:
            node = json.loads(line)
            node_id = '/'.join((node_type, node['properties']['id'].replace(' ', '_')))
            if node_id:
                type_triple = IRI_TEMPLATE % node_id, IRI_TEMPLATE % 'rel/type', node_type_iri
                print('%s %s %s' % type_triple)
                for k, v in node['properties'].items():
                    rel = 'rel/%s' % k
                    if v:
                        vtype = None
                        if k in type_mapping:
                            vtype = type_mapping[k]
                        if vtype is None:
                            v = V_TEMPLATE % v
                        else:
                            v = TV_TEMPLATE % (v, vtype)
                        triple = IRI_TEMPLATE % node_id, IRI_TEMPLATE % rel, v
                        print('%s %s %s' % triple)
