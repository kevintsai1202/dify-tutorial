# Dify 完全教學 - 從入門到精通

<p align="center">
  <img src="https://img.shields.io/badge/Dify-Tutorial-blue?style=for-the-badge" alt="Dify Tutorial">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
</p>

<p align="center">
  一個精美的互動式教學網站，帶您深入了解 Dify AI 應用開發平台
</p>

---

## ✨ 功能特色

### 🎨 精美的視覺設計
- 深色/淺色主題切換
- 漸層背景與卡片式設計
- 流暢的動畫效果與過渡

### 📱 互動式側邊欄導航
- 固定側邊欄，方便快速跳轉
- 即時顯示學習進度（百分比）
- 自動高亮當前閱讀的章節
- 顯示每個章節的預計時長

### ⏱️ 學習計時器
- 精確的學習時間追蹤
- 今日學習時間統計
- 總學習時間累計
- 資料持久化儲存

### 💻 程式碼高亮與複製
- 使用 Prism.js 進行語法高亮
- 一鍵複製程式碼功能
- 支援多種程式語言
- 複製成功有視覺回饋

### 📊 學習進度追蹤
- 每個章節都有「標記為已完成」按鈕
- 進度自動儲存到 localStorage
- 刷新頁面後進度不會遺失
- 視覺化進度條顯示

### 📱 響應式設計
- 支援桌面與行動裝置
- 自動調整佈局

---

## 📚 課程內容

### 第一章：環境準備篇
- 本地安裝 Docker
- 安裝社群版 Dify
- 透過 Zeabur 安裝社群版 Dify

### 第二章：入門篇 - Dify 基礎入門
- 課程介紹
- Dify 雲端版本與社群版本差異
- 介面說明
- AI 模型設定說明
- 五種應用的適用場景介紹
- 聊天助手與文字生成應用說明

### 第三章：基本操作篇 - 打造第一個 AI 對話助手
- Prompt 工程基礎
- 對話參數調整
- 發布與分享應用
- 插件系統介紹
- 常用工具說明
- Agent 說明
- 工作流說明
- 工作流節點介紹
- 手動驅動工作流 vs 事件驅動工作流
- 聊天流說明

### 第四章：應用篇 - 實戰應用開發
- RAG 知識庫概念
- 文件上傳與分塊設定
- 檢索策略設定
- Embedding 模型說明
- Rerank 模型說明
- Dify 中 RAG 的兩種類型
- 提升 RAG 準確率的小技巧

### 第五章：進階應用篇 - 進階技巧與深度應用
- Workflow 畫布操作
- 條件分支與邏輯控制
- API 整合與外部呼叫
- 代碼節點進階應用
- 模板轉換節點進階應用
- 迭代節點進階應用
- 循環節點與迭代節點的差異
- 網路爬蟲工具應用
- 擴展插件應用

### 第六章：進階開發篇 - 插件與 MCP 應用（進階選修）
- 插件市場探索
- MCP 協議介紹
- 自訂工具開發
- 插件開發環境建置
- 修改現有插件
- 將現有流程轉為 MCP 服務
- AI 應用整合

---

## 🚀 快速開始

### 線上訪問
直接訪問 GitHub Pages 網站：[立即開始學習](https://kevintsai1202.github.io/dify-tutorial/)

### 本地運行

1. 克隆此倉庫：
```bash
git clone https://github.com/kevintsai1202/dify-tutorial.git
cd dify-tutorial
```

2. 使用任意本地伺服器開啟（因為需要載入 JSON 和 Markdown 檔案）：
```bash
# 使用 Python
python -m http.server 8080

# 或使用 Node.js
npx http-server -p 8080

# 或使用 VS Code Live Server 擴充功能
```

3. 在瀏覽器開啟 `http://localhost:8080`

---

## 🛠️ 技術棧

| 技術 | 用途 |
|------|------|
| HTML5 | 網頁結構 |
| CSS3 | 樣式設計（Grid、Flexbox、動畫） |
| Vanilla JavaScript (ES6+) | 互動邏輯 |
| [Prism.js](https://prismjs.com/) | 程式碼語法高亮 |
| [marked.js](https://marked.js.org/) | Markdown 解析 |
| [Font Awesome 6](https://fontawesome.com/) | 圖標系統 |

---

## 📁 檔案結構

```
dify-tutorial/
├── index.html          # 主頁面
├── style.css           # 主樣式表
├── app.js              # 主程式
├── courses.json        # 課程結構資料
├── spec.md             # 詳細技術規格文件
├── README.md           # 專案說明文件
├── 課綱/               # 課程內容 Markdown 檔案
│   ├── 1.環境準備篇/
│   ├── 2.入門篇/
│   ├── 3.基本操作篇/
│   ├── 4.應用篇/
│   ├── 5.進階應用篇/
│   └── 6.進階開發篇/
└── assets/             # 靜態資源
    └── images/
```

---

## 🎯 學習目標

完成本課程後，您將能夠：

1. ✅ 安裝並設定 Dify 開發環境
2. ✅ 熟悉 Dify 介面與各種應用類型
3. ✅ 使用 Prompt 工程打造對話助手
4. ✅ 建立並優化 RAG 知識庫應用
5. ✅ 設計複雜的 Workflow 自動化流程
6. ✅ 整合外部 API 與擴展插件
7. ✅ 開發自訂工具與 MCP 服務

---

## 📖 相關資源

- [Dify 官方網站](https://dify.ai)
- [Dify 官方文件](https://docs.dify.ai)
- [Dify GitHub](https://github.com/langgenius/dify)
- [Dify 社群](https://discord.gg/dify)

---

## 🤝 貢獻

歡迎提交 Issue 或 Pull Request 來改進這個教學網站！

1. Fork 這個專案
2. 建立您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

---

## 📄 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 檔案

---

## 👨‍💻 作者

由 AI 驅動開發，展示現代 AI 工具的強大能力

**開始您的 AI 應用開發之旅！** 🚀

---

<p align="center">
  <a href="https://www.youtube.com/@pg-kt?sub_confirmation=1">
    <img src="https://img.shields.io/badge/YouTube-訂閱頻道-red?style=for-the-badge&logo=youtube" alt="YouTube">
  </a>
  <a href="https://www.facebook.com/profile.php?id=61564137718583">
    <img src="https://img.shields.io/badge/Facebook-粉絲專頁-blue?style=for-the-badge&logo=facebook" alt="Facebook">
  </a>
  <a href="https://www.threads.com/@cai.chengkai">
    <img src="https://img.shields.io/badge/Threads-追蹤我-black?style=for-the-badge&logo=threads" alt="Threads">
  </a>
</p>
