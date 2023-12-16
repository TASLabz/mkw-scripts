def find_index(value, value_list):
    """Find the index i so value_list[i]>=value>value_list[i+1]
        We suppose value_list[i+1] < value_list[i]
            and value_list[0]>= value>=value_list[-1]"""
    n = len(value_list)
    if n == 1 :
        return 0
    h = n//2
    if value <= value_list[h]:
        return h+find_index(value, value_list[h:])
    return find_index(value, value_list[:h])
