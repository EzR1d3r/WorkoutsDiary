#!/usr/bin/python
import sys
from PyQt5.QtWidgets import (QAction, QWidget, QFileDialog, QLineEdit,
                             QApplication, QPushButton, QTableWidget, QLabel,
                             QTableWidgetItem, QDialog, QDateEdit, QVBoxLayout,
                             QHBoxLayout, QToolBar,QMessageBox, QComboBox,
                             QColorDialog,  QDialogButtonBox, QMenu, QSplitter,
                             QCalendarWidget, QFrame)
from PyQt5.QtGui import (QIcon, QFont, QBrush, QColor, QCursor, QTextCharFormat, QDesktopServices)
from PyQt5 import QtCore
import os
import track_parser

#.....................'ADD USER'-WINDOW............................
class AddUserDialog (QDialog):

    def __init__(self):
        super(AddUserDialog, self).__init__()
        self.initUI()

    def initUI(self):

        self.lbUserData = QLabel ('Fill the table:')
        self.tWidget = QTableWidget(self)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.hLay1 = QHBoxLayout()
        self.hLay1.addWidget(self.lbUserData)
        self.hLay1.addStretch(1)

        self.hLay2 = QHBoxLayout()
        self.hLay2.addWidget(self.tWidget)

        self.hLay3 = QHBoxLayout()
        self.hLay3.addStretch(1)
        self.hLay3.addWidget(buttons)

        self.vLay = QVBoxLayout()
        self.vLay.addLayout(self.hLay1)
        self.vLay.addLayout(self.hLay2)
        self.vLay.addLayout(self.hLay3)
        self.setLayout(self.vLay)

        self.setMinimumSize(700, 150)
        self.setWindowTitle('Adding new user')
        self.show()

    def fnCreateTemplate(self, wTable, user_id = 'None'):
        DataList = MainWindow.fnLoadFile(MainWindow, 'data/users.txt')[0]
        row_index = len(DataList) + 1
        if user_id != 'None':
            for DataItem in DataList:
                if DataItem[0] == user_id:
                    row_index = DataList.index(DataItem)
                    DataList = [DataList[0], DataList[row_index]]
                    MainWindow.fnMakeTable(MainWindow, DataList, wTable, 1)
                    break
        else:
            DataList = [DataList[0], []]
            print(DataList)
            MainWindow.fnMakeTable(MainWindow, DataList, wTable, 1)

        return row_index

    def fnCollectData(self):
        DataItem = []
        while len(DataItem) < self.tWidget.columnCount():
            i = len(DataItem)
            try:
                DataItem.append(
                                    self.tWidget.item(0, i).text()
                                )
            except AttributeError:
                DataItem.append('-')
        return DataItem


    def fnClose(parent="None", user_id='None'):
        dialog = AddUserDialog()
        row_index = dialog.fnCreateTemplate(dialog.tWidget, user_id)
        result = dialog.exec_()
        if user_id=='None':
            user_id = MainWindow.fnCreateID(MainWindow, 'data/users.txt')
        DataItem = [user_id] + dialog.fnCollectData()
        return result == QDialog.Accepted, DataItem, row_index

#.....................'ADD EXERCISE'-WINDOW............................
class AddExcDialog (QDialog):

    def __init__(self):
        super(AddExcDialog , self).__init__()
        self.initUI()

    def initUI(self):

        lbExcName = QLabel('Упражнение: ', self)
        lbTags = QLabel ('Описание: ', self)

        self.tExcName = QLineEdit(self)
        self.tExcName.setFixedSize(175, 25)
        self.tTags = QLineEdit(self)
        self.tTags.setFixedSize(175,25)
        self.tTags.setToolTip('Tags for the exercise')

        self.btnPickColor = QPushButton(QIcon('icons/color.png'), '', self)
        self.btnPickColor.setFixedSize(32, 32)
        self.btnPickColor.setIconSize(QtCore.QSize(29,29))
        self.btnPickColor.setToolTip('Pick background color for the exercise')
        self.btnPickColor.clicked.connect(self.fnPickColor)

        #self.btnOK = QPushButton('Add', self)
        #self.btnOK.setFixedSize(60, 30)
        #self.btnOK.clicked.connect(self.fnClose)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.hLay1 = QHBoxLayout()
        self.hLay1.addStretch(1)
        self.hLay1.addWidget(self.btnPickColor)
        self.hLay1.addWidget(lbExcName)
        self.hLay1.addWidget(self.tExcName)
        self.hLay1.addWidget(lbTags)
        self.hLay1.addWidget(self.tTags)

        self.hLay2 = QHBoxLayout()
        self.hLay2.addStretch(1)
        self.hLay2.addWidget(buttons)

        self.vLay = QVBoxLayout()
        self.vLay.addLayout(self.hLay1)
        self.vLay.addLayout(self.hLay2)
        self.setLayout(self.vLay)

        self.setFixedSize(550, 100)
        self.setWindowTitle('Adding exercize')
        self.show()

    def fnPickColor(self):
        col = QColorDialog.getColor()
        print (col)

        if col.isValid():
            self.tExcName.setStyleSheet("QWidget { background-color: %s }"
                %col.name())

    def fnFillForm(self, exc_id='None'):
        DataList = MainWindow.fnLoadFile(MainWindow, ex.strPathExc)[0]
        for DataItem in DataList:
            if DataItem[0] == exc_id:
                excData = DataItem
                break

        rgba = eval(excData[3])
        col = QColor(rgba[0], rgba[1], rgba[2], rgba[3])
        self.tExcName.setStyleSheet("QWidget { background-color: %s }"
                %col.name())
        self.tExcName.setText(excData[1])
        self.tTags.setText(excData[2])

    def fnClose(parent="None", exc_id='None'):
        dialog = AddExcDialog()
        if exc_id=='None':
            exc_id = MainWindow.fnCreateID(MainWindow, ex.strPathExc)
        else:
            dialog.fnFillForm(exc_id)
        result = dialog.exec_()

        ColorExc = dialog.tExcName.palette()
        ColorExc = ColorExc.color(1)
        ColorExc = ColorExc.getRgb()

        return result == QDialog.Accepted, [exc_id, dialog.tExcName.text(), dialog.tTags.text(), str(ColorExc)]

#.....................'ADD HEADERS'-DIALOG............................
class AddHeadersDialog (QDialog):

    def __init__(self):
        super(AddHeadersDialog, self).__init__()
        self.initUI()

    def initUI(self):

        lbConst = QLabel('Постоянная часть: ', self)
        lbValues = QLabel('Повторяющаяся часть: ', self)

        self.elConst = QLineEdit(self)
        self.elConst.setFixedSize(225, 25)
        self.elConst.setToolTip('Type here non-repeat headers, splitted by "&".\n (Date, exercise, etc...)\nName of the headers type will be the first word.')
        self.elValues = QLineEdit(self)
        self.elValues.setFixedSize(225, 25)
        self.elValues.setToolTip('Type here repeat headers, splitted by "&". Use "{0}" for numbers.\n For example: set {0}&weight {0}.\nIt will be: |set 1|weigth 1|set 2|, etc...')

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.hLay1 = QHBoxLayout()
        self.hLay1.addWidget(lbConst)
        self.hLay1.addWidget(self.elConst)
        self.hLay1.addStretch(1)
        self.hLay1.addWidget(lbValues)
        self.hLay1.addWidget(self.elValues)

        self.hLay2 = QHBoxLayout()
        self.hLay2.addStretch(1)
        self.hLay2.addWidget(buttons)

        self.vLay = QVBoxLayout()
        self.vLay.addLayout(self.hLay1)
        self.vLay.addLayout(self.hLay2)
        self.setLayout(self.vLay)

        self.setFixedSize(750, 100)
        self.setWindowTitle('Adding headers set')
        self.show()

    def fnClose(parent="None", exc_id='None'):
        dialog = AddHeadersDialog()
        headers_id = ex.fnCreateID(ex.strPathHeaders)
        dialog.elConst.setText('Силовой 1&Дата&Упражнение&Тэги')
        result = dialog.exec_()
        return result == QDialog.Accepted, [headers_id,
                                            dialog.elConst.text(),
                                            dialog.elValues.text()]


#.....................'ADD WORKOUT'-WINDOW............................

class AddWorkoutWindow(QDialog):
#............................GUI........................

    def loadForm(self, strPath, wTable):

        listRows = (MainWindow.fnLoadFile(MainWindow, strPath))[0]
        intColumn = (
                        max([len(row) for row in listRows])
                    )
        wTable.setRowCount(2)
        wTable.setColumnCount(intColumn)

        wTable.setHorizontalHeaderLabels(listRows[0])
        #wTable.resizeColumnsToContents()

        wTable.removeColumn(0)
        wTable.removeRow(0)

        wTable.setColumnWidth(0, 150)

    def saveWork(self, user_id):
        work_id = MainWindow.fnCreateID(self, 'data/work.txt')
        fileWork = open('data/work.txt', 'a')
        DateTuple = self.wSetDate.date().getDate()
        workData = ('\n' + work_id + '$%&' + user_id
                        + '$%&' + str(DateTuple) )
        fileWork.write(workData)
        fileWork.close()

        return work_id

    def saveExercises(self, strExercise):
        exc_id = MainWindow.fnCreateID(self, ex.strPathExc)
        fileExc = open(ex.strPathExc, 'a')
        excData = '\n' + exc_id + '$%&' + strExercise + '$%&' + '$%&' + '(255, 255, 255, 255)'
        fileExc.write(excData)
        fileExc.close()

        return exc_id

    def saveSet(self):
        set_id = MainWindow.fnCreateID(self, 'data/sets.txt')
        fileSets = open('data/sets.txt', 'a')
        r = 0
        list_sets_ids = []
        while r < self.tAddData.rowCount():
            if r != 0:
                set_id = hex(int(set_id, 16) + 1)
            list_sets_ids.append(set_id)
            setsData = '\n' + set_id
            c = 0

            while c < self.tAddData.columnCount():
                item = self.tAddData.item(r, c)
                print(item)

                if c == 0:
                    item = self.tAddData.cellWidget(r, c)
                    exc_id = MainWindow.find_id(MainWindow, ex.strPathExc, item.currentText())

                    if exc_id == 'None':
                        exc_id = self.saveExercises(item.currentText())

                    setsData = setsData + '$%&' + exc_id
                    c = c + 1
                    continue

                try:
                    setsData = setsData + '$%&' + item.text()
                except AttributeError:
                    setsData = setsData + '$%&' + '-'
                c = c + 1
            fileSets.write(setsData)
            r = r + 1

        print(list_sets_ids)
        return list_sets_ids

    def saveSummary(self, work_id, list_sets_ids):

        sum_id = MainWindow.fnCreateID(self, 'data/sum.txt')

        fileSum = open('data/sum.txt', 'a')
        for set_id in list_sets_ids:
            sumData = '\n' + sum_id + '$%&' + work_id + '$%&' + set_id
            sum_id = hex(int(sum_id, 16) + 1)
            fileSum.write(sumData)
        fileSum.close()


    #slots
    def fnParseTrack(self):
        filePath = QFileDialog.getOpenFileName(self, ('Choose track'), 'D:/','*.gpx')[0]
        if filePath != '':
            distancesList, timeIntervalsList = track_parser.getDistancesAndTimes(filePath)
            Date = track_parser.getDate(filePath)
            SummaryDistance = track_parser.getSummaryDistance(distancesList)
            SummaryTime = track_parser.getSummaryTime(timeIntervalsList)
            AvgSpeed = track_parser.getAvgSpeed(SummaryDistance, SummaryTime)
            AvgPace = track_parser.getAvgPace(SummaryDistance, SummaryTime)
            AvgPace = str(AvgPace)[2:7]
            paceList = track_parser.getPacesOneKm(distancesList, timeIntervalsList)
            paceList = [str(pace)[2:7] for pace in paceList ]

            DataItem=[Date, SummaryDistance, SummaryTime, AvgSpeed, AvgPace] + paceList
            DataItem = [str(item) for item in DataItem]
            return DataItem

    def slotImportTrack(self):
        DataItem = self.fnParseTrack()
        Date = DataItem[0][0:6] + '20' + DataItem[0][6:8]
        Date = QtCore.QDate.fromString(Date, 'dd.MM.yyyy')
        self.wSetDate.setDate(Date)
        DataItem.pop(0)
        self.addRow()

        row_index=self.tAddData.rowCount() - 1
        ex.fnFillRow(DataItem, self.tAddData, row_index, 1)
        self.slotSetHeaders()
        self.cbHeaders.setCurrentText('Циклический 1')

    def slotSaveData(self):
        user_id = MainWindow.find_id(MainWindow, "data/users.txt", ex.lbLogin.text())
        work_id = self.saveWork(user_id)
        list_sets_ids = self.saveSet()
        self.saveSummary(work_id, list_sets_ids)
        self.close()
        text = '\n' + 'new_work' + '$%&' + work_id
        MainWindow.fnSaveDataListToFile(
                        MainWindow, text, 'data/temp.txt', 'a')

    def fncreateCBox(self, currentText = ''):
        DataList = MainWindow.fnLoadFile(MainWindow, ex.strPathExc)[0]
        excList = [DataItem[1] for DataItem in DataList]
        excList.pop(0)
        cBox = QComboBox()
        cBox.setEditable(1)
        cBox.addItems(excList)
        cBox.setMinimumContentsLength(50)
        if currentText != '':
            cBox.setCurrentText (currentText)
        return cBox


    def addRow(self):
        self.tAddData.setRowCount(self.tAddData.rowCount() + 1)
        cBox = self.fncreateCBox()
        self.tAddData.setCellWidget((self.tAddData.rowCount() - 1), 0, cBox)

    def delRow(self):
        index = self.tAddData.currentRow()
        self.tAddData.removeRow(index)

    def addColumn(self):
        self.tAddData.insertColumn(self.tAddData.columnCount())
        self.slotSetHeaders()

    def removeColumn(self):
        self.tAddData.removeColumn(self.tAddData.columnCount() - 1)

    def slotSetHeaders(self):
        ex.fnSetHeaders(self.cbHeaders, self.tAddData, 3, 4, 5, 100)

    def OpenDialog(self, work_id = 'None'):
        dialog = AddWorkoutWindow()
        if work_id == 'None':
            dialog.loadForm('data/form.txt', dialog.tAddData)
        else:
            DataList = MainWindow.fnLoadFile(MainWindow, 'data/work.txt')[0]
            DataItem = MainWindow.find_DataItem(MainWindow, DataList, work_id, 0)
            DateTuple = eval( DataItem[2])
            Date = QtCore.QDate(DateTuple[0], DateTuple[1], DateTuple[2])
            dialog.wSetDate.setDate(Date)
            DataList = ex.fnLoadSelectedWorkout(work_id)
            MainWindow.fnMakeTable(MainWindow, DataList, dialog.tAddData, 1)
            MainWindow.fnDeleteColumns(MainWindow, dialog.tAddData,[0, 1, 3, 4])
            for i in DataList:
                print(i)

        i = 0
        while i < dialog.tAddData.rowCount():
            try:
                currentText = dialog.tAddData.item(i, 0).text()
            except AttributeError:
                currentText = ''
            cBox = dialog.fncreateCBox(currentText)
            dialog.tAddData.setCellWidget(i, 0, cBox)
            i += 1
        text = 'old_work' + '$%&' + work_id
        MainWindow.fnSaveDataListToFile(
                        MainWindow, text, 'data/temp.txt', 'w')
        dialog.slotSetHeaders()
        dialog.exec_()

    def __init__(self):
        super(AddWorkoutWindow , self).__init__()
        self.initUI()

    def initUI(self):

        #tables
        self.tAddData = QTableWidget(self)
        self.tAddData.setGeometry(15, 65, 1000, 200)

        #date widget
        self.wSetDate = QDateEdit(QtCore.QDate.currentDate(), self)
        self.wSetDate.setGeometry(55, 20, 105, 25)
        self.wSetDate.setCalendarPopup(1)

        #Labels
        labelDate = QLabel(self)
        labelDate.setText('Date:')
        labelDate.setGeometry(15, 20, 50, 25)

        lbTypeHeaders = QLabel(self)
        lbTypeHeaders.setGeometry(200, 20, 75, 25)
        lbTypeHeaders.setText('Headers type:')

        #buttons

        btnOK = QPushButton('OK', self)
        btnOK.setGeometry(965, 285, 50, 25)
        btnOK.clicked.connect(self.slotSaveData)

        btnAddRow = QPushButton('+ set', self)
        btnAddRow.setGeometry(15, 285, 50, 25)
        btnAddRow.clicked.connect(self.addRow)

        btnDelRow = QPushButton('- set', self)
        btnDelRow.setGeometry(70, 285, 50, 25)
        btnDelRow.clicked.connect(self.delRow)

        btnAddColumn = QPushButton('+', self)
        btnAddColumn.setGeometry(960, 20, 25, 25)
        btnAddColumn.clicked.connect(self.addColumn)

        btnRemoveColumn = QPushButton('-', self)
        btnRemoveColumn.setGeometry(990, 20, 25, 25)
        btnRemoveColumn.clicked.connect(self.removeColumn)

        btnImportTrack = QPushButton('track', self)
        btnImportTrack.setGeometry(125, 285, 50, 25)
        btnImportTrack.setToolTip('Choose a *.gpx file for import a track')
        btnImportTrack.clicked.connect(self.slotImportTrack)

        #Combo-boxes
        self.cbHeaders = QComboBox(self)
        self.cbHeaders.setGeometry(280, 20, 150, 25)
        HeadersNames = ex.fnLoadNamesHeaders()
        self.cbHeaders.addItems(HeadersNames)
        self.cbHeaders.currentIndexChanged.connect(self.slotSetHeaders)

        #Main window
        self.setFixedSize(1050, 350)
        self.setWindowTitle('Add workout')
        self.show()


class MainWindow(QWidget):

    def fnLoadFile(self, pathFile):
        #print(('Loading:' + str(pathFile)))
        fileData = open(pathFile, 'r')
        Data = fileData.read()
        listRows = Data.split('\n')
        fileData.close()
        listRows = [row.split('$%&') for row in listRows]
        return [listRows, pathFile]

    def fnMakeTable(self, listRows, wTable, enableCells = 0):
        wTable.setRowCount(0)
        wTable.setColumnCount(0)
        try:
            wTable.cellDoubleClicked.disconnect()
        except TypeError:
            print("OK")

        intRow = len(listRows)
        intColumn = (
                        max([len(row) for row in listRows])
                    )

        wTable.setRowCount(intRow)
        wTable.setColumnCount(intColumn)

        i = 0
        while i < intRow:
            indexRow = i
            if indexRow == 0:
                headerRow = listRows[indexRow]
                wTable.setHorizontalHeaderLabels(headerRow)
                i += 1
                continue
            while len(listRows[indexRow]) < intColumn:
                listRows[indexRow].append('')
            row = listRows[indexRow]
            indexColumn = 0
            for item in row:
                tableItem = QTableWidgetItem(item)
                tableItem.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                if enableCells == 1:
                    tableItem.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsEditable)
                wTable.setItem(indexRow, indexColumn, tableItem)
                indexColumn = indexColumn + 1
            i += 1

        wTable.removeRow(0)
        wTable.removeColumn(0)

        return [intColumn, headerRow]

    def fnFillRow(self, DataItem, wTable, row_index, index_column_start=0):
        new_column_count = len(DataItem) + index_column_start
        if new_column_count > wTable.columnCount():
            wTable.setColumnCount(new_column_count)
        i = 0
        for item in DataItem:
            tableItem = QTableWidgetItem(item)
            wTable.setItem(row_index, (index_column_start + i), tableItem)
            i += 1

    def fnFillCalendar(self, calendarWidget, DateColorDict):
        for item in DateColorDict:
            Date = QtCore.QDate.fromString(item, '(yyyy, M, d)')
            rgba = DateColorDict[item]
            Brush = QBrush(QColor(rgba[0], rgba[1], rgba[2], rgba[3]))
            charf = QTextCharFormat()
            charf.setBackground(Brush)
            calendarWidget.setDateTextFormat(Date, charf)

    #def slotFillCalendar(self):
        #self.calendar.setDateTextFormat(QtCore.QDate(),QTextCharFormat())

        #UserWorksList = self.fnLoadUserWorks()
        #UserWorksList.pop(0)
        #DateList = [DataItem[6] for DataItem in UserWorksList]
        #ColorList = [self.fnCreateWorkoutColor(DataItem[0]) for DataItem in UserWorksList]
        #DateColorDict = {DateList[i]:ColorList[i] for i in range(len(DateList))}
        #for i in DateColorDict:
            #print(str(i)+' : '+str(DateColorDict[i]))
        #self.fnFillCalendar(self.calendar, DateColorDict)

    def slotFillCalendar(self):
        self.calendar.setDateTextFormat(QtCore.QDate(),QTextCharFormat())

        user_id = self.find_id("data/users.txt", self.lbLogin.text())
        tempList = self.fnCreateDataList(user_id, 'data/users.txt', 1, 'data/work.txt')
        DataList=[]
        for row in tempList:
            work_id = row[0]
            addList = self.fnCreateDataList(
                work_id, 'data/work.txt', 1, 'data/sum.txt')
            DataList += addList

        SetsList = self.fnLoadFile('data/sets.txt')[0]
        DataList = self.fnInsertByID(DataList, 3, SetsList)
        ExcList = self.fnLoadFile(self.strPathExc)[0]
        DataList = self.fnInsertByID(DataList, 3, ExcList)
        newDataList=[]
        for DataItem in DataList:
            try:
                date = eval(DataItem[2])
                type(date)
                newDataList.append(DataItem)
            except TypeError:
                1
            except NameError:
                1
            except SyntaxError:
                1
        print('=============')

        DateList = [DataItem[2] for DataItem in newDataList]
        ColorList = [eval(DataItem[5]) for DataItem in newDataList]

        uniqDateList = list(set(DateList))
        DateColorDict = {}
        for uniqDate in uniqDateList:
            i=0
            tempList=[]
            while i < len(DateList):
                if uniqDate == DateList[i]:
                     tempList.append(ColorList[i])
                i+=1
            r = g = b = a = 0
            for col in tempList:
                r+=col[0]
                g+=col[1]
                b+=col[2]
                a+=col[3]
            r//=len(tempList)
            g//=len(tempList)
            b//=len(tempList)
            a//=len(tempList)
            DateColorDict[uniqDate] = (r,g,b,a)
        self.fnFillCalendar(self.calendar, DateColorDict)

    def fnTest(self):
        print(self.tWidget.currentRow())

    def fnMergeCellsInColumn(self, wTable, index_column, type_int = 0):
        if (type_int == 0) or (type_int == 1):
            i = 1
            try:
                baseText = wTable.item(0, 0).text()
            except AttributeError:
                baseText = ''
            baseIndex = 0
            lenMerge = 1
            while i <= wTable.rowCount():
                try:
                    cellText = wTable.item(i, index_column).text()
                except AttributeError:
                    cellText = ''
                if baseText != cellText:
                    wTable.setSpan(baseIndex, index_column, lenMerge, 1)
                    baseText = cellText
                    baseIndex = i
                    lenMerge = 1
                    i += 1
                    continue
                lenMerge += 1
                i += 1

        if (type_int == 0) or (type_int == 2):
                r = 0
                lenMerge = wTable.columnCount()
                while r < wTable.rowCount():
                    try:
                        if wTable.item(r, 0).text() == '':
                            wTable.setSpan(r, 0, 1, lenMerge)
                    except AttributeError:
                        print (str(r) + ': row' + "- has no TableWidgetItem" )
                    r += 1

    def fnSetColorStyleTable(self, wTable, type_int = 0):
        c = 0
        if type_int == 0:
            while c < wTable.columnCount():
                r = 0
                while r < wTable.rowCount():
                    if r%2 == 0:
                        brush = QBrush(QColor(245, 245, 245, 255))
                        wTable.item(r, c).setBackground(brush)
                    r += 1
                c += 1

        if type_int == 1:
            while c < wTable.columnCount():
                r = 0
                while r < wTable.rowCount():
                    try:
                        if wTable.item(r, 0).text() == '':
                            wTable.item(r, c).setBackground(QBrush(QColor(235, 235, 235, 255)))
                    except AttributeError:
                        print (str(r) + ':' + str(c) + "- has no TableWidgetItem" )
                    r += 1
                c += 1

    def fnPersonalColored(self, wTable, path, index_in_path):
        DataListExc = self.fnLoadFile(self.strPathExc)[0]
        r = 0
        while r < wTable.rowCount():
            c = 0
            while c < wTable.columnCount():
                for DataItemExc in DataListExc:
                    if  DataItemExc.count(wTable.item(r, c).text()) != 0:
                        if wTable.item(r, c).text() != '':
                            rgba = eval(DataItemExc[index_in_path])
                            col = QColor(rgba[0], rgba[1], rgba[2], rgba[3])
                            tc = c
                            while tc < wTable.columnCount():
                                wTable.item(r, tc).setBackground(QBrush(col))
                                tc +=1
                c += 1
            r += 1

    def fnCreateWorkoutColor(self, work_id):
        DataList = self.fnLoadSelectedWorkout(work_id)
        print('=======')
        for i in DataList:
            print(i)
        DataList.pop(0)
        ColorsList = [eval(DataItem[5]) for DataItem in DataList]
        r = g = b = a = 0
        for item in ColorsList:
            r += item[0]
            g += item[1]
            b += item[2]
            a += item[3]
        try:
            r //= len(ColorsList)
            g //= len(ColorsList)
            b //= len(ColorsList)
            a //= len(ColorsList)
        except ZeroDivisionError:
            r = g = b = 0
            a = 255
        print(r, g, b, a)
        return (r, g, b, a)

    def fnDeleteColumns (self, wTable, ColumnList):
        transfColumnList = []
        for c in ColumnList:
            c = c - ColumnList.index(c)
            transfColumnList.append(c)
        for c in transfColumnList:
            wTable.removeColumn(c)

    def fnCreateDataList(self, item_id, path_file_source, column_index, path_file_dest):
        listRows_source = (self.fnLoadFile (path_file_source))[0]
        for item in listRows_source:
            if item[0] == item_id:
                sourceItem = [listRows_source[0], item.copy()]
                for item in sourceItem:
                    item.pop(0)
                break

        listRows_dest = (self.fnLoadFile (path_file_dest))[0]
        item_headers = (
                          listRows_dest[0][0:column_index]
                        + sourceItem[0]
                        + listRows_dest[0][(column_index + 1):len(listRows_dest[0])]
                        )
        DataList = [item_headers,]
        for item in listRows_dest:
            if item[column_index] == item_id:
                item_to_append = (
                                    item[0:column_index]
                                    + sourceItem[1]
                                    + item[(column_index + 1):len(item)]
                                 )
                DataList.append(item_to_append)
        return DataList

    def fnCreateID (self, arg):
        if type(arg) == str:
            fileData = open(arg, 'r')
            Data = fileData.read()
            listRows = Data.split('\n')
            fileData.close()
            listRows = [row.split('$%&') for row in listRows]
        else:
            listRows = arg
        print (arg)
        last_ID = listRows[len(listRows) - 1][0]
        ID = hex(eval(last_ID) + 1)
        return ID

    def fnInsertByID(self, DataList, column_index, SourceList):
        DataList[0] = (
                        DataList[0][0:column_index]
                        + SourceList[0][1:len(SourceList[0])]
                        + DataList[0][(column_index + 1):len(DataList[0])]
                      )
        SourceList.pop(0)
        for DataItem in DataList:
            for strRow in SourceList:
                if DataItem[column_index] == strRow[0]:
                    index = DataList.index (DataItem)
                    insert_item = strRow.copy()
                    insert_item.pop(0)
                    DataItem = (DataItem[0:column_index] +
                                insert_item +
                                DataItem[(column_index + 1):len(DataItem)]
                                )
                    DataList[index] = DataItem
                    break
        return DataList

    def fnLoadNamesHeaders(self):
        print ('--------------------')
        DataList = self.fnLoadFile(self.strPathHeaders)[0]
        namesList = [DataItem[1] for DataItem in DataList]
        namesList.pop(0)
        return namesList

    def fnCreatePersData(self, user_id):
        #exercises
        base = open('data/exh/exercises_base.txt')
        data = base.read()
        base.close()

        path = 'data/exh/' + user_id + '_c.txt'
        new_file = open (path, 'w')
        new_file.write(data)
        new_file.close()

        #headers
        base = open('data/exh/headers_base.txt')
        data = base.read()
        base.close()

        path = 'data/exh/' + user_id + '_h.txt'
        new_file = open (path, 'w')
        new_file.write(data)
        new_file.close()

    def fnSetHeaders(self, cBox, wTable, int1, int2, int3=0, int4=0):
        #print('Setting headers')
        DataList = self.fnLoadFile(self.strPathHeaders)[0]
        DataItem = self.find_DataItem(DataList, cBox.currentText(), 1)
        DataItem = DataItem[int1:int2] + DataItem[int3:int4]
        wTable.setHorizontalHeaderLabels(DataItem)
        wTable.resizeColumnsToContents()

    def slotSetHeaders(self):
        self.fnSetHeaders(self.cbHeaders, self.tWidget, 2, 100)

    def slotReloadLast(self):
        self.reloadAction.trigger()

    def slotDateChanged(self):
        if self.dateFilter.isChecked():
            self.reloadAction.trigger()

    def fnClean (self, pathFile):
        fileData = open(pathFile, 'w')
        fileData.close()

    def fnDateSort(self, DataList, index):
        def fnKeyDate(DataItem):
            Date = QtCore.QDate.fromString(DataItem[index], '(yyyy, M, d)')
            if Date.toJulianDay()>0:
                return Date.toJulianDay()
            else:
                return 1
        DataList.sort(key=fnKeyDate)
        return DataList

    def writeData(self, strPath):

        index = self.fnCreateID(strPath)
        Data = ('\n' + index)
        fileData = open(strPath, 'a')
        intColumns = self.tImput.columnCount()
        print(('COLUMN COUNT:  ' + str(intColumns)))

        while intColumns > 0:
            i = self.tImput.columnCount() - intColumns
            itemImput = self.tImput.item(0, i)
            if str(type(itemImput)) != "<class 'NoneType'>":
                Data = Data + '$%&' + itemImput.text()
                itemImput.setText('')
            else:
                Data = Data + '$%&' + '-'
            intColumns = intColumns - 1
            print(Data)

        fileData.write(Data)
        fileData.close()

    def find_id(self, pathFile, item, column_index=1):
        fileData = open(pathFile)
        Data = fileData.read()
        fileData.close()
        DataList = Data.split('\n')
        DataList = [DataItem.split('$%&') for DataItem in DataList]
        #DataList = (self.fnLoadFile(pathFile))[0]
        item_id = 'None'
        for DataItem in DataList:
            if DataItem[column_index] == item:
                item_id = DataItem[0]
                break
        return item_id

    def find_DataItem(self, DataList, item, column_index=1):
        for DataItem in DataList:
            if DataItem[column_index] == item:
                return DataItem
                break

    def fnDisplayData(self, DataList, index_column):
        for DataItem in DataList:
            indexDataItem = DataList.index(DataItem)
            try:
                DateTuple = eval(DataItem[index_column])
            except SyntaxError:
                continue
            except NameError:
                continue
            DisplayDate = QtCore.QDate(DateTuple[0], DateTuple[1], DateTuple[2])
            DataList[indexDataItem][index_column] = DisplayDate.toString('dd MMM yyyy, ddd')
        return DataList

    def fnDataListToString(self, DataList, paramWriting='w'):
        strDataListString=''

        for DataItem in DataList:

            if (DataList.index(DataItem) != 0) or (paramWriting == 'a'):
                strDataListString += '\n'

            strDataItemString=''
            for item in DataItem:
                if len(strDataItemString) != 0:
                    strDataItemString += '$%&'
                strDataItemString += item
            strDataListString += strDataItemString

        return strDataListString


    def fnSaveDataListToFile(self, strString, strPathFile, param='w'):
        DataFile = open (strPathFile, param)
        DataFile.write(strString)
        DataFile.close()

    def fnDelDataItemByID(self,item_id_List, column_index,
                                        DataList, column_index_to_collect=0):
        deleteList=[]
        id_List_cln = []
        for item_id in item_id_List:
            for DataItem in DataList:
                if DataItem[column_index] == item_id:
                    deleteList.append(DataItem)
                    id_List_cln.append(DataItem[column_index_to_collect])

        for deleteItem in deleteList:
            DataList.remove(deleteItem)

        return [DataList, id_List_cln]

    def fnDateFilter(self, DataList, dFrom, dTo, index_column):
        #dFrom, dTo is strings
        NewDataList = []
        dateFrom = QtCore.QDate.fromString(dFrom, '(yyyy, M, d)')
        dateTo = QtCore.QDate.fromString(dTo, '(yyyy, M, d)')
        for DataItem in DataList:
            if DataList.index(DataItem) == 0:
                NewDataList.append(DataItem)
                continue
            dateCheck = DataItem[index_column]
            dateCheck = QtCore.QDate.fromString(dateCheck, '(yyyy, M, d)')
            if  dateFrom <= dateCheck <= dateTo:
                NewDataList.append(DataItem)
        return NewDataList

    def fnStringFilter(self, DataList, strString):
        newDataList = []
        for DataItem in DataList:
            if DataList.index(DataItem) == 0:
                newDataList.append(DataItem)
                continue
            for Item in DataItem:
                if Item.find(strString) != -1:
                    newDataList.append(DataItem)
                    break
        return newDataList

    def fnTagFilter(self, DataList):
        strTags = self.tFilter.text()
        splitList = [',', ' ,', ', ']
        filterList = []
        for item in splitList:
            filterList += strTags.split(item)
        filterList = [item.split('++') for item in filterList]

        for item in filterList:
            while filterList.count(item) != 1:
                filterList.remove(item)
        print (filterList)

        finalList=[]
        for List in filterList:
            tempDataList = DataList.copy()
            for strString in List:
                tempDataList = self.fnStringFilter(tempDataList, strString)
            finalList += tempDataList

        finalList.reverse()
        for item in finalList:
            if item[0] != '':
                while finalList.count(item) != 1:
                    finalList.remove(item)

        finalList.reverse()
        return finalList

    def addColumn(self):
        self.tImput.setColumnCount(self.tImput.columnCount() + 1)

    def setUser (self):
        row_index = self.tWidget.currentRow()
        item_login = self.tWidget.item(row_index, 0)
        user_id = self.find_id('data/users.txt', item_login.text())
        self.strPathExc = 'data/exh/' + user_id + '_c.txt'

        self.cbHeaders.clear()
        self.strPathHeaders = 'data/exh/' + user_id + '_h.txt'
        self.cbHeaders.addItems(self.fnLoadNamesHeaders())

        self.lbLogin.setText(item_login.text())
        self.fnEnable_GUI_Elements()
        self.slotFillCalendar()
        #print (str(self.tWidget.currentRow()) + " : " + str(self.tWidget.currentColumn()))
        #print (self.tWidget.item(self.tWidget.currentRow(), self.tWidget.currentColumn()))

    def showDialog(self, strQuestion):

        mb = QMessageBox(0,'Training Diary', strQuestion,
                        QMessageBox.Ok | QMessageBox.Cancel)
        return mb.exec_()

    def fnDisable_GUI_Elements(self, enable=0):
        self.workDelAction.setEnabled(enable)
        self.setDelAction.setEnabled(enable)
        self.excEditAction.setEnabled(enable)
        self.one_workoutAction.setEnabled(enable)
        self.edit_workoutAction.setEnabled(enable)
        self.cbHeaders.setEnabled(enable)
        self.PColored.setEnabled(enable)

        self.btnAddHeaders.setEnabled(enable)
        self.btnDelHeaders.setEnabled(enable)

    def fnEnable_GUI_Elements(self, enable=1):
        self.all_workoutAction.setEnabled(enable)
        self.userEditAction.setEnabled(enable)
        self.userDelAction.setEnabled(enable)
        self.calendar.setEnabled(enable)

    def slotCalendarClicked(self):
        self.slotLoadAllWorkout(1)

    def slotLoadUsers(self):
        loadData = self.fnLoadFile('data/users.txt')
        UsersList = loadData[0]

        if self.wordFilter.isChecked():
            UsersList = self.fnTagFilter(UsersList)

        self.fnMakeTable(UsersList, self.tWidget)
        self.fnSetColorStyleTable(self.tWidget, 0)
        self.tWidget.cellDoubleClicked.connect(self.setUser)

        self.reloadAction.disconnect()
        self.reloadAction.triggered.connect(self.slotLoadUsers)
        self.fnDisable_GUI_Elements()

    def fnLoadUserWorks(self):
        user_id = self.find_id("data/users.txt", self.lbLogin.text())
        UserWorksList = self.fnCreateDataList(user_id, 'data/users.txt', 1, 'data/work.txt')
        UserWorksList = self.fnDateSort(UserWorksList, 6)

        return UserWorksList

    def slotLoadUserWorks(self):
        UserWorksList = self.fnLoadUserWorks()

        #Date filter
        if self.dateFilter.isChecked():
            dFrom = str(self.wFromDate.date().getDate())
            dTo = str(self.wToDate.date().getDate())
            print(dFrom + " - " + dTo)
            UserWorksList = self.fnDateFilter(UserWorksList, dFrom, dTo, 6)

        UserWorksList = self.fnDisplayData(UserWorksList, 6)

        if self.wordFilter.isChecked():
            UserWorksList = self.fnTagFilter(UserWorksList)

        self.fnMakeTable(UserWorksList, self.tWidget)
        self.fnSetColorStyleTable(self.tWidget)

        strString = self.fnDataListToString(UserWorksList)
        self.fnSaveDataListToFile(strString, 'data/temp.txt')

        self.fnDisable_GUI_Elements()
        self.one_workoutAction.setEnabled(1)
        self.workDelAction.setEnabled(1)
        self.reloadAction.disconnect()

    def fnLoadSelectedWorkout(self, work_id):
        DataList = self.fnCreateDataList(work_id, 'data/work.txt', 1, 'data/sum.txt')

        SetsList = self.fnLoadFile('data/sets.txt')[0]
        DataList = self.fnInsertByID(DataList, 3, SetsList)
        ExcList = self.fnLoadFile(self.strPathExc)[0]
        DataList = self.fnInsertByID(DataList, 3, ExcList)
        DataList = self.fnDisplayData(DataList, 2)
        return DataList

    def slotLoadSelectedWorkout(self):
        row_index = self.tWidget.currentRow()
        set_id = (self.fnLoadFile('data/temp.txt'))[0][row_index + 1][0]
        DataList = (self.fnLoadFile('data/sum.txt'))[0]
        work_id = self.find_DataItem(DataList, set_id, 2)[1]

        DataList = self.fnLoadSelectedWorkout(work_id)
        strString = self.fnDataListToString(DataList)
        self.fnSaveDataListToFile(strString, 'data/temp.txt')

        self.fnMakeTable(DataList, self.tWidget)
        self.fnDeleteColumns(self.tWidget, [0, 4])
        self.slotSetHeaders()

        self.fnDisable_GUI_Elements()
        self.setDelAction.setEnabled(1)
        self.btnAddHeaders.setEnabled(1)
        self.btnDelHeaders.setEnabled(1)
        self.edit_workoutAction.setEnabled(1)
        self.cbHeaders.setEnabled(1)

    def slotLoadAllWorkout(self, typeDateFilter = 0):

        user_id = self.find_id("data/users.txt", self.lbLogin.text())
        tempList = self.fnCreateDataList(user_id, 'data/users.txt', 1, 'data/work.txt')
        tempList = self.fnDateSort(tempList, 6)

        if self.dateFilter.isChecked() and typeDateFilter == 0:
            dFrom = str(self.wFromDate.date().getDate())
            dTo = str(self.wToDate.date().getDate())
            print (dFrom + " - " + dTo)
            tempList = self.fnDateFilter(tempList, dFrom, dTo, 6)
        elif typeDateFilter == 1:
            dFrom = dTo = str (self.calendar.selectedDate().getDate())
            tempList = self.fnDateFilter(tempList, dFrom, dTo, 6)
            if len(tempList) > 1:
                self.tempDate = self.calendar.selectedDate()
            else:
                self.calendar.setSelectedDate(self.tempDate)

        tempList = self.fnDisplayData(tempList, 6)
        tempList.pop(0)
        DataList = []

        if len(tempList) != 0:
            for row in tempList:
                work_id = row[0]
                addList = self.fnCreateDataList(
                    work_id, 'data/work.txt', 1, 'data/sum.txt')

                #clearing useless headers:
                if len(DataList) != 0:
                    for item in addList[0]:
                        i = addList[0].index(item)
                        addList[0][i] = ''
                DataList += addList

            SetsList = self.fnLoadFile('data/sets.txt')[0]
            DataList = self.fnInsertByID(DataList, 3, SetsList)

            ExcList = self.fnLoadFile(self.strPathExc)[0]
            DataList = self.fnInsertByID(DataList, 3, ExcList)
            DataList = self.fnDisplayData(DataList, 2)

            strString = self.fnDataListToString(DataList)
            self.fnSaveDataListToFile(strString, 'data/temp.txt')

            if self.wordFilter.isChecked():
                DataList = self.fnTagFilter(DataList)

            self.fnMakeTable(DataList, self.tWidget)
            self.fnDeleteColumns(self.tWidget, [0, 4])
            self.slotSetHeaders()

            if self.wordFilter.isChecked():
                self.fnSetColorStyleTable(self.tWidget, 0)
            else:
                self.fnSetColorStyleTable(self.tWidget, 1)

            if self.PColored.isChecked():
                self.fnPersonalColored(self.tWidget, self.strPathExc, 3)

            self.fnMergeCellsInColumn(self.tWidget, 0)

            self.fnDisable_GUI_Elements(1)
            self.excEditAction.setEnabled(0)

            self.reloadAction.disconnect()
            if typeDateFilter == 0:
                self.reloadAction.triggered.connect(self.slotLoadAllWorkout)
            else:
                self.reloadAction.triggered.connect(self.slotCalendarClicked)
            self.slotFillCalendar()
        else:
            self.showDialog('There is no workout in selected range')



    def slotLoadExercises(self):
        loadData = self.fnLoadFile(self.strPathExc)
        excList = loadData[0]

        if self.wordFilter.isChecked():
            excList = self.fnTagFilter(excList)

        self.fnMakeTable(excList, self.tWidget)
        self.tWidget.removeColumn(2)

        if self.PColored.isChecked():
            self.fnPersonalColored(self.tWidget, self.strPathExc, 3)
        else:
            self.fnSetColorStyleTable(self.tWidget, 0)

        self.fnDisable_GUI_Elements()
        self.excEditAction.setEnabled(1)
        self.PColored.setEnabled(1)

        self.reloadAction.disconnect()
        self.reloadAction.triggered.connect(self.slotLoadExercises)

    def slotAddHeaders(self):
        ok, Data = AddHeadersDialog.fnClose()
        if ok:
            name = Data[1].split('&')[0]
            if self.find_id(self.strPathHeaders, name) == "None":
                DataItem = [Data[0]] + (Data[1].split('&'))
                i = 1
                while i < 51:
                    DataItem += Data[2].format(i).split('&')
                    i += 1
                DataList = [DataItem]
                DataItemString = self.fnDataListToString (DataList, 'a')
                self.fnSaveDataListToFile(DataItemString, self.strPathHeaders, 'a')
                self.cbHeaders.addItems([name])
            else:
                self.showDialog( '"' + name + '"' + ' is already exists')

    def slotDeleteHeaders(self):
        strQuestion = ('Are you want to delete headers '
                        +  self.cbHeaders.currentText()
                        + '?')
        choice = self.showDialog(strQuestion)
        if choice == 1024:
            headers_id = self.find_id(self.strPathHeaders, self.cbHeaders.currentText())
            headers_id = [headers_id]

            #deleting sets
            OldList = (self.fnLoadFile(self.strPathHeaders))[0]
            NewList = self.fnDelDataItemByID(headers_id, 0, OldList)
            NewList = NewList[0]
            strNewList = self.fnDataListToString(NewList)
            self.fnSaveDataListToFile(strNewList, self.strPathHeaders)
            self.cbHeaders.removeItem(self.cbHeaders.currentIndex())
            self.slotSetHeaders()

    def slotAddExercise(self):
        ok, DataItem = AddExcDialog.fnClose(self, 'None')
        if ok:
            if  self.find_id(self.strPathExc, DataItem[1]) == "None":
                DataList = [DataItem]
                DataItemString = self.fnDataListToString (DataList, 'a')
                self.fnSaveDataListToFile(DataItemString, self.strPathExc, 'a')
                self.slotLoadExercises()
            else:
                self.showDialog('This exercise is already exists')

    def slotEditExercise(self):
        row_index = self.tWidget.currentRow()
        exc_name = self.tWidget.item(row_index, 0).text()
        exc_id = self.find_id(self.strPathExc, exc_name, 1)
        DataList = (self.fnLoadFile(self.strPathExc))[0]
        ok, DataItem = AddExcDialog.fnClose(self, exc_id)
        if ok:
            DataList[row_index + 1] = DataItem
            DataItemString = self.fnDataListToString(DataList, 'w')
            self.fnSaveDataListToFile(DataItemString, self.strPathExc, 'w')
            self.slotLoadExercises()

    def slotAddUser(self):
        ok, DataItem, row_index = AddUserDialog.fnClose(self, 'None')
        if ok:
            if self.find_id('data/users.txt', DataItem[1]) == "None":
                self.fnCreatePersData(DataItem[0])
                DataList = [DataItem]
                DataItemString = self.fnDataListToString (DataList, 'a')
                print (DataItemString)
                self.fnSaveDataListToFile(DataItemString, 'data/users.txt', 'a')
                self.slotLoadUsers()
            else:
                self.showDialog('This user is already exists')

    def slotEditUser(self):
        user_id = self.find_id('data/users.txt', self.lbLogin.text())
        if user_id != 'None':
            ok, DataItem, row_index = AddUserDialog.fnClose(self, user_id)
            if ok:
                DataList = self.fnLoadFile('data/users.txt')[0]
                DataList[row_index] = DataItem
                DataItemString = self.fnDataListToString (DataList, 'w')
                self.fnSaveDataListToFile(DataItemString, 'data/users.txt', 'w')
                self.slotLoadUsers()

    def slotDeleteUser(self):
        strQuestion = ('Are you want to delete user '
                        +  self.lbLogin.text()
                        + '?')
        choice = self.showDialog(strQuestion)
        if choice == 1024:

            #deleting user
            id_user_list = self.find_id("data/users.txt", self.lbLogin.text())
            id_user_list = [id_user_list]
            OldListUsers = (self.fnLoadFile('data/users.txt'))[0]
            NewListUsers = self.fnDelDataItemByID(id_user_list, 0, OldListUsers)
            NewListUsers = NewListUsers[0]
            strNewListUsers = self.fnDataListToString(NewListUsers)
            self.fnSaveDataListToFile(strNewListUsers, 'data/users.txt')

            #deleting workouts and collecting workouts id
            OldListWorks = (self.fnLoadFile('data/work.txt'))[0]
            NewListWorks = self.fnDelDataItemByID(id_user_list, 1,
                                                    OldListWorks, 0)
            work_id_list = NewListWorks[1]
            NewListWorks = NewListWorks[0]
            strNewListWorks = self.fnDataListToString(NewListWorks)
            self.fnSaveDataListToFile(strNewListWorks, 'data/work.txt')

            #deleting summury and collecting sets ids
            OldListSum = (self.fnLoadFile('data/sum.txt'))[0]
            NewListSum = self.fnDelDataItemByID(work_id_list, 1, OldListSum, 2)
            sets_id_list = NewListSum[1]
            NewListSum = NewListSum[0]
            strNewListSum = self.fnDataListToString(NewListSum)
            self.fnSaveDataListToFile(strNewListSum, 'data/sum.txt')

            #deleting sets
            OldListSets = (self.fnLoadFile('data/sets.txt'))[0]
            NewListSets = self.fnDelDataItemByID(sets_id_list, 0, OldListSets)
            NewListSets = NewListSets[0]
            strNewListSets = self.fnDataListToString(NewListSets)
            self.fnSaveDataListToFile(strNewListSets, 'data/sets.txt')

            #deleting personal files
            os.remove(self.strPathExc)
            os.remove(self.strPathHeaders)

            #post-actions
            self.lbLogin.setText('')
            self.slotLoadUsers()
            self.fnDisable_GUI_Elements()
            self.fnEnable_GUI_Elements(0)

    def fnDeleteWorkout(self, work_id):
        #deleting workouts and collecting workouts id
        work_id = [work_id]
        OldListWorks = (self.fnLoadFile('data/work.txt'))[0]
        NewListWorks = self.fnDelDataItemByID(work_id, 0, OldListWorks)
        work_id_list = NewListWorks[1]
        NewListWorks = NewListWorks[0]
        strNewListWorks = self.fnDataListToString(NewListWorks)
        self.fnSaveDataListToFile(strNewListWorks, 'data/work.txt')

        #deleting summury and collecting sets ids
        OldListSum = (self.fnLoadFile('data/sum.txt'))[0]
        NewListSum = self.fnDelDataItemByID(work_id_list, 1, OldListSum, 2)
        sets_id_list = NewListSum[1]
        NewListSum = NewListSum[0]
        strNewListSum = self.fnDataListToString(NewListSum)
        self.fnSaveDataListToFile(strNewListSum, 'data/sum.txt')

        #deleting sets
        OldListSets = (self.fnLoadFile('data/sets.txt'))[0]
        NewListSets = self.fnDelDataItemByID(sets_id_list, 0, OldListSets)
        NewListSets = NewListSets[0]
        strNewListSets = self.fnDataListToString(NewListSets)
        self.fnSaveDataListToFile(strNewListSets, 'data/sets.txt')


    def slotDeleteWorkout(self):
        row_index = self.tWidget.currentRow()
        work_date = self.tWidget.item(row_index,0).text()
        strQuestion = ('Are you want to delete this workout: '
                        +  work_date
                        + '?')
        choice = self.showDialog(strQuestion)
        if choice == 1024:
            set_id = (self.fnLoadFile('data/temp.txt'))[0][row_index + 1][0]
            DataList = (self.fnLoadFile('data/sum.txt'))[0]
            work_id = self.find_DataItem(DataList, set_id, 2)[1]
            self.fnDeleteWorkout(work_id)

            #post-actions
            self.fnClean('data/temp.txt')
            self.slotReloadLast()

    def slotDelSelectedSet(self):
        row_index = self.tWidget.currentRow()
        row_index = self.tWidget.currentRow()
        set_exc = self.tWidget.item(row_index, 1).text()
        strQuestion = ('Are you want to delete this set: '
                        +  set_exc
                        + '?')
        choice = self.showDialog(strQuestion)
        if choice == 1024:

            set_id = (self.fnLoadFile('data/temp.txt'))[0][row_index + 1][0]
            set_id = [set_id]

            #deleting sets
            OldListSets = (self.fnLoadFile('data/sets.txt'))[0]
            NewListSets = self.fnDelDataItemByID(set_id, 0, OldListSets)
            NewListSets = NewListSets[0]
            strNewListSets = self.fnDataListToString(NewListSets)
            self.fnSaveDataListToFile(strNewListSets, 'data/sets.txt')

            #deleting sum
            OldListSum = (self.fnLoadFile('data/sum.txt'))[0]
            NewListSum = self.fnDelDataItemByID(set_id, 2, OldListSum, 1)
            work_id = NewListSum[1][0]
            print(('work_id :' + str(work_id)))
            NewListSum = NewListSum[0]
            strNewListSum = self.fnDataListToString(NewListSum)
            self.fnSaveDataListToFile(strNewListSum, 'data/sum.txt')

            #post-actions
            self.fnClean('data/temp.txt')
            self.slotReloadLast()

    def slotAddWorkout(self):
        if self.lbLogin.text() != '':
            AddWorkoutWindow.OpenDialog(self, 'None')
            self.slotReloadLast()
        else:
            self.showDialog('Please choose the user')

    def slotEditWorkout(self):
        row_index = self.tWidget.currentRow()
        set_id = (self.fnLoadFile('data/temp.txt'))[0][row_index + 1][0]
        DataList = (self.fnLoadFile('data/sum.txt'))[0]
        work_id = self.find_DataItem(DataList, set_id, 2)[1]
        print((self.fnCreateWorkoutColor(work_id)))

        AddWorkoutWindow.OpenDialog(self, work_id)

        DataList = (self.fnLoadFile('data/temp.txt'))[0]
        try:
            DataList[0][0] == 'old_work'
            DataList[1][0] == 'new_work'
            self.fnDeleteWorkout(DataList[0][1])
        except IndexError:
            print("Workout hasn't been changed")

        self.slotReloadLast()

    def OpenUrl(self, sUrl):
        url = QtCore.QUrl(sUrl)
        QDesktopServices.openUrl(url)

    def slotShowInfo(self):
        sVersion = 'Version: 15.0.0\n'
        sDeveloper = 'Delevoper: EzR1d3r\n'
        sEmail = 'e-mail: brd1080@yandex.ru\n'
        sGitHub = 'https://github.com/EzR1d3r/WorkoutsDiary\n'
        sSupport = 'Suppot the project: https://money.yandex.ru/to/410011144650865\n'
        sInfo = sVersion + sDeveloper + sEmail + sGitHub + sSupport
        mb = QMessageBox(0,'Info',sInfo, QMessageBox.Ok )
        mb.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        return mb.exec_()

    def contextMenuEvent1(self, event):
        rc_menu = QMenu(self)
        rc_menu.addAction(self.excEditAction)
        rc_menu.addAction(self.edit_workoutAction)
        rc_menu.addSeparator()
        rc_menu.addAction(self.workDelAction)
        rc_menu.addAction(self.setDelAction)
        rc_menu.popup(QCursor.pos())


#.....................GUI........................

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        #values
        self.strPathExc = 'data/exercises.txt'
        self.strPathHeaders = 'data/headers.txt'
        self.tempDate = QtCore.QDate.currentDate()

        #calendars
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(1)
        self.calendar.setFixedWidth(300)
        self.calendar.setEnabled(0)
        self.calendar.activated.connect(self.slotCalendarClicked)

        #tables
        self.tWidget = QTableWidget(self)
        self.tWidget.setMinimumHeight(200)
        self.tWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tWidget.customContextMenuRequested.connect(self.contextMenuEvent1)

        #date widget
        self.wFromDate = QDateEdit(QtCore.QDate.currentDate().addDays(-30), self)
        self.wFromDate.dateChanged.connect(self.slotDateChanged)

        self.wToDate = QDateEdit(QtCore.QDate.currentDate(), self)
        self.wToDate.dateChanged.connect(self.slotDateChanged)

        #Actions
        usersAction = QAction(QIcon('icons/users.png'), 'Users', self)
        usersAction.setShortcut('Ctrl+U')
        usersAction.setStatusTip('Open users')
        usersAction.triggered.connect(self.slotLoadUsers)

        self.userDelAction = QAction(QIcon('icons/users_del.png'), 'Delete user', self)
        self.userDelAction.setStatusTip('Delete user')
        self.userDelAction.triggered.connect(self.slotDeleteUser)
        self.userDelAction.setEnabled(0)

        self.userEditAction = QAction(QIcon('icons/user_edit.png'), 'Edit user', self)
        self.userEditAction.setStatusTip('Edit user')
        self.userEditAction.triggered.connect(self.slotEditUser)
        self.userEditAction.setEnabled(0)

        self.workDelAction = QAction(QIcon('icons/the_one_work_del.png'), 'Delete workout', self)
        self.workDelAction.setStatusTip('Delete workout')
        self.workDelAction.triggered.connect(self.slotDeleteWorkout)
        self.workDelAction.setEnabled(0)

        self.setDelAction = QAction(QIcon('icons/set_del.png'), 'Delete set', self)
        self.setDelAction.setStatusTip('Delete set')
        self.setDelAction.triggered.connect(self.slotDelSelectedSet)
        self.setDelAction.setEnabled(0)

        self.showInfo = QAction (QIcon('icons/info.png'),'Info', self)
        self.showInfo.setStatusTip('Info')
        self.showInfo.triggered.connect(self.slotShowInfo)
        self.showInfo.setEnabled(1)

        exercisesAction = QAction(QIcon('icons/exercises.png'), 'Exercises list', self)
        exercisesAction.setShortcut('Ctrl+E')
        exercisesAction.setStatusTip('Open exercises list')
        exercisesAction.triggered.connect(self.slotLoadExercises)

        excAddAction = QAction(QIcon('icons/add_exc.png'), 'Add exercise', self)
        excAddAction.setStatusTip('Add exercise')
        excAddAction.triggered.connect(self.slotAddExercise)

        self.excEditAction = QAction(QIcon('icons/exc_edit.png'), 'Edit exercise', self)
        self.excEditAction.setStatusTip('Edit exercise')
        self.excEditAction.triggered.connect(self.slotEditExercise)
        self.excEditAction.setEnabled(0)

        self.one_workoutAction = QAction(QIcon('icons/the_one_work.png'), 'Load workout', self)
        self.one_workoutAction.setStatusTip('Open workout')
        self.one_workoutAction.triggered.connect(self.slotLoadSelectedWorkout)
        self.one_workoutAction.setEnabled(0)

        self.edit_workoutAction = QAction(QIcon('icons/work_edit.png'), 'Edit workout', self)
        self.edit_workoutAction.setStatusTip('Edit workout')
        self.edit_workoutAction.triggered.connect(self.slotEditWorkout)
        self.edit_workoutAction.setEnabled(0)

        self.all_workoutAction = QAction(QIcon('icons/full_works.png'), 'Load all workouts', self)
        self.all_workoutAction.setStatusTip('Open all workouts')
        self.all_workoutAction.triggered.connect(self.slotLoadAllWorkout)
        self.all_workoutAction.setEnabled(0)

        userAddAction = QAction(QIcon('icons/add_user.png'), 'Add user', self)
        userAddAction.setStatusTip('Add user')
        userAddAction.triggered.connect(self.slotAddUser)

        self.dateFilter = QAction(QIcon('icons/date_filter.png'), 'Filter by dates', self)
        self.dateFilter.setStatusTip('Filter by date')
        self.dateFilter.setCheckable(1)
        self.dateFilter.triggered.connect(self.slotReloadLast)

        self.wordFilter = QAction(QIcon('icons/find.png'), 'Filter by dates', self)
        self.wordFilter.setStatusTip('Filter by date')
        self.wordFilter.setCheckable(1)
        self.wordFilter.toggled.connect(self.slotReloadLast)

        self.PColored = QAction(QIcon('icons/color.png'), 'Paint exercises', self)
        self.PColored.setStatusTip('Paint exercises')
        self.PColored.setCheckable(1)
        self.PColored.setEnabled(0)
        self.PColored.toggled.connect(self.slotReloadLast)

        self.reloadAction = QAction(self)
        self.reloadAction.triggered.connect(self.slotLoadUsers)

        #Toolbars
        self.toolbar = QToolBar('Tool bar', self)
        self.toolbar.setIconSize(QtCore.QSize(25, 30))
        self.toolbar.addAction(usersAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.edit_workoutAction)
        #self.toolbar.addAction(self.one_workoutAction)
        self.toolbar.addAction(self.all_workoutAction)
        self.toolbar.addSeparator()

        self.toolbar2 = QToolBar('Tool bar',self)
        self.toolbar2.setIconSize(QtCore.QSize(25, 30))
        self.toolbar2.addSeparator()
        self.toolbar2.addAction(self.userDelAction)
        self.toolbar2.addAction(self.workDelAction)
        self.toolbar2.addAction(self.setDelAction)
        self.toolbar2.addSeparator()
        self.toolbar2.addAction(self.showInfo)

        self.toolbar4 = QToolBar('Tool bar',self)
        self.toolbar4.addSeparator()
        self.toolbar4.setIconSize(QtCore.QSize(25, 30))
        self.toolbar4.addAction(userAddAction)
        self.toolbar4.addAction(self.userEditAction)
        self.toolbar4.addAction(exercisesAction)
        self.toolbar4.addAction(excAddAction)
        self.toolbar4.addAction(self.excEditAction)
        self.toolbar4.addSeparator()

        self.toolbar5 = QToolBar('Tool bar',self)
        self.toolbar5.setIconSize(QtCore.QSize(25, 30))
        self.toolbar5.addAction(self.wordFilter)
        self.toolbar5.addAction(self.PColored)

        self.toolbar3 = QToolBar('Tool bar',self)
        self.toolbar3.setIconSize(QtCore.QSize(25, 30))
        self.toolbar2.addSeparator()
        self.toolbar3.addAction(self.dateFilter)

        #Labels
        self.lbUser = QLabel(self)
        self.lbUser.setText('User:')

        self.lbLogin = QLabel(self)
        self.lbLogin.setFixedWidth(150)
        self.lbLogin.setText('')
        self.lbLogin.setFont(QFont('Tahoma', 12))

        lbTypeHeaders = QLabel()
        lbTypeHeaders.setText('Headers type:')

        lbWordFilter = QLabel()
        lbWordFilter.setText('Word filter:')

        self.lbFrom = QLabel(self)
        self.lbFrom.setText('From')

        self.lbTo = QLabel(self)
        self.lbTo.setText('To')

        #Combo-boxes
        self.cbHeaders = QComboBox()
        #HeadersNames = self.fnLoadNamesHeaders()
        #self.cbHeaders.addItems(HeadersNames)
        self.cbHeaders.setFixedWidth(130)
        self.cbHeaders.setEnabled(0)
        self.cbHeaders.activated.connect(self.slotSetHeaders)

        #EditLines
        self.tFilter = QLineEdit(self)
        self.tFilter.setToolTip('Type here word or words, splitting by ",".\n Use "++" if you want the result, contains all words.')
        self.tFilter.setFixedSize(175, 25)
        self.tFilter.returnPressed.connect(self.wordFilter.trigger)

        #buttons
        btnAddWork = QPushButton(self)
        btnAddWork.setFixedSize(102, 27)
        btnAddWork.setIcon(QIcon('icons/add.png'))
        btnAddWork.setIconSize(QtCore.QSize(100, 25))
        btnAddWork.setToolTip('Add workout for current user')
        btnAddWork.clicked.connect(self.slotAddWorkout)

        self.btnAddHeaders = QPushButton('+', self)
        self.btnAddHeaders.setFixedSize(20, 20)
        self.btnAddHeaders.setToolTip('Add type of headers')
        self.btnAddHeaders.clicked.connect(self.slotAddHeaders)
        self.btnAddHeaders.setEnabled(0)

        self.btnDelHeaders = QPushButton('-', self)
        self.btnDelHeaders.setFixedSize(20, 20)
        self.btnDelHeaders.setToolTip('Delete current type of headers')
        self.btnDelHeaders.clicked.connect(self.slotDeleteHeaders)
        self.btnDelHeaders.setEnabled(0)

        #layouts
        hLay1 = QHBoxLayout()
        hLay1.addStretch(1)
        hLay1.addWidget(btnAddWork)

        hLay4 = QHBoxLayout()
        hLay4.addWidget(self.lbFrom)
        hLay4.addWidget(self.wFromDate)
        hLay4.addWidget(self.lbTo)
        hLay4.addWidget(self.wToDate)
        hLay4.addWidget(self.toolbar3)

        hLay2 = QHBoxLayout()
        hLay2.addWidget(self.lbUser)
        hLay2.addWidget(self.lbLogin)
        hLay2.addStretch(1)
        hLay2.addWidget(lbTypeHeaders)
        hLay2.addWidget(self.cbHeaders)
        hLay2.addWidget(self.btnAddHeaders)
        hLay2.addWidget(self.btnDelHeaders)
        hLay2.addStretch(1)
        hLay2.addWidget(lbWordFilter)
        hLay2.addWidget(self.tFilter)
        hLay2.addWidget(self.toolbar5)
        hLay2.addStretch(1)
        hLay2.addLayout(hLay4)

        hLay3 = QHBoxLayout()
        hLay3.addWidget(self.toolbar)
        hLay3.addWidget(self.toolbar4)
        hLay3.addWidget(self.toolbar2)
        hLay3.addStretch(1)

        hLay5 = QHBoxLayout()
        hSplit1 = QSplitter(QtCore.Qt.Horizontal)
        hSplit1.addWidget(self.tWidget)
        vSplit1 = QSplitter(QtCore.Qt.Vertical)
        vSplit1.addWidget(self.calendar)
        vSplit1.addWidget(QFrame())
        vSplit1.setCollapsible(0,0)
        hSplit1.addWidget(vSplit1)
        handle0 = hSplit1.handle(1)
        handle0.setStyleSheet("QWidget { background-color: #a9a9a9 }")
        hLay5.addWidget(hSplit1)

        vLay1 = QVBoxLayout()
        vLay1.addLayout(hLay3)

        vLay1.addLayout(hLay2)
        vLay1.addLayout(hLay5)
        vLay1.addLayout(hLay1)
        self.setLayout(vLay1)

        #Right click menu

        #Main window
        self.setGeometry(25, 55, 1150, 600)
        self.setMinimumSize(1100, 500)
        self.setWindowTitle('Дневник тренировок')
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())