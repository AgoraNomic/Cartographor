from datetime import datetime as dt
from re import sub
import fractal

# get the date for the generated html file name
date = dt.now().date()

# function to get the contents of a file
def get_contents(fn):
    with open(fn) as f:
        return f.read()

html = get_contents("template.html") # get the template file
changes = [i for i in fractal.load(get_contents("data/changes.fr")) if type(i) != type("")] # get all recorded changes

table_html = "" # this contains html code that will be injected into the file
table_data = [] # this will contain dictionaries that describe each square

attrs = [] # this will store all the values we want to track, as set by the "track" command
players = []

alttype = "b"

# these are the lowest possible latitude and longitude values.
min_lat = 0
min_lon = 0
max_lat = 0
max_lon = 0

# generates single-letter strings from a list for labeling.
def create_initials(long_names):
    long_names = [str(i) for i in long_names]
    initials = {}
    for name in long_names:
        name = sub(r"[*. ]", "", name)
    long_names.sort(key=len)
    for name in long_names:
        index = 0
        found = False
        while found == False:
            for i,initial in initials.items():
                if name[index] == initial:
                    index +=1
                    break
            else:
                initials[name] = name[index]
                found = True
    return initials

# uses data/changes.fr to update the map to its current state
for change in changes:
    try: command, pargs, args = change
    except ValueError: command, args = change
    
    if command == "track":
        args["name"] = pargs[0]
        try: args["display"]
        except KeyError: args["display"] = pargs[0]
        attrs.append(args)
    
    elif command == "untrack":
        attrs = [i for i in attrs if i["name"] != pargs[0]]
        for row in table_data:
            for col in row:
                try: col.pop(pargs[0])
                except KeyError: pass
        
    elif command == "set":
        row = int(pargs[0])-min_lat
        col = int(pargs[1])-min_lon
        try:
            if args["type"] == "x":
                args["type"] = alttype
                if alttype == "b": alttype = "w"
                else: alttype = "b"
        except: pass
        for attr, value in args.items():
            table_data[row][col][attr] = value
        try:
            if args["type"] == "a":
                table_data[row][col] = {}
        except: pass

    elif command == "resize":
        try: min_lat = int(args["min_lat"])
        except: pass
        try: min_lon = int(args["min_lon"])
        except: pass
        try: max_lat = int(args["max_lat"])
        except: pass
        try: max_lon = int(args["max_lon"])
        except: pass
        
        max_row = max_lat - min_lat + 1
        max_col = max_lon - min_lon + 1

        table_data = table_data[:max_row]
        for row in range(max_row):
            try: table_data[row]
            except: table_data.append([])
            table_data[row] = table_data[row][:max_col]
            for col in range(max_col):
                try: table_data[row][col]
                except: table_data[row].append({})

    elif command == "register":
        args["name"] = pargs[0]
        try: args["full"]
        except KeyError: args["full"] = pargs[0]
        try: args["location"]
        except KeyError: args["location"] = "0 0"
        players.append(args)

    elif command == "deregister":
        players = [i for i in players if i["name"] != pargs[0]]

    elif command == "move":
        for player in players:
            if player["name"] == pargs[0]:
                player["location"] = args["to"]

# add values that are still default
for row in table_data:
    for col in row:
        for attr in attrs:
            name = attr["name"]
            try: col[name]
            except KeyError: col[name] = attr["default"]

# populates table_html
for row, i in enumerate(table_data):
    lat = row + min_lat
    table_html += "    <tr class='row' id='r%d'>\n      " % lat
    for col,j in enumerate(i):
        lon = col + min_lon
        table_html += "<td class='cell' id='r%dc%d' onclick='getStats(%d, %d)'\n      ></td>" % (lat, lon, lon, lat)
    table_html += "</tr>\n"

table_list = table_html.split("\n") # get a list of lines to make searching easier
cell_list = [i-1 for i, j in enumerate(table_list) if j.find("</td>") != -1] # get the numbers of the lines we want to add to

# generate html for table 
for row, i in enumerate(table_data):
    for col, j in enumerate(i):
        for attr, k in j.items():
            table_list[cell_list[row*(max_lon-min_lon+1)+col]] += " %s='%s'" % (attr, k)

player_html = ""

# generate player list
for player in players:
    player_lat, player_lon = player["location"].split()
    player_html = "%s%s: (%s, %s)<br>" % (player_html, player["full"], player_lat, player_lon)

# add the generated table html to the template
table_html = "\n".join(table_list)
html = html.replace("{{tabledata}}", table_html)

# add the generated player list html
html = html.replace("{{players}}", player_html)

# add the values we're tracking to the template
html = html.replace("{{attributes}}", str([j["name"] for i,j in enumerate(attrs)]))
html = html.replace("{{dispnames}}", str([j["display"] for i,j in enumerate(attrs)]))

# add dates
html = html.replace("{{date}}", date.isoformat())

with open("maps/map-%s.html" % (date.isoformat()), "w") as f:
    f.write(html)
