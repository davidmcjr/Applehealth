#Created with GROK 3 (I have very little coding abilty)

import xml.etree.ElementTree as ET
import csv
from collections import defaultdict

# Open CSV file for writing
with open('workouts_complete.csv', 'w', newline='') as csvfile:
    headers = [
        'workoutActivityType', 'duration', 'durationUnit', 
        'totalEnergyBurned', 'totalEnergyBurnedUnit', 
        'totalDistance', 'totalDistanceUnit', 
        'sourceName', 'startDate', 'endDate', 
        'metadata', 
        'eventType', 'eventDate', 
        'avgHeartRate', 'avgHeartRateUnit', 
        'totalSteps', 'totalStepsUnit'
    ]
    writer = csv.writer(csvfile)
    writer.writerow(headers)

    # Track dynamic metadata keys
    metadata_keys = set()

    # Parse XML incrementally with error handling
    try:
        context = ET.iterparse('export.xml', events=('start', 'end'))
    except FileNotFoundError:
        print("Error: 'export.xml' not found")
        exit(1)
    except ET.ParseError:
        print("Error: Invalid XML format in 'export.xml'")
        exit(1)

    current_workout = None
    workout_data = defaultdict(str)
    workout_count = 0
    metadata_count = 0
    event_count = 0
    stats_count = 0

    for event, elem in context:
        if event == 'start' and elem.tag == 'Workout':
            current_workout = elem
            workout_data = defaultdict(str, {
                'workoutActivityType': elem.get('workoutActivityType', ''),
                'duration': elem.get('duration', ''),
                'durationUnit': elem.get('durationUnit', ''),
                'totalEnergyBurned': elem.get('totalEnergyBurned', ''),
                'totalEnergyBurnedUnit': elem.get('totalEnergyBurnedUnit', ''),
                'sourceName': elem.get('sourceName', ''),
                'startDate': elem.get('startDate', ''),
                'endDate': elem.get('endDate', '')
            })
            workout_count += 1

        elif event == 'end' and elem.tag == 'MetadataEntry' and current_workout is not None:
            key = elem.get('key', '')
            value = elem.get('value', '')
            workout_data[f'metadata_{key}'] = value
            metadata_keys.add(f'metadata_{key}')
            metadata_count += 1

        elif event == 'end' and elem.tag == 'WorkoutEvent' and current_workout is not None:
            workout_data['eventType'] = elem.get('type', '')
            workout_data['eventDate'] = elem.get('date', '')
            event_count += 1

        elif event == 'end' and elem.tag == 'WorkoutStatistics' and current_workout is not None:
            stat_type = elem.get('type', '')
            if stat_type == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
                workout_data['totalDistance'] = elem.get('sum', '')
                workout_data['totalDistanceUnit'] = elem.get('unit', '')
            elif stat_type == 'HKQuantityTypeIdentifierDistanceCycling':
                workout_data['totalDistance'] = elem.get('sum', '')
                workout_data['totalDistanceUnit'] = elem.get('unit', '')
            elif stat_type == 'HKQuantityTypeIdentifierDistanceSwimming':
                workout_data['totalDistance'] = elem.get('sum', '')
                workout_data['totalDistanceUnit'] = elem.get('unit', '')
            elif stat_type == 'HKQuantityTypeIdentifierHeartRate':
                workout_data['avgHeartRate'] = elem.get('average', '')
                workout_data['avgHeartRateUnit'] = elem.get('unit', '')
            elif stat_type == 'HKQuantityTypeIdentifierStepCount':
                workout_data['totalSteps'] = elem.get('sum', '')
                workout_data['totalStepsUnit'] = elem.get('unit', '')
            elif stat_type == 'HKQuantityTypeIdentifierActiveEnergyBurned':
                workout_data['totalEnergyBurned'] = elem.get('sum', '')
                workout_data['totalEnergyBurnedUnit'] = elem.get('unit', '')
            stats_count += 1

        elif event == 'end' and elem.tag == 'Workout' and current_workout is not None:
            row = [
                workout_data['workoutActivityType'],
                workout_data['duration'],
                workout_data['durationUnit'],
                workout_data['totalEnergyBurned'],
                workout_data['totalEnergyBurnedUnit'],
                workout_data['totalDistance'],
                workout_data['totalDistanceUnit'],
                workout_data['sourceName'],
                workout_data['startDate'],
                workout_data['endDate'],
                ';'.join(f"{k}={v}" for k, v in workout_data.items() if k.startswith('metadata_')),
                workout_data['eventType'],
                workout_data['eventDate'],
                workout_data['avgHeartRate'],
                workout_data['avgHeartRateUnit'],
                workout_data['totalSteps'],
                workout_data['totalStepsUnit']
            ]
            writer.writerow(row)
            current_workout = None
            workout_data.clear()
            elem.clear()  # Clear the element to free memory

    # Summary of counts
    print(f"Processed: {workout_count} workouts, {metadata_count} metadata entries, "
          f"{event_count} workout events, {stats_count} workout statistics")

print("Complete workout data has been written to workouts_complete.csv")   
