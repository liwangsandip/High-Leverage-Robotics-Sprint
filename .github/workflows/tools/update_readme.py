import sys

def update_sprint_status(day_to_start):
    """
    Updates the status in README.md:
    1. Sets the previous day (day_to_start - 1) to 'COMPLETE'.
    2. Sets the current day (day_to_start) to 'IN PROGRESS'.
    """
    
    # Day to be set to COMPLETE
    day_to_complete = day_to_start - 1
    # Day to be set to IN PROGRESS
    day_to_ip = day_to_start

    print(f"Targeting Day {day_to_complete} for COMPLETE and Day {day_to_ip} for IN PROGRESS.")

    try:
        with open('README.md', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: README.md not found.")
        sys.exit(1)

    new_lines = []
    completed_updated = False
    ip_updated = False
    
    # Strings to match in the README table's first column (using bold formatting)
    complete_str = f"| **{day_to_complete}** |" 
    ip_str = f"| **{day_to_ip}** |" 

    for line in lines:
        original_line = line
        
        # 1. Update the previous day to COMPLETE
        if day_to_complete >= 4 and complete_str in line and not completed_updated:
            parts = line.split('|')
            if len(parts) >= 5:
                current_status = parts[4].strip()
                if current_status not in ('**COMPLETE**', 'COMPLETE'):
                    parts[4] = ' **COMPLETE** '
                    line = '|'.join(parts).rstrip() + '\n'
                    completed_updated = True
        
        # 2. Update the current day to IN PROGRESS
        elif ip_str in line and not ip_updated:
            parts = line.split('|')
            if len(parts) >= 5:
                current_status = parts[4].strip()
                if current_status not in ('IN PROGRESS', '**IN PROGRESS**'):
                    parts[4] = ' IN PROGRESS '
                    line = '|'.join(parts).rstrip() + '\n'
                    ip_updated = True
        
        new_lines.append(line)

    if completed_updated or ip_updated:
        with open('README.md', 'w') as f:
            f.writelines(new_lines)
        print("README.md successfully updated.")
        print(f" - Day {day_to_complete}: COMPLETE")
        print(f" - Day {day_to_ip}: IN PROGRESS")
        return True
    else:
        print("No status changes were needed or found.")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_readme.py <day_number_to_start>")
        sys.exit(1)
        
    try:
        day_number = int(sys.argv[1])
    except ValueError:
        print("Error: Day number must be an integer.")
        sys.exit(1)

    # We start tracking from Day 5, so the first trigger should be Day 5 (completing 4)
    if day_number < 5: 
        print("Automation only runs for Day 5 and onward.")
        sys.exit(0)

    update_sprint_status(day_number)
