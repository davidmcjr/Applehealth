import xml.etree.ElementTree as ET
import csv

# Parse the XML file
tree = ET.parse('export.xml')  # Replace with your file path
root = tree.getroot()

# Define CSV headers
headers = ['activity type', 'duration', 'date', 'lowest SWolf score', 'distance', 'distance units', 'stroke count', 'heart rate']

# Open CSV file for writing
with open('swimming_workouts.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    # Find all Workout elements
    for workout in root.findall('.//Workout'):
        # Check if it's a swimming workout
        if workout.get('workoutActivityType') == 'HKWorkoutActivityTypeSwimming':
            # Find the lowest SWolf score from WorkoutEvent/MetadataEntry
            swolf_scores = []
            for event in workout.findall('.//WorkoutEvent'):
                for metadata in event.findall('.//MetadataEntry'):
                    if metadata.get('key') == 'HKSWOLFScore':
                        score = metadata.get('value')
                        if score:  # Ensure it’s not None
                            swolf_scores.append(float(score))
            lowest_swolf = min(swolf_scores) if swolf_scores else ''

            # Extract distance, distance units, stroke count, and heart rate from WorkoutStatistics
            distance = ''
            distance_units = ''
            stroke_count = ''
            heart_rate = ''
            for stats in workout.findall('.//WorkoutStatistics'):
                stats_type = stats.get('type')
                if stats_type == 'HKQuantityTypeIdentifierDistanceSwimming':
                    distance = stats.get('sum', '')
                    distance_units = stats.get('unit', '')
                elif stats_type == 'HKQuantityTypeIdentifierSwimmingStrokeCount':
                    stroke_count = stats.get('sum', '')
                elif stats_type == 'HKQuantityTypeIdentifierHeartRate':
                    heart_rate = stats.get('average', '')

            row = {
                'activity type': 'Swimming',
                'duration': workout.get('duration', ''),
                'date': workout.get('startDate', ''),
                'lowest SWolf score': str(lowest_swolf) if lowest_swolf else '',
                'distance': distance,
                'distance units': distance_units,
                'stroke count': stroke_count,
                'heart rate': heart_rate
            }
            writer.writerow(row)

print("Swimming workouts extracted! Check swimming_workouts.csv")
