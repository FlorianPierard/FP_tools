#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 16:20:30 2020

@author: florian
"""
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox 
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.config import Config
import subprocess

import os
import configparser

# =============================================================================
# Parameters needed to create the GUI 
# =============================================================================
# Here, you can choose different name for some of the parameters. Otherwise,
# the name will be the attribute capitalized attribute name
label_names_dict = {
    "fastq1" : "Path to fastq 1",
    "output_dir" : "Output directory",
    "input_dir" : "Input directory",
    "fastq2" : "Path to fastq 2 (not obliged)",
    "ref_consensus" : "Other consensus",
    "bam_file" : "BAM file",
    "bam_ref" : "BAM file ref fasta",
    "contigs_file" : "Contigs file",
    "splitter" : "Character to split the name with",
    "analysis_id" : "ID (if not, infered from fastq1)",
    }
current_path = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(current_path)
pipeline_dir = os.path.dirname(main_dir)

# Remove multituch emulation
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# =============================================================================
# Functions
# =============================================================================
# def on_enter(self, instance, value):
#     print('User pressed enter in', instance)

# Keep track of the parameters that need to be changed in the config file
# screen: [section, attribute]
changing_parameters = {}

def update_cfg(screen):
    # screen_attributes = dir(screen)
    for section, attributes in changing_parameters.items():
        for attribute in attributes:
            try:
                cfg[section][attribute] = getattr(screen, attribute).text
            except:
                try:
                    if getattr(screen, attribute).active:
                        cfg[section][attribute] = "true"
                    else:
                        cfg[section][attribute] = "false"
                except:
                    continue
    
def add_cfg_parameters(section, RootObject, ChildObject, only=[]):
    for attribute in cfg[section].keys():
        if len(only) > 0:
            if not attribute in only:
                continue
        para_grid = ParaGridLayout(cols = 2)
        try:
            label_name = label_names_dict[attribute]
        except:
            label_name = attribute.capitalize()
        para_grid.add_widget(ParaLabel(text=label_name,
                                        size_hint = (.8, None)))
        default_text = cfg[section][attribute]
        setattr(RootObject, attribute,
                TextInput(text=default_text, multiline = False))
        # getattr(RootObject, attribute).bind(on_text_validate=on_enter)
        para_grid.add_widget(getattr(RootObject, attribute))
        ChildObject.add_widget(para_grid)
        if section in changing_parameters.keys():
            changing_parameters[section].append(attribute)
        else:
            changing_parameters[section] = [attribute]

def add_parameters(RootObject, ChildObject, *parameters):
    for para in parameters:
        para_grid = ParaGridLayout(cols = 2)
        # Get its label name
        label_name = label_names_dict[para]
        para_grid.add_widget(ParaLabel(text=label_name,
                                        size_hint = (.8, None)))
        setattr(RootObject, para,
                TextInput(multiline = False))
        para_grid.add_widget(getattr(RootObject, para))
        ChildObject.add_widget(para_grid)

def add_check_box(section, RootObject, ChildObject, only=[]):
    count = 0
    for attribute in cfg[section].keys():
        if len(only) > 0:
            if not attribute in only:
                continue
        # So you have 2 checkboxes per line
        if count % 2 == 0:
            para_grid = ParaGridLayout(cols = 4, spacing = 20)
        try:
            label_name = label_names_dict[attribute]
        except:
            label_name = attribute.capitalize()
         
        para_grid.add_widget(ParaLabel(text=label_name,
                                       size_hint_x = 0.7))
        # Get the default value from the config file
        default_boolean = cfg[section].getboolean(attribute)
        # add_small_check_box(attribute, para_grid, RootObject, default_boolean)
        
        setattr(RootObject, attribute,
                MyCheckBox(active=default_boolean))
        para_grid.add_widget(getattr(RootObject, attribute))
        if count % 2 ==0:
            ChildObject.add_widget(para_grid)
        # Add +1 to the number fo elements added
        count += 1
        if section in changing_parameters.keys():
            changing_parameters[section].append(attribute)
        else:
            changing_parameters[section] = [attribute]
def add_one_check_box(attribute, Grid, RootObject, default):
    Grid.add_widget(ParaLabel(text=attribute,
                                       size_hint_x = 0.7))
    # Get the default value from the config file
    setattr(RootObject, attribute,
            MyCheckBox(active=default))
    Grid.add_widget(getattr(RootObject, attribute))

# =============================================================================
# Custom layouts and labels
# =============================================================================
# Import the kv files with the layouts, labels, screens,...

class ParaLabel(Label):
    pass

class TitleLabel(Label):
    pass

class ParaGridLayout(GridLayout):
    pass

class MyCheckBox(CheckBox):
    pass

class MyScrollView(ScrollView):
    pass

class MyButton(Button):
    pass

class ScrollingBoxLayout(BoxLayout):
    pass

# =============================================================================
# The different screens
# =============================================================================

class WelcomeScreen(Screen):
    """The welcome screen is the first screen that is showed. Here, you must
    choose a virus where the defaul analysis is already set. Afterwards, you'll
    be able to change the configuration as you want. If you have already fine 
    tuned some parameters, you can give your config file to the GUI in the 
    text box and click on 'Other config'"""
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        master_layout = BoxLayout(orientation= 'vertical', spacing= 5)
        # TODO a small explanation of the pipeline close to the image

        # Add the type of analysis you want to perform
        master_layout.add_widget(Image(
            source = 'images/icon.png', allow_stretch = True,
            size_hint = (1.5, 1.5),
            pos_hint = {"center_x": .5, "center_y": .5}))

        master_layout.add_widget(TitleLabel(
            text = "Choose the type of analysis"))
        # add_dropdown(self, master_layout, "analysis_button",
        #               ["SAMPLE","FOLDER"])
        # ANALYSIS TO PERFORM
        # para_grid = ParaGridLayout(cols = 2, spacing = 50)
        # para_grid.add_widget(ParaLabel(text="Analysis",
        #                                 size_hint = (.7, 1)))
        config_grid_layout = GridLayout(rows = 1, cols = 4, spacing = 5,
                                    padding = 5)
        config_grid_layout.add_widget(
            ParaLabel(text='Select if you have only 1\nor multiple samples:',
                       size_hint = (1, None), height=100,
                      pos_hint= {"center_x": .5, "center_y": .5}))
        self.analysis_button = Button(text='SAMPLE', size_hint=(None, None))
        global analysis_dropdown
        analysis_dropdown = DropDown()
        analysis_dropdown.bind(on_select=lambda instance, x: setattr(
            self.analysis_button, 'text', x))
        list_of_elements = ["SAMPLE", "FOLDER"]
        for elt in list_of_elements:
            btn = Button(text= elt, size_hint_y=None, height=44,
                          on_release=lambda btn: analysis_dropdown.select(btn.text))
            analysis_dropdown.add_widget(btn)
        self.analysis_button.bind(on_release=analysis_dropdown.open)
        config_grid_layout.add_widget(self.analysis_button)
        # master_layout.add_widget(para_grid)
        
        # CONFIGURATION TO START WITH
        config_grid_layout.add_widget(
            ParaLabel(text='Select the configuration\nfile you want:',
                       size_hint = (1, None), height=100,
                      pos_hint= {"center_x": .5, "center_y": .5}))
        self.config_button = Button(text='HIV', size_hint=(None, None))
        global config_dropdown
        config_dropdown = DropDown()
        config_dropdown.bind(on_select=lambda instance, x: setattr(
            self.config_button, 'text', x))
        # config_dropdown.bind(on_select=self.start)
        list_of_elements = ["HIV", "HCV", "Other_config"]
        for elt in list_of_elements:
            btn = Button(text= elt, size_hint_y=None, height=44,
                          on_release=lambda btn: config_dropdown.select(btn.text))
            config_dropdown.add_widget(btn)
        self.config_button.bind(on_release=config_dropdown.open)
        config_grid_layout.add_widget(self.config_button)
        master_layout.add_widget(config_grid_layout)
        self.config_path = TextInput(
            hint_text='If you have another config file, give the path here and select "Other_config" as configuration file', 
            multiline = False, height = 10)
        master_layout.add_widget(self.config_path)       
        
        master_layout.add_widget(
            Button(text="Start configuration", on_press= self.start,
                     size_hint = (.9, None), font_size = 35,
                     pos_hint= { 'center_x' : .5 }))
        self.add_widget(master_layout)
    
    def start(self, btn):
        # Check the configuration file chosen
        if self.config_button.text == "Other_config":
            config_file = self.config_path
        else:
            virus = self.config_button.text
            config_file = os.path.join(pipeline_dir, "configs", 
                                       "%s_config.ini" % virus)
        global cfg
        cfg = configparser.ConfigParser()
        cfg.read(config_file)
        self.generate_analysis(self.manager.get_screen("analysis"))
        self.generate_config(self.manager.get_screen("config"))
        self.manager.current = 'analysis'
    
    def write_config(self, config_file):
        output_dir = os.path.dirname(config_file)
        # Create the output directory
        os.makedirs(output_dir, exist_ok=True)
        update_cfg(self.manager.get_screen('analysis'))
        update_cfg(self.manager.get_screen('config'))
        with open(config_file,'w') as ConfigWriteFile:
            cfg.write(ConfigWriteFile)
        
    def generate_analysis(self, analysis_screen):
        analysis_screen.clear_widgets()
        master_layout = GridLayout(rows = 2, cols = 1, spacing = 5,
                                   padding = 5)
        master_layout.add_widget(MyButton(text="--> SUBMIT <--",
                                          height = 60, font_size = 35,
                                          on_press= self.run_pipeline))
        layout = ScrollingBoxLayout()
        layout.bind(minimum_height=layout.setter('height'))  
             
        layout.add_widget(TitleLabel(text="Files and directories"))
        if self.analysis_button.text == "SAMPLE":
            add_cfg_parameters("Already_done", analysis_screen, layout,
                        ["fastq1", "fastq2", "output_dir"])
            add_parameters(analysis_screen, layout, "analysis_id")
        elif self.analysis_button.text == "FOLDER":
            add_parameters(analysis_screen, layout, "input_dir", 
                           "output_dir", "splitter")
        # Analyses to perform
        layout.add_widget(TitleLabel(text="Analyses to perform"))
        add_check_box("Analysis", analysis_screen, layout)
        # Files that you could have generated from another analysis
        if self.analysis_button.text == "SAMPLE":
            layout.add_widget(TitleLabel(
                text="Files already generated? (not obliged)"))
            add_cfg_parameters("Already_done", analysis_screen, layout,
                            ["ref_consensus", "bam_file", "bam_ref", 
                             "contigs_file"])
        
        scroll_box = MyScrollView()
        scroll_box.add_widget(layout)
        master_layout.add_widget(scroll_box)
        analysis_screen.add_widget(master_layout)
        
    def generate_config(self, config_screen):
        config_screen.clear_widgets()
        master_layout = GridLayout(rows = 2, cols = 1, spacing = 5,
                                   padding = 5)
        master_layout.add_widget(MyButton(text="--> SUBMIT <--",
                                          height = 60, font_size = 35,
                                          on_press= self.run_pipeline))
        layout = ScrollingBoxLayout()
        layout.bind(minimum_height=layout.setter('height'))
        # Files to give to the pipeline
        # CLEANING
        layout.add_widget(TitleLabel(text="Global"))
        add_cfg_parameters("Global", config_screen, layout,
                       only=["threads", "ref_alignment_file"])
        
        layout.add_widget(TitleLabel(text="Cleaning"))
        add_cfg_parameters("Cleaning", config_screen, layout,
                       only=["adapters_file","primers_file",
                             "nucleotide_quality","minimum_length","sliding"])
        
        
        add_check_box("Cleaning", config_screen, layout,
                      only=["adapters", "primers", "quality_trimming", 
                            "get_fastqc", "clean_contaminant_reads"])
        # MAPPING
        layout.add_widget(TitleLabel(text="Mapping"))
        add_cfg_parameters("Mapping", config_screen, layout,
                       only =["de_novo_assembler","mapper"])
        
        add_check_box("Mapping", config_screen, layout,
                      only=["correct_contigs",
                            "mapping_against_commonref" ])
        # CONSENSUS
        layout.add_widget(TitleLabel(text="Consensus"))
        add_cfg_parameters("Consensus", config_screen, layout)
        # CODON
        layout.add_widget(TitleLabel(text="Codon"))
        add_cfg_parameters("Codon", config_screen, layout)
        # Deep analysis blast simplots
        layout.add_widget(TitleLabel(text="Deep analysis"))
        add_cfg_parameters("Deep_analysis", config_screen, layout, 
                       only = ["pure_ref_alignment_file", "min_number_of_reads"])
        add_check_box("Deep_analysis", config_screen, layout,
                      only = ["contig_simplot", "contig_along_ref_plot",
                              "blast_deep_simplot"])
        
        layout.add_widget(TitleLabel(text="Threshold for stats and plots"))
        add_cfg_parameters("Threshold", config_screen, layout)
        # Files that you could have generated from another analysis
        scroll_box = MyScrollView()
        scroll_box.add_widget(layout)
        master_layout.add_widget(scroll_box)
        config_screen.add_widget(master_layout)
   
    def run_pipeline(self, instance): 
        # recover values from other screens
        analysis_screen = self.manager.get_screen('analysis')
        config_file = os.path.join(
            analysis_screen.output_dir.text, "gui_User_config.ini")
        print(config_file)
        self.write_config(config_file)
        welcome_screen = self.manager.get_screen('welcome')
        type_of_analysis =  welcome_screen.analysis_button.text
        if type_of_analysis == "SAMPLE":
            print("Running the analysis on one sample")
            script = os.path.join(main_dir,"main.py")
            print(script, os.path.isfile(script))
            fastq1 = analysis_screen.fastq1.text
            fastq2 = analysis_screen.fastq2.text
            analysis_id = analysis_screen.analysis_id.text
            print(analysis_id)
            if fastq2 == "":
                fastq2 = fastq1.replace("R1", "R2")
            if analysis_id == "":
                print("analaysis id empty")
                analysis_id = os.path.basename(fastq1).split("_")[0]
            cmd = ["python", script, "-i1", fastq1, 
                    "-i2", fastq2, 
                    "-o", analysis_screen.output_dir.text, 
                    "-id", analysis_id, 
                    "-c", config_file ]
        elif type_of_analysis == "FOLDER":
            print("Running the analaysis on all the samples of your directory")
            script = os.path.join(main_dir,"multiruns.py")
            print(script, os.path.isfile(script))
            cmd = ["python", script, "-i", analysis_screen.input_dir.text, 
                    "-o", analysis_screen.output_dir.text, 
                    "-s", analysis_screen.splitter.text, 
                    "-c", config_file ]
        # Run the command
        str_cmd = " ".join(cmd)
        print(str_cmd)
        subprocess.run(cmd)

class AnalysisScreen(Screen):
    def __init__(self, **kwargs):
        super(AnalysisScreen, self).__init__(**kwargs)
        self.add_widget(TitleLabel(
            text="You didn't choose a config file or virus",
            pos_hint = {"center_x": .5, "center_y": .5}))
    pass
       
class ConfigScreen(Screen):
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        self.add_widget(TitleLabel(
            text="You didn't choose a config file or virus",
            pos_hint = {"center_x": .5, "center_y": .5}))
    pass

class SummaryScreen(Screen):
    pass

class PlotScreen(Screen):
    pass

class PdfScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

class IlluminaIT(BoxLayout):
    pass

class IlluminaITApp(App):
    title = 'Illumina IT pipeline'
    def build(self):
        return IlluminaIT()

def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_path)
    Builder.load_file("gui.kv")
    IlluminaITApp().run()

if __name__ == "__main__":
    IlluminaITApp().run()

