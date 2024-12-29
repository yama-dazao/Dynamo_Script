# 必要なライブラリをインポート
import clr
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

# 現在のドキュメントを取得
doc = DocumentManager.Instance.CurrentDBDocument

# ファミリ名を格納するリスト
family_names = []

# 全てのファミリシンボルを取得
collector = FilteredElementCollector(doc).OfClass(Family)

for family in collector:
    # ファミリ名をリストに追加
    family_names.append(family.Name)

# OUTにファミリ名のリストを出力
OUT = family_names
