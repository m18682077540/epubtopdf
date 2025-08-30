import os
import subprocess
import glob

def convert_epub_to_pdf(epub_path, pdf_path):
    """
    使用 Calibre 的 ebook-convert 工具將 EPUB 檔案轉換為 PDF 檔案。
    程式會嘗試預設的 Calibre 安裝路徑，如果找不到則依賴系統 PATH。

    Args:
        epub_path (str): EPUB 檔案的完整路徑。
        pdf_path (str): 輸出 PDF 檔案的完整路徑。

    Returns:
        bool: 如果轉換成功則為 True，否則為 False。
    """
    # 定義 Calibre ebook-convert 在 macOS 上的常見路徑
    calibre_ebook_convert_path = "/Applications/calibre.app/Contents/MacOS/ebook-convert"
    command_prefix = ['ebook-convert'] # 預設使用 PATH 中的 ebook-convert

    # 檢查 ebook-convert 命令是否可用，優先檢查指定路徑
    try:
        # 嘗試直接使用指定路徑來測試 ebook-convert
        subprocess.run([calibre_ebook_convert_path, '--version'], check=True, capture_output=True, text=True)
        command_prefix = [calibre_ebook_convert_path] # 如果指定路徑有效，則使用它
        print(f"偵測到 ebook-convert 位於：{calibre_ebook_convert_path}")
    except FileNotFoundError:
        # 如果指定路徑找不到，則嘗試在系統 PATH 中尋找
        try:
            subprocess.run(['ebook-convert', '--version'], check=True, capture_output=True, text=True)
            print("偵測到 ebook-convert 位於系統 PATH 中。")
        except FileNotFoundError:
            print("錯誤：找不到 'ebook-convert' 命令。")
            print(f"已檢查指定路徑 '{calibre_ebook_convert_path}' 和系統 PATH。")
            print("請確保您已安裝 Calibre 並將其添加到系統 PATH 中，或 Calibre 安裝在預設位置。")
            print("您可以從 Calibre 官方網站下載：https://calibre-ebook.com/download")
            return False
        except subprocess.CalledProcessError as e:
            print(f"錯誤：系統 PATH 中的 'ebook-convert' 命令執行失敗。請檢查 Calibre 安裝。")
            print(f"錯誤輸出：\n{e.stderr}")
            return False
        except Exception as e:
            print(f"檢查系統 PATH 中的 'ebook-convert' 時發生意外錯誤：{e}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"錯誤：指定路徑 '{calibre_ebook_convert_path}' 的 'ebook-convert' 命令執行失敗。請檢查 Calibre 安裝。")
        print(f"錯誤輸出：\n{e.stderr}")
        return False
    except Exception as e:
        print(f"檢查指定路徑 '{calibre_ebook_convert_path}' 時發生意外錯誤：{e}")
        return False

    print(f"正在將 '{os.path.basename(epub_path)}' 轉換為 PDF...")
    try:
        # 轉換 EPUB 到 PDF 的命令
        # 移除了 --enable-font-subsetting 選項，因為您的 Calibre 版本不支援
        # --paper-size: 設定紙張大小，A4 是常見的預設值
        # --pdf-page-numbers: 添加頁碼
        # --output-profile: 輸出設定檔，'tablet' 適用於一般閱讀
        # --embed-all-fonts: 將所有字體嵌入 PDF 中
        command = command_prefix + [
            epub_path,
            pdf_path,
            '--paper-size', 'a4',
            '--pdf-page-numbers',
            '--output-profile', 'tablet',
            '--embed-all-fonts'
        ]
        # 執行命令並捕獲輸出
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"'{os.path.basename(epub_path)}' 已成功轉換為 '{os.path.basename(pdf_path)}'。")
        # 您可以取消註釋以下行以查看詳細的輸出（用於調試）
        # print("標準輸出：\n", result.stdout)
        # print("標準錯誤：\n", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        # 如果命令返回非零退出代碼，則表示轉換失敗
        print(f"轉換 '{os.path.basename(epub_path)}' 時發生錯誤：")
        print(f"錯誤代碼：{e.returncode}")
        print(f"標準輸出：\n{e.stdout}")
        print(f"標準錯誤：\n{e.stderr}")
        return False
    except Exception as e:
        # 捕獲其他所有可能的異常
        print(f"轉換 '{os.path.basename(epub_path)}' 時發生意外錯誤：{e}")
        return False

def main():
    """
    主函數：掃描 EPUB 檔案並提示用戶進行轉換。
    """
    print("=" * 30)
    print("         EPUB 到 PDF 轉換器         ")
    print("=" * 30)
    print("重要提示：")
    print("本程式依賴於 Calibre 的 'ebook-convert' 工具。")
    print("程式會嘗試預設的 Calibre 安裝路徑 (/Applications/calibre.app/Contents/MacOS/ebook-convert)，")
    print("如果找不到，則會嘗試從系統 PATH 中尋找。")
    print("Calibre 官方網站：https://calibre-ebook.com/download")
    print("-" * 30)

    # 獲取當前工作目錄
    current_directory = os.getcwd()
    # 查找當前目錄中所有副檔名為 .epub 的檔案
    epub_files = glob.glob(os.path.join(current_directory, '*.epub'))

    if not epub_files:
        print(f"在當前目錄 '{current_directory}' 中找不到任何 .epub 檔案。")
        print("請將 EPUB 檔案放在與此 Python 腳本相同的目錄中。")
        return

    print(f"在 '{current_directory}' 中找到以下 EPUB 檔案：")
    for i, file in enumerate(epub_files):
        print(f"{i+1}. {os.path.basename(file)}")
    print("-" * 30)

    # 遍歷每個找到的 EPUB 檔案
    for epub_file_path in epub_files:
        epub_filename = os.path.basename(epub_file_path)
        # 為輸出 PDF 檔案構建名稱 (與 EPUB 檔案同名，但副檔名為 .pdf)
        pdf_filename = os.path.splitext(epub_filename)[0] + '.pdf'
        pdf_file_path = os.path.join(current_directory, pdf_filename)

        # 循環直到用戶輸入有效的 'Y' 或 'N'
        while True:
            choice = input(f"是否要將 '{epub_filename}' 轉換為 PDF？ (Y/N): ").strip().upper()
            if choice == 'Y':
                convert_epub_to_pdf(epub_file_path, pdf_file_path)
                break  # 退出內層循環，處理下一個檔案
            elif choice == 'N':
                print(f"跳過 '{epub_filename}' 的轉換。")
                break  # 退出內層循環，處理下一個檔案
            else:
                print("無效的輸入。請輸入 'Y' 或 'N'。")
        print("-" * 30)

    print("所有 EPUB 檔案的處理已完成。")
    print("感謝使用！")

if __name__ == "__main__":
    main()
