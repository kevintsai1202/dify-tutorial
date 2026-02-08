
import re

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
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements_list = [
        ("Entropic", "Anthropic"),
        ("Libre", "Zeabur"),
        ("Aging", "Agent"),
        ("Github", "GitHub"),
        ("ESA社區", "Exa Search"),
        ("ESA社群", "Exa Search"),
        ("ESA Search", "Exa Search"), 
        ("ESA", "Exa"), 
        ("FireClaw", "Firecrawl"),
        ("FireCore", "Firecrawl"),
        ("FireCORE", "Firecrawl"),
        ("FireCrawl", "Firecrawl"),
        ("ChairGPT", "ChatGPT"),
        ("Gemline", "Gemini"),
        ("Gemini", "Gemini"),
        ("每一緊張升高", "美伊緊張升高"),
        ("一分訂好", "一旦定好"),
        ("s我們", "我們"),
        ("DG 觀光", "Dify 官方"),
        ("DG", "Dify"),
        ("觀光", "官方"), 
        ("WebScraper", "Web Scraper"),
        ("Function calling", "Function Calling"),
        ("接取", "擷取"),
        ("Dhub", "GitHub"),
        ("Dg", "Dify"),
        ("Workflow", "Workflow"), 
        ("WorkFlow", "Workflow"),
        ("ChatFlow", "Chatflow"),
        ("ChaFlow", "Chatflow"),
        ("WORKFLOW", "Workflow"),
        ("Agent", "Agent"),
        ("Start", "Start"),
        ("End", "End"),
        ("LLM", "LLM"),
        ("Knowledge Retrieval", "Knowledge Retrieval"),
        ("Answer", "Answer"),
        ("Question Classifier", "Question Classifier"),
        ("If/Else", "If/Else"),
        ("Code", "Code"),
        ("Template", "Template"),
        ("Variable Aggregator", "Variable Aggregator"),
        ("Iteration", "Iteration"),
        ("Parameter Extractor", "Parameter Extractor"),
        ("HTTP Request", "HTTP Request"),
        ("Tool", "Tool"),
        # New additions for 2-1
        ("Docker Desktop", "Docker Desktop"),
        ("Docker", "Docker"),
        ("GUI", "GUI"),
        ("Mac", "Mac"),
        ("Windows", "Windows"),
        ("Microsoft Store", "Microsoft Store"),
        ("ON", "ARM"), 
        ("WSL", "WSL"),
        ("WSL2", "WSL 2"),
        ("Hyper-V", "Hyper-V"),
        ("Linux", "Linux"),
        ("Defy", "Dify"), 
        ("container", "Container"),
        ("cmd", "cmd"),
        ("Command Mode", "Command Prompt"), 
        ("accept", "Accept"),
        ("Google", "Google"),
        # New Additions for 2-2
        ("Git", "Git"),
        ("Clone", "Clone"),
        ("URL", "URL"),
        ("Env", "env"),
        ("example", "example"),
        ("Docker compose", "Docker Compose"),
        ("Docker Compose", "Docker Compose"),
        ("YML", "YAML"),
        ("Yaml", "YAML"),
        ("yaml", "YAML"),
        ("Up", "Up"),
        ("Down", "Down"),
        ("Stop", "Stop"),
        ("Restart", "Restart"),
        ("Logs", "Logs"),
        ("Localhost", "localhost"),
        ("Admin", "Admin"),
        ("Password", "Password"),
        ("Email", "Email"),
        ("Login", "Login"),
        ("Setup", "Setup"),
        ("Install", "Install"),
        # Additions for 1-4
        ("OpenAI", "OpenAI"),
        ("API Key", "API Key"),
        ("Anthropic", "Anthropic"),
        ("Azure", "Azure"),
        ("Bedrock", "Bedrock"),
        ("Hugging Face", "Hugging Face"),
        ("Replicate", "Replicate"), 
        ("Groq", "Groq"),
        ("Cohere", "Cohere"),
        ("Mistral", "Mistral"),
        ("Ollama", "Ollama"),
        ("Xinference", "Xinference"),
        ("OpenLLM", "OpenLLM"),
        ("LocalAI", "LocalAI"),
        ("Text Embedding", "Text Embedding"),
        ("Moderation", "Moderation"),
        ("Speech to Text", "Speech to Text"),
        ("Text to Speech", "Text to Speech"),
        ("Vision", "Vision"),
        ("Dall-E", "DALL-E"),
        ("Stable Diffusion", "Stable Diffusion"),
        ("Midjourney", "Midjourney"),
        ("System Model", "System Model"),
        ("Custom Model", "Custom Model"),
        # Additions for 1-5 (Dify App Types)
        ("Chatbot", "Chatbot"),
        ("Text Generator", "Text Generator"),
        ("Agent", "Agent"),
        ("Workflow", "Workflow"),
        ("Prompt", "Prompt"),
        ("Rule-based", "Rule-based"),
        ("Conversation", "Conversation"),
        ("Context", "Context"),
        ("Memory", "Memory"),
        ("RAG", "RAG"),
        ("Variables", "Variables"),
        ("Form", "Form"),
        ("Table", "Table"),
        ("Code Interpreter", "Code Interpreter"),
        ("Text Generation", "Text Generation"),
        ("App", "App"),
        ("Assistant", "Assistant"),
        # Additions for 1-6
        ("Prompt 1:1", "Prompt 1:1"),
        ("Prefix", "Prefix"),
        ("Prompt", "Prompt"),
        ("History", "History"),
        ("Role", "Role"),
        ("Completion", "Completion"),
        ("Icon", "Icon"),
        ("Description", "Description"),
        ("Opener", "Opener"),
        ("Opening Statement", "Opening Statement"),
        ("Instruction", "Instruction"),
        ("Pre-prompt", "Pre-prompt"),
        ("Variable", "Variable"),
        ("Add Feature", "Add Feature"),
        ("Next Step Questions", "Next Step Questions"),
    ]
    
    # Remove dangerous replacements for Ch1 where model names are real
    replacements_list = [r for r in replacements_list if r[0] not in ["Replicate"]]
    
    replacements_list.sort(key=lambda x: len(x[0]), reverse=True)
    
    # Pre-correction for specific tricky ones
    content = content.replace("ON的版本", "ARM 的版本") 
    
    for old, new in replacements_list:
        content = content.replace(old, new)
        
    lines = content.splitlines()
    new_lines_content = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        is_index = line.isdigit()
        def is_timecode_next():
             if i + 1 < len(lines):
                 return '-->' in lines[i+1]
             return False

        if is_index and is_timecode_next():
            new_lines_content.append(line)
            i += 1
            if i < len(lines):
                new_lines_content.append(lines[i].strip())
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
    return final_content

import os
file_path = r"e:\github\dify-tutorial\課綱\1.入門篇 - Dify 基礎入門\單元 6 - 聊天助手與文字生成應用說明\1-6.srt"
processed = process_srt(file_path)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(processed)
