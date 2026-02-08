
import os
import glob
import re

def get_sc_to_tc_map():
    # Comprehensive SC->TC mapping
    return {
        "图片": "圖片", "向量化": "向量化", "注册": "註冊", "链接": "連結", "网页": "網頁",
        "申请": "申請", "额度": "額度", "费用": "費用", "便宜": "便宜", "千万": "千萬",
        "亿": "億", "资料": "資料", "除非": "除非", "大量": "大量", "设定": "設定",
        "建立": "建立", "复制": "複製", "配置": "配置", "显示": "顯示", "列表": "列表",
        "预设": "預設", "流浪客": "Rerank", "REG": "RAG", "Relank": "Rerank", "Relunk": "Rerank",
        "Text Embedding": "Text Embedding", "Vision": "Vision", "Voyage": "Voyage", "Jina": "Jina",
        "OpenAI": "OpenAI", "API Key": "API Key", "MIS": "一致", "Docker": "Docker",
        "插线": "插件", "插線": "插件", "Ji等A": "Jina", "这": "這", "么": "麼", "见": "見",
        "间": "間", "还": "還", "进": "進", "个": "個", "们": "們", "来": "來", "说": "說",
        "书": "書", "对应": "對應", "对": "對", "为": "為", "与": "與", "关": "關", "系": "係",
        "别": "別", "处": "處", "实": "實", "应": "應", "开": "開", "当": "當", "从": "從",
        "后": "後", "得": "得", "微": "微", "心": "心", "志": "誌", "忙": "忙", "态": "態",
        "总": "總", "愛": "愛", "感": "感", "我": "我", "才": "才", "找": "找", "把": "把",
        "提": "提", "改": "改", "教": "教", "数": "數", "文": "文", "新": "新", "方": "方",
        "施": "施", "明": "明", "时": "時", "更": "更", "最": "最", "有": "有", "期": "期",
        "机": "機", "次": "次", "比": "比", "气": "氣", "水": "水", "活": "活", "流": "流",
        "测": "測", "满": "滿", "湾": "灣", "演": "演", "无": "無", "然": "然", "照": "照",
        "片": "片", "版": "版", "物": "物", "特": "特", "产": "產", "用": "用", "由": "由",
        "电": "電", "的": "的", "目": "目", "直": "直", "真": "真", "知": "知", "确": "確",
        "示": "示", "社": "社", "种": "種", "科": "科", "程": "程", "空": "空", "立": "立",
        "第": "第", "等": "等", "简": "簡", "算": "算", "管": "管", "类": "類", "精": "精",
        "系": "系", "约": "約", "级": "級", "红": "紅", "纪": "紀", "纳": "納", "纹": "紋",
        "统": "統", "维": "維", "网": "網", "置": "置", "美": "美", "考": "考", "者": "者",
        "而": "而", "能": "能", "自": "自", "色": "色", "花": "花", "苦": "苦", "英": "英",
        "华": "華", "万": "萬", "落": "落", "叶": "葉", "著": "著", "号": "號", "虽": "雖",
        "行": "行", "表": "表", "见": "見", "视": "視", "言": "言", "计": "計", "认": "認",
        "让": "讓", "讯": "訊", "记": "記", "讲": "講", "变": "變", "象": "象", "货": "貨",
        "费": "費", "资": "資", "路": "路", "身": "身", "车": "車", "转": "轉", "辑": "輯",
        "办": "辦", "边": "邊", "过": "過", "运": "運", "进": "進", "近": "近", "连": "連",
        "选": "選", "还": "還", "那": "那", "部": "部", "配": "配", "里": "裡", "量": "量",
        "金": "金", "钱": "錢", "开": "開", "间": "間", "阁": "閣", "阅": "閱", "阳": "陽",
        "际": "際", "陆": "陸", "队": "隊", "阶": "階", "隋": "隨", "集": "集", "难": "難",
        "需": "需", "面": "面", "音": "音", "页": "頁", "顶": "頂", "项": "項", "预": "預",
        "领": "領", "头": "頭", "颜": "顏", "类": "類", "风": "風", "飘": "飄", "飞": "飛",
        "饥": "飢", "马": "馬", "验": "驗", "体": "體", "高": "高", "发": "發", "麻": "麻",
        "黄": "黃", "点": "點", "么": "麼", "虽然": "雖然", "已经": "已經", "进来": "進來",
        "之后": "之後", "说明": "說明", "怎么": "怎麼", "使用": "使用", "安装": "安裝", "插线": "插線",
        "这边": "這邊", "一样": "一樣", "找到": "找到", "搜寻": "搜尋", "列出来": "列出來", "这个": "這個",
        "设定": "設定", "刚才": "剛才", "这里": "這裡", "供应商": "供應商", "稍微": "稍微", "新增": "新增",
        "连结": "連結", "就会": "就會", "注册": "註冊", "其实": "其實", "基本上": "基本上", "容易": "容易",
        "只要": "只要", "另外": "另外", "申请": "申請", "底下": "底下", "自己": "自己", "提供": "提供",
        "非常": "非常", "大方": "大方", "之内": "之內", "尽量": "盡量", "练习": "練習", "便宜": "便宜",
        "实际上": "實際上", "千万": "千萬", "用不完": "用不完", "直接": "直接", "呈现": "呈現", "建立": "建立",
        "看不到": "看不到", "复制": "複製", "变成": "變成", "绿灯": "綠燈", "表示": "表示", "下面": "下面",
        "很多": "很多", "使用": "使用", "标示": "標示", "一般": "一般", "这样子": "這樣", "写": "寫",
        "最新": "最新", "后面": "後面", "加个": "加個", "针对": "針對", "讲一下": "講一下", "搭配": "搭配",
        "向量": "向量", "流程": "流程", "列表": "列表", "上次": "上次", "没加": "沒加", "加上来": "加上來",
        "预设": "預設", "最高": "最高", "版本": "版本", "加上去": "加上去", "透过": "透過", "资料库": "資料庫",
        "上传": "上傳", "上去": "上去", "档案": "檔案", "特别": "特別", "注意": "注意", "处理": "處理",
        "一开始": "一開始", "文件": "文件", "动作": "動作", "查询": "查詢", "一定": "一定", "同一个": "同一個",
        "同样": "同樣", "一组": "一組", "讨厌": "討厭", "地方": "地方", "未来": "未來", "做法": "做法",
        "提出": "提出", "类似": "類似", "一系列": "一系列", "共用": "共用", "空间": "空間", "其他家": "其他家",
        "设计": "設計", "内": "內", "录": "錄", "号": "號", "软": "軟", "体": "體", "区": "區",
        "学": "學", "习": "習", "请": "請", "问": "問", "题": "題", "答": "答", "术": "術",
        "强": "強", "够": "夠", "写": "寫", "谢": "謝", "帮": "幫", "助": "助", "块": "塊"
    }

def process_files(base_dir):
    srt_files = glob.glob(os.path.join(base_dir, "**", "*.srt"), recursive=True)
    replacements = get_sc_to_tc_map()
    
    multi_line_report = []
    
    for file_path in srt_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Convert SC to TC
        for sc, tc in replacements.items():
            content = content.replace(sc, tc)
            
        # Parse for multi-line detection
        lines = content.splitlines()
        new_content = []
        i = 0
        file_multi_lines = []
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Check for ID
            is_index = line.isdigit()
            is_valid_block = False
            if is_index:
                if i + 1 < len(lines) and '-->' in lines[i+1]:
                    is_valid_block = True
            
            if is_valid_block:
                # Append ID and Timestamp
                new_content.append(line)
                i += 1 # Move to timestamp
                new_content.append(lines[i])
                i += 1 # Move to text
                
                # Collect text lines
                text_lines = []
                while i < len(lines):
                    text_line = lines[i].strip()
                    if not text_line:
                        break # End of block
                    
                    # Check if next block starts (in case of missing empty line)
                    if text_line.isdigit() and (i+1 < len(lines)) and ('-->' in lines[i+1]):
                        break 
                    
                    text_lines.append(text_line)
                    i += 1
                
                # Check line count
                if len(text_lines) > 1:
                    file_multi_lines.append({
                        "id": line,
                        "text": text_lines
                    })
                
                # Append text lines to new content
                new_content.extend(text_lines)
                
                # Add empty line separator
                new_content.append("")
                
                # If we broke due to next block, don't increment i, loop will handle
                if i < len(lines) and not lines[i].strip():
                    i += 1 # valid empty line
            else:
                # Just append miscellaneous lines (though SRT structure should be strict)
                if line:
                    new_content.append(line)
                else:
                    new_content.append("")
                i += 1

        # Write converted content back to file
        final_content = "\n".join(new_content)
        # remove multiple consecutive newlines potentially created
        final_content = re.sub(r'\n{3,}', '\n\n', final_content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        if file_multi_lines:
            multi_line_report.append({
                "file": file_path,
                "issues": file_multi_lines
            })
            
    return multi_line_report

def main():
    base_dir = r"e:\github\dify-tutorial\課綱"
    report = process_files(base_dir)
    
    report_file = r"C:\Users\kevintsai\.gemini\antigravity\brain\71684e64-8e8e-40d8-b979-e3102b9d77f8\multi_line_report.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Multi-line Subtitle Report\n\n")
        if not report:
            f.write("No multi-line subtitles found.\n")
        else:
            for item in report:
                f.write(f"## File: {item['file']}\n")
                for issue in item['issues']:
                    f.write(f"- **ID {issue['id']}**:\n")
                    for line in issue['text']:
                        f.write(f"  > {line}\n")
                    f.write("\n")

if __name__ == "__main__":
    main()
