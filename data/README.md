This folder stores all the data that is used to generate maps.

## changes.json syntax description

changes.json contains a list. This list tracks every change made to the map. Each change is also formatted as a list with the syntax:

    ["command", {"arg1": "x", "arg2": "y"}]

Here's a list of commands and their arguments:

### track

The `track` command adds an attribute to each square of the table.

Arguments:

- `"name"` is the string that will be used to refer to it.
- `"default"` is the default value of the attribute.
- `"display"` *(optional)* is the name that will be used in rendered HTML and TXT.

### untrack

The `untrack` command stops tracking the attribute.

Arguments:

- `"name"` is the name of the variable to stop tracking.

### set

The `set` command changes the value of the attribute in a square.

Arguments:

- `"coords"` is a list containing the latitude then the longitude coordinates of the square to change.
- After that all the arguments are a pair of an attribute name, then the value to set it to.