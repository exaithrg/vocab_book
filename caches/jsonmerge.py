import os
import json
from collections import defaultdict, Counter
from datetime import datetime
import glob
import pandas as pd

# Helper function to chunk the list into groups of n items
def chunk_list(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Get current date and time formatted as a string including year, month, day, hour, minute, second
current_datetime = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

# Use glob module to automatically retrieve all JSON files in the current directory starting with 'counter-'
json_files = glob.glob('counter-*.json')

if not json_files:
    print("No 'counter-' prefixed .json files found for merging.")
else:
    # Print the list of files that are about to be merged
    print("The following files will be merged:")
    for file in json_files:
        print(f"  - {file}")
    
    # Prompt user for confirmation
    confirmation = input("Please enter 'yes' to confirm and proceed with the merge: ").strip().lower()
    
    if confirmation == 'yes':
        # Create a dictionary with default integer 0 to store merged data
        merged_data = defaultdict(int)

        # Iterate over all JSON files and merge the data
        for file in json_files:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for key, value in data.items():
                    merged_data[key] += value

        # Prepare data for two different sorts
        sorted_by_alphabet = dict(sorted(merged_data.items()))
        sorted_by_frequency = dict(sorted(merged_data.items(), key=lambda item: (-item[1], item[0])))

        # Function to save JSON and CSV files
        def save_files(data, base_filename):
            json_output_file = f'{base_filename}.json'
            csv_output_file = f'{base_filename}.csv'

            # Save JSON file
            with open(json_output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            # Convert dictionary to flat list of word-frequency pairs and group them into chunks of 6
            flat_list = [item for pair in data.items() for item in pair]
            chunked_list = list(chunk_list(flat_list, 6))

            # Save as CSV without header
            with open(csv_output_file, 'w', encoding='utf-8', newline='') as f:
                for chunk in chunked_list:
                    f.write(','.join(map(str, chunk)) + '\n')

            return json_output_file, csv_output_file

        # Save alphabetically sorted result
        alphabet_base_filename = f'merged_vocab_alphabet_{current_datetime}'
        alphabet_json_file, alphabet_csv_file = save_files(sorted_by_alphabet, alphabet_base_filename)

        # Save frequency-sorted result
        frequency_base_filename = f'merged_vocab_freqency_{current_datetime}'
        frequency_json_file, frequency_csv_file = save_files(sorted_by_frequency, frequency_base_filename)

        print(f"All JSON files have been successfully merged and saved to '{alphabet_json_file}' (alphabetical order)")
        print(f"CSV version saved to '{alphabet_csv_file}'")
        print(f"All JSON files have been successfully merged and saved to '{frequency_json_file}' (frequency order)")
        print(f"CSV version saved to '{frequency_csv_file}'")
    else:
        print("Operation cancelled.")