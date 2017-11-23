import json

def get_contents(fn):
    with open(fn) as f:
        return f.read()

html = get_contents("template.html")
table_data = json.loads(get_contents("data/map.json"))

table_html = ""

for i, o in enumerate(table_data):
    table_html += "    <tr class='row' id='r%d'>\n" % (i)
    for j, p in enumerate(o):
        table_html += "      <td class='cell %s' id='r%dc%d'></td>\n" % (p, i, j)
    table_html += "    </tr>\n"

html = html.replace("{{tabledata}}", table_html)

with open("map.html", "w") as f:
    f.write(html)