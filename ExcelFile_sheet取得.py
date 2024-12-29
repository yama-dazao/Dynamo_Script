import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import OpenFileDialog

import openpyxl  # 必要に応じてインストールしてください

# 1. ファイル選択ダイアログを開く
def open_file_dialog():
    dialog = OpenFileDialog()
    dialog.Filter = "Excel Files (*.xlsx)|*.xlsx"
    dialog.Multiselect = False  # 単一ファイルのみ選択可能
    if dialog.ShowDialog() == True:
        return dialog.FileName
    return None

# 2. Excelファイルを開いてシート一覧を取得
def get_excel_sheets(file_path):
    try:
        workbook = openpyxl.load_workbook(file_path, read_only=True)
        return workbook.sheetnames
    except Exception as e:
        return ["Error: " + str(e)]

# 3. Dynamoの出力
excel_file = open_file_dialog()  # ユーザーにファイルを選択させる
sheet_list = []

if excel_file:
    sheet_list = get_excel_sheets(excel_file)

OUT = excel_file, sheet_list
