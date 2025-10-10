import sys
import tkinter as tk
from rectpack import newPacker

class CustomCanvas:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, height=height, width=width, bg="white")
        self.canvas.pack()

    def draw_rectangle(self, rect, color="lightblue"):
        self.canvas.create_rectangle(
            rect.x, rect.y,
            rect.x + rect.width, rect.y + rect.height,
            outline="black", fill=color
        )

    def display(self):
        self.root.mainloop()


class Rectangle:
    def __init__(self, height: int, width: int, x: int = 0, y: int = 0):
        self.height = height
        self.width = width
        self.x = x
        self.y = y


def pack(allRect, canvasSize):
    packer = newPacker()

    for rect in allRect:
        packer.add_rect(rect.width, rect.height)

    packer.add_bin(canvasSize[1], canvasSize[0])
    packer.pack()

    packed_rects = []
    for rect_data in packer.rect_list():
        bin_id, x, y, w, h, rid = rect_data
        packed_rects.append(Rectangle(h, w, x, y))

    return packed_rects


def main():
    # Read file path from command-line argument
    if len(sys.argv) < 2:
        print("Usage: python Assignment5.py <input_file>")
        return

    filepath = sys.argv[1]

    # Read and parse the input file
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # First line = canvas size
    canvas_height, canvas_width = map(int, lines[0].split(","))

    # The rest = rectangles
    rectangles = []
    for line in lines[1:]:
        h, w = map(int, line.split(","))
        rectangles.append(Rectangle(h, w))

    # Pack rectangles
    packed_rects = pack(rectangles, (canvas_height, canvas_width))

    # Draw on canvas
    canvas = CustomCanvas(canvas_height, canvas_width)
    colors = ["lightblue", "pink", "lightgreen", "orange", "yellow", "violet"]

    for i, rect in enumerate(packed_rects):
        canvas.draw_rectangle(rect, colors[i % len(colors)])

    # Display window
    canvas.display()


# Run only when executed directly (not imported)
if __name__ == "__main__":
    main()
