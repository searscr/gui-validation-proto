import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QFormLayout, QLineEdit, QPushButton, QStatusBar, QLabel
from PyQt5.QtGui import QDoubleValidator

INVALID_QLINEEDIT = """
QLineEdit {
border-color: red;
border-style: outset;
border-width: 2px;
border-radius: 4px;
padding-left: -1px;
padding-right: -1px;
padding-top: 1px;
padding-bottom: 1px;
}
"""

REQUIRED_QLINEEDIT = """
QLineEdit {
background-color: lightyellow;
}
"""


class SimpleGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.required_items = []
        self.error_text = {}

        # Create QLineEdit fields
        self.lineEdit1 = QLineEdit(self)
        self.lineEdit2 = QLineEdit(self)
        self.lineEdit3 = QLineEdit(self)
        self.lineEdit3.setPlaceholderText('e.g. x,y,z')
        self.lineEdit1.setToolTip('Enter the name of a reduction plan.\n'
                                  'if the name already exists, the existing plan will be overwritten.')
        self.lineEdit2.setToolTip('Set the wavelength (in Å) for the PeaksWorkspace,\nthe goniometer'
                                  ' rotation will be calculated when the createPeak method is used.')
        self.lineEdit3.setToolTip(
            "List of symmetry operations, or a point/space group symbol."
            "\nSee MDNorm algorithm documentation for more information."
        )
        self.status_label = QLabel('', self)
        

        self.set_required_style(self.lineEdit1)
        self.set_required_style(self.lineEdit2)

        self.lineEdit2.defaultValue = 1.486
        self.lineEdit2.setValidator(QDoubleValidator(0, 100, 4))
        self.lineEdit2.setText(str(self.lineEdit2.defaultValue))

        # Create QPushButton (initially disabled)
        self.button = QPushButton('Run Reduction', self)
        self.button.setEnabled(False)  # Disable the button by default
        self.button.clicked.connect(self.print_text)

        # Create QStatusBar
        self.status_bar = QStatusBar()
        self.status_bar.addWidget(self.status_label)
        # self.status_bar.setStyleSheet('QStatusBar{border-top: 1px solid #000000;}')
        self.status_bar.setFixedWidth(600)


        # Connect textChanged signals to update button state
        self.lineEdit1.textChanged.connect(self.update_name_le)
        self.lineEdit2.textChanged.connect(self.update_wavelength)
        self.lineEdit3.textChanged.connect(self.update_symmetry_operations)

        # create labels
        label1 = QLabel('Reduction Plan Name *', self)
        label2 = QLabel('Wavelength *', self)
        label3 = QLabel('Symmetry Operations', self)

        
        # self.setLayout(vbox)
        form_layout = QFormLayout()
        form_layout.addRow(label1, self.lineEdit1)
        form_layout.addRow(label2, self.lineEdit2)
        form_layout.addRow(label3, self.lineEdit3)
        form_layout.addRow(self.button)
        form_layout.addRow(self.status_bar)

        self.setLayout(form_layout)

        self.setWindowTitle('Simple PyQt GUI')
        self.show()

    def update_symmetry_operations(self):
        self.update_status({self.lineEdit3: '', self.button: ''})

    def update_name_le(self):
        if self.lineEdit1.text() == '':
            self.set_invalid_style(self.lineEdit1)
            error_text = 'Reduction Plan Name: Name is required.'
        else:
            if len(self.lineEdit1.text()) < 6:
                self.set_invalid_style(self.lineEdit1)
                error_text = 'Reduction Plan Name: Name must be at least 6 characters long.'
            else:
                self.set_valid_sytle(self.lineEdit1)
                error_text = ''
        self.update_status({self.lineEdit1: error_text})

    def update_wavelength(self):
        text2 = self.lineEdit2.text()
        fl2 = self.lineEdit2.defaultValue
        try:
            fl2 = float(text2)
        except ValueError:
            pass

        if (fl2 != self.lineEdit2.defaultValue and fl2 > 5) or text2 == '':
            self.set_invalid_style(self.lineEdit2)
            error_text = f"Wavelength: Must be less than 5 Current Value ({self.lineEdit2.text()})."
        else:
            self.set_valid_sytle(self.lineEdit2)
            error_text = ''
        self.update_status({self.lineEdit2: error_text})

    def set_invalid_style(self, item):
        item.setStyleSheet(INVALID_QLINEEDIT)

    def set_valid_sytle(self, item):
        item.setStyleSheet('')

    def set_required_style(self, item):
        item.setStyleSheet(REQUIRED_QLINEEDIT)

    def update_status(self, error_text=None):
        has_invalid = self.update_status_label(error_text)
        self.update_button_state(has_invalid)

    def update_button_state(self, has_invalid):
        if has_invalid:
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def update_status_label(self, error_text=None):
        # Update self.error_text with the incoming error_text
        if error_text is not None:
            for entry in error_text.keys():
                self.error_text[entry] = error_text[entry]

        # Remove items where the value is ''
        self.error_text = {k: v for k, v in self.error_text.items() if v != ''}

        # Check if any values in self.error_text are non-empty
        has_invalid = any(self.error_text.values())

        # Set the text of the status label
        self.status_label.setText('\n'.join(self.error_text.values()))

        return has_invalid

    def print_text(self):
        
        text3 = self.lineEdit3.text()
        if text3 != '' and len(text3.split(',')) < 3:
            self.set_invalid_style(self.lineEdit3)
            error_text = 'Symmetry Operations: Must be a valid list of symmetry operations.'
            self.update_status({self.button: error_text})
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setWindowTitle('Invalid Symmetry Operations')
            messageBox.setText('Symmetry Operations: Must be a valid list of symmetry operations.')
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.exec()
        else:
            self.set_valid_sytle(self.lineEdit3)
            self.update_status()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleGUI()
    sys.exit(app.exec_())
