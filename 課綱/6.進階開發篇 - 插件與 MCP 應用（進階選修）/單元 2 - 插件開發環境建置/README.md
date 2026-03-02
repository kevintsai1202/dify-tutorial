# 單元 2 - 插件開發環境建置

![封面](cover.png)

> 🕐 預估時長：20 分鐘

## 學習目標

完成本單元後，您將能夠：

- 安裝並設定 Dify Plugin 開發專用的 CLI 工具
- 了解 Dify SDK 的基本目錄結構
- 在本地成功初始化並啟動第一個 Hello World 插件

## 內容大綱

如果您決定親自開發 Dify 原生插件，必須先準備好合適的開發環境。Dify 官方提供了開發者套件 (SDK) 和命令列工具 (CLI) 來簡化這個流程。

### 1. 下載與設定 Dify Plugin Daemon

現在 Dify 官方提供了更先進的 Plugin 開發工具，也就是 Dify Plugin Daemon。

1.  **下載執行檔**：前往 [Dify Plugin Daemon Releases](https://github.com/langgenius/dify-plugin-daemon/releases) 頁面，下載適合您作業系統的最新執行檔。
2.  **設定環境變數**：下載後將檔案改名為 `dify.exe`（如果在 Windows 上），並將其所在的路徑加入系統的 `PATH` 環境變數中。
3.  *(詳細設定與說明請參考官網：[Getting Started with Dify Plugin](https://docs.dify.ai/en/develop-plugin/getting-started/getting-started-dify-plugin))*

### 2. 結合 AI 技能快速開發

為了大幅加速開發流程，我們可以透過安裝特定的 AI 技能，讓 AI 來協助我們自動生成 Dify Plugin 的骨架與程式碼。

1.  **安裝技能**：打開您的終端機 (Terminal / Command Prompt)，執行以下指令：
    ```bash
    npx skills add skilzy-ai/official-skills@dify-tool-developer -g -y
    ```
2.  **快速生成專案**：安裝完成後，您只需要跟 AI 提出需求，例如：
    > 「**使用技能開發 Dify plugin，工具類別，功能是查詢出貨訂單**」
    
    AI 就會自動幫您建立起專案結構、撰寫相關邏輯程式碼，並指引您完成測試，省去繁瑣的手動初始化過程！

---

## 📝 課後小測驗

> [!QUIZ]
> **Q: 要開發 Dify 原生插件，目前官方最完整支援與推薦的開發語言為何？**
>
> - [x] Python
> - [ ] Java
> - [ ] C++

> [!QUIZ]
> **Q: 在初始化的插件目錄中，哪一個檔案是用來紀錄該插件的版本資訊與宣告包含哪些工具介面，被視為是插件的「身分證」？**
>
> - [ ] `requirements.txt`
> - [x] `manifest.yaml`
> - [ ] `main.py`
