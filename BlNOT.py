from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.filechooser import FileChooserListView
import speech_recognition as sr
import pyperclip


class Notepad(App):
    def build(self):
        self.title = 'Простой блокнот на Kivy'

        # Создание текстового поля
        self.text_input = TextInput(size_hint=(1, 0.8))

        # Создание кнопки "Сохранить"
        save_button = Button(text='Сохранить', size_hint=(0.3, 0.1), on_press=self.save_text)

        # Создание кнопки "Удалить"
        delete_button = Button(text='Удалить', size_hint=(0.3, 0.1), on_press=self.delete_text)

        # Создание кнопки "Голосовой ввод"
        voice_input_button = Button(text='Голосовой ввод', size_hint=(0.3, 0.1), on_press=self.voice_input)

        # Создание кнопки "Контекстное меню"
        context_menu_button = Button(text='Контекстное меню', size_hint=(0.3, 0.1), on_press=self.show_context_menu)

        # Создание кнопки "Выбрать цвет текста"
        color_picker_button = Button(text='Выбрать цвет текста', size_hint=(0.3, 0.1), on_press=self.show_color_picker)

        # Создание кнопки "Сохранить через FilePicker"
        file_picker_button = Button(text='Сохранить через FilePicker', size_hint=(0.3, 0.1), on_press=self.save_with_file_picker)

        # Создание главного макета
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.text_input)

        # Создание макета для кнопок
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
        buttons_layout.add_widget(save_button)
        buttons_layout.add_widget(delete_button)
        buttons_layout.add_widget(voice_input_button)
        buttons_layout.add_widget(context_menu_button)
        buttons_layout.add_widget(color_picker_button)
        buttons_layout.add_widget(file_picker_button)
        layout.add_widget(buttons_layout)

        return layout

    # Метод для сохранения текста в файл
    def save_text(self, instance):
        filename = "saved_text.txt"
        with open(filename, 'w') as f:
            f.write(self.text_input.text)

    # Метод для удаления текста из поля ввода
    def delete_text(self, instance):
        self.text_input.text = ''

    # Метод для голосового ввода текста
    def voice_input(self, instance):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Говорите что-нибудь...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            self.text_input.text += text
        except sr.UnknownValueError:
            print("Голос не распознан")
        except sr.RequestError as e:
            print("Ошибка сервиса распознавания: {0}".format(e))

    # Метод для отображения контекстного меню
    def show_context_menu(self, instance):
        text_from_clipboard = pyperclip.paste()
        self.text_input.text += text_from_clipboard

    # Метод для отображения палитры выбора цвета текста
    def show_color_picker(self, instance):
        color_picker = ColorPicker()
        color_popup = Popup(title='Выберите цвет текста', content=color_picker, size_hint=(None, None), size=(400, 400))
        color_picker.bind(color=self.set_text_color)
        color_popup.open()

    # Метод для установки цвета текста
    def set_text_color(self, instance, color):
        self.text_input.foreground_color = color

    # Метод для сохранения текста в файл через FilePicker
    def save_with_file_picker(self, instance):
        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=self.save_file)
        popup = Popup(title='Выберите файл для сохранения', content=file_chooser, size_hint=(None, None), size=(400, 400))
        popup.open()

    # Метод для сохранения текста в выбранный файл
    def save_file(self, instance, file_path, file_name):
        with open(file_path, 'w') as f:
            f.write(self.text_input.text)


if __name__ == '__main__':
    Notepad().run()
