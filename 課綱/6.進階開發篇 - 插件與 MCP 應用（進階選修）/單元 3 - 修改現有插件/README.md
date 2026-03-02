# 單元 3 - 修改現有插件

![封面](cover.png)

> 🕐 預估時長：20 分鐘

## 學習目標

完成本單元後，您將能夠：

- 從 Github 下載開源的 Dify Plugin 原始碼
- 看懂並修改 `manifest.yaml` 中的參數定義
- 在原本的 Tool 中新增客製化邏輯重新打包

## 內容大綱

從零開始寫一個插件可能有些困難，對大多數開發者來說，最快的學習方式是**拿別人寫好的開源插件來修改**。

### 1. 取得開源插件源碼

您可以前往 Dify 官方的 Github Repository 或社群開發者的專案，找到感興趣的 Plugin 源碼（例如：Google Search Plugin、Discord 發訊 Plugin）。
將其 Clone 到您的本地電腦：
```bash
git clone https://github.com/dify-plugins/some-plugin.git
cd some-plugin
```

### 2. 認識清單檔 (Manifest) 與 UI 渲染

在修改前，必須先看懂 `manifest.yaml` 或是裡面特定的工具定義檔。
Dify 插件非常聰明，**您不需要寫前端畫面！**
只要你在 yaml 檔案裡面定義了輸入參數，Dify 網頁畫面上就會自動長出針對這些參數的文字方塊、下拉選單或是 Toggle 開關。

例如：
```yaml
# 在工具定義檔中可能會看到類似結構
parameters:
  - name: show_details
    type: boolean
    required: false
    label:
      zh_Hant: 是否顯示詳細資訊
```
只要新增這段，等一下重新測試時，使用者畫面上就會多出一個名為「是否顯示詳細資訊」的勾選框！

### 3. 修改核心邏輯

打開對應的 Python 實作檔（如 `my_tool.py`）。
該函數通常會透過 `args.get("show_details")` 來接收剛剛使用者在畫面上勾選的變數。

您可以加入判斷：
```python
if args.get("show_details"):
    return {"result": f"這是超級詳細結果：{data.full_json}"}
else:
    return {"result": f"這是摘要結果：{data.summary}"}
```

### 4. 重新打包與發布

修改完畢並用 `dify-plugin dev` 在本地調試確認無誤後，您可以將整個資料夾重新打包：
```bash
dify-plugin build
```
指令會產生一個包含你最新程式碼的 `.difypkg` (或 zip) 檔案。只要回到 Dify 介面，在插件頁面點選「本地安裝 / 上傳檔案」，將這個包傳上去，你專屬客製化版本的插件就上線服役了！

---

## 📝 課後小測驗

> [!QUIZ]
> **Q: 如果想要讓使用這個插件的人，在 Dify 畫面上看到一個新的下拉選單來選擇參數，我們需要在哪裡修改？**
>
> - [x] 在 `manifest.yaml` (或工具定義的設定檔) 中新增該參數的定義
> - [ ] 去寫 HTML/JavaScript 前端程式碼
> - [ ] 在 Python `main.py` 印出特殊字串

> [!QUIZ]
> **Q: 修改並打包好的插件檔案（通常是一個壓縮包），如何部署到 Dify 上？**
>
> - [ ] 必須提交給官方審核，等兩個禮拜
> - [ ] 將程式碼用 FTP 傳上 Dify 原廠伺服器
> - [x] 透過 Dify 網頁介面的「本地安裝/上傳檔案」功能直接上傳
