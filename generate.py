import json
from datetime import datetime as dt

# get the date for the generated html file name
date = dt.now().date()

# function to get the contents of a file
def get_contents(fn):
    with open(fn) as f:
        return f.read()

html = get_contents("template.html") # get the template file
changes = [i for i in json.loads(get_contents("data/changes.json")) if type(i) != type("")] # get all recorded changes

table_html = "" # this contains html code that will be injected into the file
table_data = [] # this will contain dictionaries that describe each square

# prepares the table_html and table_data variables with 19x19 grids filled with default values
for row in range(-9, 10):
    table_html += "    <tr class='row' id='r%d'>\n      " % row
    table_data.append([])
    for col in range(-9, 10):
        table_html += "<td class='cell' id='r%dc%d' onmouseover='getStats(%d, %d)'\n      ></td>" % (row, col, col, row)
        table_data[row+9].append({})
    table_html += "</tr>\n"

to_track = [] # this will store all the values we want to track, as set by the "track" command.
defaults = {} # this will hold the default values of the values in to_track.

# uses data/changes.json to update the map to its current state
for change in changes:
    command = change[0]
    args = change[1]
    if command == "track":
        to_track.append(args["name"])
        defaults[args["name"]] = args["default"]
    
    elif command == "set":
        row = args["coords"][0]+9
        col = args["coords"][1]+9
        for attr, value in args.items():
            if attr != "coords":
                table_data[row][col][attr] = value

# add values that are still default
for row in table_data:
    for col in row:
        for attr in to_track:
            try: col[attr]
            except KeyError: col[attr] = defaults[attr]

table_list = table_html.split("\n") # get a list of lines to make searching easier
cell_list = [i-1 for i, j in enumerate(table_list) if j.find("</td>") != -1] # get the numbers of the lines we want to add to

# generate html for table 
for row, i in enumerate(table_data):
    for col, j in enumerate(i):
        for attr, k in j.items():
            table_list[cell_list[row*19+col]] += " %s='%s'" % (attr, k)

# add the generated table html to the template
table_html = "\n".join(table_list)
html = html.replace("{{tabledata}}", table_html)

# add the values we're tracking to the template.
# this method allows us to change which attributes we want to track simply by editing data/defaults.json.
to_track = []
for attr, value in defaults.items(): to_track.append(attr)
html = html.replace("{{attributes}}", str(to_track))

with open("maps/map-%s.html" % (date.isoformat()), "w") as f:
    f.write(html)