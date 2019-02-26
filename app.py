import csv
import subprocess
from utils import calc_dist
from flask import Flask, jsonify

app = Flask(__name__)
filename = 'data/remorquages.csv'

@app.route('/')
def hello_world():
	proc = subprocess.Popen(["python -V"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	return out

@app.route('/frequent-boroughs')
def frequent_boroughs():
    frequent_boroughs_dict = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader, None)

        borough_index = headers.index('ARRONDISSEMENT_ORIGINE')
        long_orig_index = headers.index('LONGITUDE_ORIGINE')
        lat_orig_index = headers.index('LATITUDE_ORIGINE')
        long_dest_index = headers.index('LONGITUDE_DESTINATION')
        lat_dest_index = headers.index('LATITUDE_DESTINATION')

        for row in reader:
            borough = row[borough_index]
            long_orig, lat_orig = row[long_orig_index], row[lat_orig_index]
            long_dest, lat_dest = row[long_dest_index], row[lat_dest_index]

            if not borough:
                continue
            
            distance = calc_dist(long_orig, lat_orig, long_dest, lat_dest)
            if borough in frequent_boroughs_dict.keys():
                frequent_boroughs_dict[borough]['number_towing'] += 1
                frequent_boroughs_dict[borough]['sum_distance'] += distance
            else:
                frequent_boroughs_dict[borough] = {'number_towing': 1, 'sum_distance': distance}

    frequent_boroughs = []
    for borough, stats in frequent_boroughs_dict.items():
        frequent_boroughs.append({
            'borough': borough,
            'number_towing': stats['number_towing'],
            'average_distance': stats['sum_distance']/stats['number_towing'],
            'distance_unit': 'km'
        })
    
    return jsonify(frequent_boroughs)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5001)
