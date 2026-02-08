# 單元 2 - Embedding 及 Rerank 模型說明

![封面](cover.png)

> 🕐 預估時長：15 分鐘

## 學習目標

完成本單元後，您將能夠：
- 區分 Embedding (向量化) 與 Rerank (重排序) 模型的用途
- 選擇適合的供應商 (OpenAI vs Jina/Voyage)
- 理解「多模態 Embedding」如何處理圖片內容

## 內容大綱

### 1. 雙塔架構：Embedding + Rerank

要實作高精準度的搜尋，我們通常採用「兩階段搜尋」：

1.  **第一階段：Embedding (粗篩)**
    -   **原理**：將文字轉成向量 (一大串數字)，透過數學距離找出相似的內容。
    -   **優點**：速度快，可以處理海量資料。
    -   **缺點**：精準度約 80%，有時候會抓到相關但非關鍵的資料。
    -   **主流模型**：OpenAI text-embedding-3, Jina Embeddings, Voyage.

2.  **第二階段：Rerank (精排)**
    -   **原理**：將第一階段篩選出的前 50~100 筆資料，與使用者的問題進行深度比對與評分。
    -   **優點**：精準度極高 (可達 90% 以上)。
    -   **缺點**：速度較慢，成本較高 (因此只用於第二階段少量資料)。
    -   **主流模型**：Jina Reranker, Voyage Rerank, Cohere Rerank.

### 2. 模型供應商選擇

-   **Jina AI / Voyage AI**：
    -   **推薦原因**：專精於搜尋技術，同時提供 Embedding 與 Rerank 模型，整合度高。
    -   **特色**：部分模型支援 **Vision (視覺)**，可以對圖片進行向量化搜尋。
    -   **費用**：通常有提供免費額度，練習時非常夠用。
-   **OpenAI**：
    -   只提供 Embedding 模型，**沒有 Rerank 模型**。
    -   如果您只使用 OpenAI，建議另外搭配 Cohere 或 Jina 的 Rerank 模型以提升效果。

### 3. 設定注意事項

-   **對稱性原則**：上傳文件時使用哪個 Embedding 模型，查詢時就必須使用同一個。如果你換了模型，整個知識庫必須重新建立 (Re-index)。
-   **API Key 配置**：在 Dify 的「模型供應商」頁面設定 Jina 或 Voyage 的 API Key 後，記得在知識庫設定中切換過去，不要傻傻地一直用預設模型。

---

## 📝 課後小測驗

> [!QUIZ]
> **Q: 為什麼有了 Embedding 還需要 Rerank？**
> - [ ] 因為 Rerank 比較便宜
> - [ ] Embedding 只能處理英文
> - [x] Embedding 負責快速粗篩，Rerank 負責高精度排序，兩者結合效果最好

> [!QUIZ]
> **Q: 如果我在 Dify 中使用 OpenAI 的 Embedding 模型，可以直接使用 OpenAI 的 Rerank 模型嗎？**
> - [ ] 可以，OpenAI 是萬能的
> - [x] 不行，OpenAI 目前官方並未提供 Rerank 模型
