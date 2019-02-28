import csv
import subprocess
from flask import Flask, jsonify
from common.constant import weekdays
from common.utils import calc_dist, get_weekday_from_datetime

app = Flask(__name__)
filename = 'data/remorquages.csv'

@app.route('/')
def hello_world():
	proc = subprocess.Popen(["python -V"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	return "Python Flask Towing Endpoints.<br> Python version %s" % out.strip()

@app.route('/data', defaults={'date_id': None})
@app.route('/data/<date_id>')
def data(date_id):
    '''
    Endpoint that returns the data in json format.
    Can filter the data using the the date.
    '''

    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        origin_date_index = headers.index('DATE_ORIGINE')

        if date_id:
            for row in reader:
                origin_date = row[origin_date_index].split('T')[0].strip()
                if origin_date == date_id.strip():
                    data.append(dict(zip(headers, row)))
        else:
            data = [dict(zip(headers, row)) for row in reader]
    return jsonify(data)

@app.route('/boroughs-stats', defaults={'borough_id': None})
@app.route('/boroughs-stats/<borough_id>')
def boroughs_stats(borough_id):
    '''
    Endpoint that returns the number of towings per borough 
    and the average towed distance in each borough.
    Can filter the data using the borough name.
    '''

    boroughs_stats_dict = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader, None)

        borough_index = headers.index('ARRONDISSEMENT_ORIGINE')
        long_orig_index = headers.index('LONGITUDE_ORIGINE')
        lat_orig_index = headers.index('LATITUDE_ORIGINE')
        long_dest_index = headers.index('LONGITUDE_DESTINATION')
        lat_dest_index = headers.index('LATITUDE_DESTINATION')

        for row in reader:
            distance = 0.0
            distance_error = False

            borough = row[borough_index]
            long_orig, lat_orig = row[long_orig_index], row[lat_orig_index]
            long_dest, lat_dest = row[long_dest_index], row[lat_dest_index]

            if not borough:
                continue
            
            try:
                distance = calc_dist(long_orig, lat_orig, long_dest, lat_dest)
            except ValueError:
                distance_error = True
                pass
            
            if borough in boroughs_stats_dict.keys():
                boroughs_stats_dict[borough]['number_towing'] += 1
                boroughs_stats_dict[borough]['sum_distance'] += distance
                if distance_error:
                    boroughs_stats_dict[borough]['distance_errors'] += 1
            else:
                distance_errors_count = 1 if distance_error else 0
                boroughs_stats_dict[borough] = {
                    'number_towing': 1, 
                    'sum_distance': distance,
                    'distance_errors': distance_errors_count
                }

    boroughs_stats = []
    if borough_id != None:
        average_distance = (boroughs_stats_dict[borough_id]['sum_distance'] / 
                            (boroughs_stats_dict[borough_id]['number_towing'] -
                            boroughs_stats_dict[borough_id]['distance_errors']))
        boroughs_stats.append({
            'borough': borough_id,
            'number_towing': boroughs_stats_dict[borough_id]['number_towing'],
            'average_distance': average_distance,
            'distance_unit': 'km'
        })
    else:
        for borough, stats in boroughs_stats_dict.items():
            average_distance = (stats['sum_distance'] /
                                (stats['number_towing'] - stats['distance_errors']))
            boroughs_stats.append({
                'borough': borough,
                'number_towing': stats['number_towing'],
                'average_distance': average_distance,
                'distance_unit': 'km'
            })
    
    return jsonify(boroughs_stats)

@app.route('/weekdays-stats')
def weekdays_stats():
    '''Endpoint that returns the number of towings per weekday'''

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
	app.run(debug=True, host='0.0.0.0')
