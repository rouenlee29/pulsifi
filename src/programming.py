import sys

def identify_unique_pairs(input_list):
    unique_sets = []
    for i in input_list:
        input_list_copy = input_list.copy()
        input_list_copy.remove(i)
        for c in input_list_copy:
            #print(f"i: {i}, c: {c}")
            if i < c:
                pair = (i,c)
                unique_sets.append((i,c))
            else:
                pair = (c,i)
            if pair not in unique_sets:
                unique_sets.append(pair)
    print(unique_sets)
            


def count_pairs(input_list, min_diff, max_diff):
    count = 0
    input_list_copy = input_list.copy()
    for i in input_list:
        print(input_list_copy)
        input_list_copy.remove(i)
        
        for c in input_list_copy:
            print(f"i: {i}, c: {c}")
            diff = abs(c-i)
            if diff >= min_diff and diff <= max_diff:
                count += 1
    return count

if __name__ == "__main__":
    input_list = [int(i) for i in sys.argv[1].split(",")]
    min_diff = int(sys.argv[2])
    max_diff = int(sys.argv[3])
    print(f"input_list: {input_list}, min_diff: {min_diff}, max_diff: {max_diff}")
    #print(f"function output: {count_pairs(input_list, min_diff, max_diff)}")
    print(f"function output: {identify_unique_pairs(input_list)}")
