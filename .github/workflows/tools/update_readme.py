import sys

def update_status(day_to_complete):
    """Updates the status of the specified day in the README.md file to 'COMPLETE'."""
    
    try:
        with open('README.md', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: README.md not found.")
        sys.exit(1)

    # Convert the input day to a string format expected in the table: '| **4** |'
    day_str = f"| **{day_to_complete}** |"
    
    new_lines = []
    updated = False
    
    for line in lines:
        if day_str in line:
            # Check if the line is the target line
            # We look for the status column ('| Status |') which is the fourth column from the right
            parts = line.split('|')
            if len(parts) >= 5:
                # The status is the second-to-last item (parts[4].strip())
                if parts[4].strip() in ('IN PROGRESS', 'PENDING'):
                    # Replace the old status with the new status
                    parts[4] = ' **COMPLETE** '
                    line = '|'.join(parts).rstrip() + '\n'
                    updated = True
        
        new_lines.append(line)

    if updated:
        with open('README.md', 'w') as f:
            f.writelines(new_lines)
        print(f"Successfully updated Day {day_to_complete} status to COMPLETE.")
        return True
    else:
        print(f"Day {day_to_complete} status was already COMPLETE or line not found.")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_readme.py <day_number>")
        sys.exit(1)
        
    try:
        day_number = int(sys.argv[1])
    except ValueError:
        print("Error: Day number must be an integer.")
        sys.exit(1)

    # Only run if a day was successfully completed
    if update_status(day_number):
        # We don't commit here; we rely on the GitHub Action to handle the modified file.
        pass
