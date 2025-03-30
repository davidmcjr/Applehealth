import xml.etree.ElementTree as ET
import csv

# Define the output CSV file path
output_csv = 'cycling_workouts.csv'

# Define the headers as requested
headers = [
    'activity type', 'duration', 'temperature', 'indoor workout', 'humidity',
    'climbing', 'average heart rate', 'maximum heart rate', 'average Cadance', 'max Cadance'
]

# Function to extract metadata by key from Workout element
def get_metadata(workout, key):
    for metadata in workout.findall('MetadataEntry'):
        if metadata.get('key') == key:
            return metadata.get('value')
    return 'N/A'

# Function to extract statistics (e.g., heart rate, cadence) from WorkoutStatistics
def get_statistic(workout, stat_type, attr):
    for stats in workout.findall('WorkoutStatistics'):
        if stats.get('type') == stat_type:
            return stats.get(attr, 'N/A')
    return 'N/A'

# Parse the XML file
tree = ET.parse('export.xml')  # Replace with your XML file path
root = tree.getroot()

# Filter for cycling workouts and collect data
cycling_workouts = []
for workout in root.findall('.//Workout'):
    if workout.get('workoutActivityType') == 'HKWorkoutActivityTypeCycling':
        workout_data = {
            'activity type': 'Cycling',
            'duration': workout.get('duration', 'N/A'),
            'temperature': get_metadata(workout, 'HKWeatherTemperature'),
            'indoor workout': get_metadata(workout, 'HKIndoorWorkout'),
            'humidity': get_metadata(workout, 'HKWeatherHumidity'),
            'climbing': get_metadata(workout, 'HKElevationAscended'),
            'average heart rate': get_statistic(workout, 'HKQuantityTypeIdentifierHeartRate', 'average'),
            'maximum heart rate': get_statistic(workout, 'HKQuantityTypeIdentifierHeartRate', 'maximum'),
            'average Cadance': get_statistic(workout, 'HKQuantityTypeIdentifierCyclingCadence', 'average'),
            'max Cadance': get_statistic(workout, 'HKQuantityTypeIdentifierCyclingCadence', 'maximum')
        }
        cycling_workouts.append(workout_data)

# Write to CSV
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    for workout in cycling_workouts:
        writer.writerow(workout)

print(f"Conversion complete. Cycling workouts saved to {output_csv}")
