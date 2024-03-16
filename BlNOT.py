import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QColorDialog, QMessageBox, QFileDialog
import speech_recognition as sr

class NotepadApp(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = []
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.notes_layout = QVBoxLayout()
        self.layout.addLayout(self.notes_layout)

        add_button = QPushButton('+')
        add_button.clicked.connect(self.add_note)
        
        save_button = QPushButton('Сохранить записи в файл')
        save_button.clicked.connect(self.save_notes)
        
        voice_button = QPushButton('Голосовой ввод')
        voice_button.clicked.connect(self.voice_input)
        
        color_button = QPushButton('Изменить цвет текста')
        color_button.clicked.connect(self.change_text_color)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(voice_button)
        button_layout.addWidget(color_button)

        self.layout.addStretch(1)
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def add_note(self):
        note_input = QTextEdit()
      
        save_button = QPushButton('Сохранить запись')
        save_button.clicked.connect(lambda: self.save_note(note_input))
        
        note_layout = QHBoxLayout()
        note_layout.addWidget(note_input)
        note_layout.addWidget(save_button)

        self.notes_layout.addLayout(note_layout)

    def save_note(self, note_input):
        note_text = note_input.toPlainText()
        self.notes.append(note_text)

    def save_notes(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить файл', '', 'Text Files (*.txt)')
        
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    for note in self.notes:
                        file.write(note + '\n')
                QMessageBox.information(self, 'Успех', 'Записи успешно сохранены в файл')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Ошибка при сохранении файла: {str(e)}')

    def voice_input(self):
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("Скажите что-нибудь...")
            audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio, language='ru-RU')
            self.add_voice_note_to_ui(text)
        except sr.UnknownValueError:
            print("Извините, не удалось распознать речь")
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания речи; {e}")

    def add_voice_note_to_ui(self, text):
        note_input = QTextEdit()
        note_input.setPlainText(text)
        
        save_button = QPushButton('Сохранить запись')
        save_button.clicked.connect(lambda: self.save_note(note_input))
        
        note_layout = QHBoxLayout()
        note_layout.addWidget(note_input)
        note_layout.addWidget(save_button)

        self.notes_layout.addLayout(note_layout)

    def change_text_color(self):
        color = QColorDialog.getColor()
        
        for layout_index in range(self.notes_layout.count()):
            layout_item = self.notes_layout.itemAt(layout_index)
            if layout_item is not None:
                text_edit = layout_item.itemAt(0).widget()  # Получаем QTextEdit из текущего Layout
                text_edit.setTextColor(color)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    notepad_app = NotepadApp()
    notepad_app.show()
    sys.exit(app.exec())
