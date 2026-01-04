# Dify 互動式教學網站 - 規格文件

## 1. 架構與選型

### 1.1 專案概述
建立一個精美的互動式教學網站，用於教授 Dify 平台的使用方法。網站設計參考 [gemini-cli-tutorial](https://github.com/kevintsai1202/gemini-cli-tutorial) 的架構，提供深色主題、側邊欄導航、學習計時器、進度追蹤等功能。

### 1.2 技術選型
| 技術 | 說明 |
|------|------|
| HTML5 | 網頁結構，語義化標籤 |
| CSS3 | 樣式設計，使用 Grid、Flexbox、動畫 |
| Vanilla JavaScript (ES6+) | 互動邏輯，無需框架 |
| Prism.js | 程式碼語法高亮 |
| Font Awesome 6 | 圖標系統 |
| marked.js | Markdown 渲染（用於載入課程內容） |

### 1.3 設計理念
- **深色主題**：專業護眼，適合長時間學習
- **漸層背景**：現代視覺效果
- **卡片式設計**：內容區塊清晰分明
- **響應式佈局**：支援桌面與行動裝置

---

## 2. 資料模型

### 2.1 課程結構資料模型
```javascript
/**
 * 課程章節資料結構
 */
const CourseChapter = {
  id: String,           // 章節唯一識別碼，例如 "chapter-1"
  title: String,        // 章節標題
  duration: Number,     // 預估學習時間（分鐘）
  units: Array<Unit>,   // 單元列表
  isCompleted: Boolean  // 章節完成狀態
};

/**
 * 單元資料結構
 */
const Unit = {
  id: String,           // 單元唯一識別碼，例如 "unit-1-1"
  title: String,        // 單元標題
  duration: Number,     // 預估學習時間（分鐘）
  contentPath: String,  // Markdown 內容路徑
  isCompleted: Boolean  // 單元完成狀態
};

/**
 * 學習進度資料結構（存於 localStorage）
 */
const LearningProgress = {
  completedUnits: Array<String>,  // 已完成的單元 ID 列表
  totalStudyTime: Number,         // 總學習時間（秒）
  todayStudyTime: Number,         // 今日學習時間（秒）
  lastStudyDate: String,          // 最後學習日期 (YYYY-MM-DD)
  currentUnit: String             // 目前閱讀的單元 ID
};
```

### 2.2 課程內容對應
根據 `課綱` 目錄結構，課程分為 6 大章節：

| 章節 | 標題 | 單元數 |
|------|------|--------|
| 1 | 環境準備篇（增加社群版安裝方式） | 3 |
| 2 | 入門篇 - Dify 基礎入門 | 6 |
| 3 | 基本操作篇 - 打造第一個 AI 對話助手 | 10 |
| 4 | 應用篇 - 實戰應用開發 | 8 |
| 5 | 進階應用篇 - 進階技巧與深度應用 | 11 |
| 6 | 進階開發篇 - 插件與 MCP 應用（進階選修） | 9 |

---

## 3. 關鍵流程

### 3.1 頁面載入流程
1. 載入 HTML 基礎結構
2. 初始化 CSS 樣式與動畫
3. 載入課程章節資料 (`courses.json`)
4. 從 localStorage 讀取學習進度
5. 渲染側邊欄導航選單
6. 載入預設/上次閱讀的單元內容
7. 啟動學習計時器

### 3.2 單元切換流程
1. 使用者點擊側邊欄單元項目
2. 更新 URL hash（支援書籤）
3. 載入對應的 Markdown 內容
4. 使用 marked.js 渲染 HTML
5. 使用 Prism.js 高亮程式碼
6. 捲動至頁面頂部
7. 更新目前單元狀態

### 3.3 進度追蹤流程
1. 使用者點擊「標記為已完成」按鈕
2. 更新 localStorage 中的 completedUnits
3. 更新側邊欄對應項目的完成狀態圖示
4. 計算並更新整體進度百分比
5. 更新進度條顯示

---

## 4. 虛擬碼

### 4.1 課程載入
```
FUNCTION loadCourseData():
    data = FETCH("courses.json")
    FOR EACH chapter IN data.chapters:
        createChapterElement(chapter)
        FOR EACH unit IN chapter.units:
            createUnitElement(unit)
    END FOR
    loadProgress()
    navigateToLastUnit()
END FUNCTION
```

### 4.2 Markdown 內容載入
```
FUNCTION loadUnitContent(unitId):
    unit = findUnitById(unitId)
    IF unit IS NULL:
        showError("單元不存在")
        RETURN
    END IF
    
    markdown = FETCH(unit.contentPath)
    html = marked.parse(markdown)
    contentElement.innerHTML = html
    
    Prism.highlightAll()
    updateCurrentUnit(unitId)
    scrollToTop()
END FUNCTION
```

### 4.3 學習計時器
```
CLASS StudyTimer:
    PROPERTY totalSeconds = 0
    PROPERTY todaySeconds = 0
    PROPERTY intervalId = null
    
    METHOD start():
        intervalId = setInterval(() => {
            totalSeconds++
            todaySeconds++
            updateTimerDisplay()
            saveProgress()
        }, 1000)
    END METHOD
    
    METHOD stop():
        clearInterval(intervalId)
    END METHOD
    
    METHOD formatTime(seconds):
        hours = floor(seconds / 3600)
        minutes = floor((seconds % 3600) / 60)
        secs = seconds % 60
        RETURN format("{hours}:{minutes}:{secs}")
    END METHOD
END CLASS
```

---

## 5. 系統脈絡圖 (System Context Diagram)

```mermaid
graph TB
    subgraph "使用者"
        User[學習者]
    end
    
    subgraph "Dify 教學網站"
        Website[互動式教學網站]
    end
    
    subgraph "外部資源"
        CDN[CDN 資源<br/>Prism.js, Font Awesome]
        GitHub[GitHub Pages<br/>靜態網站託管]
    end
    
    User -->|瀏覽課程內容| Website
    User -->|追蹤學習進度| Website
    Website -->|載入外部資源| CDN
    Website -->|部署| GitHub
```

---

## 6. 容器/部署概觀

```mermaid
graph LR
    subgraph "GitHub Repository"
        Source[原始碼]
    end
    
    subgraph "GitHub Pages"
        HTML[index.html]
        CSS[style.css]
        JS[app.js]
        Data[courses.json]
        Content[課程內容 Markdown]
    end
    
    subgraph "CDN"
        Prism[Prism.js]
        FA[Font Awesome]
        Marked[marked.js]
    end
    
    subgraph "Client Browser"
        Browser[瀏覽器]
        LocalStorage[localStorage<br/>學習進度]
    end
    
    Source -->|GitHub Actions| HTML
    Source -->|GitHub Actions| CSS
    Source -->|GitHub Actions| JS
    
    Browser -->|載入| HTML
    Browser -->|載入| CSS
    Browser -->|載入| JS
    Browser -->|載入| Data
    Browser -->|載入| Content
    Browser -->|載入| Prism
    Browser -->|載入| FA
    Browser -->|載入| Marked
    Browser <-->|讀寫| LocalStorage
```

---

## 7. 模組關係圖 (Frontend Module Architecture)

```mermaid
graph TD
    subgraph "HTML"
        Index[index.html]
    end
    
    subgraph "CSS Modules"
        Variables[variables.css<br/>CSS 變數定義]
        Base[base.css<br/>基礎樣式]
        Layout[layout.css<br/>佈局]
        Components[components.css<br/>元件樣式]
        Animations[animations.css<br/>動畫效果]
    end
    
    subgraph "JavaScript Modules"
        App[app.js<br/>主程式進入點]
        Navigation[navigation.js<br/>導航邏輯]
        ContentLoader[content-loader.js<br/>內容載入]
        ProgressTracker[progress-tracker.js<br/>進度追蹤]
        Timer[timer.js<br/>學習計時器]
        Theme[theme.js<br/>主題切換]
    end
    
    subgraph "Data"
        Courses[courses.json<br/>課程資料]
        Markdown[*.md<br/>課程內容]
    end
    
    Index --> Variables
    Index --> Base
    Index --> Layout
    Index --> Components
    Index --> Animations
    
    Index --> App
    App --> Navigation
    App --> ContentLoader
    App --> ProgressTracker
    App --> Timer
    App --> Theme
    
    ContentLoader --> Courses
    ContentLoader --> Markdown
```

---

## 8. 序列圖

### 8.1 頁面載入序列圖

```mermaid
sequenceDiagram
    participant User as 使用者
    participant Browser as 瀏覽器
    participant App as app.js
    participant ContentLoader as 內容載入器
    participant LocalStorage as localStorage
    
    User->>Browser: 開啟網頁
    Browser->>App: DOMContentLoaded
    App->>LocalStorage: 讀取學習進度
    LocalStorage-->>App: 進度資料
    App->>ContentLoader: 載入課程資料
    ContentLoader->>ContentLoader: Fetch courses.json
    ContentLoader-->>App: 課程結構
    App->>App: 渲染側邊欄
    App->>ContentLoader: 載入上次閱讀的單元
    ContentLoader->>ContentLoader: Fetch Markdown
    ContentLoader->>ContentLoader: marked.parse()
    ContentLoader->>ContentLoader: Prism.highlightAll()
    ContentLoader-->>App: 渲染完成
    App->>App: 啟動計時器
    App-->>Browser: 頁面就緒
    Browser-->>User: 顯示內容
```

### 8.2 標記完成序列圖

```mermaid
sequenceDiagram
    participant User as 使用者
    participant UI as 介面
    participant ProgressTracker as 進度追蹤器
    participant LocalStorage as localStorage
    
    User->>UI: 點擊「標記為已完成」
    UI->>ProgressTracker: markUnitComplete(unitId)
    ProgressTracker->>LocalStorage: 更新 completedUnits
    ProgressTracker->>ProgressTracker: 計算進度百分比
    ProgressTracker->>UI: 更新側邊欄圖示
    ProgressTracker->>UI: 更新進度條
    UI-->>User: 顯示完成動畫
```

---

## 9. ER 圖

本專案為純前端靜態網站，無後端資料庫。資料儲存於：
1. **courses.json** - 課程結構資料
2. **localStorage** - 使用者學習進度

```mermaid
erDiagram
    COURSE_DATA ||--o{ CHAPTER : contains
    CHAPTER ||--o{ UNIT : contains
    UNIT ||--o| MARKDOWN_CONTENT : references
    
    LOCAL_STORAGE ||--o{ COMPLETED_UNIT : stores
    LOCAL_STORAGE ||--|| STUDY_TIME : stores
    LOCAL_STORAGE ||--|| CURRENT_UNIT : stores
    
    COURSE_DATA {
        string version
        array chapters
    }
    
    CHAPTER {
        string id PK
        string title
        number duration
        array units
    }
    
    UNIT {
        string id PK
        string title
        number duration
        string contentPath
    }
    
    MARKDOWN_CONTENT {
        string path PK
        string content
    }
    
    LOCAL_STORAGE {
        string key
        object value
    }
    
    COMPLETED_UNIT {
        string unitId FK
    }
    
    STUDY_TIME {
        number totalSeconds
        number todaySeconds
        string lastStudyDate
    }
    
    CURRENT_UNIT {
        string unitId FK
    }
```

---

## 10. 類別圖（前端關鍵類別）

```mermaid
classDiagram
    class App {
        -NavigationController navigation
        -ContentLoader contentLoader
        -ProgressTracker progressTracker
        -StudyTimer timer
        -ThemeManager theme
        +init()
        +loadCourseData()
        +handleNavigation()
    }
    
    class NavigationController {
        -Element sidebar
        -Array~ChapterNode~ chapters
        +renderSidebar(courseData)
        +highlightCurrentUnit(unitId)
        +expandChapter(chapterId)
        +collapseChapter(chapterId)
        +handleHashChange()
    }
    
    class ContentLoader {
        -Element contentArea
        -Object courseData
        +loadCourseJSON()
        +loadUnitContent(unitId)
        +parseMarkdown(md)
        +highlightCode()
        +addCopyButtons()
    }
    
    class ProgressTracker {
        -Array~String~ completedUnits
        -Number progressPercentage
        +loadProgress()
        +saveProgress()
        +markUnitComplete(unitId)
        +markUnitIncomplete(unitId)
        +getProgressPercentage()
        +isUnitCompleted(unitId)
    }
    
    class StudyTimer {
        -Number totalSeconds
        -Number todaySeconds
        -String lastStudyDate
        -Number intervalId
        +start()
        +stop()
        +reset()
        +formatTime(seconds)
        +loadFromStorage()
        +saveToStorage()
        +updateDisplay()
    }
    
    class ThemeManager {
        -String currentTheme
        +init()
        +toggle()
        +setTheme(theme)
        +loadFromStorage()
        +saveToStorage()
    }
    
    App --> NavigationController
    App --> ContentLoader
    App --> ProgressTracker
    App --> StudyTimer
    App --> ThemeManager
```

---

## 11. 流程圖

### 11.1 內容載入流程圖

```mermaid
flowchart TD
    Start([開始]) --> CheckHash{URL 有 hash?}
    CheckHash -->|是| ParseHash[解析 hash 取得 unitId]
    CheckHash -->|否| CheckStorage{localStorage 有紀錄?}
    
    CheckStorage -->|是| LoadLastUnit[載入上次閱讀的單元]
    CheckStorage -->|否| LoadFirstUnit[載入第一個單元]
    
    ParseHash --> ValidateUnit{unitId 有效?}
    ValidateUnit -->|是| LoadUnit[載入指定單元]
    ValidateUnit -->|否| LoadFirstUnit
    
    LoadLastUnit --> FetchMarkdown
    LoadFirstUnit --> FetchMarkdown
    LoadUnit --> FetchMarkdown
    
    FetchMarkdown[Fetch Markdown 檔案] --> ParseMD{Fetch 成功?}
    ParseMD -->|是| RenderHTML[marked.parse 渲染 HTML]
    ParseMD -->|否| ShowError[顯示錯誤訊息]
    
    RenderHTML --> HighlightCode[Prism.highlightAll]
    HighlightCode --> AddCopyBtn[添加複製按鈕]
    AddCopyBtn --> UpdateNav[更新導航高亮]
    UpdateNav --> SaveCurrent[儲存目前單元至 localStorage]
    SaveCurrent --> ScrollTop[捲動至頁面頂部]
    ScrollTop --> End([結束])
    ShowError --> End
```

### 11.2 進度追蹤流程圖

```mermaid
flowchart TD
    Start([使用者點擊完成按鈕]) --> CheckStatus{該單元已完成?}
    
    CheckStatus -->|是| MarkIncomplete[標記為未完成]
    CheckStatus -->|否| MarkComplete[標記為已完成]
    
    MarkIncomplete --> RemoveFromList[從 completedUnits 移除]
    MarkComplete --> AddToList[加入 completedUnits]
    
    RemoveFromList --> Calculate[計算進度百分比]
    AddToList --> Calculate
    
    Calculate --> UpdateStorage[更新 localStorage]
    UpdateStorage --> UpdateUI[更新 UI]
    
    subgraph UpdateUI[更新 UI]
        UpdateIcon[更新側邊欄圖示]
        UpdateProgress[更新進度條]
        UpdatePercentage[更新百分比數字]
        PlayAnimation[播放完成動畫]
    end
    
    UpdateUI --> End([結束])
```

---

## 12. 狀態圖

### 12.1 單元狀態圖

```mermaid
stateDiagram-v2
    [*] --> Unread: 載入課程
    
    Unread --> Reading: 點擊單元
    Reading --> Completed: 標記為已完成
    Completed --> Reading: 重新閱讀
    Completed --> Unread: 取消完成標記
    
    Reading --> Unread: 切換到其他單元
    
    state Unread {
        [*] --> Collapsed
        Collapsed --> Expanded: 展開章節
        Expanded --> Collapsed: 收合章節
    }
    
    state Reading {
        [*] --> Viewing
        Viewing --> Scrolling: 捲動頁面
        Scrolling --> Viewing: 停止捲動
    }
    
    state Completed {
        [*] --> Marked
        Marked --> Checked: 顯示勾選圖示
    }
```

### 12.2 計時器狀態圖

```mermaid
stateDiagram-v2
    [*] --> Stopped: 初始化
    
    Stopped --> Running: 頁面載入 / 使用者返回
    Running --> Paused: 視窗失去焦點
    Paused --> Running: 視窗獲得焦點
    Running --> Stopped: 頁面卸載
    
    Running: 每秒更新計時
    Running: 每 30 秒儲存進度
    
    Paused: 暫停計時
    Paused: 保留目前時間
```

---

## 13. 檔案結構

```
dify-tutorial/
├── index.html              # 主頁面
├── style.css               # 主樣式檔（或拆分為多個 CSS）
├── app.js                  # 主程式
├── courses.json            # 課程結構資料
├── README.md               # 專案說明
├── spec.md                 # 規格文件（本文件）
├── api.md                  # API 文件（本專案為靜態網站，無需）
├── 課綱/                   # 課程內容 Markdown 檔案
│   ├── 1.環境準備篇/
│   │   ├── 單元 1 - 本地安裝 Docker/
│   │   │   └── readme.md
│   │   ├── 單元 2 - 安裝社群版 Dify/
│   │   │   └── readme.md
│   │   └── 單元 3 - 透過 Zeabur 安裝社群版 Dify/
│   │       └── readme.md
│   ├── 2.入門篇 - Dify 基礎入門/
│   │   └── ... (6 單元)
│   ├── 3.基本操作篇/
│   │   └── ... (10 單元)
│   ├── 4.應用篇/
│   │   └── ... (8 單元)
│   ├── 5.進階應用篇/
│   │   └── ... (11 單元)
│   └── 6.進階開發篇/
│       └── ... (9 單元)
└── assets/                 # 靜態資源
    ├── images/             # 圖片
    └── icons/              # 自訂圖標
```

---

## 14. 功能清單

### 核心功能
- [x] 深色主題介面設計
- [x] 響應式側邊欄導航
- [x] Markdown 內容渲染
- [x] 程式碼語法高亮
- [x] 一鍵複製程式碼
- [x] 學習進度追蹤
- [x] 學習計時器
- [x] 章節展開/收合
- [x] URL hash 導航支援
- [x] localStorage 持久化

### 進階功能（可選）
- [ ] 淺色/深色主題切換
- [ ] 搜尋功能
- [ ] 目錄自動生成
- [ ] 圖片燈箱效果
- [ ] 互動式小測驗
- [ ] 學習筆記功能

---

## 15. 效能考量

1. **延遲載入**：僅在需要時載入 Markdown 內容
2. **快取策略**：已載入的內容可暫存避免重複請求
3. **最小化依賴**：僅使用必要的外部函式庫
4. **CSS 動畫**：使用 GPU 加速的 transform/opacity 屬性
5. **節流/防抖**：對捲動和視窗調整事件進行最佳化
