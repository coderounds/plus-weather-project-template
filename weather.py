import csv
from datetime import datetime

DEGREE_SYMBOL = u"\N{DEGREE SIGN}C"


def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees
        and Celcius symbols.

    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees Celcius."
    """
    return f"{temp}{DEGREE_SYMBOL}"


def convert_date(iso_string):
    """Converts an ISO formatted date into a human-readable format.

    Args:
        iso_string: An ISO date string.
    Returns:
        A date formatted like: Weekday Date Month Year e.g. Tuesday 06 July 2021
    """
    # Convert the ISO string to a datetime object
    date_obj = datetime.fromisoformat(iso_string)  
    # Return the formatted date string
    return date_obj.strftime("%A %d %B %Y")
# print(convert_date("2020-01-01"))

def convert_f_to_c(temp_in_fahrenheit):
    """Converts a temperature from Fahrenheit to Celcius.

    Args:
        temp_in_fahrenheit: float representing a temperature.
    Returns:
        A float representing a temperature in degrees Celcius, rounded to 1 decimal place.
    """
    # pass
    celsius = (float(temp_in_fahrenheit) - 32) * 5/9
    return round(celsius, 1)
# print(f'convert_f_to_c(145) = {convert_f_to_c(145)}')

def calculate_mean(weather_data):
    """Calculates the mean value from a list of numbers.

    Args:
        weather_data: a list of numbers.
    Returns:
        A float representing the mean value.
    """
    # pass
    try:
        total = sum(float(value) for value in weather_data)
        return total / len(weather_data)
    except ZeroDivisionError:
        return 0.0
    except ValueError:
        return "Cannot divide by zero"



def load_data_from_csv(csv_file):
    """Reads a csv file and stores the data in a list.

    Args:
        csv_file: a string representing the file path to a csv file.
    Returns:
        A list of lists, where each sublist is a (non-empty) line in the csv file.
    """
    data = []
    
    try:
        with open(csv_file, 'r', newline='') as file:
            reader = csv.reader(file)
            header_skipped = False
            for row in reader:
                # to filter out empty rows or rows with whitespace
                if row and("for cell in row"):
                    # Skip the header row
                    if not header_skipped:
                        header_skipped = True
                        continue
                    
                    # Convert numeric values to integers (skips date)
                    processed_row = [row[0]]  # Keep date as string
                    for i in range(1, len(row)):
                        try:
                            processed_row.append(int(row[i]))
                        except ValueError:
                            processed_row.append(row[i])  # Keep as string if conversion fails
                    
                    data.append(processed_row)
                    
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return data

def find_min(weather_data):
    """Calculates the minimum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The minimum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """
    if not weather_data:  # Handle empty list
        return ()
    
    # Convert all values to floats
    float_data = [float(value) for value in weather_data]
    
    min_value = min(float_data)  # Find the minimum value
    # Find the *last* occurrence of this minimum value
    last_index = len(float_data) - 1 - float_data[::-1].index(min_value)
    
    return (min_value, last_index)



def find_max(weather_data):
    """Calculates the maximum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The maximum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """
    if not weather_data:  # Handle empty list
        return ()
    
    # Convert all values to floats
    float_data = [float(value) for value in weather_data]
    
    max_value = max(float_data)  # Find the maximum value
    # Find the *last* occurrence of this maximum value
    last_index = len(float_data) - 1 - float_data[::-1].index(max_value)
    
    return (max_value, last_index)


def generate_summary(weather_data):
    """Outputs a summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
   
    if not weather_data:
         return ""

    # Extract all minimum and maximum temperatures
    min_temps = [float(row[1]) for row in weather_data]  # All minimum temperatures
    max_temps = [float(row[2]) for row in weather_data]  # All maximum temperatures

    # Find overall minimum temperature and its date
    overall_min_temp, min_index = find_min(min_temps)
    min_temp_celsius = convert_f_to_c(overall_min_temp)
    min_temp_formatted = format_temperature(min_temp_celsius)
    min_date_formatted = convert_date(weather_data[min_index][0])

    # Find overall maximum temperature and its date
    overall_max_temp, max_index = find_max(max_temps)
    max_temp_celsius = convert_f_to_c(overall_max_temp)
    max_temp_formatted = format_temperature(max_temp_celsius)
    max_date_formatted = convert_date(weather_data[max_index][0])

    # Calculate average temperatures
    avg_low = calculate_mean(min_temps)
    avg_high = calculate_mean(max_temps)
    avg_low_formatted = format_temperature(convert_f_to_c(avg_low))
    avg_high_formatted = format_temperature(convert_f_to_c(avg_high))

    # Create the summary
    num_days = len(weather_data)
    summary = f"{num_days} Day Overview\n"
    summary += f"  The lowest temperature will be {min_temp_formatted}, and will occur on {min_date_formatted}.\n"
    summary += f"  The highest temperature will be {max_temp_formatted}, and will occur on {max_date_formatted}.\n"
    summary += f"  The average low this week is {avg_low_formatted}.\n"
    summary += f"  The average high this week is {avg_high_formatted}.\n"

    return summary


def generate_daily_summary(weather_data):
    """Outputs a daily summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    summary_lines = []
    
    for row in weather_data:
        # Extract date, min and max temperatures
        date_str = row[0]  # ISO date string
        min_temp = row[1]  # Minimum temperature in Fahrenheit
        max_temp = row[2]  # Maximum temperature in Fahrenheit
        
        # Convert date to human-readable format
        formatted_date = convert_date(date_str)
        
        # Convert temperatures from Fahrenheit to Celsius
        min_temp_celsius = convert_f_to_c(min_temp)
        max_temp_celsius = convert_f_to_c(max_temp)
        
        # Format temperatures with degree symbol
        min_temp_formatted = format_temperature(min_temp_celsius)
        max_temp_formatted = format_temperature(max_temp_celsius)
        
        # Create the daily summary for this day
        day_summary = f"---- {formatted_date} ----\n"
        day_summary += f"  Minimum Temperature: {min_temp_formatted}\n"
        day_summary += f"  Maximum Temperature: {max_temp_formatted}\n"
        
        summary_lines.append(day_summary)
    
    # Join all daily summaries with blank lines between them
    return "\n".join(summary_lines) + "\n"
