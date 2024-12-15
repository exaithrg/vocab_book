import os
from typing import List

class VocabularyUnit:
    def __init__(self, entry: str, contents: str):
        self.entry = entry.strip()
        self.contents = contents.strip()

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
    entry_line = lines[1] if len(lines) > 1 and lines[0].startswith('========================================================================') else lines[0]
    entry = entry_line if not entry_line.startswith('>>>') else entry_line[4:]
    return entry, ''.join(lines)

# Usage example
if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), 'test_vocab_book.txt')
    vocab_units = parse_vocab_book(file_path)
    for unit in vocab_units:
        print(f"entry: {unit.entry}")
        print(f"contents: {unit.contents}\n")