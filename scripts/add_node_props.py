import json
import os
import sys


IRI_TEMPLATE = '<pug://%s>'


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python %s <NODE_TYPE> <JSONLINES_FILE>' % sys.argv[0])
        sys.exit(255)
    node_type = sys.argv[1]
    node_type_iri = IRI_TEMPLATE % ('type/%s' % node_type)
    fn = os.path.abspath(sys.argv[2])

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
                        triple = IRI_TEMPLATE % node_id, IRI_TEMPLATE % rel, v
                        print('%s %s "%s"' % triple)
