import sys
import speech_recognition as sr
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QComboBox
from PyQt6.QtGui import QTextCursor
import pyttsx3

class Notepad(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = []
        layout = QVBoxLayout()

        self.input_text = QTextEdit()
        layout.addWidget(self.input_text)

        button_layout = QHBoxLayout()

        add_button = QPushButton('Добавить запись')
        add_button.clicked.connect(self.add_note)
        button_layout.addWidget(add_button)

        delete_button = QPushButton('Удалить запись')
        delete_button.clicked.connect(self.delete_note)
        button_layout.addWidget(delete_button)

        edit_button = QPushButton('Вставить запись')
        edit_button.clicked.connect(self.edit_note)
        button_layout.addWidget(edit_button)

        clear_button = QPushButton('Очистить текст')
        clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(clear_button)

        color_dropdown = QComboBox()
        colors = ['red', 'green', 'blue', 'yellow', 'purple']
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

    def edit_note(self):
        # Реализация редактирования записи из базы данных
        pass

    def clear_text(self):
        self.input_text.clear()

    def apply_color(self, color):
        selected_text = self.input_text.textCursor().selectedText()
        if selected_text:
            color_code = {'red': '#FF0000', 'green': '#00FF00', 'blue': '#0000FF',
                          'yellow': '#FFFF00', 'purple': '#800080'}
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
