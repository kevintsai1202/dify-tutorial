import json
import os
import re
import math
from pathlib import Path

def parse_duration_from_srt(srt_path):
    """
    Parses the last timestamp from an SRT file and returns the duration in minutes.
    Returns None if no comprehensive timestamp is found.
    """
    try:
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex to find timestamps: 00:00:00,000 --> 00:00:05,000
        # We want the end time of the last block.
        # It's safer to find all matches and take the last one's end time.
        timestamp_pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2})[,.](\d{3})')
        matches = list(timestamp_pattern.finditer(content))
        
        if not matches:
            return None
            
        # Last match is naturally the end time of the last subtitle? 
        # Actually SRT structure is: 
        # N
        # Start --> End
        # Text
        #
        # So every block has two timestamps. The pattern will match twice per block.
        # The very last match in the file should be the end time of the last subtitle.
        
        last_match = matches[-1]
        hours = int(last_match.group(1))
        minutes = int(last_match.group(2))
        seconds = int(last_match.group(3))
        milliseconds = int(last_match.group(4))
        
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
        duration_minutes = math.ceil(total_seconds / 60.0) # Round up to nearest minute
        
        # If it's 0 minutes (very short), make it at least 1
        return max(1, duration_minutes)
        
    except Exception as e:
        print(f"Error parsing {srt_path}: {e}")
        return None

def update_courses():
    courses_path = Path('courses.json')
    if not courses_path.exists():
        print("courses.json not found!")
        return

    with open(courses_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_course_duration = 0
    updates_log = []

    for chapter in data.get('chapters', []):
        chapter_duration = 0
        print(f"Processing Chapter: {chapter.get('title')}")
        
        for unit in chapter.get('units', []):
            original_duration = unit.get('duration', 0)
            content_path_str = unit.get('contentPath', '')
            
            # Resolve absolute path to content directory
            # contentPath is relative to root, e.g. "課綱/..."
            # We assume the .srt file is in the same directory as the content file
            
            if not content_path_str:
                chapter_duration += original_duration
                continue
                
            content_path = Path(content_path_str)
            content_dir = content_path.parent
            
            # Search for .srt files in this directory
            # We look for a file that contains the unit ID or just any .srt if there's only one video per folder
            # The folder structure seems to be one unit per folder usually.
            
            if not content_dir.exists():
                # Try relative to current script dir if paths are relative
                content_dir = Path.cwd() / content_dir
                
            found_duration = None
            if content_dir.exists():
                srt_files = list(content_dir.glob('*.srt'))
                
                # Heuristic: if multiple srt, try to match unit ID? 
                # IDs are like 'unit-1-1', filenames like '1-1.srt'
                # Let's try to match the filename specifically if possible.
                # Extract '1-1' from 'unit-1-1'
                unit_id_short = unit['id'].replace('unit-', '') # '1-1'
                
                target_srt = None
                for srt in srt_files:
                    if unit_id_short in srt.name:
                        target_srt = srt
                        break
                
                # If no specific match, but there is exactly one srt, use it.
                if not target_srt and len(srt_files) == 1:
                    target_srt = srt_files[0]
                    
                if target_srt:
                    duration = parse_duration_from_srt(target_srt)
                    if duration is not None:
                        found_duration = duration
                        print(f"  - Unit {unit['title']}: Found {target_srt.name}, duration {duration} min (was {original_duration})")
            
            if found_duration is not None:
                unit['duration'] = found_duration
                chapter_duration += found_duration
                if found_duration != original_duration:
                    updates_log.append(f"Updated {unit['title']} ({unit['id']}): {original_duration} -> {found_duration} min")
            else:
                print(f"  - Unit {unit['title']}: No matching .srt found, keeping {original_duration} min")
                chapter_duration += original_duration

        chapter['duration'] = chapter_duration
        total_course_duration += chapter_duration
        print(f"  -> Chapter Total: {chapter_duration} min")

    data['estimatedTotalTime'] = total_course_duration
    print(f"Total Course Duration: {total_course_duration} min")

    with open(courses_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print("\ncourses.json updated successfully.")
    
    if updates_log:
        print("\nSummary of updates:")
        for log in updates_log:
            print(log)

if __name__ == "__main__":
    update_courses()
