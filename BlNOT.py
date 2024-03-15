import sys
import speech_recognition as sr
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QComboBox
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QPoint
import sqlite3
class Notepad(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = []
        self.initUI()
        self.create_db()

    def initUI(self):
        layout = QVBoxLayout()

        self.input_text = QTextEdit()
        layout.addWidget(self.input_text)

        button_layout = QHBoxLayout()

        add_button = QPushButton('Добавить запись')
        add_button.clicked.connect(self.add_note)
        button_layout.addWidget(add_button)

        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(self.save_notes)
        button_layout.addWidget(save_button)

        clear_button = QPushButton('Очистить текст')
        clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def create_db(self):
        self.connection = sqlite3.connect('notes.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, text TEXT)')

    def add_note(self):
        note = self.input_text.toPlainText()
        self.notes.append(note)
        self.input_text.clear()

    def save_notes(self):
        for note in self.notes:
            self.save_to_db(note)
        self.notes.clear()

    def save_to_db(self, note):
        self.cursor.execute('INSERT INTO notes (text) VALUES (?)', (note,))
        self.connection.commit()

    def clear_text(self):
        self.input_text.clear()
class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.last_point = QPoint()
        self.current_point = QPoint()
        self.drawing = False
        self.lines = []

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_point = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.drawing:
            self.current_point = event.pos()
            self.lines.append((self.last_point, self.current_point))
            self.last_point = self.current_point
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setColor(QColor(Qt.GlobalColor.black))
        pen.setWidth(2)
        painter.setPen(pen)

        for line in self.lines:
            painter.drawLine(line[0], line[1])

class Notepad(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = []
        layout = QVBoxLayout()

        self.input_text = QTextEdit()
        layout.addWidget(self.input_text)

        self.drawing_widget = DrawingWidget()
        layout.addWidget(self.drawing_widget)

        button_layout = QHBoxLayout()

        clear_button = QPushButton('Очистить рисунок')
        clear_button.clicked.connect(self.clear_drawing)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def clear_drawing(self):
        self.drawing_widget.lines.clear()
        self.drawing_widget.update()

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.last_point = None
        self.painting = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(Qt.GlobalColor.black))
        painter.drawLine(self.last_point, event.pos() if self.last_point else event.pos())

    def mousePressEvent(self, event):
        self.last_point = event.pos()
    
    def mouseMoveEvent(self, event):
        self.update()

    def mouseReleaseEvent(self, event):
        self.last_point = None
        self.update()

class Notepad(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = []
        layout = QVBoxLayout()

        self.input_text = QTextEdit()
        layout.addWidget(self.input_text)

        self.drawing_widget = DrawingWidget()
        layout.addWidget(self.drawing_widget)

        button_layout = QHBoxLayout()

        add_button = QPushButton('Добавить запись')
        add_button.clicked.connect(self.add_note)
        button_layout.addWidget(add_button)

        clear_button = QPushButton('Очистить текст')
        clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(clear_button)

        color_dropdown = QComboBox()
        colors = ['Красный', 'Зелёный', 'Синий', 'Жёлтый', 'Пурпурный']
        color_dropdown.addItems(colors)
        color_dropdown.currentTextChanged.connect(self.apply_color)
        button_layout.addWidget(color_dropdown)

        voice_button = QPushButton('Голос')
        voice_button.clicked.connect(self.voice_input)
        button_layout.addWidget(voice_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def add_note(self):
        note = self.input_text.toPlainText()
        self.save_to_db(note)
        self.input_text.clear()

    def delete_note(self):
        # Реализация удаления записи из базы данных
        pass

    def clear_text(self):
        self.input_text.clear()

    def apply_color(self, color):
        selected_text = self.input_text.textCursor().selectedText()
        if selected_text:
            color_code = {'Красный': '#FF0000', 'Зелёный': '#00FF00', 'Синий': '#0000FF',
                          'Жёлтый': '#FFFF00', 'Пурпурный': '#800080'}
            new_text = f'<font color="{color_code[color]}">{selected_text}</font>'
            cursor = self.input_text.textCursor()
            cursor.insertHtml(new_text)

    def save_to_db(self, note):
        # Реализация сохранения записи в базу данных
        pass

    def voice_input(self):
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("Скажите что-нибудь:")
            audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio, language='ru-RU')
            cursor = self.input_text.textCursor()
            cursor.insertText(text)
        
        except sr.UnknownValueError:
            print("Извините, не удалось распознать речь")
        
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    notepad = Notepad()
    notepad.show()
    sys.exit(app.exec())
