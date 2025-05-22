import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from Autodesk.Revit.DB import BuiltInCategory
from Autodesk.Revit.UI.Selection import ObjectType
from RevitServices.Persistence import DocumentManager

from System.Windows.Forms import Form, Button, Label, Application, DialogResult
from System.Drawing import Point, Size

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

selected_floor = None
selected_room = None

class SelectForm(Form):
    def __init__(self):
        self.Text = "床と部屋の選択"
        self.Size = Size(500, 300)
        self.StartPosition = 1
        self.TopMost = True
        self.result = None

        # 床選択
        self.btn_floor = Button()
        self.btn_floor.Text = "① 床を選択"
        self.btn_floor.Location = Point(30, 30)
        self.btn_floor.Click += self.select_floor
        self.Controls.Add(self.btn_floor)

        self.lbl_floor = Label()
        self.lbl_floor.Text = "未選択"
        self.lbl_floor.Location = Point(30, 70)
        self.lbl_floor.Size = Size(420, 30)
        self.Controls.Add(self.lbl_floor)

        # 部屋選択
        self.btn_room = Button()
        self.btn_room.Text = "② 部屋を選択"
        self.btn_room.Location = Point(30, 110)
        self.btn_room.Click += self.select_room
        self.Controls.Add(self.btn_room)

        self.lbl_room = Label()
        self.lbl_room.Text = "未選択"
        self.lbl_room.Location = Point(30, 150)
        self.lbl_room.Size = Size(420, 30)
        self.Controls.Add(self.lbl_room)

        # OKボタン
        self.btn_ok = Button()
        self.btn_ok.Text = "③ OK"
        self.btn_ok.Location = Point(150, 220)
        self.btn_ok.Click += self.ok_clicked
        self.Controls.Add(self.btn_ok)

        # キャンセルボタン
        self.btn_cancel = Button()
        self.btn_cancel.Text = "④ キャンセル"
        self.btn_cancel.Location = Point(250, 220)
        self.btn_cancel.Click += self.cancel_clicked
        self.Controls.Add(self.btn_cancel)

    def select_floor(self, sender, args):
        global selected_floor
        try:
            ref = uidoc.Selection.PickObject(ObjectType.Element, "床を選択してください")
            elem = doc.GetElement(ref.ElementId)
            if elem.Category.Id.IntegerValue != int(BuiltInCategory.OST_Floors):
                raise Exception("選択された要素は床ではありません")
            selected_floor = elem
            self.lbl_floor.Text = f"✔ {elem.Name} / {elem.Category.Name} / ID: {elem.Id}"
        except Exception as e:
            selected_floor = None
            self.lbl_floor.Text = f"❌ キャンセルまたはエラー: {str(e)}"

    def select_room(self, sender, args):
        global selected_room
        try:
            ref = uidoc.Selection.PickObject(ObjectType.Element, "部屋または部屋タグを選択してください")
            elem = doc.GetElement(ref.ElementId)

            if elem.Category.Id.IntegerValue == int(BuiltInCategory.OST_Rooms):
                room = elem
            elif elem.Category.Id.IntegerValue == int(BuiltInCategory.OST_RoomTags):
                room = elem.Room
                if room is None:
                    raise Exception("RoomTag に関連する部屋が存在しません")
            else:
                raise Exception("選択された要素は部屋でもタグでもありません")

            selected_room = room
            category_name = room.Category.Name if room.Category else "(カテゴリ不明)"
            self.lbl_room.Text = f"✔ カテゴリ: {category_name} / ID: {room.Id}"

        except Exception as e:
            selected_room = None
            self.lbl_room.Text = f"❌ エラー: {str(e)}"

    def ok_clicked(self, sender, args):
        if selected_floor is None or selected_room is None:
            self.lbl_floor.Text = "⚠️ 床または部屋が未選択です"
        else:
            self.result = DialogResult.OK
            self.Close()

    def cancel_clicked(self, sender, args):
        self.result = DialogResult.Cancel
        self.Close()

# フォーム実行
form = SelectForm()
Application.Run(form)

# 出力処理
try:
    if form.result == DialogResult.OK and selected_floor and selected_room:
        OUT = [selected_floor.Id.IntegerValue, selected_room.Id.IntegerValue]
    elif form.result == DialogResult.Cancel:
        OUT = "キャンセルされました"
    else:
        OUT = "⚠️ OKが押されましたが、未選択の項目があります"
except Exception as e:
    OUT = f"⚠️ 実行エラー：{str(e)}"
