
import os
import glob
import re
import json

def generate_summary_from_srt(srt_path):
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract text lines (skipping ID and timestamp)
    lines = content.splitlines()
    text_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.isdigit() and i+1 < len(lines) and '-->' in lines[i+1]:
            i += 2
            while i < len(lines) and lines[i].strip():
                text_lines.append(lines[i].strip())
                i += 1
        else:
            i += 1
            
    # Simple extraction of key content for summary (first few lines + middle + end)
    # A real summary would require an LLM, but for now we'll create a description based on filename and some content extraction
    full_text = "".join(text_lines)
    
    # Just return the first 500 chars as a "preview" for the prompt, 
    # and we will use the filename for the README title.
    return full_text[:1000]

def create_readme(folder_path, srt_file):
    readme_path = os.path.join(folder_path, "README.md")
    if os.path.exists(readme_path):
        return False # Already exists
        
    srt_path = os.path.join(folder_path, srt_file)
    content_preview = generate_summary_from_srt(srt_path)
    
    folder_name = os.path.basename(folder_path)
    
    # Create a simple README
    readme_content = f"""# {folder_name}

## 課程摘要
本單元重點內容包含：
{content_preview[:200]}...

## 影片內容
(請參考影片或字幕檔 {srt_file})

![Cover](./cover.png)
"""
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    return True

def main():
    base_dir = r"e:\github\dify-tutorial\課綱"
    target_prefixes = ["3.", "4.", "5.", "6."]
    
    missing_images_list = []
    
    # Iterate through Chapter directories
    for start_dir in os.listdir(base_dir):
        msg = ""
        is_target = False
        for prefix in target_prefixes:
            if start_dir.startswith(prefix):
                is_target = True
                break
        
        if not is_target:
            continue
            
        chapter_dir = os.path.join(base_dir, start_dir)
        if not os.path.isdir(chapter_dir):
            continue
            
        # Iterate through Unit directories
        for unit_dir_name in os.listdir(chapter_dir):
            unit_dir = os.path.join(chapter_dir, unit_dir_name)
            if not os.path.isdir(unit_dir):
                continue
                
            # Check for SRT
            srt_files = glob.glob(os.path.join(unit_dir, "*.srt"))
            if not srt_files:
                continue
                
            srt_file = os.path.basename(srt_files[0])
            
            # Check/Create README
            created_readme = create_readme(unit_dir, srt_file)
            if created_readme:
                print(f"Created README for {unit_dir_name}")
            
            # Check for Image (cover.png or anything)
            image_files = glob.glob(os.path.join(unit_dir, "*.png")) + \
                          glob.glob(os.path.join(unit_dir, "*.jpg")) + \
                          glob.glob(os.path.join(unit_dir, "*.jpeg"))
                          
            if not image_files:
                # Need to generate image
                # Create a prompt based on folder name and SRT content
                content_preview = generate_summary_from_srt(os.path.join(unit_dir, srt_file))
                prompt = f"A modern, tech-focused course cover illustration for '{unit_dir_name}'. Abstract representation of: {content_preview[:100]}... Minimalist, clean, Dify branding colors (blue/white/purple)."
                
                missing_images_list.append({
                    "folder": unit_dir,
                    "image_name": "cover",
                    "prompt": prompt
                })

    # Output the list of missing images to a JSON file for the agent to read
    with open("missing_images_tasks.json", "w", encoding='utf-8') as f:
        json.dump(missing_images_list, f, ensure_ascii=False, indent=2)
        
    print(f"Found {len(missing_images_list)} units missing images.")

if __name__ == "__main__":
    main()
