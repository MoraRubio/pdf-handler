from main import *
from pdf2image import convert_from_path
from numpy import ceil
from os import getcwd

from window_ui import *
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PIL.ImageQt import ImageQt, toqpixmap

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.paths = []
        self.destination = getcwd()
        self.pushButton_choosefile.clicked.connect(self.choose_files) 
        self.pushButton_clear.clicked.connect(self.clear_files)  
        self.pushButton_merge.clicked.connect(self.merge_files) 
        self.pushButton_split.clicked.connect(self.split_files) 
        self.pushButton_reorganize.clicked.connect(self.reorganize_file)
        self.pushButton.clicked.connect(self.choose_destination)
        self.listWidget_files.itemSelectionChanged.connect(self.show_pages)
        self.label_3.setText(self.destination)

        self.msg = QMessageBox()
        self.msg.setWindowTitle('Confirmar orden seleccionado')
        self.msg.setIcon(QMessageBox.Question)
        self.msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Retry)
        self.msg.setDefaultButton(QMessageBox.Ok)
    
    def clear_files(self):
        self.listWidget_files.clear()

    def choose_files(self):
        paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, 'OpenFile', '*.pdf')
        self.listWidget_files.addItems([get_filename(path) for path in paths])
        self.paths.extend(paths)

    def choose_destination(self):
        self.destination = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        self.label_3.setText(self.destination)

    def merge_files(self):
        ordered_paths = []
        for filename in [self.listWidget_files.item(x).text() for x in range(self.listWidget_files.count())]:
            ordered_paths.append(next(path for path in self.paths if filename in path))
        merge(ordered_paths, self.destination)
        self.paths = ordered_paths.copy()
        self.msg_completed()

    def split_files(self):
        for path in self.paths:
            split(path, self.destination)
        self.msg_completed()

    def reorganize_file(self):
        self.msg.setText('El orden seleccionado es: '+', '.join([item.text() for item in self.listWidget.selectedItems()]))
        x = self.msg.exec_()
        if str(x) == '1024':
            reorganize(self.paths[self.listWidget_files.currentRow()],
                       [int(item.text()[-1]) for item in self.listWidget.selectedItems()],
                       self.destination)
            self.msg_completed()
        else:
            pass
    
    def msg_completed(self):
        msg_completed = QMessageBox()
        msg_completed.setWindowTitle('Operación completada')
        msg_completed.setIcon(QMessageBox.Information)
        msg_completed.setText('Operación completada!')
        msg_completed.setStandardButtons(QMessageBox.Ok)
        msg_completed.exec_()

    def show_pages(self):
        self.listWidget.clear()
        self.clean_layout()
        ordered_paths = []
        for filename in [self.listWidget_files.item(x).text() for x in range(self.listWidget_files.count())]:
            ordered_paths.append(next(path for path in self.paths if filename in path))
        images = convert_from_path(ordered_paths[self.listWidget_files.currentRow()])
        self.plot_images(images)
        self.listWidget.addItems([f'Página {str(n+1)}' for n in range(len(images))])

    def clean_layout(self):
        for i in reversed(range(self.gridLayout.count())): 
            temp = self.gridLayout.itemAt(i).layout()
            while temp.count():
                temp.takeAt(0).widget().setParent(None)
    
    def plot_images(self, images):
        n_images = len(images)
        i, j = 0, 0
        for n, image in enumerate(images):
            img_label = QLabel()
            text_label = QLabel()
            img_label.setAlignment(Qt.AlignCenter)
            text_label.setAlignment(Qt.AlignCenter)
            img_label.setMargin(0)
            text_label.setMargin(0)
            qim = ImageQt(image)
            pixmap = QPixmap.fromImage(qim)
            pixmap = pixmap.scaled(QSize(1500, 300), 1, 1)
            img_label.setPixmap(pixmap)
            text_label.setText(f'Página {str(n+1)}')
            thumbnail = QVBoxLayout()
            thumbnail.addWidget(img_label)
            thumbnail.addWidget(text_label)
            self.gridLayout.addLayout(thumbnail, i, j)            
            j+=1
            if n_images>4 and n_images<12:
                top = ceil(n_images/2).astype(int)
            elif n_images<=4:
                top = n_images
            else:
                top = 6
            if j==top:
                j=0
                i+=1

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()