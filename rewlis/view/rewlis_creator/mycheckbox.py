from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label


class MyCheckBox(BoxLayout):

    def __init__(self, **kwargs):
        BoxLayout.__init__(self,
                           size_hint=(1., None),
                           size=(1, 30),
                           **kwargs)
        self.checkbox = CheckBox(
            size_hint=(None, 1.),
            size=(30, 1),
            active=False, disabled=True
        )
        self.label = Label(
            text="<select book on left panel or click " +
                 "ADD-button for create new sync-book>",
        )
        self.add_widget(self.checkbox)
        self.add_widget(self.label)
