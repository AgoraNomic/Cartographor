class Table:

    data = [] # holds the objects that describe the map
    attrs = [] # holds the attributes we need to track

    alttype = "b" # set the first alternating type. we want it to be black

    # the bounds of the map, in the game-specified coordinate system
    min_lat = 0
    min_lon = 0
    max_lat = 0
    max_lon = 0

    # use this to track an attribute with the fractal "track" command
    def track(self, name, args):
        args["name"] = name # add the name to the list of arguments

        # set the display name to the name if no display name is specified
        try: args["display"]
        except: args["display"] = name

        self.attrs.append(args) # add this to the attrs list

    # use this to stop tracking an attribute
    def untrack(self, name):
        self.attrs = [attr for attr in self.attrs if attr["name"] != name] # remove this attribute from the attrs list

        # get rid of all occurances of this attribute
        for row in self.data:
            for col in row:
                try: col.pop(name)
                except: pass

    # use this to change the properties of a land unit
    def set(self, unit, args):
        # get the position for use in indices
        row = int(unit[0])-min_lat
        col = int(unit[1])-min_lon
        
        # handle alternating land types
        try:
            if args["type"] == "x":
                args["type"] = alttype
                if alttype == "b": alttype = "w"
                else: alttype = "b"
        except: pass

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
        try: min_lat = int(args["min_lat"])
        except: pass
        try: min_lon = int(args["min_lon"])
        except: pass
        try: max_lat = int(args["max_lat"])
        except: pass
        try: max_lon = int(args["max_lon"])
        except: pass

        # convert the latitute and longitude into indices
        max_row = max_lat - min_lat + 1
        max_col = max_lon - min_lon + 1

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

    def register(self, name, args):
        args["name"] = name # add the player's name to the dict

        # set full name if specified
        try: args["full"]
        except KeyError: args["full"] = name

        # set location if specified
        try: args["location"]
        except KeyError: args["location"] = "0 0"

        self.players.append(args) # add the object to the list of players
