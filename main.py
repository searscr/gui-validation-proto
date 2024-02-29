import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QFormLayout, QPushButton, QLabel
from PyQt5.QtGui import QDoubleValidator
from base.BaseLineEdit import BaseLineEdit
from base.BaseStatusBar import BaseStatusBar


class SimpleGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create QLineEdit fields
        self.plan_name = BaseLineEdit(required=True, parent=self)
        self.wavelength = BaseLineEdit(required=True, default_value=1.486, parent=self)
        self.symmetry_operations = BaseLineEdit(parent=self)
        self.symmetry_operations.setPlaceholderText('e.g. x,y,z')
        self.plan_name.setToolTip('Enter the name of a reduction plan.\n'
                                  'If the name already exists, the existing plan will be overwritten.')
        self.wavelength.setToolTip('Set the wavelength (in Å) for the PeaksWorkspace,\nthe goniometer'
                                  ' rotation will be calculated when the createPeak method is used.')
        self.symmetry_operations.setToolTip(
            "List of symmetry operations, or a point/space group symbol."
            "\nSee MDNorm algorithm documentation for more information."
        )

        # Set QLineEdit validators
        self.wavelength.setValidator(QDoubleValidator(0, 100, 4))

        # Create QPushButton and set as disabled
        self.button = QPushButton('Run Reduction', self)
        self.button.setEnabled(False)  # Disable the button by default
        self.button.clicked.connect(self.print_text)

        # Create QStatusBar
        self.status_bar = BaseStatusBar(self)

        # Connect textChanged signals to update button state
        self.plan_name.textChanged.connect(self.update_plan_name)
        self.wavelength.textChanged.connect(self.update_wavelength)
        self.symmetry_operations.textChanged.connect(self.update_symmetry_operations)

        # create labels
        label1 = QLabel('Reduction Plan Name *', self)
        label2 = QLabel('Wavelength *', self)
        label3 = QLabel('Symmetry Operations', self)

        # Create form layout
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
            self.plan_name.set_invalid_style()
            error_text = 'Reduction Plan Name: Name is required.'
        elif len(text1) < 6:
            self.plan_name.set_invalid_style()
            error_text = 'Reduction Plan Name: Name must be at least 6 characters long.'
        else:
            self.plan_name.set_empty_style()
            error_text = ''
        self.update_status({self.plan_name: error_text})

    def update_wavelength(self):
        text2 = self.wavelength.text()
        try:
            fl2 = float(text2)
        except ValueError:
            fl2 = 6

        if fl2 > 5 or not text2:
            self.wavelength.set_invalid_style()
            error_text = f"Wavelength: Must be a float less than 5. Current Value ({text2})."
        else:
            self.wavelength.set_empty_style()
            error_text = ''
        self.update_status({self.wavelength: error_text})

    def update_status(self, error_text=None):
        has_invalid = self.status_bar.update_status_label(error_text)
        self.button.setEnabled(not has_invalid)

    def print_text(self):
        text3 = self.symmetry_operations.text()
        if text3 != '' and len(text3.split(',')) < 3:
            self.symmetry_operations.set_invalid_style()
            error_text = 'Symmetry Operations: Must be a valid list of symmetry operations.'
            self.update_status({self.button: error_text})
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle('Invalid Symmetry Operations')
            message_box.setText('Symmetry Operations: Must be a valid list of symmetry operations.')
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec()
        else:
            self.symmetry_operations.set_empty_style()            
            self.status_bar.update_cwe_label('Reduction Complete')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleGUI()
    sys.exit(app.exec_())
