def name2groupname(name):
    res = name.rsplit(".", 1)
    if len(res) == 1:
        return "global", name
    else:
        return res[0], res[1]
