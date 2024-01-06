def write():

    file="./result.txt"
    f1=open(file,'r')
    data=[]
    addr=str(0)
    for line in f1.readlines():
        for i in line.split():
            data.append(int(i))
            if len(data)==14:
                data.append(str(int(addr)+1))
                filename = "./rblks/%s.blk" % addr
                f = open(filename, 'w')
                f.writelines(str(data[i])+' ' for i in range(len(data)))
                addr=str(int(addr)+1)
                data=[]
                f.close()
    if len(data)!=0:
        filename = "./rblks/%s.blk" % addr
        f = open(filename, 'w')
        f.writelines(str(data[i]) + ' ' for i in range(len(data)))
        f.close()


if __name__ == '__main__':
    write()


