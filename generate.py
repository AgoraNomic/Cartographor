from datetime import datetime as dt
from re import sub
from cart import table

date = dt.now().date() # get the date for the generated html file name

# get all recorded changes
changefile = ""
with open("data/changes.fr") as f: changefile = f.read()

t = table.Table()
t.update(changefile)
t.fill_table()

table_html = "" # this contains html code that will be injected into the file

# populates table_html
for i, row in enumerate(t.data):
    lat = t.to_lat(i)
    table_html += "    <tr class='row' id='r%d'>\n      " % lat
    for j, col in enumerate(row):
        lon = t.to_lon(j)
        table_html += "<td class='cell' id='r%dc%d' onclick='getStats(%d, %d)'\n      ></td>" % (lat, lon, lon, lat)
    table_html += "</tr>\n"

table_list = table_html.split("\n") # get a list of lines to make searching easier
cell_list = [i-1 for i, j in enumerate(table_list) if j.find("</td>") != -1] # get the numbers of the lines we want to add to

# generate html for table 
for i, row in enumerate(t.data):
    for j, col in enumerate(row):
        for k, attr in col.items():
            table_list[cell_list[i*t.width+j]] += " %s='%s'" % (k, attr)

player_html = ""

# generate player list
for i, player in t.players.items():
    player_lat, player_lon = player["location"].split()
    player_html = "%s%s: (%s, %s)<br>" % (player_html, player["full"], player_lat, player_lon)

# get the template file
html = ""
with open("template.html") as f: html = f.read()

# add the generated table html to the template
table_html = "\n".join(table_list)
html = html.replace("{{tabledata}}", table_html)

# add the generated player list html
html = html.replace("{{players}}", player_html)

# add the values we're tracking to the template
html = html.replace("{{attributes}}", str([i for i,j in t.attrs.items()]))
html = html.replace("{{dispnames}}", str([j["display"] for i,j in t.attrs.items()]))

# add dates
html = html.replace("{{date}}", date.isoformat())

with open("maps/map-%s.html" % (date.isoformat()), "w") as f:
    f.write(html)
