import pickle, json, time, re
from difflib import SequenceMatcher
from threading import Thread, main_thread, Event
from queue import Queue
from itertools import permutations

import kivy
from kivy.app import App
from kivy.uix.label import Label # Imports Label element
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout # Imports layout call function which pulls from .kv file with the same name as the class that calls it
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard



class RootLayout(BoxLayout): # Constructs a UI element based on the kivy BoxLayout class 
    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs) # Calls the superconstructor 
        
class CTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_text(self, _, text: str):
        app = App.get_running_app()
        app.genOutput()

        
class CPopup(Popup):
    pass

class CButton(Button):
    pass

class CScrollView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = "testid"
    pass



class SR_GUIApp(App): 
    """
    This class inherits the App class from kivy
    The name of this class will also determine the name of the .kv files (for layout/design)
    .kv file name is not case-sensitive to the class name but should be all lowercase to avoid issues
    .kv file name can exclude "App" portion of App class identifier
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.finished_check = Event() # Cross-thread event to indicate whether or not drug checking has finished
        self.reports_queue = Queue() # Queue for nodes to be added 
    
    def copyLabel(self):
        Clipboard.copy(self.root.ids.output_label.text)
    
    def genOutput(self):
        output_label: Label = self.root.ids.output_label
        factors: TextInput = self.root.ids.factors
        outcomes: TextInput = self.root.ids.outcomes
        analyses: TextInput = self.root.ids.analyses
        
        list_fact: list[str] = factors.text.split("\n")
        list_out: list[str] = outcomes.text.split("\n")
        list_an: list[str] = analyses.text.split("\n")
        
        output_text = ""
        
        for analysis in [i for i in list_an if i]:
            for outcome in [i for i in list_out if i]:
                for factor in [i for i in list_fact if i]:
                    output_text += F"{factor} | {outcome} | N | {analysis}\n"
        
        output_label.text = output_text
        
    
    
    
        
    
    
    # def build(self): # Returns the UI
    #     root = RootLayout()
    #     return root # Return whatever root element you are using for the UI
        


app_instance = SR_GUIApp() # Creates instance of the app
app_instance.run() # Runs the instance of the app 
