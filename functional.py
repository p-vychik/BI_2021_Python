def sequential_map(*args):
    # with func_chain
    funcs = func_chain(*args[:-1])
    container = list(map(funcs, args[-1]))
    return container

    # without func_chain, to check comment lines above
    for i in range(len(args)-1):
        container = list(map(args[i], args[-1]))
    return container


def consensus_filter(*args):
    container = args[-1]
    out = []
    for val in container:
        if all([args[func](val) for func in range(len(args) - 1)]):
            out.append(val)
    return out


def conditional_reduce(filter_func, func, container):
    filtered_container = list(filter(filter_func, container))
    result = filtered_container[0]
    for val in range(1, len(filtered_container)):
        result = func(result, filtered_container[val])
    return result


def func_chain(*args):
    def out(v):
        result = args[0](v)
        for i in range(1, len(args)):
            result = args[i](result)
        return result

    return out
