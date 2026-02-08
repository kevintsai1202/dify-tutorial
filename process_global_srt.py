
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

def get_replacements(file_path):
    # Base replacements for ALL files
    replacements = [
        # AI/Model Terms
        ("Entropic", "Anthropic"),
        ("ChairGPT", "ChatGPT"),
        ("Gemline", "Gemini"),
        ("Gemini", "Gemini"), # Case fix if needed
        ("LLM", "LLM"),
        ("OpenAI", "OpenAI"),
        ("Dall-E", "DALL-E"),
        ("Midjourney", "Midjourney"),
        ("Stable Diffusion", "Stable Diffusion"),
        
        # Tools/Platforms
        ("Libre", "Zeabur"), # Global fix per user legacy
        ("Github", "GitHub"),
        ("Dhub", "GitHub"),
        ("ESA社區", "Exa Search"),
        ("ESA社群", "Exa Search"),
        ("ESA Search", "Exa Search"), 
        ("ESA", "Exa"), 
        ("FireClaw", "Firecrawl"),
        ("FireCore", "Firecrawl"),
        ("FireCORE", "Firecrawl"),
        ("FireCrawl", "Firecrawl"),
        ("WebScraper", "Web Scraper"),
        ("Web Scraper", "Web Scraper"),
        ("Supabase", "Supabase"),
        
        # Dify / App Terms
        ("DG 觀光", "Dify 官方"),
        ("DG", "Dify"),
        ("Dg", "Dify"),
        ("Defy", "Dify"),
        ("Dify", "Dify"),
        ("Aging", "Agent"),
        ("Agent", "Agent"),
        ("Workflow", "Workflow"), 
        ("WorkFlow", "Workflow"),
        ("ChatFlow", "Chatflow"),
        ("Chatbot", "Chatbot"),
        ("Knowledge Retrieval", "Knowledge Retrieval"),
        ("Function calling", "Function Calling"),
        ("HTTP Request", "HTTP Request"),
        ("RAG", "RAG"),
        ("Context", "Context"),
        
        # Docker / Env
        ("Docker Desktop", "Docker Desktop"),
        ("Docker compose", "Docker Compose"),
        ("Docker Compose", "Docker Compose"),
        ("Docker", "Docker"),
        ("docker", "Docker"), # Fix lowercase
        ("都可", "Docker"),    # Fix typo
        ("都科", "Docker"),    # Fix typo
        ("WSL2", "WSL 2"),
        ("Hyper-V", "Hyper-V"),
        ("Linux", "Linux"),
        ("Command Mode", "Command Prompt"),
        ("ON的版本", "ARM 的版本"),
        ("container", "Container"),
        ("cmd", "cmd"),
        
        # Typos
        ("每一緊張升高", "美伊緊張升高"),
        ("一分訂好", "一旦定好"),
        ("s我們", "我們"),
        ("觀光", "官方"), 
        ("接取", "擷取"),
        ("GUI", "GUI"),
        ("Divi", "Dify"),     # Fix typo
        ("dify", "Dify"),     # Fix lowercase
        ("git", "Git"),       # Fix lowercase
        ("github", "GitHub"), # Fix lowercase
    ]

    # Context Specific: Replicate
    # If we are in Chapter 1 (Intro), Replicate is likely the Provider.
    # If we are in Chapter 3 (Basic Ops), "Replicate" might be the misheard "Zeabur" (based on 3-1 history), 
    # BUT I will only replace "Libre". I will NOT replace "Replicate" to "Zeabur" automatically unless explicitly safe.
    # The user approved plan says: "Ensure Replicate is NOT globally replaced".
    # So I will NOT add ("Replicate", "Zeabur") to the list.
    
    # Sort by length
    replacements.sort(key=lambda x: len(x[0]), reverse=True)
    return replacements

def process_srt(file_path):
    print(f"Processing: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = get_replacements(file_path)
    
    replacements = get_replacements(file_path)
    
    # Context Specific: dify1-1.srt
    if "dify1-1.srt" in file_path or "1-1.srt" in file_path:
         replacements.extend([
             ("Cloud", "Claude"), 
             ("QRGBT", "ChatGPT"),
             ("Gem9", "Gemini"),
             ("AIAGINE", "AI Agent"),
             ("AIAGIN", "AI Agent"),
             ("Aging", "Agent"),
             ("AI Aging", "AI Agent"),
             ("RLEG", "RAG"),
             ("Haha", "Hahow"),
             ("Trade", "Threads"),
             ("vibcoding", "Writing Code"), 
             ("NCP", "MCP"),
             ("開發查檢", "開發插件"),
             ("創接", "串接"),
             ("7月級", "企業級"),
             ("取寫", "學習"),
             ("節止", "截止"),
             ("ChairGPT", "ChatGPT"),
         ])

    # Context Specific: dify1-2.srt
    if "dify1-2.srt" in file_path or "1-2.srt" in file_path:
         replacements.extend([
             ("self host", "Self-hosted"),
             ("update", "Update"),
             ("script", "Script"),
             ("maintain", "Maintain"),
             ("cover", "Cover"),
             ("纔有", "才有"),
             ("色情版本", "社群版本"),
             ("剋制", "客製"),
         ])

    # Context Specific: dify1-3.srt
    if "dify1-3.srt" in file_path or "1-3.srt" in file_path:
        replacements.extend([
            ("Context7", "Context"),
            ("登錄", "登入"),
        ])

    # General misc additions
    replacements.extend([
        ("n8n", "n8n"),
        ("make", "Make"),
    ])
    
    # Sort again to ensure new additions are prioritized if longer
    replacements.sort(key=lambda x: len(x[0]), reverse=True)
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    lines = content.splitlines()
    new_lines_content = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        is_index = line.isdigit()
        is_valid_index = False
        if is_index:
            if i + 1 < len(lines) and '-->' in lines[i+1]:
                is_valid_index = True
        
        if is_valid_index:
            new_lines_content.append(line)
            i += 1
            if i < len(lines):
                new_lines_content.append(lines[i].strip())
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
            
        text_block = [line]
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if not next_line:
                break
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
    # Define the 3 chapter directories
    base_dirs = [
        r"e:\github\dify-tutorial\課綱\1.入門篇 - Dify 基礎入門",
        r"e:\github\dify-tutorial\課綱\2.環境準備篇（增加社群版安裝方式）",
        r"e:\github\dify-tutorial\課綱\3.基本操作篇 - 打造第一個 AI 對話助手"
    ]
    
    for base_dir in base_dirs:
        srt_files = glob.glob(os.path.join(base_dir, "**", "*.srt"), recursive=True)
        for srt_file in srt_files:
            process_srt(srt_file)

if __name__ == "__main__":
    main()
