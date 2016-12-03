import pickle
import re

from PyQt4 import QtCore, QtGui
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def load_obj(name):
	with open('Database/' + name + '.pkl','rb') as f:
		return pickle.load(f)

dicto = load_obj('dicto_phrase')
ranks = load_obj('ranks')

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(594, 394)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.item = QtGui.QListWidgetItem()
        self.verticalLayout.addWidget(self.listWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("Search Engine", "Search Engine", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:72pt; font-weight:600;\">SEARCH</span></p></body></html>", None))
        #self.lineEdit.setToolTip(_translate("MainWindow", "<html><head/><body><p>Search for a word</p></body></html>", None))
        self.lineEdit.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Search for a word</p></body></html>", None))
        self.pushButton.setText(_translate("MainWindow", "Search", None))
        MainWindow.show()
        self.pushButton.connect(self.pushButton, SIGNAL("clicked()"),self.linedit)

    def linedit(self):
        realQ = self.lineEdit.text()
        ip = realQ.lower()
        buttonclicked(self,ip,realQ)

def one_word_query(wordquery):
    pattern = re.compile('[\W_]+')
    wordquery = pattern.sub('',wordquery)
    result = []
    if(wordquery not in dicto):
        return result
    else:
        result = dicto[wordquery].keys()
        return list(result)

def standard_query(query):
    pattern = re.compile('[\W_]+')
    query = pattern.sub(' ',query)
    all_words_list = []
    for word in query.split():
        all_words_list.append(one_word_query(word))
    result = set(all_words_list[0]).intersection(*all_words_list)
    return list(result)

def phrase_query(query):
    pattern = re.compile('[\W_]+')
    query = pattern.sub(' ',query)
    query_list = query.split()

    if len(query_list) == 1:
        return one_word_query(query)

    all_words_list,result = [],[]
    for word in query_list:
        all_words_list.append(one_word_query(word))
    intersect = set(all_words_list[0]).intersection(*all_words_list)
    for filename in intersect:
        temp = []
        for word in query_list:
            temp.append(dicto[word][filename][:])
        for i in range(len(temp)):
            for ind in range(len(temp[i])):
                temp[i][ind] -= i
        if set(temp[0]).intersection(*temp):
            result.append(filename)
    return result

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
    return K

def compare(a,b):
    if(ranks[a] < ranks[b]):
        return 1
    elif(ranks[a] == ranks[b]):
        return 0
    else:
        return -1

def buttonclicked(object,ip,realQ):

    object.listWidget.clear()
    object.item = QListWidgetItem("%s" % "Results for '" + realQ + "'  :-")
    object.listWidget.addItem(object.item)
    
    ip_list = ip.split()
    result = []
    
    if(len(ip_list) > 1 and not ip.startswith('"')):
        result = standard_query(ip)
    elif (len(ip_list) == 1 and not ip.startswith('"')):
        result = one_word_query(ip)
    elif (len(ip_list) >= 1 and ip.startswith('"')):
        result = phrase_query(ip)

    if(len(result) == 0):
        object.item = QListWidgetItem("%s" % "Your search '" + realQ + "' did not match any documents!")
        object.listWidget.addItem(object.item)
    else:
        result.sort(key = cmp_to_key(compare))
        object.item = QListWidgetItem("%s" % "No. of results found: " + str(len(result)))
		#object.item.setFont(QtGui.QFont.setBold('Verdana',1))
        object.listWidget.addItem(object.item)
        for name in result:
            object.item = QListWidgetItem("%s" % 'https://en.wikipedia.org'+ name)
            object.listWidget.addItem(object.item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMainWindow()
    window = Ui_MainWindow()
    window.setupUi(win)
    sys.exit(app.exec_())
