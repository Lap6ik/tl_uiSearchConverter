#!/usr/bin/env python
from PySide2 import QtWidgets, QtGui, QtCore
import os, sys
#import shutil
import subprocess
from importlib import reload
#from pathlib import Path


import uiSearchConverterUI as ui
reload(ui)
            
class UiSearchConverter(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(UiSearchConverter, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.devPath = '/home/explosiveprogrammers/Dev'
        self.uiFilePath = None

        self.__buildUI()
        
    def __buildUI(self):
        '''
        Function used to build the UI. All the signal, slot and default state are initialized here
        '''  
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)

        #fill the buttons  - we don't fill the buttons, don't have comboboxes
        self.ui.convertUiBtn.setEnabled(False)  
        self.bg = QtWidgets.QButtonGroup()
        self.bg.addButton(self.ui.sameFolderCheckBox,1)
        self.bg.addButton(self.ui.parentFolderCheckBox,1)
         
        # -------Signals-------------#   
        self.ui.openFileDialogBtn.clicked.connect(self._fileDialogOpen)
        self.bg.buttonClicked.connect(self._enableConvertUiBtn)
        self.ui.convertUiBtn.clicked.connect(self.__convertUI) 


    def _fileDialogOpen(self):
        '''
        Function opens Filedialog from which only .ui files can be selected. Updates the text edit 
            with selected .ui file path
        '''
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, None, self.devPath, "UI files (*.ui)")
        self.uiFilePath = dialog[0]
        self.ui.uiPathTextEdit.setText(self.uiFilePath)
    
    def _enableConvertUiBtn(self):
        self.ui.convertUiBtn.setEnabled(True)
        print ('convertUIBtn enabled')
        

    def __convertUI(self):
        '''
        The function defines the python file path based on selected by user options(checkBoxes) and
            writes the .py file based on the .ui file 
        '''
        print ('UI file path: %s'%self.uiFilePath)
        dirUI = os.path.dirname(self.uiFilePath)
      
        if self.ui.sameFolderCheckBox.isChecked():
            pyFilePath = self.uiFilePath.replace('.ui','.py')
            print ('Py file path will be: %s'%pyFilePath)

        elif self.ui.parentFolderCheckBox.isChecked():
            dirPy = dirUI.rpartition('/')[0]
            uiFileSplit = self.uiFilePath.rpartition('/')[-1]
            pyFileName = uiFileSplit.replace('.ui','.py')
            pyFilePath = ('%s/%s'%(dirPy,pyFileName))
            print ('Py file path will be: %s'%pyFilePath)
        
        proc = subprocess.call('pyside2-uic %s -o %s'%(self.uiFilePath, pyFilePath), shell = True)
        #checking that pyside-uic works from shell:   
        #proc = subprocess.call('pyside2-uic --help', shell = True)
        #proc = subprocess.call('pwd >> file.txt', Shell = True)
        #print (type(proc))
        #print (proc)

        print ('%s  - Done'%pyFilePath)

def main():
    '''
    Main function for starting the application
    '''

    app = QtWidgets.QApplication(sys.argv)
    widget = UiSearchConverter()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
        main()
