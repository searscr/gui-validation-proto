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
        # Create QLineEdit fields
        self.plan_name = QLineEdit(self)
        self.wavelength = QLineEdit(self)
        self.symmetry_operations = QLineEdit(self)
        self.symmetry_operations.setPlaceholderText('e.g. x,y,z')
        self.plan_name.setToolTip('Enter the name of a reduction plan.\n'
                                  'If the name already exists, the existing plan will be overwritten.')
        self.wavelength.setToolTip('Set the wavelength (in Å) for the PeaksWorkspace,\nthe goniometer'
                                  ' rotation will be calculated when the createPeak method is used.')
        self.symmetry_operations.setToolTip(
            "List of symmetry operations, or a point/space group symbol."
            "\nSee MDNorm algorithm documentation for more information."
        )
        self.status_label = QLabel('', self)

        self.set_required_style(self.plan_name)
        self.set_required_style(self.wavelength)

        self.wavelength.defaultValue = 1.486
        self.wavelength.setValidator(QDoubleValidator(0, 100, 4))
        self.wavelength.setText(str(self.wavelength.defaultValue))

        # Create QPushButton (initially disabled)
        self.button = QPushButton('Run Reduction', self)
        self.button.setEnabled(False)  # Disable the button by default
        self.button.clicked.connect(self.print_text)

        # Create QStatusBar
        self.status_bar = QStatusBar()
        self.status_bar.addWidget(self.status_label)
        self.status_bar.setFixedWidth(600)
        self.error_text = {}

        # Connect textChanged signals to update button state
        self.plan_name.textChanged.connect(self.update_plan_name)
        self.wavelength.textChanged.connect(self.update_wavelength)
        self.symmetry_operations.textChanged.connect(self.update_symmetry_operations)

        # create labels
        label1 = QLabel('Reduction Plan Name *', self)
        label2 = QLabel('Wavelength *', self)
        label3 = QLabel('Symmetry Operations', self)

        form_layout = QFormLayout()
        form_layout.addRow(label1, self.plan_name)
        form_layout.addRow(label2, self.wavelength)
        form_layout.addRow(label3, self.symmetry_operations)
        form_layout.addRow(self.button)
        form_layout.addRow(self.status_bar)

        self.setLayout(form_layout)

        self.setWindowTitle('Demo PyQT Validation GUI')
        self.show()

    def update_symmetry_operations(self):
        self.update_status({self.symmetry_operations: '', self.button: ''})

    def update_plan_name(self):
        text1 = self.plan_name.text()
        if not text1:
            self.set_invalid_style(self.plan_name)
            error_text = 'Reduction Plan Name: Name is required.'
        elif len(text1) < 6:
            self.set_invalid_style(self.plan_name)
            error_text = 'Reduction Plan Name: Name must be at least 6 characters long.'
        else:
            self.set_valid_style(self.plan_name)
            error_text = ''
        self.update_status({self.plan_name: error_text})

    def update_wavelength(self):
        text2 = self.wavelength.text()
        try:
            fl2 = float(text2)
        except ValueError:
            fl2 = self.wavelength.defaultValue

        if fl2 != self.wavelength.defaultValue and fl2 > 5 or not text2:
            self.set_invalid_style(self.wavelength)
            error_text = f"Wavelength: Must be less than 5. Current Value ({text2})."
        else:
            self.set_valid_style(self.wavelength)
            error_text = ''
        self.update_status({self.wavelength: error_text})

    def set_invalid_style(self, item):
        item.setStyleSheet(INVALID_QLINEEDIT)

    def set_valid_style(self, item):
        item.setStyleSheet('')

    def set_required_style(self, item):
        item.setStyleSheet(REQUIRED_QLINEEDIT)

    def update_status(self, error_text=None):
        has_invalid = self.update_status_label(error_text)
        self.update_button_state(has_invalid)

    def update_button_state(self, has_invalid):
        self.button.setEnabled(not has_invalid)

    def update_status_label(self, error_text=None):
        if error_text is not None:
            for entry in error_text.keys():
                self.error_text[entry] = error_text[entry]

        self.error_text = {k: v for k, v in self.error_text.items() if v != ''}
        has_invalid = any(self.error_text.values())
        self.status_label.setText('\n'.join(self.error_text.values()))
        return has_invalid

    def print_text(self):
        text3 = self.symmetry_operations.text()
        if text3 != '' and len(text3.split(',')) < 3:
            self.set_invalid_style(self.symmetry_operations)
            error_text = 'Symmetry Operations: Must be a valid list of symmetry operations.'
            self.update_status({self.button: error_text})
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle('Invalid Symmetry Operations')
            message_box.setText('Symmetry Operations: Must be a valid list of symmetry operations.')
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec()
        else:
            self.set_valid_style(self.symmetry_operations)
            self.update_status()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleGUI()
    sys.exit(app.exec_())
