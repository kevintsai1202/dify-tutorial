
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
    # Base replacements for ALL files (Inherited from process_global_srt.py)
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

    replacements.extend([
        ("相量", "向量"),
        ("像樣化", "向量化"), 
        ("大圓模型", "大語言模型"),
        ("大元模型", "大語言模型"),
        ("代言模型", "大語言模型"),
        ("待言模型", "大語言模型"),
        ("Find Tuning", "Fine-tuning"),
        ("Find Turing", "Fine-tuning"),
        ("Turing", "tuning"),
        ("EMBEDDING", "Embedding"),
        ("Embedding", "Embedding"), 
        ("Embedded", "Embedding"),
        ("Inventing", "Embedding"),
        ("Inventive", "Embedding"),
        ("eBedit", "Embedding"),
        ("RERANK", "Rerank"),
        ("Rerank", "Rerank"),
        ("Relunk", "Rerank"),
        ("LiRank", "Rerank"),
        ("Relant", "Rerank"),
        ("Reorg", "Rerank"),
        ("理論", "Rerank"), # Context: 用理論 -> 用 Rerank
        ("DV", "Dify"),
        ("DB", "Dify"), # Check context usually safe here
        ("D級", "Dify"),
        ("QMA", "Q&A"),
        ("Jina", "Jina"),
        ("Cinah", "Jina"),
        ("GNAR", "Jina"),
        ("Cohere", "Cohere"),
        ("Voyage", "Voyage"),
        ("Vision", "Vision"),
        ("精酷", "精確"),
        ("柔程", "流程"),
        ("物打機", "問答集"),
        ("100小", "100條"),
        ("上單", "帳單"),
        ("才前面", "排前面"),
        # Contextual fixes for "文" -> "我們"
        ("雖然文", "雖然我們"),
        ("所以文", "所以我們"),
        ("就是文", "就是我們"),
        ("因為文", "因為我們"),
        ("文就是", "我們就是"),
    ])
    
    # Sort by length
    replacements.sort(key=lambda x: len(x[0]), reverse=True)
    return replacements

def process_srt(file_path):
    print(f"Processing: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = get_replacements(file_path)
    
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
    # Define Chapter 4 directory
    base_dir = r"e:\github\dify-tutorial\課綱\4.應用篇 - 實戰應用開發"
    
    srt_files = glob.glob(os.path.join(base_dir, "**", "*.srt"), recursive=True)
    if not srt_files:
        print(f"No SRT files found in {base_dir}")
        return

    for srt_file in srt_files:
        process_srt(srt_file)

if __name__ == "__main__":
    main()
