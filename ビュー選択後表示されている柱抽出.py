import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
clr.AddReference('RevitAPIUI')
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from Autodesk.Revit.DB import View as DBView
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
from System.Windows.Forms import *
from System.Drawing import *

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

# ビュー一覧取得（テンプレート除外）
views = FilteredElementCollector(doc).OfClass(DBView).ToElements()
valid_views = [v for v in views if not v.IsTemplate]

class ViewSelectForm(Form):
    def __init__(self):
        self.Text = "① ビュー選択"
        self.Size = Size(400, 150)
        self.StartPosition = FormStartPosition.CenterScreen
        self.TopMost = True

        self.label = Label()
        self.label.Text = "表示したいビューを選んでください："
        self.label.Location = Point(10, 20)
        self.label.Size = Size(350, 20)
        self.Controls.Add(self.label)

        self.cb_views = ComboBox()
        self.cb_views.Location = Point(10, 50)
        self.cb_views.Size = Size(350, 20)
        self.cb_views.DropDownStyle = ComboBoxStyle.DropDownList
        self.cb_views.Items.AddRange([v.Name for v in valid_views])
        if self.cb_views.Items.Count > 0:
            self.cb_views.SelectedIndex = 0
        self.Controls.Add(self.cb_views)

        self.btn_ok = Button()
        self.btn_ok.Text = "OK"
        self.btn_ok.Location = Point(250, 80)
        self.btn_ok.DialogResult = DialogResult.OK
        self.Controls.Add(self.btn_ok)

        self.btn_cancel = Button()
        self.btn_cancel.Text = "キャンセル"
        self.btn_cancel.Location = Point(150, 80)
        self.btn_cancel.DialogResult = DialogResult.Cancel
        self.Controls.Add(self.btn_cancel)

        self.selected_view = None

# フォーム実行
form = ViewSelectForm()
result = form.ShowDialog()

if result == DialogResult.OK:
    selected_view_name = form.cb_views.SelectedItem
    selected_view = next((v for v in valid_views if v.Name == selected_view_name), None)
    if selected_view:
        # 選ばれたビューに見える構造柱を取得
        columns = FilteredElementCollector(doc, selected_view.Id) \
            .OfCategory(BuiltInCategory.OST_StructuralColumns) \
            .WhereElementIsNotElementType() \
            .ToElements()
        OUT = columns
    else:
        OUT = "ビューが見つかりません"
else:
    OUT = "キャンセルされました"
