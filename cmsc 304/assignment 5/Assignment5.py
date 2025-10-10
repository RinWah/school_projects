import sys
import tkinter as tk
from rectpack import newPacker
class CustomCanvas:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="white")
        self.canvas.pack()
    def draw_rect(self, rect, color="lightblue"):
        self.canvas.create_rectangle(
            rect.x, rect.y,
            rect.x + rect.width, rect.y + rect.height,
            outline="black", fill=color
        )
    def show(self):
        self.root.mainloop()
class Rectangle:
    def __init__(self, h: int, w: int, x: int = 0, y: int = 0):
        self.height = h
        self.width = w
        self.x = x
        self.y = y
def pack_rects(rects, canvas_size):
    packer = newPacker()
    for r in rects:
        packer.add_rect(r.width, r.height)
    packer.add_bin(canvas_size[1], canvas_size[0])
    packer.pack()
    packed = []
    for data in packer.rect_list():
        bin_id, x, y, w, h, rid = data
        packed.append(Rectangle(h, w, x, y))
    return packed
def main():
    if len(sys.argv) < 2:
        print("Usage: python Assignment5.py <input_file>")
        return
    file_name = sys.argv[1]
    with open(file_name, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    canvas_h, canvas_w = map(int, lines[0].split(","))
    rects = []
    for line in lines[1:]:
        h, w = map(int, line.split(","))
        rects.append(Rectangle(h, w))
    packed = pack_rects(rects, (canvas_h, canvas_w))
    canvas = CustomCanvas(canvas_h, canvas_w)
    colors = ["lightblue", "pink", "lightgreen", "orange", "yellow", "violet"]
    for i, r in enumerate(packed):
        canvas.draw_rect(r, colors[i % len(colors)])
    canvas.show()
if __name__ == "__main__":
    main()
