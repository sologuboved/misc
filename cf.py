def show_contents(source_filename1, source_filename2, target_filename=None):

    def compare_contents():

        with open(source_filename1) as source_handler1, open(source_filename2) as source_handler2:

            if target_filename:
                num = 0
                for line1, line2 in zip(source_handler1.readlines(), source_handler2.readlines()):
                    num += 1
                    n = len(str(num)) + 6
                    if line1 != line2:
                        target_handler.write("Line " + str(num) + " " + line1 + " " * n + line2)
            else:
                for line1, line2 in zip(source_handler1.readlines(), source_handler2.readlines()):
                    if line1 != line2:
                        print
                        print line1
                        print line2
                        break
                else:
                    print "are the same"

    if target_filename:
        with open(target_filename, 'w') as target_handler:
            compare_contents()
    else:
        compare_contents()


if __name__ == '__main__':
    # show_contents('varsd1.txt', 'varsd2.txt', target_filename='varsd0.txt')
    # show_contents('varsd1.txt', 'varsd2.txt')
    pass
