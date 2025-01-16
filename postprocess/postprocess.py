import os
import sys
import re
import pdb
from typing import List, Dict
from datetime import datetime

# 2025.1.16 I have fully understood these codes.

class VocabularyUnit:
    def __init__(self, entry: str, contents: str):
        self.entry = entry.strip()
        self.contents = contents.strip()
        self.count = 1  # Initialize the counter for occurrences
        self.first_4_words = self.extract_first_4_words(entry)

    @staticmethod
    def extract_first_4_words(text: str) -> str:
        words = text.split()
        if words:
            # return words[:4]
            return ' '.join(words[:4])
        return ''

def parse_vocab_book(file_path: str) -> List[VocabularyUnit]:
    units: List[VocabularyUnit] = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # pdb.set_trace()
            # 2025.1.15 2:56:33 I wrote "lines: List[str] = file.readlines()"
            #   which indicates that my python skill is rapidly improving
            lines: List[str] = file.readlines()
            current_unit_lines = []
            previous_line_empty = False  # Track whether the last line was empty
            # regular expressions pattern
            vocab_unit_start_separator='^={72}$'
            for line in lines:
                stripped_line:str = line.strip()
                # if stripped_line.startswith('='*72):
                if re.match(vocab_unit_start_separator, stripped_line):
                    if current_unit_lines:  # If there's a unit accumulated, finalize it and add to the list.
                        # current_unit_lines: List[str]
                        entry, contents = extract_entry_and_contents(current_unit_lines)
                        units.append(VocabularyUnit(entry, ''.join(current_unit_lines)))
                        current_unit_lines = [line]  # Start new unit with separator('^={72}$')
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

    except FileNotFoundError as e:
        print(type(e))
        print(f"Error: The file at {file_path} was not found. {e}")
    except IOError as e:
        print(type(e))
        print(f"Error reading file: {e}")
    
    return units

# process a vocab unit (multiple continious lines)
def extract_entry_and_contents(lines: List[str]) -> (str, str):
    # Check if lines only have 1 line which is "^={72}$"
    if len(lines) == 1:
        assert False, "This should never happen"
    # Check if the line[1] contains phonetic symbols (indicating an entry with pronunciation)
    if '[' in lines[1]:
        # Extract the part before the phonetic symbols
        entry = lines[1].split('[')[0].strip()
    # Standard starts
    elif lines[1].startswith('>>>'):
        # Remove the leading '>>>' and take the rest of the line as entry
        entry = lines[1][3:].strip()
    else:
        # Take the whole line as entry
        entry = lines[1].strip()

    return entry, ''.join(lines)

# Do not change entry and contents
def replace_commas_with_caret(units: List[VocabularyUnit]) -> List[VocabularyUnit]:
    for unit in units:
        # Replace commas with carets in the `first_4_words` attribute
        unit.first_4_words = unit.first_4_words.replace(',', '^')
    return units

def alphabet_sort_units(units: List[VocabularyUnit]) -> List[VocabularyUnit]:
    # sort name first, then sort counts
    return sorted(units, key=lambda unit: (unit.entry.lower(), unit.count))

def count_and_merge_duplicate_entries(units: List[VocabularyUnit]) -> List[VocabularyUnit]:
    merged_units: List[VocabularyUnit] = []
    seen_entries: Dict[str, VocabularyUnit] = {}

    for unit in units:
        if unit.entry in seen_entries:
            # Increment the count of the existing unit
            seen_entries[unit.entry].count += 1
            # Use the latest version
            seen_entries[unit.entry].contents = unit.contents
        else:
            # Add new unit to the dictionary and list
            seen_entries[unit.entry] = unit
            merged_units.append(unit)

    return merged_units

def query_frequency_sort_units(units: List[VocabularyUnit]) -> List[VocabularyUnit]:
    # sort name first, then sort counts
    return sorted(units, key=lambda unit: (-unit.count, unit.entry.lower()))

def update_original_units_count(units_ori: List[VocabularyUnit], units: List[VocabularyUnit]) -> List[VocabularyUnit]:
    # Dict: {entry: count}
    entry_to_count = {unit.entry: unit.count for unit in units}
    for unit_ori in units_ori:
        if unit_ori.entry in entry_to_count:
            unit_ori.count = entry_to_count[unit_ori.entry]
    return units_ori

def query_frequency_sort_units(units: List[VocabularyUnit]) -> List[VocabularyUnit]:
    # sort name first, then sort counts
    return sorted(units, key=lambda unit: unit.count, reverse=True)

def merge_continous_duplicate_entries(units: List[VocabularyUnit]) -> List[VocabularyUnit]:
    if not units:
        return []

    merged_units: List[VocabularyUnit] = []
    previous_unit: VocabularyUnit = units[0]
    merged_units.append(previous_unit)

    for current_unit in units[1:]:
        if current_unit.entry != previous_unit.entry:
            merged_units.append(current_unit)
            previous_unit = current_unit

    return merged_units

# MAIN
if __name__ == "__main__":

    # print(sys.path)
    # pdb.set_trace()

    # input_file_path = './testcase/testcase_language.txt'
    # generated_path_prefix = './testcase/generated/testcase_language'

    input_file_path = './250116/academic_language.txt'
    # AVL: ACADEMIC VOCABULARY LEXICON
    generated_path_prefix = './250116/generated/AVL'

    # input_file_path = './250116/everyday_language.txt'
    # # EED: EVERYDAY ENGLISH DICTIONARY
    # generated_path_prefix = './250116/generated/EED'

    output_brief_file_path = generated_path_prefix + '_BRIEF.txt'
    # WORD DETAILS with ALPHABETICAL ORDER
    output_detail_file_path = generated_path_prefix + '_WD_AO.txt'
    # WORD LIST with ALPHABETICAL ORDER
    output_alphabet_csv_file_path = generated_path_prefix + '_WL_AO.csv'
    # WORD LIST with QUERY-FREQUENCY ORDER
    output_frequency_csv_file_path = generated_path_prefix + '_WL_QFO.csv'
    # WORD LIST with QUERY ORDER
    output_oriwithfreq_csv_file_path = generated_path_prefix + '_WL_QO.csv'

    vocab_units = parse_vocab_book(input_file_path)
    careted_vocab_units = replace_commas_with_caret(vocab_units)
    alphabet_sorted_vocab_units = alphabet_sort_units(careted_vocab_units)
    merged_vocab_units = count_and_merge_duplicate_entries(alphabet_sorted_vocab_units)

    directory = os.path.dirname(output_brief_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write brief information to one file
    with open(output_brief_file_path, 'w', encoding='utf-8') as brief_file:
        for unit in merged_vocab_units:
            brief_file.write(f"entry: {unit.entry}\n")
            brief_file.write(f"occurrences: {unit.count}\n")
            brief_file.write(f"first 4 words: {unit.first_4_words}\n")
            brief_file.write("\n")

    # Write detailed contents to another file
    with open(output_detail_file_path, 'w', encoding='utf-8') as detail_file:
        for unit in merged_vocab_units:
            detail_file.write(f"{unit.contents}\n\n")

    # Write first_4_words and unit.count to csv file
    # Do not use encoding='utf-8', or will cause Excel 
    with open(output_alphabet_csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
        # 3 units in 1 csv line
        chunknum = 0
        for unit in merged_vocab_units:
            csv_line = ','.join([unit.first_4_words, str(unit.count)])
            csv_file.write(f"{csv_line}")
            chunknum += 1
            if chunknum == 3:
                csv_file.write("\n")
                chunknum = 0
            else:
                csv_file.write(",")

    freq_alphabet_vocab_units = query_frequency_sort_units(merged_vocab_units)

    with open(output_frequency_csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
        # 3 units in 1 csv line
        chunknum = 0
        for unit in freq_alphabet_vocab_units:
            csv_line = ','.join([unit.first_4_words, str(unit.count)])
            csv_file.write(f"{csv_line}")
            chunknum += 1
            if chunknum == 3:
                csv_file.write("\n")
                chunknum = 0
            else:
                csv_file.write(",")

    freqed_ori_vocab_units = update_original_units_count(vocab_units, merged_vocab_units)
    # freq_query_order_vocab_units = query_frequency_sort_units(freqed_ori_vocab_units)
    # merged_fqo_vocab_units = merge_continous_duplicate_entries(freq_query_order_vocab_units)

    with open(output_oriwithfreq_csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
        # 3 units in 1 csv line
        chunknum = 0
        for unit in freqed_ori_vocab_units:
            csv_line = ','.join([unit.first_4_words, str(unit.count)])
            csv_file.write(f"{csv_line}")
            chunknum += 1
            if chunknum == 3:
                csv_file.write("\n")
                chunknum = 0
            else:
                csv_file.write(",")

    print("Output has been written to:")
    print(f"Brief output: {output_brief_file_path}")
    print(f"Detail output: {output_detail_file_path}")
    print(f"Alphabet CSV output: {output_alphabet_csv_file_path}")
    print(f"Frequency CSV output: {output_frequency_csv_file_path}")
    print(f"Original Sequnce with Freqency CSV output: {output_oriwithfreq_csv_file_path}")
