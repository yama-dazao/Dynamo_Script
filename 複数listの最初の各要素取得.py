# DynamoのPythonスクリプト
# IN[0]には構造ファイル(Listデータ構造)が入力されることを前提としています

# 入力データ
data = IN[0]

# ファミリ名を格納するリスト
family_names = []

# データ構造を走査し、"List > 数字 > 0" の値を取得
for list_item in data:
    if isinstance(list_item, list) and len(list_item) > 0:
        family_name = list_item[0]  # 各Listの最初の要素を取得
        family_names.append(family_name)

# 出力
OUT = family_names
