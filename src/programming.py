import sys

def identify_unique_pairs(input_list):
    unique_pairs = []
    input_list_copy = input_list.copy()
    for i in input_list_copy:
        input_list_copy = input_list.copy()
        input_list_copy.remove(i)

        for c in input_list_copy:
            pair = None
            if i < c:
                pair = (i,c)
            elif i > c:
                pair = (c,i)

            if (pair is not None) and (pair not in unique_pairs):
                unique_pairs.append(pair)
    return unique_pairs
            

def count_pairs(input_list, min_diff, max_diff):
    count = 0
    unique_pairs = identify_unique_pairs(input_list)

    for u in unique_pairs:
            diff = u[1] - u[0]
            if diff >= min_diff and diff <= max_diff:
                count += 1
    return count

if __name__ == "__main__":
    input_list = [int(i) for i in sys.argv[1].split(",")]
    min_diff = int(sys.argv[2])
    max_diff = int(sys.argv[3])
    print(f"input_list: {input_list}, min_diff: {min_diff}, max_diff: {max_diff}")
    print(f"function output: {count_pairs(input_list, min_diff, max_diff)}")
    #print(f"function output: {identify_unique_pairs(input_list)}")
