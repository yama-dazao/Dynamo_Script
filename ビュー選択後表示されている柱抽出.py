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

def get_visible_columns_in_view(view):
    collector = FilteredElementCollector(doc, view.Id) \
        .OfCategory(BuiltInCategory.OST_StructuralColumns) \
        .WhereElementIsNotElementType()

    visible_columns = []

    # ビューのCropBox（表示範囲）で交差判定を行う
    if view.CropBoxActive and view.CropBoxVisible:
        crop_box = view.CropBox
        view_box = Outline(crop_box.Min, crop_box.Max)

        for element in collector:
            if element.IsHidden(view):
                continue
            bbox = element.get_BoundingBox(view)
            if bbox and view_box.Intersects(Outline(bbox.Min, bbox.Max), 0.0001):
                visible_columns.append(element)
    else:
        # CropBoxが無効なら、IsHiddenだけで判定（やや粗いがfallbackとして有効）
        for element in collector:
            if not element.IsHidden(view):
                visible_columns.append(element)

    return visible_columns

if result == DialogResult.OK:
    selected_view_name = form.cb_views.SelectedItem
    selected_view = next((v for v in valid_views if v.Name == selected_view_name), None)
    if selected_view:
        columns = get_visible_columns_in_view(selected_view)
        OUT = columns
    else:
        OUT = "ビューが見つかりません"
else:
    OUT = "キャンセルされました"
