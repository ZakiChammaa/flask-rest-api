import csv
import subprocess
from common.utils import calc_dist, get_weekday_from_datetime
from common.constant import weekdays
from flask import Flask, jsonify

app = Flask(__name__)
filename = 'data/remorquages.csv'

@app.route('/')
def hello_world():
	proc = subprocess.Popen(["python -V"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	return out

@app.route('/frequent-boroughs', defaults={'borough_id': None})
@app.route('/frequent-boroughs/<borough_id>')
def frequent_boroughs(borough_id):
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
    if borough_id != None:
        average_distance = frequent_boroughs_dict[borough_id]['sum_distance']/frequent_boroughs_dict[borough_id]['number_towing']
        frequent_boroughs.append({
            'borough': borough_id,
            'number_towing': frequent_boroughs_dict[borough_id]['number_towing'],
            'average_distance': average_distance,
            'distance_unit': 'km'
        })
    else:
        for borough, stats in frequent_boroughs_dict.items():
            frequent_boroughs.append({
                'borough': borough,
                'number_towing': stats['number_towing'],
                'average_distance': stats['sum_distance']/stats['number_towing'],
                'distance_unit': 'km'
            })
    
    return jsonify(frequent_boroughs)

@app.route('/weekdays-stats')
def weekdays_stats():
    weekdays_stats_dict = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader, None)

        origin_date_index = headers.index('DATE_ORIGINE')

        for row in reader:
            weekday = None
            try:
                weekday = get_weekday_from_datetime(row[origin_date_index])
            except ValueError:
                print('Error parsing date from file.')
                print('Skipping...')
                continue

            if weekday in weekdays_stats_dict.keys():
                weekdays_stats_dict[weekday]['number_towing'] += 1
            else:
                weekdays_stats_dict[weekday] = {'number_towing': 1}

        weekdays_stats = []
        for weekday, stats in weekdays_stats_dict.items():
            weekdays_stats.append({
                'weekday': weekdays[weekday],
                'number_towing': stats['number_towing']
            })
        
        return jsonify(weekdays_stats)


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5001)
