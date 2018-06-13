# generates single-letter strings from a list for labeling.
# TODO: add some sort of fail case.
def create_initials(long_names):
    initials = {}
    long_names.sort(key=len)
    for name in long_names:
        index = 0
        found = False
        while found == False:
            for i,initial in initials.items():
                if name[index] == initial:
                    index += 1
                    break
            else:
                initials[name] = name[index]
                found = True
    return initials
