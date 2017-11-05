"""1st file is current, 
2nd and 3rd files are for comparison, 
!!!!in the 4th file the results will be written,
so BE CAREFUL WITH IT -
the original contens will be deleted!!!!
""" 

from sys import argv
file0, file1, file2, file3 = argv

result = open(file3, 'w')

number = 0

for line1, line2 in zip(open(file1).readlines(), open(file2).readlines()):
    number += 1
    n = len(str(number)) + 6
    if line1 != line2:
        result.write("Line " + str(number) + " " + line1 + " " * n + line2) 