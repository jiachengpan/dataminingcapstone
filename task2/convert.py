import json
import glob


for f in glob.glob('output/*.json'):
    data = None
    with open(f) as fh:
        data = json.load(fh)

    nodes = []
    edges = []
    for i in range(len(data['meta']['categories'])):
        if 'cluster' not in data:
            cluster = 0
        else:
            cluster = data['cluster'][i]
        nodes.append([
            i,
            data['meta']['categories'][i],
            cluster
            ])

    for edge in data['data']:
        edges.append(edge)

    with open(f + '.gdf', 'w') as fh:
        fh.write('nodedef>name VARCHAR, label VARCHAR, group VARCHAR\n')
        fh.write('\n'.join([','.join([str(i) for i in n]) for n in nodes]))
        fh.write('\n')
        fh.write('edgedef>node1 VARCHAR, node2 VARCHAR, weight DOUBLE\n')
        fh.write('\n'.join([','.join([str(i) for i in e]) for e in edges]))
        fh.write('\n')

