import sys
import ast
import operator
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QGridLayout,
    QPushButton,
)


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator")
        self.setGeometry(300, 300, 280, 340)

        self.expression = ""

        layout = QVBoxLayout()

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size: 20px; padding: 5px;")
        layout.addWidget(self.display)

        grid = QGridLayout()
        buttons = [
            "AC", "DEL", "", "",
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            ".", "0", "=", "+",
        ]

        row, col = 0, 0
        for btn_text in buttons:
            if not btn_text:
                col += 1
                if col > 3:
                    col = 0
                    row += 1
                continue

            button = QPushButton(btn_text)
            button.setStyleSheet("font-size: 16px; padding: 10px;")
            button.clicked.connect(self.on_button_click)
            grid.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        layout.addLayout(grid)
        self.setLayout(layout)

    def calculate(self, expression):
        """Hitung ekspresi matematika tanpa menjalankan kode Python sembarang."""
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
                left = evaluate(node.left)
                right = evaluate(node.right)
                return allowed_operators[type(node.op)](left, right)
            if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
                return allowed_operators[type(node.op)](evaluate(node.operand))
            raise ValueError("Ekspresi tidak valid")

        tree = ast.parse(expression, mode="eval")
        return evaluate(tree)

    def on_button_click(self):
        button = self.sender()
        text = button.text()

        if text == "AC":
            self.expression = ""
        elif text == "DEL":
            self.expression = self.expression[:-1]
        elif text == "=":
            try:
                if not self.expression.strip():
                    return
                result = self.calculate(self.expression)
                self.expression = str(result)
            except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError):
                self.expression = "Error"
        else:
            if self.expression == "Error":
                self.expression = ""
            self.expression += text

        self.display.setText(self.expression)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
