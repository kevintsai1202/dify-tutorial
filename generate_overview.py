#!/usr/bin/env python3
"""
生成詳細的課程概覽 - 每個單元至少100字
包含：學習內容、關鍵難點、學習成果
"""

import json
import os
import re

def extract_learning_objectives(content):
    """提取完整的學習目標列表"""
    match = re.search(r'## 學習目標\n\n完成本單元後，您將能夠：\n((?:- .+\n)+)', content)
    if match:
        objectives_text = match.group(1)
        objectives = []
        for line in objectives_text.split('\n'):
            if line.strip().startswith('- '):
                obj = line.strip()[2:].strip()
                objectives.append(obj)
        return objectives
    return []

def extract_content_outline(content):
    """提取內容大綱的主要章節"""
    # 找所有 ### 開頭的小節
    sections = []
    for match in re.finditer(r'###\s+\d+\.\s+(.+)', content):
        sections.append(match.group(1).strip())
    return sections

def extract_key_points(content):
    """提取關鍵要點或注意事項"""
    key_points = []
    
    # 查找「為什麼」段落 - 這通常說明重要性
    why_match = re.search(r'###\s+\d+\.\s+為什麼.+?\n(.+?)(?=\n###|\n##|\Z)', content, re.DOTALL)
    if why_match:
        why_text = why_match.group(1)
        # 提取列表項
        for line in why_text.split('\n'):
            if re.match(r'\s*[\d\-\*]+\.?\s+\*\*(.+?)\*\*', line):
                point = re.search(r'\*\*(.+?)\*\*', line)
                if point:
                    key_points.append(point.group(1))
    
    # 查找「注意事項」或「設定注意事項」
    note_match = re.search(r'###\s+\d+\.\s+.*注意事項.*\n(.+?)(?=\n###|\n##|\Z)', content, re.DOTALL)
    if note_match:
        note_text = note_match.group(1)
        for line in note_text.split('\n'):
            if line.strip().startswith('- '):
                key_points.append(line.strip()[2:].strip())
    
    return key_points[:3]  # 最多取3個關鍵點

def generate_detailed_overview(unit_title, readme_path, duration):
    """生成詳細的單元概覽（至少100字）"""
    
    if not os.path.exists(readme_path):
        # 為準備中的課程生成更詳細的描述
        return (f"📚 **課程簡介**：本單元預計 {duration} 分鐘，將深入探討「{unit_title}」的核心概念與實務應用。\n\n"
                f"🎯 **學習內容**：課程將涵蓋{unit_title}的基本原理、實作技巧以及最佳實踐。透過循序漸進的講解，"
                f"您將了解如何在 Dify 平台上有效運用{unit_title}相關功能，並學習業界常用的開發模式與技巧。\n\n"
                f"✅ **學習成果**：完成本單元後，您將能夠獨立完成{unit_title}的相關操作，並能夠將所學知識應用於實際專案開發中。"
                f"這將為您後續的進階學習奠定堅實的基礎。")
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        objectives = extract_learning_objectives(content)
        sections = extract_content_outline(content)
        key_points = extract_key_points(content)
        
        # 如果沒有標準的學習目標，嘗試提取第一段實質內容
        if not objectives:
            # 跳過標題、圖片等，找到第一段實質描述
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                # 找到長度合理且不是標記語法的段落
                if (len(line) > 30 and 
                    not line.startswith('#') and 
                    not line.startswith('!') and 
                    not line.startswith('>') and
                    not line.startswith('|') and
                    not line.startswith('---')):
                    # 將這段作為描述
                    objectives = [line[:100] if len(line) > 100 else line]
                    break
        
        # 構建詳細說明
        overview_parts = []
        
        # 第一段：課程簡介與時長
        intro = f"📚 **課程簡介**：本單元預計 {duration} 分鐘，"
        
        if objectives:
            if len(objectives) == 1:
                intro += f"將幫助您{objectives[0]}。"
            elif len(objectives) == 2:
                intro += f"將幫助您{objectives[0]}，以及{objectives[1]}。"
            else:
                intro += f"將幫助您{objectives[0]}、{objectives[1]}等核心技能。"
        else:
            intro += f"將深入講解{unit_title}的理論與實作。"
        
        overview_parts.append(intro)
        
        # 第二段：學習內容
        if sections:
            content_desc = f"\n\n🎯 **學習內容**："
            if len(sections) <= 2:
                content_desc += '、'.join(sections) + "。"
            elif len(sections) == 3:
                content_desc += f"從「{sections[0]}」開始，接著探討「{sections[1]}」，最後深入「{sections[2]}」。"
            else:
                content_desc += f"課程涵蓋{len(sections)}個主題，包括{sections[0]}、{sections[1]}等重要觀念，並透過{sections[-1]}進行整合應用。"
            overview_parts.append(content_desc)
        else:
            # 如果沒有明確的章節，補充通用描述
            overview_parts.append(f"\n\n🎯 **學習內容**：本單元將透過理論講解與實務演練相結合的方式，幫助您全面理解{unit_title}的核心概念與應用場景。")
        
        # 第三段：關鍵難點或重點
        if key_points:
            difficulty_desc = f"\n\n⚠️ **學習重點**："
            if len(key_points) == 1:
                difficulty_desc += f"特別注意{key_points[0]}的部分。"
            else:
                difficulty_desc += f"課程中會特別強調" + '、'.join(key_points[:2])
                if len(key_points) > 2:
                    difficulty_desc += f"等關鍵概念"
                difficulty_desc += "，這些是實務應用的核心。"
            overview_parts.append(difficulty_desc)
        
        # 第四段：學習成果
        if objectives:
            outcome_desc = f"\n\n✅ **學習成果**：完成本單元後，"
            if len(objectives) >= 2:
                outcome_desc += f"您將具備{objectives[-1]}的能力，"
            outcome_desc += f"能夠在實際專案中應用所學，解決{unit_title}相關的實務問題。"
            overview_parts.append(outcome_desc)
        else:
            # 通用的學習成果描述
            overview_parts.append(f"\n\n✅ **學習成果**：完成本單元後，您將能夠獨立運用{unit_title}的相關技巧，並具備解決實際問題的能力。")
        
        full_overview = ''.join(overview_parts)
        
        # 確保至少100字（中文字符）
        if len(full_overview) < 100:
            # 補充通用結尾
            full_overview += f"透過循序漸進的講解與實作練習，您將能夠完全掌握{unit_title}的精髓，為後續的進階課程打下堅實基礎。"
        
        return full_overview
        
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return f"本單元將探討{unit_title}的核心概念與實作技巧。課程內容豐富，包含理論講解、實務演練及案例分析，幫助您循序漸進地掌握這個主題，並能夠在實際工作中靈活運用。"

def main():
    # 讀取 courses.json
    with open('courses.json', 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    print("開始生成詳細課程概覽...\n")
    
    # 生成 Markdown
    with open('COURSE_OVERVIEW.md', 'w', encoding='utf-8') as f:
        f.write("# Dify 課程概覽 - 詳細說明\n\n")
        f.write("> 每個單元的詳細學習指南，包含學習內容、關鍵難點與學習成果\n\n")
        f.write("---\n\n")
        
        chapter_num = 0
        for chapter in courses['chapters']:
            chapter_num += 1
            
            f.write(f"## 第 {chapter_num} 章：{chapter['title']}\n\n")
            if chapter.get('subtitle'):
                f.write(f"**{chapter['subtitle']}**\n\n")
            
            f.write(f"📊 本章共 {len(chapter['units'])} 個單元，預計學習時間 {chapter['duration']} 分鐘\n\n")
            f.write("---\n\n")
            
            unit_num = 0
            for unit in chapter['units']:
                unit_num += 1
                content_path = unit['contentPath'].replace('/', os.sep)
                overview = generate_detailed_overview(
                    unit['title'], 
                    content_path,
                    unit['duration']
                )
                
                f.write(f"### {chapter_num}.{unit_num} {unit['title']}\n\n")
                f.write(f"{overview}\n\n")
                f.write("---\n\n")
                
                # 顯示進度和字數
                char_count = len(overview)
                status = "✅" if char_count >= 100 else "⚠️"
                print(f"{status} 第{chapter_num}章 單元{unit_num}: {unit['title']} ({char_count}字)")
        
        f.write("\n---\n\n")
        f.write("*本課程概覽由系統自動生成，如有疑問請參考各單元詳細內容*\n")
    
    print("\n✅ 詳細課程概覽已生成: COURSE_OVERVIEW.md")
    print("\n📊 統計資訊：")
    print(f"   - 總章節數: {len(courses['chapters'])}")
    total_units = sum(len(ch['units']) for ch in courses['chapters'])
    print(f"   - 總單元數: {total_units}")
    print(f"   - 總時長: {courses['estimatedTotalTime']} 分鐘")

if __name__ == "__main__":
    main()
