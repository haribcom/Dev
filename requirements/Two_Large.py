def two_largest(input3):
    """ Two Largest Numbers"""
    largest = 0
    second_largest = 0
    for item in input3:
        if item > largest:
            second_largest=largest
            largest = item
        elif largest > item > second_largest:
            second_largest = item
    input2 = len([largest,second_largest])
    print("input2 :",input2)
    print("input3 :",largest,second_largest)
    print('sum :',sum([largest , second_largest]))


if __name__ == "__main__":
    print("Marathon Drive")
    input1 = int(input("enter candidates to attend:"))
    input3 = []
    for i in range(input1):
        input3.append(int(input("enter scores:")))
    print("input1 :",input1)
    two_largest(input3)
    print(input3)