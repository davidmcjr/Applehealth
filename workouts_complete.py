#Created with GROK 3 (I have very little coding abilty)
import xml.etree.ElementTree as ET
import csv

def import_running_workouts(xml_file='export.xml', csv_file='activity_data.csv'):
    try:
        # Define the headers
        headers = [
            'activity type',
            'duration',
            'duration unit',
            'start date',
            'temperature',
            'humidity',
            'average ground contact time',
            'average vertical Oscillation',
            'average running speed',
            'total distance',
            'average heart rate'
        ]

        # Parse XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Open CSV file for writing
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write headers
            writer.writerow(headers)
            
            # Count running workouts processed
            running_count = 0
            
            # Find all Workout elements with HKWorkoutActivityTypeRunning
            for workout in root.findall(".//Workout[@workoutActivityType='HKWorkoutActivityTypeRunning']"):
                row = []
                
                # Extract data for each header
                row.append(workout.get('workoutActivityType', ''))  # activity type
                
                # Handle duration
                duration = workout.get('duration', '')
                try:
                    duration = f"{float(duration):.2f}" if duration else ''
                except ValueError:
                    pass
                row.append(duration)  # duration
                
                row.append(workout.get('durationUnit', ''))  # duration unit
                row.append(workout.get('startDate', ''))  # start date
                
                # Look for temperature and humidity in MetadataEntry
                temperature = ''
                humidity = ''
                for metadata in workout.findall('.//MetadataEntry'):
                    if metadata.get('key') == 'HKWeatherTemperature':
                        temperature = metadata.get('value', '')
                    elif metadata.get('key') == 'HKWeatherHumidity':
                        humidity = metadata.get('value', '')
                row.append(temperature)  # temperature
                row.append(humidity)     # humidity
                
                # Look for workout statistics
                ground_contact_time = ''
                vertical_oscillation = ''
                running_speed = ''
                heart_rate_stats = ''
                distance_stats = ''
                for stats in workout.findall('.//WorkoutStatistics'):
                    if stats.get('type') == 'HKQuantityTypeIdentifierRunningGroundContactTime':
                        ground_contact_time = stats.get('average', '')
                        try:
                            ground_contact_time = f"{float(ground_contact_time):.2f}" if ground_contact_time else ''
                        except ValueError:
                            pass
                    elif stats.get('type') == 'HKQuantityTypeIdentifierRunningVerticalOscillation':
                        vertical_oscillation = stats.get('average', '')
                        try:
                            vertical_oscillation = f"{float(vertical_oscillation):.2f}" if vertical_oscillation else ''
                        except ValueError:
                            pass
                    elif stats.get('type') == 'HKQuantityTypeIdentifierRunningSpeed':
                        running_speed = stats.get('average', '')
                        try:
                            running_speed = f"{float(running_speed):.2f}" if running_speed else ''
                        except ValueError:
                            pass
                    elif stats.get('type') == 'HKQuantityTypeIdentifierHeartRate':
                        heart_rate_stats = stats.get('average', '')
                        try:
                            heart_rate_stats = f"{float(heart_rate_stats):.2f}" if heart_rate_stats else ''
                        except ValueError:
                            pass
                    elif stats.get('type') == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
                        distance_stats = stats.get('sum', '')
                        try:
                            distance_stats = f"{float(distance_stats):.2f}" if distance_stats else ''
                        except ValueError:
                            pass
                row.append(ground_contact_time)  # average ground contact time
                row.append(vertical_oscillation)  # average vertical Oscillation
                row.append(running_speed)        # average running speed
                
                # Handle total distance, preferring WorkoutStatistics over Workout attribute
                distance = distance_stats  # Use WorkoutStatistics sum if available
                if not distance:
                    distance = workout.get('totalDistance', '')
                    try:
                        distance = f"{float(distance):.2f}" if distance else ''
                    except ValueError:
                        pass
                row.append(distance)  # total distance
                
                # Look for heart rate, preferring WorkoutStatistics over MetadataEntry
                heart_rate = heart_rate_stats
                if not heart_rate:
                    for metadata in workout.findall('.//MetadataEntry'):
                        if metadata.get('key') == 'HKAverageHeartRate':
                            heart_rate = metadata.get('value', '')
                            try:
                                heart_rate = f"{float(heart_rate):.2f}" if heart_rate else ''
                            except ValueError:
                                pass
                            break
                row.append(heart_rate)  # average heart rate
                
                writer.writerow(row)
                running_count += 1

        print(f"Successfully imported {running_count} running workouts from {xml_file} to {csv_file}")

    except FileNotFoundError:
        print(f"Error: '{xml_file}' file not found in the current directory")
    except ET.ParseError:
        print("Error: Unable to parse XML file - invalid XML format")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

# Run the function
import_running_workouts()
