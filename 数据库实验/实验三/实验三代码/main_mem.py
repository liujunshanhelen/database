

class R:
    def __init__(self,a,b):
        self.f=a
        self.s=b
class S:
    def __init__(self,c,d):
        self.f=c
        self.s=d
import extmem
import random
from PyQt5.QtWidgets import QApplication, QMainWindow
import mem
import sys

#生成数据：编写程序，随机生成关系R和S，使得R中包含16 * 7 = 112个元组，S中包含32 * 7 = 224个元组。
def randomR(r,s):
    for i in range(112):
        r.append(R(random.randint(1, 40), random.randint(1, 1000)))

    for i in range(224):
        s.append(S(random.randint(20, 60), random.randint(1, 1000)))


def writetodisk(relation,blk,addr):
    for i in range(blk):
        blk_num = buffer.getNewBlockInBuffer()  # 申请一个块
        data = []
        for j in range(7):
            data.extend([str(relation[i * 7 + j].f), str(' '), str(relation[i * 7 + j].s),
                         str(' ')])
        data.append(str(addr + 1))
        if i == blk - 1:
            data[-1] = str(0)
        buffer.data[blk_num].append(data)
        if not buffer.writeBlockToDisk(addr, blk_num):
            print("写入磁盘文件号 %s 失败" % addr)
            exit()
        addr += 1
    return addr
    # for i in range(blk):
    #    buffer_blk=Buffer.getNewBlockInBuffer()
    #    data=[]
    #    for j in range(7):
    #         data.extend([relation[i*7+j].f,str(' '),relation[i*7+j].s,str(' ')])
    #    data.append(str(addr+1))
    #    if i==blk-1:
    #        data[-1]=str(0)
    #    Buffer.data[buffer_blk].append(data)
    #    if not Buffer.writeBlockToDisk(addr, buffer_blk):
    #        print("写入磁盘文件号 %s 失败" % addr)
    #        exit()
    #    addr+=1
    # return addr
# def select(select1,select2,num,addr,ui):
#     ui.log.clear()
#     if select1=="R" and select2=="A" or select1=="S" and select2=="C":
#         index=0
#     if select1=="R" and select2=="B" or select1=="S" and select2=="D":
#         index=1
#     if select1=="R":
#         begin_num=0
#     else:
#         begin_num=16
#
#     data=[]
#     while True:
#         index_1=Buffer.readBlockFromDisk(begin_num)
#         ui.log.append(str(begin_num))
#         read_data=Buffer.data[index_1][1]
class RelationSelectionAlgorithm:
    @staticmethod
    def selection_linear(relation, attribute, value, addr,ui):
        # ui.log.clear()
        ui.res.clear()
        if relation != 'R' and relation != 'S':
            # ui.log.append("名称不正确")
            return addr

        # 看选择的属性是第一个属性还是第二个属性
        if attribute == 'A' and relation == "R" or attribute == 'C' and relation == "S":
            attr_index = 0
        elif attribute == 'B' and relation == "R" or attribute == 'D' and relation == "S":
            attr_index = 1
        else:
            # ui.log.append("属性不正确")
            return addr

        # 首先找到关系的起始文件块号
        relation_start_blk_number = blk_dict[relation]
        present_blk_number = relation_start_blk_number
        data = []  # 保存满足条件的元组，会写入到文件块中
        # write_blk_index = buffer.getNewBlockInBuffer()  # 为选择的数据申请一个缓冲区
        # if write_blk_index == -1:
        #     ui.log.append("缓冲区已满，不能为选择的数据申请一个缓冲区")
        #     return addr
        # buffer.freeBlockInBuffer(write_blk_index)
        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            if index == -1:
                # ui.log.append("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break
            # ui.log.append("读取块"+str(present_blk_number)+"到缓冲区0")
            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 线性搜索
            for i in range(int(number_of_tuple)):

                if int(read_data[i * 2 + attr_index]) == value:
                    data.append([read_data[i * 2], read_data[i* 2 + 1]])
                    ui.res.append(str(read_data[i * 2])+"  "+str(read_data[i * 2 + 1]))

            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # ui.log.append("释放缓冲区0")
            if present_blk_number == '0':
                break

        if len(data) == 0:
       #     print("没有对应的数据")
            return addr

    #    addr = write_data(data, int(ceil(len(data) / 7.0)), 7, addr)
        return addr

class RelationProjectionAlgorithm:
    @staticmethod
    def project(relation, attribute, blk_number,ui):
        ui.res.clear()
        # ui.log.clear()
        if relation != 'R' and relation != 'S':
            print("关系名称错误")
            return blk_number

        # 看选择的属性是第一个属性还是第二个属性
        if attribute == 'A' and relation == "R" or attribute == 'C' and relation =="S":
            attr_index = 0
        elif attribute == 'B' and relation =="R" or attribute == 'D' and relation == "S":
            attr_index = 1
        else:
            # ui.log.append("属性输入错误")
            return blk_number

        # 首先找到关系的起始文件块号
        present_blk_number = blk_dict[relation]
        data = []  # 保存满足条件的元组，会写入到文件块中
        # write_blk_index = buffer.getNewBlockInBuffer()  # 为选择的数据申请一个缓冲区
        # if write_blk_index == -1:
        #     print("缓冲区已满，不能为选择的数据申请一个缓冲区")
        #     return blk_number
        # buffer.freeBlockInBuffer(write_blk_index)

        data1 = []
        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            # ui.log.append("读入块"+str(present_blk_number)+"到缓冲区0")
            if index == -1:
                # ui.log.append("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号
            # 投影
            for i in range(int(number_of_tuple)):
                tmp = read_data[i * 2 + attr_index]

                if tmp not in data1:
                    data.append(tmp)
                    ui.res.append(str(tmp))
                    data1.append(tmp)



            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # ui.log.append("释放缓冲区0")
            if present_blk_number == '0':
                break

        if len(data) == 0:
    #        print("没有对应的数据")
            return blk_number

     #   blk_number = write_data(data, int(ceil(len(data) / 14.0)), 14, blk_number)
        return blk_number



class JoinOperationAlgorithm:
    @staticmethod
    def nest_loop_join(relation_first, relation_second, blk_numbers_of_first, blk_numbers_of_second,
                       blk_number,ui):
        #较小的关系作为外层
        # ui.log.clear()
        ui.res.clear()
        if blk_numbers_of_first > blk_numbers_of_second:
            out_relation = relation_second
            in_relation = relation_first
        else:
            out_relation = relation_first
            in_relation = relation_second

        # 首先找到外层关系的起始文件块号
        out_present_blk_number = blk_dict[out_relation]
        data = []  # 保存满足条件的元组，会写入到文件块中

        while True:
            out_index = buffer.readBlockFromDisk(out_present_blk_number)  # 为关系的数据申请一个缓冲
            # ui.log.append("读入块"+str(out_present_blk_number)+"到缓冲区")
            if out_index == -1:

                break

            out_read_data = buffer.data[out_index][1]  # 从磁盘块中读取的数据
            out_number_of_tuple = (len(out_read_data) - 1) / 2
            out_next_blk_number = out_read_data[-1]  # 文件的后继磁盘块号

            # 首先找到关系的起始文件块号
            in_present_blk_number = blk_dict[in_relation]
            while True:
                #一块外层循环，一块输出，六块内层循环



                in_index = buffer.readBlockFromDisk(in_present_blk_number)

                in_read_data = buffer.data[in_index][1]


                in_number_of_tuple = (len(in_read_data) - 1) / 2


                in_next_blk_number = in_read_data[-1]


                for i in range(int(out_number_of_tuple)):
                    for j in range(int(in_number_of_tuple)):

                        if out_read_data[i * 2] == in_read_data[j * 2]:
                            data.append([int(out_read_data[i * 2]), int(out_read_data[i * 2 + 1]),
                                         int(in_read_data[j * 2 + 1])])
                            ui.res.append(str(out_read_data[i * 2])+"  "+str(out_read_data[i * 2 + 1])+"  "+str(in_read_data[j * 2])+"  "+str(in_read_data[j * 2 + 1]))
                in_present_blk_number = in_next_blk_number
                buffer.freeBlockInBuffer(in_index)
                # ui.log.append("释放缓冲区"+str(in_index))
                if in_present_blk_number == '0':
                    break

            out_present_blk_number = out_next_blk_number
            buffer.freeBlockInBuffer(out_index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # ui.log.append("释放缓冲区"+str(out_index))
            if out_present_blk_number == '0':
                break

        if len(data) == 0:
      #      print("没有对应的数据")
            return blk_number

     #   blk_number = write_data(data, int(ceil(len(data) / 5.0)), 5, blk_number)
        return blk_number


    @staticmethod
    def sort_merge_join(relation_first, relation_second, blk_number,ui):
        ui.res.clear()
        #归并段8个

        first_data = []
        present_blk_number = blk_dict[relation_first]
        # 然后读取第一个关系的数据
        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
        ##    ui.log.append("读入块"+str(present_blk_number)+"到缓冲区")
            if index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break
            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 读取所有的元组
            for i in range(int(number_of_tuple)):
                first_data.append([int(read_data[i * 2]), int(read_data[i * 2 + 1])])
            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # 读完退出
            if present_blk_number == '0':
                break
        second_data = []
        present_blk_number = blk_dict[relation_second]
        # 然后读取第二个关系的数据
        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
    #        ui.log.append("读入块"+str(present_blk_number)+"到缓冲区")


            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 读取所有的元组
            for i in range(int(number_of_tuple)):
                second_data.append([int(read_data[i * 2]), int(read_data[i * 2 + 1])])
            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # 读完退出
            if present_blk_number == '0':
                break
    #    ui.log.append("内存排序")
    #    ui.log.append("写回并清空")
        # sort
       # JoinOperationAlgorithm.logintoui()
        first_data = sorted(first_data, key=lambda t: t[0])
        second_data = sorted(second_data, key=lambda t: t[0])

        # merge
        data = []
        i = 0
        j = 0
        while i < len(first_data) or j < len(second_data):
            if i < len(first_data) and j < len(second_data):
                if first_data[i][0] == second_data[j][0]:
                    ui.res.append(str(first_data[i][0])+"  "+str(first_data[i][1])+"  "+str(second_data[j][0])+"  "+str(second_data[j][1]))
                    # ui.log.append("正处理外关系中的"+str(first_data[i][0]))
                    temp_index = j + 1  # 让第二个关系先移动
                    while temp_index < len(second_data) and first_data[i][0] == \
                            second_data[temp_index][0]:
                        ui.res.append(str(first_data[i][0])+"  "+str(first_data[i][1])+"   "+str(second_data[temp_index][0])+"   "+ str(second_data[temp_index][1]))
                        temp_index += 1
                    i += 1  # 只移动第二个关系不移动第一个关系
                elif first_data[i][0] < second_data[j][0]:
                    i += 1
                elif first_data[i][0] > second_data[j][0]:
                    j += 1
            else:
                break

       # if len(data) == 0:
        #    print("没有对应的数据")
        #    return blk_number

    #    blk_number = write_data(data, int(ceil(len(data) / 5.0)), 5, blk_number)
        return blk_number

    @staticmethod
    def hash_join(relation_first, relation_second, number_of_bucket, blk_number,ui):
        # ui.log.clear()
        ui.res.clear()
        if relation_first != 'R' and relation_first != 'S':
            print("关系名称错误")
            return blk_number
        elif relation_second != 'R' and relation_second != 'S':
            print("关系名称错误")
            return blk_number

        # 构造桶
        bucket_of_r = []
        bucket_of_s = []
        for i in range(number_of_bucket):
            bucket_of_r.append([])
            bucket_of_s.append([])

        # 首先找到第一个关系的起始文件块号
        present_blk_number = blk_dict[relation_first]
        # 然后读取第一个关系的数据
        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 读取所有的元组
            for i in range(int(number_of_tuple)):
                bucket_index = (int(read_data[i * 2]) + 2) % number_of_bucket  # hash一下
                bucket_of_r[bucket_index].append([int(read_data[i * 2]), int(read_data[i * 2 + 1])])
                # ui.log.append("桶"+str(bucket_index)+"被加入一个元素")
            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # 读完退出
            if present_blk_number == '0':
                break
        # ui.log.append("第一个关系处理结束")
        # 首先找到第二个关系的起始文件块号
        present_blk_number = blk_dict[relation_second]
        # 然后读取第二个关系的数据
        while True:
            index = buffer.readBlockFromDisk(present_blk_number)  # 为关系的数据申请一个缓冲
            if index == -1:
                print("缓冲区已满，不能为关系的数据申请一个缓冲区")
                break

            read_data = buffer.data[index][1]  # 从磁盘块中读取的数据
            number_of_tuple = (len(read_data) - 1) / 2
            next_blk_number = read_data[-1]  # 文件的后继磁盘块号

            # 读取所有的元组
            for i in range(int(number_of_tuple)):
                bucket_index = (int(read_data[i * 2]) + 2) % number_of_bucket  # hash一下
                bucket_of_s[bucket_index].append([int(read_data[i * 2]), int(read_data[i * 2 + 1])])
                # ui.log.append("桶" + str(bucket_index) + "被加入一个元素")
            present_blk_number = next_blk_number
            buffer.freeBlockInBuffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
            # 读完退出
            if present_blk_number == '0':
                break
        # ui.log.append("第二个关系处理结束")
        # join
        data = []
        for i in range(number_of_bucket):
            # ui.log.append("正连接第"+str(i)+"个桶")
            for j_ in range(len(bucket_of_r[i])):
                for k_ in range(len(bucket_of_s[i])):
                    if bucket_of_r[i][j_][0] == bucket_of_s[i][k_][0]:
                        ui.res.append(
                            str(bucket_of_r[i][j_][0])+"  "+ str(bucket_of_r[i][j_][1])+"  "+ str(bucket_of_s[i][k_][0])+"  "+ str(bucket_of_s[i][k_][1]))

        if len(data) == 0:
      #      print("没有对应的数据")
            return blk_number

      #  blk_number = write_data(data, int(ceil(len(data) / 5.0)), 5, blk_number)
        return blk_number

def joinexecute():
    type = ui.join1.currentText()
    if type == "sort_merge_join":
        blk_number = JoinOperationAlgorithm.sort_merge_join('R', 'S', 16,ui)
    if type == "nlj":
        blk_number = JoinOperationAlgorithm.nest_loop_join('R', 'S', blk_numbers_of_R, blk_numbers_of_S, 16,ui)
    if type == "hash_join":
        blk_number = JoinOperationAlgorithm.hash_join('R', 'S', 5, 16,ui)
import write

import shutil
import os
def savetofile():

    shutil.rmtree('./rblks')
    os.mkdir('./rblks')
    with open('result.txt', 'w') as file_handle:  # .txt可以不自己新建,代码会自动新建
        file_handle.write(ui.res.toPlainText())  # 写入
        file_handle.write('\n')  # 有时放在循环里面需要自动转行，不然会覆盖上一条数据

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
    blk_number = 0  # 磁盘文件号
    blk_numbers_of_R = 16  # 关系R的磁盘块数
    blk_numbers_of_S = 32  # 关系S的磁盘块数
    blk_dict = {}  # 用于记录关系和关系存放的第一个文件块的编号

    buffer = extmem.Buffer(64, 8)  # 块大小

    # 首先产生数据
    r = []
    s = []
    randomR(r, s)

    # 将r写入到磁盘中
    # blk_dict['R'] = 0
    print('关系R写入磁盘')
    blk_dict['R'] = blk_number
    blk_number = writetodisk(r, blk_numbers_of_R, blk_number)
    print('关系S写入磁盘')
    blk_dict['S'] = blk_number
    # print(blk_number)
    blk_number = writetodisk(s, blk_numbers_of_S, blk_number)
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = mem.Ui_Dialog()
    # 向主窗口上添加控件
    ui.setupUi(mainWindow)
    ui.selectb.clicked.connect(lambda: RelationSelectionAlgorithm.selection_linear(ui.select1.currentText(), ui.select2.currentText(),int(ui.select3.text()), blk_number, ui))
    ui.projectb.clicked.connect(
       lambda: RelationProjectionAlgorithm.project(ui.project1.currentText(), ui.project2.currentText(), blk_number, ui))
    ui.projectc.clicked.connect(joinexecute)
    ui.save.clicked.connect(savetofile)

    mainWindow.show()
    sys.exit(app.exec_())











