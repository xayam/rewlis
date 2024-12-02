from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label


class MyCheckBox(BoxLayout):

    def __init__(self, **kwargs):
        BoxLayout.__init__(self,
                           size_hint=(1., None),
                           size=(1, 30),
                           padding=(7, 7),
                           **kwargs)
        self.checkbox = CheckBox(
            size_hint=(None, 1.),
            size=(30, 1),
            active=False, disabled=True
        )
        self.label = Label(
            text="<Select book on left panel>",
            halign="left",
        )
        self.add_widget(self.checkbox)
        self.add_widget(self.label)
