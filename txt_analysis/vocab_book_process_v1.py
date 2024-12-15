import os
from typing import List, Dict

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
            for line in lines:
                if line.startswith('========================================================================'):
                    if current_unit_lines:  # If there's a unit accumulated, finalize it and add to the list.
                        entry, contents = extract_entry_and_contents(current_unit_lines)
                        units.append(VocabularyUnit(entry, '\n'.join(current_unit_lines)))
                        current_unit_lines = []
                current_unit_lines.append(line)

            # Handle the last unit if any
            if current_unit_lines:
                entry, contents = extract_entry_and_contents(current_unit_lines)
                units.append(VocabularyUnit(entry, '\n'.join(current_unit_lines)))

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
    return sorted(units, key=lambda unit: unit.entry)

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
    file_path = os.path.join(os.path.dirname(__file__), 'test_vocab_book.txt')
    vocab_units = parse_vocab_book(file_path)
    sorted_vocab_units = sort_units(vocab_units)
    merged_vocab_units = merge_duplicate_entries(sorted_vocab_units)

    for unit in merged_vocab_units:
        print(f"entry: {unit.entry}")
        print(f"first word: {unit.first_word}")
        # print(f"contents: {unit.contents}")
        print(f"occurrences: {unit.count}\n")