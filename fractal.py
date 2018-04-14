def load(str):

    batches = []

    # split the file into lines, then sides.
    list = [arg.split(":") for arg in str.split("\n")]

    # this will hold json code.
    data = []

    for line in list:
        indent_level = line[0].count("\t") # necessary for batches.
        line_data = [] # holds json for individual lines.
        
        try: line_data = [" ".join(arg.split()) for arg in line[0].split(",")] # split left side into arguments, then individual words.
        except IndexError: pass

        line_data = [
            line_data[0].split(" ").pop(0),
            [" ".join(line_data[0].split(" ")[1:]), *line_data[1:]]
        ]
        
        try: line_data = [
            *line_data,
            {arg.split()[0]: " ".join(arg.split()[1:]) for arg in line[1].split(",")}
        ]
        except IndexError:
            line_data = [*line_data, {}]

        for i in range(indent_level, len(batches)): batches.pop()

        if line_data[0] == "batch":
            batches.append([line_data[1], line_data[2]])
        else:
            for batch in batches:
                try: line_data = [line_data[0], [*batch[0], *line_data[1]], {**line_data[2], **batch[1]}]
                except IndexError: line_data = [line_data[0], [*batch[0], *line_data[1]], {**batch[1]}]
            data.append(line_data)

    return(data)