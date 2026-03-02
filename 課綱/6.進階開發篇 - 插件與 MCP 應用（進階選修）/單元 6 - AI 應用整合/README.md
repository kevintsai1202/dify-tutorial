# 單元 6 - AI 應用整合

![封面](cover.png)

> 🕐 預估時長：20 分鐘

## 學習目標

完成本單元後，您將能夠：

- 理解如何將 Dify 開放的 API 與 MCP 服務整合至外部客戶端
- 將 Dify 封裝好的 MCP 工具放入 Claude Desktop 開啟強大使用體驗
- 利用 Dify 的 API (API Extension) 將智慧工作流串接入現有企業系統中

## 內容大綱

在前面的單元中，我們將 Dify 開發好的流程或知識庫封裝成了 **API** 或者是 **MCP 服務 (MCP Server)**。
這個單元的重點，就是跳出 Dify 網站，到「外面」的世界，用其他外部工具來調用從 Dify 發布出來的能力。

### 1. 外部客戶端使用 MCP 的情境 (以 Claude Desktop 為例)

當您在上個單元取得了一組由 Dify 工作流產生的 MCP API URL 與 API Key，您可以將它整合進像是 **Claude Desktop** (Anthropic 官方電腦版應用) 等支援 MCP 的客戶端中。

**設定步驟概覽（以 Claude Desktop 為例）：**
1.  打開 Claude Desktop 的設定檔 (`claude_desktop_config.json`)。
2.  在 `mcpServers` 區塊下新增一筆伺服器設定。
3.  將設定型態指定為 `sse` (Server-Sent Events) 或者使用命令列工具進行遠端請求，填入從 Dify 取得的 URL。
4.  將 Dify 的 API Key 放在連線環境變數或是 Header 設定中。

重啟客戶端後，您從 Claude 聊天框裡，就會看到多出了一把工具圖示 🔨。這就代表您的 Claude 現在可以自由自在地呼叫您在 Dify 上的超級工作流了！

### 2. 外部企業系統使用 API 的情境

除了 MCP 之外，Dify 所有的工作流、對話應用程式也都能發布成標準的 **RESTful API**。這是更沒有系統門檻的整合方式。

**常見 API 整合範例：**
*   **整合到公司官網**：將 Dify 發布的 `ChatBot API` 嵌入到官網的客服對話方塊。客戶在官網問問題，背後其實是在呼叫 Dify 的 API 來回答。
*   **內部 ERP / Slack 機器人**：寫一段簡單的小程式，讓公司的 Slack 機器人每天收到指令後，透過 HTTP POST 打向 Dify 發布的 `Workflow API` 產生投資日報，拿到純文字結果後再發送到 Slack 頻道裡。

### 3. 一次開發，無限延伸的 AI 生態

綜合第六章所學的 Plugins、MCP 與 API：
Dify 不只是一個獨立的對話網頁沙箱。它是一個**超級大腦與加工廠**。
您可以把自己寫的程式 (Plugin) 丟進 Dify 讓 AI 用；也可以把 Dify 組合好的頂級智能，化身成 API 或 MCP 工具，發送到全世界給您的網頁、手機 App 或其他大平台 (如 Claude、Cursor 等) 使用。

恭喜您，現在您已經看懂了大語言模型生態系未來最重要的發展方向：**能力解耦與無縫的系統級整合**。

---

## 📝 課後小測驗

> [!QUIZ]
> **Q: 我們將 Dify 的流程開放成 MCP API 後，接下來通常要將這組 API 填入哪裡？**
>
> - [ ] 貼到 Facebook 粉絲團
> - [x] 設定在各種支援 MCP 協議的外部客戶端應用中（例如 Claude Desktop 的 `claude_desktop_config.json`）
> - [ ] 貼回到 Dify 的一開始的知識庫中

> [!QUIZ]
> **Q: 如果我的公司官網需要放一個 AI 客服對話框，通常我們會使用 Dify 釋出的哪一種功能來進行整合最普遍？**
>
> - [x] 發布成標準網頁應用，並使用它提供的 RESTful API
> - [ ] 要求所有客戶去下載 Claude Desktop 來裝 MCP
> - [ ] 原生 Plugin
