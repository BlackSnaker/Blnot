from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
import speech_recognition as sr
import pyperclip


class FunctionsTab(TabbedPanelHeader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Функции"
        self.content = BoxLayout(orientation='vertical', spacing=10)
        self.add_buttons()

    def add_buttons(self):
        # Создание кнопок для вкладки "Функции"
        save_button = Button(text='Сохранить', size_hint=(1, None), height=50, background_color=(0.3, 0.7, 0.5, 1))
        delete_button = Button(text='Удалить', size_hint=(1, None), height=50, background_color=(0.9, 0.2, 0.2, 1))
        voice_input_button = Button(text='Голосовой ввод', size_hint=(1, None), height=50, background_color=(0.5, 0.5, 0.8, 1))
        context_menu_button = Button(text='Вставить текст', size_hint=(1, None), height=50, background_color=(0.7, 0.7, 0.7, 1))
        color_picker_button = Button(text='Выбрать цвет текста', size_hint=(1, None), height=50, background_color=(0.9, 0.5, 0.1, 1))
        file_picker_button = Button(text='Сохранить в файлы', size_hint=(1, None), height=50, background_color=(0.2, 0.7, 0.9, 1))

        # Привязка кнопок к функциям
        save_button.bind(on_press=self.save_text)
        delete_button.bind(on_press=self.delete_text)
        voice_input_button.bind(on_press=self.voice_input)
        context_menu_button.bind(on_press=self.show_context_menu)
        color_picker_button.bind(on_press=self.show_color_picker)
        file_picker_button.bind(on_press=self.save_with_file_picker)

        # Добавление кнопок в контент вкладки
        self.content.add_widget(save_button)
        self.content.add_widget(delete_button)
        self.content.add_widget(voice_input_button)
        self.content.add_widget(context_menu_button)
        self.content.add_widget(color_picker_button)
        self.content.add_widget(file_picker_button)

    # Метод для сохранения текста в файл
    def save_text(self, instance):
        filename = "saved_text.txt"
        with open(filename, 'w') as f:
            f.write(App.get_running_app().text_input.text)

    # Метод для удаления текста из поля ввода
    def delete_text(self, instance):
        App.get_running_app().text_input.text = ''

    # Метод для голосового ввода текста
    def voice_input(self, instance):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Говорите что-нибудь...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            App.get_running_app().text_input.text += text
        except sr.UnknownValueError:
            print("Голос не распознан")
        except sr.RequestError as e:
            print("Ошибка сервиса распознавания: {0}".format(e))

    # Метод для отображения контекстного меню
    def show_context_menu(self, instance):
        text_from_clipboard = pyperclip.paste()
        App.get_running_app().text_input.text += text_from_clipboard

    # Метод для отображения палитры выбора цвета текста
    def show_color_picker(self, instance):
        color_picker = ColorPicker()
        color_popup = Popup(title='Выберите цвет текста', content=color_picker, size_hint=(None, None), size=(400, 400))
        color_picker.bind(color=self.set_text_color)
        color_popup.open()

    # Метод для установки цвета текста
    def set_text_color(self, instance, color):
        App.get_running_app().text_input.foreground_color = color

    # Метод для сохранения текста в файл через FilePicker
    def save_with_file_picker(self, instance):
        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=self.save_file)
        popup = Popup(title='Выберите файл для сохранения', content=file_chooser, size_hint=(None, None), size=(400, 400))
        popup.open()

    # Метод для сохранения текста в выбранный файл
    def save_file(self, instance, file_path, file_name):
        with open(file_path, 'w') as f:
            f.write(App.get_running_app().text_input.text)


class Notepad(App):
    def build(self):
        self.title = 'Блокнот'

        # Создание текстового поля
        self.text_input = TextInput(size_hint=(1, 0.8))

        # Создание TabbedPanel
        tab_panel = TabbedPanel(do_default_tab=False)
        functions_tab = FunctionsTab()
        tab_panel.add_widget(functions_tab)

        # Создание главного макета
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.text_input)
        layout.add_widget(tab_panel)

        return layout


if __name__ == '__main__':
    Notepad().run()
