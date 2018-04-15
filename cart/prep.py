from cart import table

# this function gets the entire up-to-date map and returns a table object describing it

def get_current_map():
    # get all recorded changes
    changefile = ""
    with open("data/changes.fr") as f: changefile = f.read()

    # make a new Table object and fill in the changes and defaults
    t = table.Table()
    t.update(changefile)
    t.fill_table()

    return t