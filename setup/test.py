#!/usr/bin/python3.5
import kivy
from kivy.app import App
from kivy.uix.button import Button

class TestApp(App):
	def build(self):
		return Button(text='Hello world')
	
	def on_start(self):
		exit()


print("Python 3.5 tkinter test.")
TestApp().run()
