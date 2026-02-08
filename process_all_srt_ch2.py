
import re
import os
import glob

def split_text(text, max_length=20):
    text = text.strip()
    if len(text) <= max_length:
        return [text]
    
    parts = re.split(r'([,，。、\s])', text)
    lines = []
    current_line = ""
    
    for part in parts:
        if len(current_line) + len(part) > max_length:
            if current_line:
                lines.append(current_line)
                current_line = part
            else:
                current_line = part
        else:
            current_line += part
            
    if current_line:
        lines.append(current_line)
        
    lines = [line.strip() for line in lines if line.strip()]
    
    final_lines = []
    for line in lines:
        if len(line) <= max_length:
            final_lines.append(line)
        else:
            for i in range(0, len(line), max_length):
                final_lines.append(line[i:i+max_length])
                
    return final_lines

def process_srt(file_path):
    print(f"Processing: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Comprehensive replacement list for Chapter 2
    replacements_list = [
        # AI/Model Terms
        ("Entropic", "Anthropic"),
        ("ChairGPT", "ChatGPT"),
        ("Gemline", "Gemini"),
        ("Gemini", "Gemini"),
        ("LLM", "LLM"),
        
        # Platforms/Tools
        ("Libre", "Zeabur"),
        ("Github", "GitHub"),
        ("Dhub", "GitHub"),
        ("Git", "Git"),
        ("Clone", "Clone"),
        ("URL", "URL"),
        ("Env", "env"),
        ("example", "example"),
        
        # Docker Terms
        ("Docker Desktop", "Docker Desktop"),
        ("Docker compose", "Docker Compose"),
        ("Docker Compose", "Docker Compose"),
        ("Docker", "Docker"),
        ("container", "Container"),
        ("YML", "YAML"),
        ("Yaml", "YAML"),
        ("yaml", "YAML"),
        ("Up", "Up"),
        ("Down", "Down"),
        ("Start", "Start"),
        ("Stop", "Stop"),
        ("Restart", "Restart"),
        ("Logs", "Logs"),
        
        # OS / General Tech
        ("GUI", "GUI"),
        ("Mac", "Mac"),
        ("Windows", "Windows"),
        ("Microsoft Store", "Microsoft Store"),
        ("ON", "ARM"), # Context fix
        ("WSL2", "WSL 2"),
        ("WSL", "WSL"),
        ("Hyper-V", "Hyper-V"),
        ("Linux", "Linux"),
        ("cmd", "cmd"),
        ("Command Mode", "Command Prompt"), 
        ("Localhost", "localhost"),
        ("Admin", "Admin"),
        ("Password", "Password"),
        ("Email", "Email"),
        ("Login", "Login"),
        ("Setup", "Setup"),
        ("Install", "Install"),
        ("accept", "Accept"),
        ("Google", "Google"),

        # Dify Terms (Less heavy in Ch2 but still relevant)
        ("DG 觀光", "Dify 官方"),
        ("DG", "Dify"),
        ("Defy", "Dify"),
        ("Dg", "Dify"),
        ("Dify", "Dify"),
        ("Aging", "Agent"),
        ("Agent", "Agent"),
        ("Workflow", "Workflow"), 
        ("WorkFlow", "Workflow"),
        ("ChatFlow", "Chatflow"),
        ("ChaFlow", "Chatflow"),
        ("WORKFLOW", "Workflow"),
        
        # General Corrections (copied from Ch3 as safeguard)
        ("每一緊張升高", "美伊緊張升高"),
        ("一分訂好", "一旦定好"),
        ("s我們", "我們"),
        ("觀光", "官方"), 
        ("接取", "擷取"),
    ]
    
    replacements_list.sort(key=lambda x: len(x[0]), reverse=True)
    
    # Pre-correction
    content = content.replace("ON的版本", "ARM 的版本") 

    for old, new in replacements_list:
        content = content.replace(old, new)
        
    lines = content.splitlines()
    new_lines_content = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # SRT Parsing logic
        is_index = line.isdigit()
        
        # Peek next line to confirm it's a timecode (index validation)
        is_valid_index = False
        if is_index:
            if i + 1 < len(lines) and '-->' in lines[i+1]:
                is_valid_index = True
        
        if is_valid_index:
            new_lines_content.append(line) # Index
            i += 1
            if i < len(lines):
                new_lines_content.append(lines[i].strip()) # Timecode
                i += 1
            continue
        
        if '-->' in line:
             new_lines_content.append(line)
             i += 1
             continue

        if not line:
            new_lines_content.append("")
            i += 1
            continue
            
        # Text block collection
        text_block = [line]
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if not next_line:
                break
            # Check if next_line is the start of a new block
            if next_line.isdigit() and (i+1 < len(lines)) and ('-->' in lines[i+1]):
                break
            text_block.append(next_line)
            i += 1
            
        full_text = " ".join(text_block)
        processed_lines = split_text(full_text)
        new_lines_content.extend(processed_lines)
        
        if i < len(lines) and not lines[i].strip():
             new_lines_content.append("")
             i += 1
             
    final_content = "\n".join(new_lines_content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

def main():
    base_path = r"e:\github\dify-tutorial\課綱\2.環境準備篇（增加社群版安裝方式）"
    # Recursive search for all .srt files
    srt_files = glob.glob(os.path.join(base_path, "**", "*.srt"), recursive=True)
    
    for srt_file in srt_files:
        process_srt(srt_file)
        
if __name__ == "__main__":
    main()
