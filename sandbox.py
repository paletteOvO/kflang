def patternMatch(matching, lst):
    # f((1 ?x 3), (1 2 3)), x => 2
    # f((1 (1 ?x 3) 3), (1 (1 2 3) 3)) => (1 f((1 ?x 3), (1 2 3)) 3)
    l1 = len(matching)
    l2 = len(lst)
    if l1 != l2:
        return False
    res = {}
    for i in range(0, l1):
        if isinstance(matching[i], str):
            if matching[i][0] == "?":
                res[matching[i][i:]] = lst[i]
            elif matching[i] != lst[i]:
                return False
        elif isinstance(lst[i], list):
            x = patternMatch(matching[i], lst[i])
            if x:
                res.update(x)
            else:
                return False
        elif matching[i] != lst[i]:
            return False
    return res or True