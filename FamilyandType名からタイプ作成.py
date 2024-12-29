# Dynamoで必要なライブラリをインポート
import clr
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

# Dynamo入力
family_names = IN[0]  # ファミリ名リスト (例: ["RC", "RC", "RC"])
type_names = IN[1]    # タイプ名リスト (例: ["1", "2", "3"])

# 現在のRevitドキュメントを取得
doc = DocumentManager.Instance.CurrentDBDocument

# 出力リスト
outputs = []

# トランザクションの開始
TransactionManager.Instance.EnsureInTransaction(doc)

try:
    # 入力リストの長さを確認
    if len(family_names) != len(type_names):
        raise Exception("ファミリ名とタイプ名のリストの長さが一致していません。")
    
    # 各ファミリ名とタイプ名のペアに対して処理を実行
    for family_name, type_name in zip(family_names, type_names):
        # ファミリシンボル（タイプ）のリストを取得
        collector = FilteredElementCollector(doc).OfClass(FamilySymbol)
        family_symbols = [fs for fs in collector if fs.Family.Name == family_name]
        
        if not family_symbols:
            outputs.append(f"指定されたファミリ '{family_name}' が見つかりません。")
            continue
        
        # 最初のタイプを基準に複製
        base_type = family_symbols[0]
        new_type = base_type.Duplicate(type_name)
        
        # 成功メッセージをリストに追加
        outputs.append(f"新しいタイプ '{type_name}' がファミリ '{family_name}' に作成されました。")

except Exception as e:
    outputs.append(f"エラー: {str(e)}")

# トランザクションの終了
TransactionManager.Instance.TransactionTaskDone()

# Dynamoに出力を渡す
OUT = outputs
