def delete(input_dict, search):

    if type(search) == list:
        for path in search:
            input_dict = delete(input_dict, path)
    else:

        # Remove whole dict
        if search == ".":
            return {}

        # String begins with a dot
        if search.startswith("."):
            search = search[1:]

        # get cur_search and next
        if "." in search:
            cur_search = search[0:(search.index("."))]
            next_search = search[(search.index(".") + 1):]
        else:
            cur_search = search
            next_search = ""

        # if exists in dict
        if cur_search.isdigit():
            cur_search = int(cur_search)

        if isinstance(input_dict, dict) or isinstance(input_dict, list):
            if  cur_search in input_dict:
                # last object = to delete
                if not next_search:
                    if type(input_dict) == list:
                        input_dict.remove(cur_search)
                    else:
                        input_dict.pop(cur_search)
                # delete sub-object
                else:
                    delete(input_dict[cur_search], next_search)

    return input_dict
