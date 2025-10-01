from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# เก็บข้อมูลกิ๊กใน list (แทนฐานข้อมูล)
giks = []
next_id = 1  # สำหรับสร้าง id ไม่ให้ซ้ำ

# ---------- HTML Template ----------
template = """
<!doctype html>
<html lang="th">
<head>
    <meta charset="utf-8">
    <title>โปรแกรมบันทึกข้อมูลกิ๊ก (ไม่ใช้ฐานข้อมูล)</title>
    <style>
        body { font-family: Tahoma, sans-serif; margin: 40px; background: #fafafa; }
        h1 { color: #444; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #aaa; padding: 8px; text-align: center; }
        th { background: #ddd; }
        form { margin-top: 20px; }
        input[type=text] { padding: 6px; margin: 4px; }
        input[type=submit] { padding: 6px 12px; margin-left: 6px; }
        a { text-decoration: none; color: blue; }
    </style>
</head>
<body>
    <h1>💖 โปรแกรมบันทึกข้อมูลกิ๊ก</h1>

    <!-- ฟอร์มเพิ่ม -->
    <form method="post" action="{{ url_for('add') }}">
        <input type="text" name="nickname" placeholder="ชื่อเล่น" required>
        <input type="text" name="favorite_food" placeholder="ชอบกิน">
        <input type="text" name="favorite_color" placeholder="ชอบสี">
        <input type="text" name="instagram" placeholder="ชื่อไอจี">
        <input type="submit" value="เพิ่มกิ๊ก">
    </form>

    <!-- ฟอร์มค้นหา -->
    <form method="get" action="{{ url_for('index') }}">
        <input type="text" name="search" placeholder="ค้นหาชื่อกิ๊ก..." value="{{ search_query }}">
        <input type="submit" value="ค้นหา">
        {% if search_query %}
            <a href="{{ url_for('index') }}">❌ ล้างการค้นหา</a>
        {% endif %}
    </form>

    <!-- ตาราง -->
    <table>
        <tr>
            <th>ชื่อเล่น</th>
            <th>ชอบกิน</th>
            <th>ชอบสี</th>
            <th>ชื่อไอจี</th>
            <th>จัดการ</th>
        </tr>
        {% for row in giks %}
        <tr>
            <td>{{ row["nickname"] }}</td>
            <td>{{ row["favorite_food"] }}</td>
            <td>{{ row["favorite_color"] }}</td>
            <td>{{ row["instagram"] }}</td>
            <td>
                <a href="{{ url_for('edit', id=row['id']) }}">แก้ไข</a> | 
                <a href="{{ url_for('delete', id=row['id']) }}" onclick="return confirm('ยืนยันการลบกิ๊กคนนี้?')">ลบ</a>
            </td>
        </tr>
        {% endfor %}
    </table>

    {% if edit_item %}
    <h2>✏️ แก้ไขข้อมูลกิ๊ก</h2>
    <form method="post" action="{{ url_for('update', id=edit_item['id']) }}">
        <input type="text" name="nickname" value="{{ edit_item['nickname'] }}" required>
        <input type="text" name="favorite_food" value="{{ edit_item['favorite_food'] }}">
        <input type="text" name="favorite_color" value="{{ edit_item['favorite_color'] }}">
        <input type="text" name="instagram" value="{{ edit_item['instagram'] }}">
        <input type="submit" value="บันทึกการแก้ไข">
    </form>
    {% endif %}
</body>
</html>
"""

# ---------- Routes ----------
@app.route("/")
def index():
    search_query = request.args.get("search", "").strip()
    if search_query:
        filtered = [g for g in giks if search_query.lower() in g["nickname"].lower()]
    else:
        filtered = giks
    return render_template_string(template, giks=filtered, edit_item=None, search_query=search_query)

@app.route("/add", methods=["POST"])
def add():
    global next_id
    giks.append({
        "id": next_id,
        "nickname": request.form["nickname"],
        "favorite_food": request.form.get("favorite_food", ""),
        "favorite_color": request.form.get("favorite_color", ""),
        "instagram": request.form.get("instagram", "")
    })
    next_id += 1
    return redirect(url_for("index"))

@app.route("/edit/<int:id>")
def edit(id):
    edit_item = next((g for g in giks if g["id"] == id), None)
    return render_template_string(template, giks=giks, edit_item=edit_item, search_query="")

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    for g in giks:
        if g["id"] == id:
            g["nickname"] = request.form["nickname"]
            g["favorite_food"] = request.form.get("favorite_food", "")
            g["favorite_color"] = request.form.get("favorite_color", "")
            g["instagram"] = request.form.get("instagram", "")
            break
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    global giks
    giks = [g for g in giks if g["id"] != id]
    return redirect(url_for("index"))

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)

