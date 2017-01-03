fobj = open("data_lidar.txt")
for lin in fobj:
    # lin = x.readline()
    # print lin
    lin = lin.split()
    lin.insert(1,',')
    lin.insert(3, ':')
    lin.insert(5, ';')
    lin.insert(7, '.')


    print ''.join(lin)
    # print
    # print "and"
    # print fobj.readline()
fobj.close()