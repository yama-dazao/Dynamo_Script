# DynamoのINデータを取得
input_families = IN[0]  # Input1: 取得済みのファミリ名リスト
list_data = IN[1]  # 数字+List構造のデータ

# 結果を格納するリスト
included_lists = []  # Input1に含まれているファミリ名を持つリスト
excluded_lists = []  # Input1に含まれていないファミリ名を持つリスト

# データ構造を走査
for numbered_list in list_data:
    family_name = numbered_list[0]  # 各リストの0番目の値がファミリ名
    if family_name in input_families:
        included_lists.append(numbered_list)  # 含まれているリストに追加
    else:
        excluded_lists.append(numbered_list)  # 含まれていないリストに追加

# 結果をOUTに出力
OUT = (included_lists, excluded_lists)
