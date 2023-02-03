from PyQt5.QtWidgets import QPushButton, QDialog, QFileDialog, QDialogButtonBox, QGraphicsScene, QMessageBox
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QListView
from PyQt5 import QtGui, QtCore
from My_merge_window import MyMergeDialog
import Ui_main_window
import os
from Acceptor import *
from History import History
import copy

class NextOptionWidget(QListWidget):
    option_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None) -> None:
        super(NextOptionWidget, self).__init__(parent)
        self.setFlow(QListView.Flow(1))
        self.setIconSize(QtCore.QSize(600, 700))
        self.setViewMode(QListView.IconMode)
        self.setSpacing(30)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(1000, 700)
        self.itemClicked.connect(self.chose_action)

    def add_item(self, img_path, i):
        item = QListWidgetItem(QtGui.QIcon(img_path), str(i))
        self.addItem(item)

    def chose_action(self, item):
        idx = self.row(item)
        self.option_signal.emit(idx)
        self.close()

class MyMainDialog(QDialog, Ui_main_window.Ui_Dialog):
    def __init__(self, parent=None):
        super(MyMainDialog, self).__init__(parent)
        self.setupUi(self)
        self.merge_page = MyMergeDialog()
        self.next_option_page = NextOptionWidget()

        self.preview_button = QPushButton('Merge')
        self.buttonBox.addButton(self.preview_button, QDialogButtonBox.ActionRole)
        self.preview_button.clicked.connect(self.merge_action)

        self.load_button = QPushButton('Load')
        self.buttonBox.addButton(self.load_button, QDialogButtonBox.ActionRole)
        self.load_button.clicked.connect(self.load_action)

        self.back_button = QPushButton('Back')
        self.buttonBox.addButton(self.back_button, QDialogButtonBox.ActionRole)
        self.back_button.clicked.connect(self.back_action)

        self.next_button = QPushButton('Next')
        self.buttonBox.addButton(self.next_button, QDialogButtonBox.ActionRole)
        self.next_button.clicked.connect(self.next_action)

        self.exit_button = QPushButton('Exit')
        self.buttonBox.addButton(self.exit_button, QDialogButtonBox.ActionRole)
        self.exit_button.clicked.connect(self.exit_action)

        self.apta_idx = 0
        self.apta = Acceptor(self.apta_idx)
        self.history = History()

        self.next_option_page.option_signal.connect(self.option_action)
        self.plainTextEdit.returnPressed.connect(self.text_change_action)

        self.k = None

    def k_is_none_info(self):
        if self.k == None:
            QMessageBox.warning(self,"Warn","You have to decide a value of k!", QMessageBox.Ok,QMessageBox.Ok)
            return

    def text_change_action(self):
        if not self.plainTextEdit.text().isdigit():
            return

        self.k = int(self.plainTextEdit.text())
        ktail = self.apta.find_ktail(self.k)
        self.apta.ktail = ktail
    
    def exit_action(self):
        exit(1)

    def merge_action(self):
        self.k_is_none_info()
        if self.history.empty() or self.k == None:
            return

        self.merge_page.comboBox.clear()
        pair, pair_idx = self.apta.equal_pair()
        if len(pair) == 0:
            QMessageBox.information(self,"Info","There is no more k-equivalent nodes.", QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            return

        for i, pair_ in enumerate(pair):
            self.merge_page.comboBox.addItem("(%d, %d) %s" % (pair_[0], pair_[1], pair_idx[i][2]))
        
        self.merge_page.save_pair_idx(pair_idx)
        self.merge_page.merge_signal.connect(self.on_merge_slot)
        self.merge_page.show()

    def on_merge_slot(self, node_pair):
        if self.k == None:
            self.k_is_none_info()
            return

        merged_state_tail_idx, merging_state_tail_idx, edge_tail = node_pair
        self.merge_page = MyMergeDialog() # 析构merge dialog并重新创建

        apta = copy.deepcopy(self.apta)

        apta.merge(merged_state_tail_idx, merging_state_tail_idx, edge_tail)
        apta.apta_idx = self.apta_idx
        apta.draw_tree(merged_state_tail_idx, edge_tail)
        ktail = apta.find_ktail(self.k) # 重新跑一遍ktail 找到可合对
        apta.ktail = ktail

        # self.apta = apta

        back_apta = self.history.get_current_apta() # 之前的apta
        self.history.set_current_apta(apta) # 设置当前的
        self.apta_idx += 1

        self.history.add_back_apta(back_apta, self.k) # 当前的back为之前的
        self.history.add_next_apta(back_apta, self.k)

        scene1 = QGraphicsScene()
        scene1.addPixmap(QtGui.QPixmap(back_apta.get_fig_path()))
        self.graphicsView.setScene(scene1)

        scene2 = QGraphicsScene()
        scene2.addPixmap(QtGui.QPixmap(apta.get_fig_path()))
        self.graphicsView_2.setScene(scene2)

        self.apta = self.history.get_current_apta()
        return

    def load_action(self):
        if self.k == None:
            self.k_is_none_info()
            return

        file_name_choose, _ = QFileDialog.getOpenFileName(self,  
                                    "Choose File",  
                                    './',
                                    "*")

        if file_name_choose == "":
            return

        if os.path.exists('output'):
            os.system("rm -rf output")
    
        os.mkdir('output')

        self.history.clear()
        self.apta_idx = 0
        self.apta = Acceptor(self.apta_idx)

        with open(file_name_choose, 'r') as f:
            self.traces = f.read().split('\n')
        
        self.apta.build_tree(self.traces)
        ktail = self.apta.find_ktail(self.k)
        self.apta.ktail = ktail

        self.apta.draw_tree()
        self.history.set_current_apta(self.apta)
        
        self.apta_idx += 1

        scene = QGraphicsScene()
        self.graphicsView.setScene(scene)

        scene2 = QGraphicsScene()
        scene2.addPixmap(QtGui.QPixmap(self.apta.get_fig_path()))
        self.graphicsView_2.setScene(scene2)

    def option_action(self, idx):
        if self.k == None:
            self.k_is_none_info()
            return

        next_options = self.history.show_next_apta_option(self.k)
        chose_apta = next_options[idx]

        scene1 = QGraphicsScene()
        scene1.addPixmap(QtGui.QPixmap(self.apta.get_fig_path()))
        self.graphicsView.setScene(scene1)

        scene2 = QGraphicsScene()
        scene2.addPixmap(QtGui.QPixmap(chose_apta.get_fig_path()))
        self.graphicsView_2.setScene(scene2)

        self.apta = chose_apta
        self.history.set_current_apta(chose_apta)

    def next_action(self):
        self.k_is_none_info()
        if self.history.empty() or self.k == None:
            return

        next_options = self.history.show_next_apta_option(self.k)
        if next_options == None: # 按next为空 说明当前历史没有后继节点 需要判断是否可以跑ktail
            pair, pair_idx = self.apta.equal_pair()
            if len(pair) == 0:
                return

            apta = copy.deepcopy(self.apta)
            merged_state_tail_idx, merging_state_tail_idx, edge_tail = pair_idx[0]
            apta.merge(merged_state_tail_idx, merging_state_tail_idx, edge_tail)
            apta.apta_idx = self.apta_idx
            apta.draw_tree(merged_state_tail_idx, edge_tail)
            ktail = apta.find_ktail(self.k) # 重新跑一遍ktail 找到可合对
            apta.ktail = ktail

            # self.apta = apta

            back_apta = self.history.get_current_apta() # 之前的apta
            self.history.set_current_apta(apta) # 设置当前的
            self.apta_idx += 1

            self.history.add_back_apta(back_apta, self.k) # 当前的back为之前的
            self.history.add_next_apta(back_apta, self.k)

            scene1 = QGraphicsScene()
            scene1.addPixmap(QtGui.QPixmap(back_apta.get_fig_path()))
            self.graphicsView.setScene(scene1)

            scene2 = QGraphicsScene()
            scene2.addPixmap(QtGui.QPixmap(apta.get_fig_path()))
            self.graphicsView_2.setScene(scene2)
            self.apta = self.history.get_current_apta()
            return

        elif len(next_options) == 1:
            apta = next_options[0]

        else:
            self.next_option_page.clear()
            for i, option_apta in enumerate(next_options):
                self.next_option_page.add_item(option_apta.get_fig_path(), i)
            self.next_option_page.show()

            return

        scene1 = QGraphicsScene()
        scene1.addPixmap(QtGui.QPixmap(self.apta.get_fig_path()))
        self.graphicsView.setScene(scene1)

        scene2 = QGraphicsScene()
        scene2.addPixmap(QtGui.QPixmap(apta.get_fig_path()))
        self.graphicsView_2.setScene(scene2)

        self.apta = apta
        self.history.set_current_apta(apta)

    def back_action(self):
        self.k_is_none_info()
        if self.history.empty() or self.k == None:
            return

        apta = self.history.get_back_apta(self.k)
        if apta == None:
            return

        self.history.set_current_apta(apta)
        self.apta = self.history.get_current_apta()
        scene1 = QGraphicsScene()
        if self.history.get_back_apta(self.k) != None:
            scene1.addPixmap(QtGui.QPixmap(self.history.get_back_apta(self.k).get_fig_path()))
        self.graphicsView.setScene(scene1)

        scene2 = QGraphicsScene()
        scene2.addPixmap(QtGui.QPixmap(self.apta.get_fig_path()))
        self.graphicsView_2.setScene(scene2)