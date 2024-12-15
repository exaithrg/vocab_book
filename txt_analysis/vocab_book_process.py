import os
from typing import List, Dict
from datetime import datetime

class VocabularyUnit:
    def __init__(self, entry: str, contents: str):
        self.entry = entry.strip()
        self.contents = contents.strip()
        self.count = 1  # Initialize the counter for occurrences
        self.first_word = self.extract_first_word(entry)

    @staticmethod
    def extract_first_word(text: str) -> str:
        words = text.split()
        if words:
            return words[0]
        return ''

def parse_vocab_book(file_path: str) -> List[VocabularyUnit]:
    units: List[VocabularyUnit] = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            current_unit_lines = []
            previous_line_empty = False  # Track whether the last line was empty
            for line in lines:
                stripped_line = line.strip()
                if stripped_line.startswith('========================================================================'):
                    if current_unit_lines:  # If there's a unit accumulated, finalize it and add to the list.
                        entry, contents = extract_entry_and_contents(current_unit_lines)
                        units.append(VocabularyUnit(entry, ''.join(current_unit_lines)))
                        current_unit_lines = [line]  # Start new unit with separator
                    else:
                        current_unit_lines.append(line)  # Add separator for the first unit
                    previous_line_empty = False  # Reset after a unit separator
                else:
                    if not (stripped_line == '' and previous_line_empty):  # Avoid consecutive empty lines
                        current_unit_lines.append(line)
                        previous_line_empty = stripped_line == ''
            # Handle the last unit if any
            if current_unit_lines:
                entry, contents = extract_entry_and_contents(current_unit_lines)
                units.append(VocabularyUnit(entry, ''.join(current_unit_lines)))

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except IOError as e:
        print(f"Error reading file: {e}")

    return units

def extract_entry_and_contents(lines: List[str]) -> (str, str):
    if len(lines) > 1 and lines[0].startswith('========================================================================'):
        first_line = lines[1]
    else:
        first_line = lines[0]

    # Check if the line contains phonetic symbols (indicating an entry with pronunciation)
    if '[' in first_line and ']' in first_line:
        # Extract the part before the phonetic symbols
        entry = first_line.split('[')[0].strip()
    elif first_line.startswith('>>>'):
        # Remove the leading '>>>' and take the rest of the line as entry
        entry = first_line[3:].strip()
    else:
        # Take the whole line as entry
        entry = first_line.strip()

    return entry, ''.join(lines)

def sort_units(units: List[VocabularyUnit]) -> List[VocabularyUnit]:
    return sorted(units, key=lambda unit: unit.entry.lower())

def merge_duplicate_entries(units: List[VocabularyUnit]) -> List[VocabularyUnit]:
    merged_units: List[VocabularyUnit] = []
    seen_entries: Dict[str, VocabularyUnit] = {}

    for unit in units:
        if unit.entry in seen_entries:
            # Increment the count of the existing unit
            seen_entries[unit.entry].count += 1
        else:
            # Add new unit to the dictionary and list
            seen_entries[unit.entry] = unit
            merged_units.append(unit)

    return merged_units

# Usage example
if __name__ == "__main__":
    input_file_path = os.path.join(os.path.dirname(__file__), '../vocab_book.txt')
    
    # Get current timestamp and format it
    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    
    # output_brief_file_path = os.path.join(os.path.dirname(__file__), f'vocab_book_brief_{timestamp}.txt')
    # output_detail_file_path = os.path.join(os.path.dirname(__file__), f'vocab_book_detail_{timestamp}.txt')
    output_brief_file_path = os.path.join(os.path.dirname(__file__), f'vocab_book_brief.txt')
    output_detail_file_path = os.path.join(os.path.dirname(__file__), f'vocab_book_detail.txt')

    vocab_units = parse_vocab_book(input_file_path)
    sorted_vocab_units = sort_units(vocab_units)
    merged_vocab_units = merge_duplicate_entries(sorted_vocab_units)

    # Write brief information to one file
    with open(output_brief_file_path, 'w', encoding='utf-8') as brief_file:
        for unit in merged_vocab_units:
            brief_file.write(f"entry: {unit.entry}\n")
            brief_file.write(f"first word: {unit.first_word}\n")
            brief_file.write(f"occurrences: {unit.count}\n\n")

    # Write detailed contents to another file
    with open(output_detail_file_path, 'w', encoding='utf-8') as detail_file:
        for unit in merged_vocab_units:
            detail_file.write(f"{unit.contents}\n\n")

    print("Output has been written to:")
    print(f"Brief output: {output_brief_file_path}")
    print(f"Detail output: {output_detail_file_path}")