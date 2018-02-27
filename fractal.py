def load(str):

    active_batches = []
    
    list = [arg.split(":") for arg in str.split("\n")]

    data = []

    for line in list:
        indent_level = line[0].count("\t")
        line_data = []
        try: line_data = [arg.split() for arg in line[0].split(",")]
        except IndexError: pass
        try: line_data = [
            *line_data,
            {arg.split()[0]: " ".join(arg.split()[1:]) for arg in line[1].split(",")}
        ]
        except IndexError: pass

        for i in range(indent_level, len(active_batches)): active_batches.pop()

        if line_data[0][0] == "batch":
            active_batches.append([line_data[0][1:], line_data[1]])
        else:
            for batch in active_batches:
                try: line_data = [*line_data[:-1], *batch[0], {**line_data[-1], **batch[1]}]
                except TypeError: line_data = [*line_data, *batch[0], {**batch[1]}]
            data.append(line_data)

    return(data)