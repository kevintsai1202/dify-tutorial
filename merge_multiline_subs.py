
import os
import glob

def merge_lines_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Normalize newlines
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    blocks = content.split('\n\n')
    
    new_blocks = []
    modified_count = 0
    
    for block in blocks:
        if not block.strip():
            continue
            
        lines = block.split('\n')
        
        # Check if first line is ID (digits) and second has timestamp
        if len(lines) >= 3 and lines[0].strip().isdigit() and '-->' in lines[1]:
            id_line = lines[0]
            time_line = lines[1]
            text_lines = lines[2:]
            
            # Filter out empty text lines
            text_lines = [l.strip() for l in text_lines if l.strip()]
            
            if len(text_lines) > 1:
                # Merge logic
                merged_text = text_lines[0]
                for next_line in text_lines[1:]:
                    # Basic check for adding space: if both border chars are alphanumeric/ASCII
                    need_space = False
                    if merged_text and next_line:
                        last_char = merged_text[-1]
                        first_char = next_line[0]
                        if (last_char.isascii() and last_char.isalnum()) and (first_char.isascii() and first_char.isalnum()):
                            need_space = True
                    
                    if need_space:
                        merged_text += " " + next_line
                    else:
                        merged_text += next_line
                        
                text_lines = [merged_text]
                modified_count += 1
            
            new_block_lines = [id_line, time_line] + text_lines
            new_blocks.append("\n".join(new_block_lines))
        else:
            # just keep as is
            new_blocks.append(block)
            
    if modified_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(new_blocks))
            f.write("\n") # Ensure final newline
            
    return modified_count

def main():
    base_dir = r"e:\github\dify-tutorial\課綱"
    # Target chapters 3, 4, 5, 6
    target_prefixes = ["3.", "4.", "5.", "6."]
    
    all_files = glob.glob(os.path.join(base_dir, "**", "*.srt"), recursive=True)
    
    total_modified = 0
    files_modified = 0
    
    for file_path in all_files:
        # Check if file is in targeted chapters
        parts = file_path.split(os.sep)
        in_target_chapter = False
        for part in parts:
            for prefix in target_prefixes:
                if part.startswith(prefix):
                    in_target_chapter = True
                    break
            if in_target_chapter:
                break
        
        if in_target_chapter:
            path_str = str(file_path)
            count = merge_lines_in_file(path_str)
            if count > 0:
                print(f"Modified {path_str}: {count} blocks merged.")
                total_modified += count
                files_modified += 1

    print(f"Done. Modified {files_modified} files, merged {total_modified} blocks.")

if __name__ == "__main__":
    main()
