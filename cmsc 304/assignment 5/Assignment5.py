# import tkinter to use canvas [built in object defined in python package]
import tkinter as tk
# for pack function
from rectpack import newPacker
# creates the root window that pops up on screen
root = tk.Tk()

# make class for custom canvas
class CustomCanvas:
    # a constructor which takes two explicit arguments, height and width, both expected to be of type int.
    def __init__(self, height: int, width: int):
        # constructor has height and width
        self.height = height
        self.width = width
        # sets the window area to specific given height and width with the background color white
        self.canvas = tk.Canvas(root, height=height, width=width, bg="white")
        # makes canvas visible to user
        self.canvas.pack()
# make class for rectangle
class Rectangle:
    # can define rectangle's height, width, x and y values
    def __init__(self, height: int, width: int, x: int = 0, y: int = 0):
        # instance variable equivalent to java
        self.height = height
        self.width = width
        self.x = x
        self.y = y
# function to arrange rectangles so they aren't overlapping
def pack(allRect, canvasSize):
    pack = newPacker()
    # for each rectangle, add it to pack
    pack.add_rect(rect.width, rect.height)
    # give bin/canvas size to pack
    pack.add_bin(canvasSize[1], canvasSize[0])
    # run packing algorithm
    pack.pack()
    # results
    

# take user input of height and width of tkinter window
height = int(input("height: "))
width = int(input("width: "))
# uses constructor to create the canvas on the user's screen
canvas = CustomCanvas(height, width)