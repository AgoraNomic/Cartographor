# Copyright (C) 2018, CodeTriangle
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#       
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#       
#     * Neither the name of CodeTriangle nor the names of other
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL CODETRIANGLE BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

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
