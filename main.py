import pickle, json, time, re, uuid
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
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem



class RootLayout(TabbedPanel): # Constructs a UI element based on the kivy BoxLayout class 
    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs) # Calls the superconstructor 
    
    def removeTab(self, tab_id):
        app: SR_GUIApp = App.get_running_app()
        tab = None
        for tab in self.tab_list:
            if tab.tab_id == tab_id:
                tab = tab
                break
        if tab:
            app.tabs.remove(tab_id)
            # self.switch_to(self.default_tab) # Ignore if you want to temporarily keep inputs
            self.remove_widget(tab)

class CBoxLayout(BoxLayout):
    def __init__(self, tab_id = 1, **kwargs):
        super().__init__(**kwargs)
        self.tab_id = tab_id
        
 
    def copyLabel(self):
        Clipboard.copy(self.ids.output_label.text)
    
    def genOutput(self):
        output_label: Label = self.ids.output_label
        factors: TextInput = self.ids.factors
        outcomes: TextInput = self.ids.outcomes
        analyses: TextInput = self.ids.analyses
        f_mod: TextInput = self.ids.f_mod
        o_mod: TextInput = self.ids.o_mod
        
        list_fact: list[str] = factors.text.split("\n")
        if f_mod.text.strip():
            new_list = []
            for modifier in [i for i in f_mod.text.split(";") if i]:
                for item in [i for i in list_fact if i]:
                    new_list.append(F"{item} ({modifier.strip()})")
            list_fact = new_list
                
        
        list_out: list[str] = outcomes.text.split("\n")
        if o_mod.text.strip():
            new_list = []
            for modifier in [i for i in o_mod.text.split(";") if i]:
                for item in [i for i in list_out if i]:
                    new_list.append(F"{item} ({modifier.strip()})")
            list_out = new_list
        list_an: list[str] = analyses.text.split("\n")
        
        output_text = ""
        
        for analysis in [i for i in list_an if i]:
            output_text += F"\n"
            for outcome in [i for i in list_out if i]:
                for factor in [i for i in list_fact if i]:
                    output_text += F"{factor} | {outcome} | N | {analysis}\n"
        
        output_label.text = output_text

    def dupeTab(self):
        app: SR_GUIApp = App.get_running_app()
        new_tab_id = app.getNewTabId() # This variable will be assigned to both the panel container and the child box to bind the two 
        new_tab = CTabbedPanelItem(text=F"Tab {new_tab_id}", tab_id=new_tab_id)
        new_content = CBoxLayout(tab_id=new_tab_id)
        
        # Copy contents
        new_content.ids.output_label.text = self.ids.output_label.text
        new_content.ids.factors.text = self.ids.factors.text
        new_content.ids.outcomes.text = self.ids.outcomes.text
        new_content.ids.analyses.text = self.ids.analyses.text
        new_content.ids.f_mod.text = self.ids.f_mod.text
        new_content.ids.o_mod.text = self.ids.o_mod.text
        
        new_tab.add_widget(new_content)
        app.root.add_widget(new_tab)
        
    def removeTab(self):
        app = App.get_running_app()
        root_layout: RootLayout = app.root
        root_layout.removeTab(self.tab_id)

        
class CTabbedPanelItem(TabbedPanelItem):
    def __init__(self, tab_id = 1, **kwargs):
        super().__init__(**kwargs)
        self.tab_id = tab_id
    pass

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
        self.tabs = [1] # Initiate tab containing 1 tab id
        self.finished_check = Event() # Cross-thread event to indicate whether or not drug checking has finished
        self.reports_queue = Queue() # Queue for nodes to be added 
    
    def getNewTabId(self) -> int:
        new_tab_id = 1
        while True: # Increment new_tab_id starting from 1 until unoccupied id found
            if new_tab_id in self.tabs:
                new_tab_id += 1
                continue
            else:
                self.tabs.append(new_tab_id) # Register new tab id
                return new_tab_id
    

        
    
    
    
        
    
    
    # def build(self): # Returns the UI
    #     root = RootLayout()
    #     return root # Return whatever root element you are using for the UI
        


app_instance = SR_GUIApp() # Creates instance of the app
app_instance.run() # Runs the instance of the app 
