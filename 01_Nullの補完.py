# DynamoのINデータを取得
input_data = IN[0]

# 前のリストの0番目の値を保持する変数
previous_family_name = None

# null (None) を埋める処理
for sublist in input_data:
    if sublist[0] is None:  # 0番目の値がnullの場合
        sublist[0] = previous_family_name
    else:
        previous_family_name = sublist[0]  # 0番目がnullでない場合、値を保持

# 処理後のデータをOUTに出力
OUT = input_data
