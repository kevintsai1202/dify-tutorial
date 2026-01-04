# 單元 3 - 透過 Zeabur 安裝社群版 Dify

![封面](cover.png)

> 🕐 預估時長：15 分鐘

## 學習目標

完成本單元後，您將能夠：
- 了解 Zeabur 雲端平台的特色
- 一鍵部署 Dify 到 Zeabur
- 設定自訂網域與環境變數

## 內容大綱

### 1. Zeabur 簡介

Zeabur 是一個台灣團隊開發的雲端部署平台，特色包括：
- **一鍵部署**：支援多種開源專案模板
- **自動擴縮**：根據流量自動調整資源
- **免費額度**：提供免費試用額度
- **中文介面**：對繁體中文用戶友善

### 2. 部署步驟

#### Step 1: 註冊 Zeabur 帳號
1. 前往 [Zeabur 官網](https://zeabur.com)
2. 使用 GitHub 或 Google 帳號登入

#### Step 2: 建立專案
1. 點擊「New Project」
2. 選擇伺服器區域（建議選擇香港或新加坡）

#### Step 3: 部署 Dify
1. 點擊「Deploy」
2. 搜尋「Dify」模板
3. 選擇並點擊「Deploy」

### 3. 環境設定

Zeabur 會自動設定以下服務：
- PostgreSQL 資料庫
- Redis 快取
- Dify 後端與前端

您可以在「Environment Variables」中調整設定。

### 4. 自訂網域

1. 進入專案設定
2. 點擊「Domains」
3. 新增自訂網域或使用 Zeabur 提供的子網域

---

## 📝 課後小測驗

> [!QUIZ]
> **Q: Zeabur 平台的主要優勢是？**
> - [x] 一鍵部署、自動擴縮、提供免費額度
> - [ ] 只支援 Python 專案
> - [ ] 需要自行管理伺服器

> [!QUIZ]
> **Q: 在 Zeabur 上部署 Dify 時，資料庫需要自己安裝嗎？**
> - [ ] 需要，要手動安裝 PostgreSQL
> - [x] 不需要，Zeabur 會自動配置所需的資料庫服務
> - [ ] 不需要資料庫
