# epubtopdf
auto transfer epub ebook to pdf 
# EPUB to PDF Converter

一個使用 Python 和 Calibre 的 `ebook-convert` 工具將 EPUB 檔案批量轉換為 PDF 檔案的程式。支援多進程並行處理，提高轉換效率。

## 功能特色

- 批量轉換當前目錄中的所有 EPUB 檔案
- 多進程並行處理，提升轉換速度
- 自動檢測 Calibre 工具
- 優化的 PDF 輸出設定（A4 紙張、頁碼、字體嵌入）

## 依賴要求

### 必需軟體
- Python 3.6+
- Calibre（包含 `ebook-convert` 工具）

### Python 模組
程式使用的所有模組都是 Python 標準庫：
- `os`
- `glob`
- `subprocess`
- `multiprocessing`

## 安裝 Calibre

### macOS
```bash
# 使用 Homebrew
brew install --cask calibre

# 或從官網下載
# https://calibre-ebook.com/download
