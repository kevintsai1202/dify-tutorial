#!/usr/bin/env python3
"""
將每個單元的 README 濃縮成「老師的話」，作為課程概覽
版本 2: 改進提取邏輯，生成更簡潔的概覽
"""

import json
import os
import re

def clean_text(text):
    """清理文本，移除多餘空白"""
    return ' '.join(text.split())

def extract_first_paragraph(content):
    """提取第一個實質段落作為概述"""
    # 跳過標題、圖片、預估時長等
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        # 找到實質內容段落（非標題、非特殊標記）
        if line and not line.startswith('#') and not line.startswith('!') and not line.startswith('>') and len(line) > 20:
            # 取這段內容
            if '**' in line or '：' in line or '。' in line:
                return clean_text(line.replace('**', '').replace('*', ''))
    return None

def generate_simple_note(unit_title, readme_path):
    """生成簡短的老師的話（2-3句話）"""
    try:
        if not os.path.exists(readme_path):
            return "課程內容準備中..."
            
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 嘗試從「為什麼」或「什麼是」開篇的段落提取
        why_match = re.search(r'###\s+\d+\.\s+為什麼.+?\n(.+?)(?=\n\n|\n###|\Z)', content, re.DOTALL)
        what_match = re.search(r'###\s+\d+\.\s+什麼是.+?\n(.+?)(?=\n\n|\n###|\Z)', content, re.DOTALL)
        
        intro_text = None
        if why_match:
            intro_text = why_match.group(1)
        elif what_match:
            intro_text = what_match.group(1)
        
        if intro_text:
            # 清理格式，取前1-2句
            sentences = re.split(r'[。！？]', intro_text)
            sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
            
            if sentences:
                # 移除markdown格式
                result = sentences[0]
                result = re.sub(r'\*\*(.+?)\*\*', r'\1', result)  # 移除粗體
                result = re.sub(r'\*(.+?)\*', r'\1', result)      # 移除斜體
                result = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', result)  # 移除連結
                result = result.replace('  ', ' ').strip()
                
                if len(result) > 80:
                    result = result[:80] + '...'
                
                return result + '。'
        
        # 如果找不到特定段落，用學習目標來生成
        objectives_match = re.search(r'## 學習目標\n\n完成本單元後，您將能夠：\n(?:- (.+)\n)', content)
        if objectives_match:
            first_obj = objectives_match.group(1)
            return f"本單元將幫助您{first_obj}。"
        
        # 最後的fallback
        return f"深入學習 {unit_title} 的核心概念與實作技巧。"
    
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return "課程內容準備中..."

def main():
    # 讀取 courses.json
    with open('courses.json', 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    # 生成 Markdown
    with open('COURSE_OVERVIEW.md', 'w', encoding='utf-8') as f:
        f.write("# Dify 課程概覽 - 老師的話\n\n")
        f.write("> 每個單元的核心概念簡介，幫助您快速了解課程重點\n\n")
        
        for chapter in courses['chapters']:
            f.write(f"## {chapter['title']}\n")
            if chapter.get('subtitle'):
                f.write(f"*{chapter['subtitle']}*\n")
            f.write(f"\n")
            
            for unit in chapter['units']:
                content_path = unit['contentPath'].replace('/', os.sep)
                teacher_note = generate_simple_note(unit['title'], content_path)
                
                f.write(f"### {unit['title']}\n\n")
                f.write(f"{teacher_note}\n\n")
                
                print(f"✓ {chapter['title']} / {unit['title']}")
    
    print("\n✅ 課程概覽已生成: COURSE_OVERVIEW.md")

if __name__ == "__main__":
    main()
