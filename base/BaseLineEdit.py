from PyQt5.QtWidgets import QLineEdit

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

class BaseLineEdit(QLineEdit):
    def __init__(self, required = False, default_value = None, parent=None):
        super().__init__(parent)
        self.required = required
        self.default_value = default_value
        if default_value is not None:
            self.setText(str(default_value))
        self.reset_style()
        
    def set_invalid_style(self):
        self.setStyleSheet(INVALID_QLINEEDIT)
    
    def set_required_style(self):
        self.setStyleSheet(REQUIRED_QLINEEDIT)
    
    def set_empty_style(self):
        self.setStyleSheet('')

    def reset_style(self):
        if self.required:
            self.set_required_style()
        else:
            self.set_empty_style()