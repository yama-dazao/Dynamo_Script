# 必要なライブラリをインポート
import clr
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

# 現在のドキュメントを取得
doc = DocumentManager.Instance.CurrentDBDocument

# タイプ名を格納するリスト
type_names = []

# 全ての要素タイプを取得
collector = FilteredElementCollector(doc).WhereElementIsElementType()

for element_type in collector:
    # ElementTypeから名前を取得
    type_name = element_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    if type_name:  # 名前が空でない場合
        type_names.append(type_name)

# OUTにタイプ名のリストを出力
OUT = type_names
