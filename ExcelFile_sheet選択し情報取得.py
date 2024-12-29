import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Form, ComboBox, Button, DialogResult, Label

import openpyxl  # 必要に応じてインストールしてください

# 1. シート選択画面を作成
def show_sheet_selector(sheet_names):
    form = Form()
    form.Text = "シート選択"
    form.Width = 300
    form.Height = 150

    label = Label()
    label.Text = "シート名を選択してください："
    label.Top = 10
    label.Left = 10
    label.Width = 260
    form.Controls.Add(label)

    combo = ComboBox()
    combo.Top = 40
    combo.Left = 10
    combo.Width = 260
    combo.DataSource = sheet_names
    form.Controls.Add(combo)

    ok_button = Button()
    ok_button.Text = "OK"
    ok_button.Top = 80
    ok_button.Left = 100
    ok_button.Width = 80

    def on_ok_click(sender, event):
        form.Tag = combo.SelectedItem  # 選択されたシート名を保存
        form.DialogResult = DialogResult.OK
        form.Close()

    ok_button.Click += on_ok_click
    form.Controls.Add(ok_button)

    if form.ShowDialog() == DialogResult.OK:
        return form.Tag  # 選択されたシート名を返す
    return None

# 2. 選択したシートの行・列情報を取得
def get_sheet_data(file_path, sheet_name):
    try:
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        sheet = workbook[sheet_name]
        data = []
        for row in sheet.iter_rows(values_only=True):
            data.append(row)
        return data
    except Exception as e:
        return ["Error: " + str(e)]

# Dynamoからの入力 (OUTで受け取る想定)
excel_file = IN[0]  # Excelファイルのパス
sheet_list = IN[1]  # シート名のリスト

selected_sheet = None
sheet_data = []

if excel_file and sheet_list:
    # ユーザーがシートを選択
    selected_sheet = show_sheet_selector(sheet_list)
    if selected_sheet:
        # 選択されたシートのデータを取得
        sheet_data = get_sheet_data(excel_file, selected_sheet)

# Dynamoへの出力
OUT = selected_sheet, sheet_data
