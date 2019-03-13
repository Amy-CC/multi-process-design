from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys
from choose import Ui_Dialog
from mainUI import Ui_Multi
from PyQt5.QtGui import *
from decimal import Decimal
import threading
from copy import deepcopy
import time
from PyQt5.QtCore import *

# 自定义输入作业
class SubDialog(QDialog,Ui_Dialog):
    def __init__(self):
        super(SubDialog,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btnClick)  # 按钮事件绑定

    # 子窗体自定义事件，存储输入的所有信息
    def btnClick(self):
        if int(self.machinenum.text()) > macnum:
            reply = QMessageBox.information(self, "注意", "磁带机数量超出范围", QMessageBox.Yes)
            return 0
        if float(self.memorynum.text()) > menum:
            reply = QMessageBox.information(self, "注意", "主存超出范围", QMessageBox.Yes)
            return 0
        # 存储的顺序
        global di_order
        # 作业名
        real_name = self.name.text()
        # 作业到达时间
        start = self.begin.text()
        # 运行时间
        run = self.running.text()
        # 所需主存空间
        mesize = self.memorynum.text()
        # 所需磁带机数量
        machnumb = self.machinenum.text()
        # 标记进入内存的时间
        time_flag = 0
        # 标志基址
        saddress = 0.00
        # 已运行时间
        haverun = 0.00
        # 带权周转
        daiquan = 0.00
        # 标志进入内存顺序
        oooder = 0
        jobs[di_order] = [real_name, float(start), float(run)*0.01, float(mesize), int(machnumb), int(di_order), int(time_flag), saddress, haverun, daiquan, int(oooder)]
        di_order += 1
        self.name.clear()
        self.begin.setValue(0.00)
        self.running.setValue(0.00)
        self.close()


# 主界面
class MainWidget(QDialog,Ui_Multi):
    def __init__(self):
        super(MainWidget,self).__init__()
        self.setupUi(self)
        # 退出按钮绑定
        self.quit.clicked.connect(self.exitClick)
        self.lcdNumber.display('0:00')
        # 设置数据层次结构
        self.model = QStandardItemModel(0,9)
        self.wmodel = QStandardItemModel(0, 7)
        self.memodel = QStandardItemModel(0, 3)
        self.rmodel = QStandardItemModel(0, 10)
        self.mjmodel = QStandardItemModel(0, 9)
        # 设置水平方向头标签文本内容
        self.model.setHorizontalHeaderLabels(['作业', '到达时间', '进入时间', '估计运行时间', '结束时间', '周转时间',
                                              '状态', '作业大小', '需磁带机数'])
        self.wmodel.setHorizontalHeaderLabels(['等待作业', '到达时间', '估计运行时间',
                                              '状态', '作业大小', '需磁带机数'])
        self.memodel.setHorizontalHeaderLabels(['空间大小', '起始地址', '分配情况'])
        self.rmodel.setHorizontalHeaderLabels(['运行作业', '到达时间', '进入时间', '估计运行时间', '已运行时间', '还需运行时间',
                                               '状态', '作业大小', '需磁带机数', '是否分配'])
        self.mjmodel.setHorizontalHeaderLabels(['作业', '到达时间', '进入时间', '估计运行时间',
                                                '状态', '作业大小', '需磁带机数', '是否分配', '基址'])
        self.tableView.setModel(self.model)
        self.outer.setModel(self.wmodel)
        self.memoryarr.setModel(self.memodel)
        self.run.setModel(self.rmodel)
        self.mj.setModel(self.mjmodel)
        # 重置按钮
        self.reset.clicked.connect(self.ress)
        # 默认按钮
        self.default_2.clicked.connect(self.DefaultEnter)
        # 运行按钮
        self.pushButton.clicked.connect(self.RunAll)
        # 空闲分区显示
        self.memodel.appendRow([
            QStandardItem('%s' % menum),
            QStandardItem('0'),
            QStandardItem('NO')
        ])
        # 计时器
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.refreshtime)




    # 重置
    def ress(self):
        global jobs,memory,di_order,me_order,menum,macnum,time,spacelist,nowposition,templist,count,otherlist,afsorted,zhouzhuan,melistcount,menumtemp,macnumtemp
        jobs = {}
        memory = {}
        di_order=0
        me_order = 0
        self.model.clear()
        self.memodel.clear()
        self.wmodel.clear()
        self.rmodel.clear()
        self.mjmodel.clear()
        self.lcdNumber.display('0:00')
        self.model.setHorizontalHeaderLabels(['作业', '到达时间', '进入时间', '估计运行时间', '结束时间', '周转时间',
                                              '状态', '作业大小', '需磁带机数'])
        self.wmodel.setHorizontalHeaderLabels(['等待作业', '到达时间', '估计运行时间',
                                               '状态', '作业大小', '需磁带机数'])
        self.memodel.setHorizontalHeaderLabels(['空间大小', '起始地址', '分配情况'])
        self.rmodel.setHorizontalHeaderLabels(['运行作业', '到达时间', '进入时间', '估计运行时间', '已运行时间', '还需运行时间',
                                               '状态', '作业大小', '需磁带机数', '是否分配'])
        self.mjmodel.setHorizontalHeaderLabels(['作业', '到达时间', '进入时间', '估计运行时间',
                                                '状态', '作业大小', '需磁带机数', '是否分配', '基址'])
        self.tableView.setModel(self.model)
        self.default_2.setEnabled(True)
        self.average2.clear()
        self.average.clear()
        menum = 0
        macnum = 0
        time = 0
        # 空闲分区表
        spacelist = []
        nowposition = 0.00
        templist = []
        count = 0
        otherlist = []
        afsorted = []
        zhouzhuan = []
        melistcount = 0
        menumtemp = 0
        macnumtemp = 0



    # 默认输入，并保存
    def DefaultEnter(self):
        if len(jobs)!=0:
            return
        global di_order
        jobs[di_order] = ['JOB1', float(10.00), float(0.25), float(15), int(2), int(di_order),
                          int(0), 0.00, 0.00, 0.00, 0]
        di_order += 1
        self.model.appendRow([
            QStandardItem('%s' % jobs[di_order - 1][0]),
            QStandardItem('%0.2f' % jobs[di_order - 1][1]),
            QStandardItem(''),
            QStandardItem('%s' % ((jobs[di_order - 1][2])*100)),
            QStandardItem(''),
            QStandardItem(''),
            QStandardItem(''),
            QStandardItem('%s' % jobs[di_order - 1][3]),
            QStandardItem('%s' % jobs[di_order - 1][4]),
        ])
        jobs[di_order] = ['JOB2', float(10.20), float(0.30), float(60), int(1), int(di_order),
                          int(0), 0.00, 0.00, 0.00, 0]
        di_order += 1
        self.model.appendRow([
            QStandardItem('%s' % jobs[di_order - 1][0]),
            QStandardItem('%0.2f' % jobs[di_order - 1][1]),
            QStandardItem(''),
            QStandardItem('%s' % ((jobs[di_order - 1][2])*100)),
            QStandardItem(''),
            QStandardItem(''),
            QStandardItem(''),
            QStandardItem('%s' % jobs[di_order - 1][3]),
            QStandardItem('%s' % jobs[di_order - 1][4]),
        ])
        jobs[di_order] = ['JOB3', float(10.30), float(0.10), float(50), int(3), int(di_order),
                          int(0), 0.00, 0.00, 0.00, 0]
        di_order += 1
        self.model.appendRow([
            QStandardItem('%s' % jobs[di_order - 1][0]),
            QStandardItem('%0.2f' % jobs[di_order - 1][1]),
            QStandardItem(''),
            QStandardItem('%s' % ((jobs[di_order - 1][2])*100)),
            QStandardItem(''),
            QStandardItem(''),
            QStandardItem(''),
            QStandardItem('%s' % jobs[di_order - 1][3]),
            QStandardItem('%s' % jobs[di_order - 1][4]),
        ])
        jobs[di_order] = ['JOB4', float(10.35), float(0.2), float(10), int(2), int(di_order),
                          int(0), 0.00, 0.00, 0.00, 0]
        di_order += 1
        self.model.appendRow([
            QStandardItem('%s' % jobs[di_order - 1][0]),
            QStandardItem('%0.2f' % jobs[di_order - 1][1]),
            QStandardItem(''),
            QStandardItem('%s' % ((jobs[di_order - 1][2])*100)),
            QStandardItem(''),
            QStandardItem(''),
            QStandardItem(''),
            QStandardItem('%s' % jobs[di_order - 1][3]),
            QStandardItem('%s' % jobs[di_order - 1][4]),
        ])
        jobs[di_order] = ['JOB5', float(10.40), float(0.15), float(30), int(2), int(di_order),
                          int(0), 0.00, 0.00, 0.00, 0]
        di_order += 1
        self.model.appendRow([
            QStandardItem('%s' % jobs[di_order - 1][0]),
            QStandardItem('%0.2f' % jobs[di_order - 1][1]),
            QStandardItem(''),
            QStandardItem('%s' % ((jobs[di_order - 1][2])*100)),
            QStandardItem(''),
            QStandardItem(''),
            QStandardItem(''),
            QStandardItem('%s' % jobs[di_order - 1][3]),
            QStandardItem('%s' % jobs[di_order - 1][4]),
        ])
        self.default_2.setEnabled(False)


    # 运行
    def RunAll(self):
        if len(jobs)==0:
            reply = QMessageBox.information(self, "注意", "未输入作业", QMessageBox.Yes)
            return 0
        global di_order,time
        # 显示初始时间计时值
        self.lcdNumber.display("%s" %str(Decimal(jobs[0][1]).quantize(Decimal('0.00'))).replace('.', ':'))
        time = jobs[0][1]
        global afsorted
        # 排序作业队列，按到达时间
        afsorted = sorted(deepcopy(jobs).items(), key=lambda d: d[1][1])
        self.timer.start()


    def refreshtime(self):
        global time
        global nowposition, menum, macnum,record, templist,count, otherlist, afsorted,zhouzhuan,memory, me_order,melistcount,menumtemp,macnumtemp,spacelist
        self.lcdNumber.display("%s" % str(Decimal(time).quantize(Decimal('0.00'))).replace('.', ':'))
        af = afsorted
        # 进程调度
        if len(templist)!=0:
            # 对内存中的作业进行按运行时间排序
            afsorted2 = sorted(templist,key=lambda d: d[2])
            t1 = int(time) * 60 + (round(time, 2) - int(time))*100
            t2 = int(afsorted2[0][6]) * 60 + (round(afsorted2[0][6],2) - int(afsorted2[0][6]))*100
            # 计算已运行多长时间
            tt = round(t1 - t2,2)
            if round(afsorted2[0][2]-0.01,2)==afsorted2[0][8]:
                # 运行时间足够，更新所有信息
                self.model.setItem(afsorted2[0][5], 4, QStandardItem('%0.2f' % round(time, 2)))
                t3 = int(afsorted2[0][1]) * 60 + (round(afsorted2[0][1],2) - int(afsorted2[0][1]))*100
                self.model.setItem(afsorted2[0][5], 5, QStandardItem(str(round(t1-t3,2))))
                jobs[afsorted2[0][5]][9]=round(tt/(afsorted2[0][2]*100),2)
                zhouzhuan.append(tt)
                spacelist.append([afsorted2[0][7], afsorted2[0][3]])
                spacelist = sorted(spacelist, key=lambda d: d[0])
                self.memodel.clear()
                self.memodel.setHorizontalHeaderLabels(['空间大小', '起始地址', '分配情况'])
                tien = 0
                while tien <= len(spacelist):
                    # 合并分区
                    for hgieb in range(len(spacelist)):
                        if hgieb>=1:
                            if spacelist[hgieb-1][1]+spacelist[hgieb-1][0]==spacelist[hgieb][0]:
                                spacelist[hgieb-1][1]+=spacelist[hgieb][1]
                                del spacelist[hgieb]
                                break
                    tien += 1
                # 刷新分区
                for bie in spacelist:
                    self.memodel.appendRow([
                        QStandardItem('%s' % bie[1]),
                        QStandardItem('%s' % bie[0]),
                        QStandardItem('NO')
                    ])
                melistcount -= 1

                self.rmodel.removeRow(0)
                dd = templist.index(afsorted2[0])
                self.mjmodel.removeRow(dd)
                menumtemp += afsorted2[0][3]
                macnumtemp += afsorted2[0][4]
                templist.remove(afsorted2[0])
                del afsorted2[0]
            else:
                # 调入作业且作业未在运行队列中
                if afsorted2[0][8]==0 or self.rmodel.item(0)==None:
                    if self.rmodel.item(0)!=None:
                        self.rmodel.removeRow(0)
                    afsorted2[0][8] += 0.01
                    afsorted2[0][8] = round(afsorted2[0][8], 2)
                    self.rmodel.appendRow([
                        QStandardItem('%s' % afsorted2[0][0]),
                        QStandardItem('%0.2f' % afsorted2[0][1]),
                        QStandardItem('%s' % afsorted2[0][6]),
                        QStandardItem('%s' % afsorted2[0][2]),
                        QStandardItem('%s' % tt),
                        QStandardItem('%s' % round(afsorted2[0][2]-tt,2)),
                        QStandardItem('Running'),
                        QStandardItem('%s' % afsorted2[0][4]),
                        QStandardItem('%s' % afsorted2[0][5]),
                        QStandardItem('YES')
                    ])
                else:
                    # 作业已在运行中，更新时间
                    afsorted2[0][8] += 0.01
                    afsorted2[0][8] = round(afsorted2[0][8], 2)
                    self.rmodel.setItem(0, 4, QStandardItem(str(afsorted2[0][8])))
                    self.rmodel.setItem(0, 5, QStandardItem(str(round(afsorted2[0][2]-afsorted2[0][8],2))))

        # 作业调度
        for i in af:
            if round(time, 2)<i[1][1]:
                break
            mark = -1
            jiel = 0
            # 条件符合要求
            if round(time,2)>=i[1][1] and menumtemp>=i[1][3] and macnumtemp>=i[1][4]:
                tivndk = 0
                # 合并空闲分区
                while tivndk<=len(spacelist):
                    for zz in range(len(spacelist)):
                        if zz>=1:
                            if spacelist[zz-1][1]+spacelist[zz-1][0]==spacelist[zz][0]:
                                spacelist[zz-1][1]+=spacelist[zz][1]
                                del spacelist[zz]
                                break
                    tivndk += 1
                # 查看是否有空闲分区适合
                for fjiejv in range(len(spacelist)):
                    if spacelist[fjiejv][1]>i[1][3]:
                        jiel = spacelist[fjiejv][0]
                        nowposition = spacelist[fjiejv][0]+i[1][3]
                        spacelist[fjiejv][1] -= i[1][3]
                        spacelist[fjiejv][0] = nowposition
                        mark = 1
                        break

                if mark==1:
                    menumtemp -= i[1][3]
                    macnumtemp -= i[1][4]
                    templist.append(i[1])
                    if i[1] in otherlist:
                        otherlist.remove(i[1])
                        d1= templist.index(i[1])
                        self.wmodel.removeRow(d1)
                    # 基址
                    i[1][7]=jiel
                    self.model.setItem(i[1][5], 2, QStandardItem('%0.2f' %round(time,2)))
                    i[1][6]=round(time,2)
                    ttlist = 0
                    self.mjmodel.appendRow([
                        QStandardItem('%s' % i[1][0]),
                        QStandardItem('%s' % i[1][1]),
                        QStandardItem('%0.2f' % time),
                        QStandardItem('%s' % i[1][2]),
                        QStandardItem(''),
                        QStandardItem('%s' % i[1][3]),
                        QStandardItem('%s' % i[1][4]),
                        QStandardItem('YES'),
                        QStandardItem('%s' % jiel)
                    ])
                    memory[me_order] = [jiel]
                    memory[me_order].append(nowposition)
                    memory[me_order].append('y')
                    #计算主存中作业总共占的大小
                    for k in memory:
                        if memory[k][2] == 'y':
                            ttlist += round(memory[k][1] - memory[k][0], 2)
                    if nowposition==menum:
                        # 空间刚好被占满
                        self.memodel.clear()
                        self.memodel.setHorizontalHeaderLabels(['空间大小', '起始地址', '分配情况'])
                        self.memodel.appendRow([QStandardItem('%s' % menum),
                                QStandardItem('0'),
                                QStandardItem('NO')])
                        me_order = 0
                        memory = {}
                        memory[me_order]=[0,menum,'n']
                    else:
                        self.memodel.clear()
                        self.memodel.setHorizontalHeaderLabels(['空间大小', '起始地址', '分配情况'])
                        for niefl in spacelist:
                            self.memodel.appendRow([
                                QStandardItem('%s' % round(niefl[1],2)),
                                QStandardItem('%s' % niefl[0]),
                                QStandardItem('NO')
                            ])
                        me_order += 1
                    self.model.setItem(i[1][5], 6, QStandardItem(str(count)))
                    i[1][10] = melistcount
                    melistcount += 1
                    count += 1
                    afsorted.remove(i)
            #添加外存
            elif round(time,2)>=i[1][1] and i[1] not in otherlist:
                self.wmodel.appendRow([
                    QStandardItem('%s' % i[1][0]),
                    QStandardItem('%0.2f' % i[1][1]),
                    QStandardItem('%s' % i[1][2]),
                    QStandardItem('Waiting'),
                    QStandardItem('%s' % i[1][3]),
                    QStandardItem('%s' % i[1][4])
                ])
                otherlist.append(i[1])

        # 计时功能，满60加1
        time += 0.01
        time=round(time,2)
        if int(time) + 0.6 == round(time, 2):
            time += 0.4

        # 作业序列和进程调度序列都不存在作业，计时结束
        if len(afsorted)==0 and len(templist)==0:
            self.timer.stop()
            self.memodel.clear()
            self.memodel.setHorizontalHeaderLabels(['空间大小', '起始地址', '分配情况'])
            self.memodel.appendRow([QStandardItem('%s' % menum),
                                QStandardItem('0'),
                                QStandardItem('NO')])
            reply = QMessageBox.information(self, "注意", "作业已全部调度完毕！", QMessageBox.Yes)
            self.calculate()

    # 计算全部作业平均周转时间、平均带权周转时间
    def calculate(self):
        global jobs, zhouzhuan
        sum1 = 0.0
        sum2 = 0.0
        for key in jobs:
            sum1 += jobs[key][9]
        for j in zhouzhuan:
            sum2+=j
        ave = round(sum1/len(jobs),2)
        av2 = round(sum2/len(jobs),2)
        # 更新界面
        self.average.setText('%s' % av2)
        self.average2.setText('%s' %ave)


    # 绑定Esc按钮退出
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    # 退出事件
    def exitClick(self):
        self.close()

    # 自定义输入显示
    def Change(self):
        self.model.appendRow([
            QStandardItem('%s' % jobs[di_order-1][0]),
            QStandardItem('%0.2f' % jobs[di_order - 1][1]),
            QStandardItem(''),
            QStandardItem('%s' % jobs[di_order - 1][2]),
            QStandardItem(''),
            QStandardItem(''),
            QStandardItem(''),
            QStandardItem('%s' % jobs[di_order - 1][3]),
            QStandardItem('%s' % jobs[di_order - 1][4]),
        ])


if  __name__=="__main__":
    # 作业队列
    jobs = {}
    # 主存中有作业的队列，标记基址、大小
    memory = {}
    # 存储的顺序
    di_order=0
    # 标记主存中作业的顺序
    me_order = 0
    # 主存大小
    menum = 0
    # 磁带机数量
    macnum = 0
    # 当前时间
    time=0
    # 空闲分区表
    spacelist = []
    # 当前空闲分区的基址
    nowposition= 0.00
    # 进程调度的序列
    templist = []
    record = -1
    # 标记运行顺序
    count = 0
    # 外存序列
    otherlist = []
    # 针对到达时间排序后的序列
    afsorted=[]
    # 标记个作业周转时间
    zhouzhuan = []
    # 当前内存作业个数
    melistcount = 0
    # 主存大小改变的状态
    menumtemp = 0
    # 磁带机数量改变的状态
    macnumtemp =0



    app=QtWidgets.QApplication(sys.argv)

    child = SubDialog()

    ui = MainWidget()

    # 磁带机数量、主存容量
    menum = float(ui.memory.text())
    macnum = int(ui.machine.text())
    menumtemp = menum
    macnumtemp = macnum
    # 主存开始的情况
    memory[0] = [0, menum,'n']
    # 空闲分区情况
    spacelist.append([0.0,menum])

    # 添加的界面
    btn = ui.add
    btn.clicked.connect(child.show)

    # 同时刷新输入界面
    sh = child.pushButton
    sh.clicked.connect(ui.Change)

    ui.show()
    sys.exit(app.exec_())