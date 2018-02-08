import json
from datetime import datetime as dt

date = dt.now().date()

def get_contents(fn):
    with open(fn) as f:
        return f.read()

html = get_contents("template.html")
table_data = json.loads(get_contents("data/map.json"))

table_html = ""

for i in range(0, 9):
    table_html += "    <tr class='row' id='r%d'>\n      " % (i)
    for j in range(0, 9):
        table_html += "<td class='cell' id='r%dc%d' onmouseover='getStats(%d, %d)'\n      ></td>" % (i, j, j, i)
    table_html += "</tr>\n"

table_list = table_html.split("\n")
cell_list = [i-1 for i, j in enumerate(table_list) if j.find("</td>") != -1]

for attr, i in table_data.items():
    for row, j in enumerate(i):
        for col, k in enumerate(j):
            table_list[cell_list[row*9+col]] += " %s='%s'" % (attr, k)

table_html = "\n".join(table_list)

html = html.replace("{{tabledata}}", table_html)

with open("maps/map-%s.html" % (date.isoformat()), "w") as f:
    f.write(html)