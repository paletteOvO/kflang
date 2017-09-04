k = [7, [6, [1, 2, 3], [4, 5]]]

nodes_to_visit = [k]
res = []
while k:
    nodes_to_visit = list(filter(lambda i: isinstance(i, list), nodes_to_visit))
    if isinstance(currentnode, list):
        currentnode.reverse()
        nodes_to_visit.reverse()
        nodes_to_visit.extend(currentnode)
        nodes_to_visit.reverse()
    else:
        print(currentnode)