from cart import fractal, initials
from hashlib import sha1

class Table:

    data = [] # holds the objects that describe the map
    attrs = {} # holds the attributes we need to track
    players = {} # holds the list of players

    alttype = "b" # set the first alternating type. we want it to be black

    # the bounds of the map, in the game-specified coordinate system
    min_lat = 0
    min_lon = 0
    max_lat = 0
    max_lon = 0

    # dimensions of the map
    width = 0
    height = 0

    # for converting between incices and latitudes
    def to_row(self, lat): return lat - self.min_lat
    def to_col(self, lon): return lon - self.min_lon
    def to_lat(self, row): return row + self.min_lat
    def to_lon(self, col): return col + self.min_lon

    # use this to track an attribute with the fractal "track" command
    def track(self, name, args):
        # set the display name to the name if no display name is specified
        try: args["display"]
        except: args["display"] = name

        self.attrs[name] = args # add this to the attrs list

    # use this to stop tracking an attribute
    def untrack(self, name):
        self.attrs.pop(name) # remove this attribute from the attrs list

        # get rid of all occurances of this attribute
        for row in self.data:
            for col in row:
                try: col.pop(name)
                except: pass

    # use this to change the properties of a land unit
    def set(self, lat, lon, args):
        # get the position for use in indices
        row = self.to_row(int(lat))
        col = self.to_col(int(lon))
        
        # handle alternating land types
        try:
            if args["type"] == "x":
                args["type"] = self.alttype
                if self.alttype == "b": self.alttype = "w"
                else: self.alttype = "b"
        except KeyError: pass

        # set the attributes of the land unit specified by the unit variable
        for attr, value in args.items():
            self.data[row][col][attr] = value

        # aether destroys everything and sends it back to Agora
        try:
            if args["type"] == "a":
                self.data[row][col] = {}
        except: pass

    def resize(self, args):
        # get all the arguments
        try: self.min_lat = int(args["min_lat"])
        except: pass
        try: self.min_lon = int(args["min_lon"])
        except: pass
        try: self.max_lat = int(args["max_lat"])
        except: pass
        try: self.max_lon = int(args["max_lon"])
        except: pass

        # convert the latitute and longitude into indices
        max_row = self.max_lat - self.min_lat + 1
        max_col = self.max_lon - self.min_lon + 1

        self.width = max_col
        self.height = max_row

        # create empty cells if they do not already exist
        # also trim excess cells
        self.data = self.data[:max_row]
        for row in range(max_row):
            try: self.data[row]
            except: self.data.append([])
            self.data[row] = self.data[row][:max_col]
            for col in range(max_col):
                try: self.data[row][col]
                except: self.data[row].append({})

    def update_initials(self):
        pi = initials.create_initials([i for i, j in self.players.items()])

        for name, player in self.players.items():
            player["initial"] = pi[name]


    def register(self, name, args):
        # set full name if specified
        try: args["full"]
        except KeyError: args["full"] = name

        # set location if specified
        try: args["location"]
        except KeyError: args["location"] = "0 0"

        try: args["color"]
        except KeyError: args["color"] = "#" + sha1(bytes(args["full"], "utf-8")).hexdigest()[0:6]

        self.players[name] = args # add the object to the list of players

        self.update_initials()

    def deregister(self, name):
        self.players.pop(name)

        self.update_initials()

    def move(self, name, to):
        self.players[name]["location"] = to

    def update(self, change_str):
        changes = fractal.load(change_str)
        for change in changes:
            command, pargs, args = change

            if command == "track": self.track(pargs[0], args)
            elif command == "untrack": self.untrack(pargs[0])
            elif command == "set": self.set(*pargs[0].split(), args)
            elif command == "resize": self.resize(args)
            elif command == "register": self.register(pargs[0], args)
            elif command == "deregister": self.deregister(pargs[0])
            elif command == "move": self.move(pargs[0], args["to"])
            else: pass

    def fill_cell(self, lat, lon):
        cell = self.data[self.to_row(lat)][self.to_row(lon)]
        for key, attr in self.attrs.items():
            try: cell[key]
            except KeyError: cell[key] = attr["default"]

    def fill_table(self):
        for i, row in enumerate(self.data):
            for j, col in enumerate(row):
                self.fill_cell(self.to_lat(i), self.to_lon(j))
