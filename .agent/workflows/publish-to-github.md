---
description: 將專案 commit 並發佈到 GitHub 和 GitHub Pages
---

# 發佈到 GitHub Pages 工作流程

## 前置條件
- 專案已初始化 Git 倉庫
- 已設定 GitHub 遠端倉庫
- 已啟用 GitHub Pages

## 執行步驟

### 1. 檢查 Git 狀態
// turbo
```powershell
git status
```
確認有哪些檔案需要提交。

### 2. 加入所有變更
// turbo
```powershell
git add .
```

### 3. 提交變更
```powershell
git commit -m "更新內容"
```
根據實際修改內容調整 commit 訊息。

### 4. 推送到 GitHub
// turbo
```powershell
git push origin master
```
將變更推送到遠端倉庫，GitHub Pages 會自動重新部署。

### 5. 驗證部署
等待 1-2 分鐘後，訪問 GitHub Pages 網址確認更新：
- 倉庫：https://github.com/kevintsai1202/dify-tutorial
- 網站：https://kevintsai1202.github.io/dify-tutorial/

## 注意事項
- 若推送失敗，請先執行 `git pull origin master` 同步遠端變更
- GitHub Pages 部署需要 1-2 分鐘，請稍等後再刷新頁面
