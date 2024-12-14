import os
import json
from collections import defaultdict, Counter
from datetime import datetime
import glob

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

        # Save the alphabetically sorted result to a new JSON file
        alphabet_output_file = f'merged_vocab_alphabet_{current_datetime}.json'
        with open(alphabet_output_file, 'w', encoding='utf-8') as f:
            json.dump(sorted_by_alphabet, f, ensure_ascii=False, indent=4)

        # Save the frequency-sorted result to a new JSON file
        frequency_output_file = f'merged_vocab_freqency_{current_datetime}.json'
        with open(frequency_output_file, 'w', encoding='utf-8') as f:
            json.dump(sorted_by_frequency, f, ensure_ascii=False, indent=4)

        print(f"All JSON files have been successfully merged and saved to '{alphabet_output_file}' (alphabetical order)")
        print(f"All JSON files have been successfully merged and saved to '{frequency_output_file}' (frequency order)")
    else:
        print("Operation cancelled.")