from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label


class MyCheckBox(BoxLayout):

    def __init__(self, **kwargs):
        BoxLayout.__init__(self,
                              **kwargs)
        self.checkbox = CheckBox(
            size_hint=(None, 1),
            size=(50, 1),
            active=False, disabled=True
        )
        self.label = Label(text="<empty>")
        self.add_widget(self.checkbox)
        self.add_widget(self.label)
