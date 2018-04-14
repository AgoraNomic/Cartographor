def load(str):

    batches = []

    # split the file into lines, then sides.
    line_list = [arg.split(":") for arg in str.split("\n")]

    # this will hold json code.
    data = []

    for line in line_list:
        indent_level = line[0].count("\t") # necessary for batches.
        line_data = [] # holds json for individual lines.
        
        try: line_data = [" ".join(arg.split()) for arg in line[0].split(",")] # split left side into arguments, then individual words.
        except IndexError: pass

        left = line_data[0].split(" ")

        if len(left) == 1: line_data = [left[0], []]
        else: line_data = [
            left.pop(0),
            [" ".join(left), *line_data[1:]]
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
                line_data = [line_data[0], [*batch[0], *line_data[1]], {**batch[1], **line_data[2]}]
            data.append(line_data)

    return(data)