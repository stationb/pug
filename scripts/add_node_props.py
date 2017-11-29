import json
import os
import sys


IRI_TEMPLATE = '<pug://%s>'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python %s <JSONLINES_FILE>' % sys.argv[0])
        sys.exit(255)
    fn = os.path.abspath(sys.argv[1])

    with open(fn) as f:
        for line in f:
            node = json.loads(line)
            node_id = node['properties']['id'].replace(' ', '_')
            if node_id:
                for k, v in node['properties'].items():
                    rel = 'rel/%s' % k
                    if v:
                        triple = IRI_TEMPLATE % node_id, IRI_TEMPLATE % rel, v
                        print('%s %s "%s"' % triple)
