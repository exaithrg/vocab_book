class VocabularyUnit:
    def __init__(self, entry, contents):
        self.entry = entry.strip()
        self.contents = contents.strip()

def parse_vocab_book(file_path):
    units = []
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
        else:
            if current_unit_lines or not line.startswith('>>>'):  # Add line to current unit unless it's the start of a new unit
                current_unit_lines.append(line)

        # Handle the last unit if any
        if current_unit_lines:
            entry, contents = extract_entry_and_contents(current_unit_lines)
            units.append(VocabularyUnit(entry, '\n'.join(current_unit_lines)))

    return units

def extract_entry_and_contents(lines):
    entry_line = lines[1] if lines[0].startswith('========================================================================') else lines[0]
    entry = entry_line if not entry_line.startswith('>>>') else entry_line[4:]
    return entry, ''.join(lines)

# Usage example
if __name__ == "__main__":
    vocab_units = parse_vocab_book('test_vocab_book.txt')
    for unit in vocab_units:
        print(f"entry: {unit.entry}")
        print(f"contents: {unit.contents}\n")