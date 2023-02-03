import Ui_merge_window
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog

class MyMergeDialog(QDialog, Ui_merge_window.Ui_Form):
    merge_signal = QtCore.pyqtSignal(tuple)

    def __init__(self, parent=None):
        super(MyMergeDialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.ok_action)

    def ok_action(self) -> None:
        chose_idx = self.get_node_pair()
        self.merge_signal.emit(self.pair_idx[chose_idx])
        self.close()
    
    def get_node_pair(self):
        chose_idx = int(self.comboBox.currentIndex())
        return chose_idx
    
    def save_pair_idx(self, pair_idx):
        self.pair_idx = pair_idx