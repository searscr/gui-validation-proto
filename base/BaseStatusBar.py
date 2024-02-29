from PyQt5.QtWidgets import QStatusBar, QLabel


class BaseStatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.error_text = {}
        self.setFixedWidth(600)
        self.cwe_label = QLabel('', self)
        self.status_label = QLabel('', self)
        self.addWidget(self.status_label)
        self.addPermanentWidget(self.cwe_label)

    def update_status_label(self, error_text=None):
        if error_text is not None:
            for entry in error_text.keys():
                self.error_text[entry] = error_text[entry]

        self.error_text = {k: v for k, v in self.error_text.items() if v != ''}
        has_invalid = any(self.error_text.values())
        self.status_label.setText('\n'.join(self.error_text.values()))
        return has_invalid
    
    def update_cwe_label(self, text):
        self.cwe_label.setText(text)