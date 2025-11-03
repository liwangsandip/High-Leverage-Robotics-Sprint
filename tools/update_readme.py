def update_sprint_status(day_to_start):
    """
    Updates the status in README.md:
    1. Sets the previous day (day_to_start - 1) to 'COMPLETE'.
    2. Sets the current day (day_to_start) to 'IN PROGRESS'.
    """
    
    day_to_complete = day_to_start - 1
    day_to_ip = day_to_start

    try:
        with open('README.md', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: README.md not found.")
        sys.exit(1)

    new_lines = []
    completed_updated = False
    ip_updated = False
    
    # Target strings to identify the correct row (relying only on the number)
    complete_match = f"| **{day_to_complete}**" 
    ip_match = f"| {day_to_ip} |" 
    
    for line in lines:
        original_line = line
        
        # 1. Update the previous day to COMPLETE
        if day_to_complete >= 4 and complete_match in original_line and not completed_updated:
            # Split the line by the pipe '|' character
            parts = original_line.split('|')
            if len(parts) >= 5:
                # The status is the 4th index from the end (index 4 in the split list)
                current_status = parts[4].strip()
                if 'COMPLETE' not in current_status:
                    parts[4] = ' **COMPLETE** '
                    line = '|'.join(parts).rstrip() + '\n'
                    completed_updated = True
        
        # 2. Update the current day to IN PROGRESS
        elif f"| {day_to_ip} " in original_line and not ip_updated: # Use a looser match for IN PROGRESS
            parts = original_line.split('|')
            if len(parts) >= 5:
                current_status = parts[4].strip()
                if 'IN PROGRESS' not in current_status:
                    parts[4] = ' IN PROGRESS '
                    line = '|'.join(parts).rstrip() + '\n'
                    ip_updated = True
        
        new_lines.append(line)

    # [REST OF THE FUNCTION REMAINS THE SAME]
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
