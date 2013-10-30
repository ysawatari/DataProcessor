# coding=utf-8
"""@dataprocessor
"""
import json
import pipes


class DataProcessorError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class InvalidJSONError(Exception):
    def __init__(self, name, msg):
        self.name = name
        self.msg = msg

    def __str__(self):
        return "while processing pipe[%s]: %s" % (self.name, self.msg)


def execute(manip):
    """
    execute pipeline
    """
    # TODO write doctest
    run_list = []
    for mn in manip:
        name = mn["name"]
        if name not in pipes.pipes_dics:
            raise InvalidJSONError(name, "invalid pipe name")
        dic = pipes.pipes_dics[name]
        if len(mn["args"]) != len(dic["args"]):
            raise InvalidJSONError(name, "The number of arguments mismatches")
        if "kwds" in mn and "kwds" in dic:
            kwds = {}
            for kwd in mn["kwds"]:
                if kwd not in dic["kwds"]:
                    continue
                kwds[kwd] = mn["kwds"][kwd]
            run_list = dic["func"](run_list,*mn["args"],**kwds)
        else:
            run_list = dic["func"](run_list,*mn["args"])
    return run_list


def execute_from_json_str(manip_json_str):
    manip = json.loads(manip_json_str)
    execute(manip)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
