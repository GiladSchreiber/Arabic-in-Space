from tkinter import Tk, Canvas, Frame, BOTH, NW, Button, RAISED, PhotoImage
from PIL import Image, ImageTk
from ctypes import windll, Structure, c_long, byref
import xlrd
import pygame as pg
from pygame import mixer, key

NUM_OF_AREAS = 9
POSITIVE = 1
NEGATIVE = 0

class Area:
    def __init__(self, row):
        self.name = row[0].value
        self.hebrew = row[1].value
        self.arabic = row[2].value
        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0


def init_data():
    tel_aviv = data[0]
    jerusalem = data[1]
    haifa = data[2]
    ghaza = data[3]
    ayush = data[4]
    north = data[5]
    center = data[6]
    south = data[7]
    beer_sheva = data[8]
    jerusalem.up = 256
    jerusalem.down = 311
    jerusalem.left = 796
    jerusalem.right = 939
    north.up = 11
    north.down = 167
    north.left = 908
    north.right = 1046
    haifa.up = 82
    haifa.down = 171
    haifa.left = 875
    haifa.right = 929
    center.up = 177
    center.down = 274
    center.left = 827
    center.right = 952
    tel_aviv.up = 205
    tel_aviv.down = 242
    tel_aviv.left = 846
    tel_aviv.right = 880
    south.up = 321
    south.down = 476
    south.left = 787
    south.right = 966
    beer_sheva.up = 470
    beer_sheva.down = 621
    beer_sheva.left = 826
    beer_sheva.right = 927
    ghaza.up = 287
    ghaza.down = 347
    ghaza.left = 777
    ghaza.right = 832
    ayush.up = 146
    ayush.down = 326
    ayush.left = 906
    ayush.right = 984


class GUI(Frame):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.initUI()

    def initUI(self):
        self.master.title("Arabic in Space")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, )
        self.my_images = []
        self.my_images.append(PhotoImage(file="Israel_outline positive.png"))
        self.my_images.append(PhotoImage(file="Israel_outline negative.png"))
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW,
                                                        image=self.my_images[
                                                            0])
        self.canvas.pack(fill=BOTH, expand=1)
        self.root.geometry("{0}x{1}+0+0".format(1136, 645))
        self.root.bind("<Button-1>", self.readPos)
        self.root.bind("<Motion>", self.audio_volume)
        self.root.mainloop()

    def audio_volume(self, event):
        x, y = event.x, event.y
        for i in range(NUM_OF_AREAS):
            if (data[i].right >= x >= data[i].left) and (data[i].down >= y >=
                                                             data[i].up):
                channel0.set_volume((data[i].arabic / 100), 0)
                channel1.set_volume(0, (data[i].hebrew / 100))
                channel2.set_volume((data[i].arabic / 100), 0)
                channel3.set_volume(0, (data[i].hebrew / 100))
                return
        channel0.set_volume(1, 0)
        channel1.set_volume(0, 1)
        channel2.set_volume(1, 0)
        channel3.set_volume(0, 1)
        return


    def readPos(self, event):
        x, y = event.x, event.y
        print(x, y)
        global state, channel0, channel1
        if 321 <= x <= 400 and 511 <= y <= 536:
            if state:
                self.canvas.itemconfig(self.image_on_canvas,
                                     image=self.my_images[1])
                self.canvas.pack()
                state = NEGATIVE
                channel0.pause()
                channel1.pause()
                channel2.unpause()
                channel3.unpause()

            else:
                self.canvas.itemconfig(self.image_on_canvas,
                                     image=self.my_images[0])
                self.canvas.pack()
                state = POSITIVE
                channel0.unpause()
                channel1.unpause()
                channel2.pause()
                channel3.pause()



def arrange_data():
    workbook = xlrd.open_workbook("data.xlsx")
    worksheet = workbook.sheet_by_index(0)
    num_rows = int(worksheet.cell(0, 0).value)
    collect_data = []
    for i in range(num_rows):
        b = Area(worksheet.row(i + 2))
        collect_data.append(b)
    return collect_data




state = POSITIVE
pg.init()
mixer.init(frequency=44000, size=-16, channels=4, buffer=4096)
sound0 = mixer.Sound('The Little Mermaid arabic edited.ogg')
sound1 = mixer.Sound('The Little Mermaid hebrew edited.ogg')
sound2 = mixer.Sound('Be Prepared arabic.ogg')
sound3 = mixer.Sound('Be Prepared hebrew.ogg')
channel0 = mixer.Channel(0)
channel1 = mixer.Channel(1)
channel2 = mixer.Channel(2)
channel3 = mixer.Channel(3)
channel2.play(sound2)
channel3.play(sound3)
channel2.pause()
channel3.pause()
channel0.play(sound0)
channel1.play(sound1)
data = arrange_data()
init_data()
root = Tk()
ex = GUI(root)




