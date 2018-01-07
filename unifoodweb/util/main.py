
import os, sys
# from PyQt5.QtWidgets import *
from db_manager import initialize_dataset, import_dataset
# from sentiment import make_sentiment, parse_format, use_vader
# from pprint import pprint

# class Table(QWidget):
#
#     def __init__(self,select,lables):
#         super().__init__()
#
#         self.initUI(select,lables)
#
#     def loadTable(self,select):
#         return execute_select(select)
#
#     def initUI(self,select,lables):
#         tabView = self.loadTable(select)
#         self.tableWidget = QTableWidget()
#         self.tableWidget.setRowCount(len(tabView))
#         self.tableWidget.setColumnCount(len(tabView[0]))
#         self.tableWidget.setHorizontalHeaderLabels(lables)
#
#         i = 0
#         for view in tabView:
#             a = 0
#             for n in view:
#                 self.tableWidget.setItem(i, a, QTableWidgetItem(str(n)))
#                 a = a+1
#             a = 0
#             i = i+1
#
#         self.layout = QBoxLayout(0)
#         self.layout.addWidget(self.tableWidget)
#         self.setLayout(self.layout)
#
#         self.setGeometry(100, 100, 2000, 1300)
#         self.setWindowTitle('Quit button')
#         self.show()
#
# class Example(QWidget):
#     classifier = 0
#
#     def __init__(self):
#         super().__init__()
#
#         self.initUI()
#
#     def openfile(self):
#         filename = QFileDialog.getOpenFileName()
#         if(filename[0] != ''):
#             import_dataset(filename[0])
#
#     def loadUsers(self):
#         lables = ['userid', 'num_rating', 'av_score', 'var_score']
#         self.nd = Table('SELECT * FROM USERS',lables)
#         self.nd.show()
#
#     def loadRatings(self):
#         lables = ['id', 'productid', 'userid', 'score','text']
#         self.nd = Table('SELECT * FROM RATINGS',lables)
#         self.nd.show()
#
#     def analyze(self):
#         text = self.textbox.text()
#         use_vader(text)
#
#     def trainModel(self):
#         self.classifier = make_sentiment()
#
#     def loadProducts(self):
#         lables = ['productid', 'num_rating', 'av_score', 'var_score']
#         self.nd = Table('SELECT * FROM PRODUCTS',lables)
#         self.nd.show()
#
#     def initUI(self):
#         loadBtn = QPushButton('Import Dataset', self)
#         loadBtn.clicked.connect(self.openfile)
#         loadBtn.resize(loadBtn.sizeHint())
#         loadBtn.move(50, 50)
#         userBtn = QPushButton('Show Users', self)
#         userBtn.clicked.connect(self.loadUsers)
#         userBtn.resize(userBtn.sizeHint())
#         userBtn.move(500, 50)
#         ratingBtn = QPushButton('Show Ratings', self)
#         ratingBtn.clicked.connect(self.loadRatings)
#         ratingBtn.resize(ratingBtn.sizeHint())
#         ratingBtn.move(500, 100)
#         prodButton = QPushButton('Show Products', self)
#         prodButton.clicked.connect(self.loadProducts)
#         prodButton.resize(prodButton.sizeHint())
#         prodButton.move(500, 150)
#         trainButton = QPushButton('Train Model', self)
#         trainButton.clicked.connect(self.trainModel)
#         trainButton.resize(trainButton.sizeHint())
#         trainButton.move(50, 150)
#         self.testButton = QPushButton('Test', self)
#         self.testButton.clicked.connect(self.analyze)
#         self.testButton.resize(self.testButton.sizeHint())
#         self.testButton.move(1100, 300)
#         self.textbox = QLineEdit(self)
#         self.textbox.move(50, 300)
#         self.textbox.resize(1000, 50)
#
#         self.setGeometry(500, 500, 1300, 400)
#         self.setWindowTitle('Quit button')
#         self.show()

########################################
# main #################################
########################################
# if __name__ == '__main__':
#
#     initialize database tables
#     initialize_dataset()
#
#     filename = 'dataset/food.tsv'
#     import_dataset(filename)
#
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())


current_path = os.path.dirname(__file__)
print(current_path)

file = 'food.tsv'
file_path = os.path.join(os.path.dirname(os.path.dirname(current_path)), file)
print(file_path)

initialize_dataset()

import_dataset(file_path)