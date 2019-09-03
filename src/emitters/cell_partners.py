import random
from elasticsearch.helpers import parallel_bulk
from hashlib import md5
from datetime import datetime


def generate_tower_docs():
    with open('./emitters/cell_towers.csv', 'r') as f:
        for record in f:
            if record[0] == '#':
                continue
            record = record.split(',')
            yield dict(
                _op_type='index',
                _index='towers',
                _id=md5(str([record[1], record[2], record[3], record[4], record[5]]).encode()).hexdigest(),
                radio=record[0],
                mcc=record[1].zfill(3),
                net=record[2].zfill(3),
                area=record[3].zfill(5),
                cell=record[4].zfill(5),
                fqtn='.'.join([record[1].zfill(3), record[2].zfill(3), record[3].zfill(5), record[4].zfill(5)]),
                unit=record[5],
                lon=float(record[6]),
                lat=float(record[7]),
                range=int(record[8]),
                samples=int(record[9]),
                changeable=True if record[10] == '1' else False,
                created=int(record[11]),
                updated=int(record[12]),
                average_signal=float(record[13]),
                location=[float(record[6]), float(record[7])],
                heartbeat=datetime.fromtimestamp(datetime.utcnow().timestamp()-random.randint(1, 3600)).isoformat()
            )


def index_partner_towers(es):
    if es.count('towers')['count'] == 106879:
        print('Skipping towers -- already indexed.')
        return
    for success, info in parallel_bulk(es, generate_tower_docs(), chunk_size=500):
        if not success:
            print(success, info)
