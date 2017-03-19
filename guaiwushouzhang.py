# -*-encoding:utf-8-*-

'''
Author:     Super_Red
Date:       3/13/2017
Describe:   Display monsters nicely
'''

import pandas as pd
from tkinter import *
from PIL import Image, ImageTk
import os

class monster:

    def __init__(self, monster_id, name, attribute, strength, intelligence, speed, glamour, lucky, technique, skill1, skill2, skill3, special, specialSkill):
        self._monster_id = monster_id
        self._name = name
        self._attribute = attribute
        self._strength = int(strength)
        self._intelligence = int(intelligence)
        self._speed = int(speed)
        self._glamour = int(glamour)
        self._lucky = int(lucky)
        self._technique = int(technique)
        self._skill1 = skill1
        self._skill2 = skill2
        self._skill3 = skill3
        self._special = special
        self._specialSkill = specialSkill

    def show(self):
        print("力:\t{st}\n智:\t{inte}\n速:\t{sp}\n魅:\t{gl}\n运:\t{lu}\n技:\t{te}".format(st=self._strength, inte=self._intelligence, sp=self._speed, gl=self._glamour, lu=self._lucky, te=self._technique))

class game(object):
    
    def __init__(self, *monsters):
        self._dataSet = pd.read_csv("handbook.csv")

    def findMonster(self, name):
        names = list(self._dataSet["名称"].values)
        label = list(self._dataSet.columns)[:9] + list(self._dataSet.columns)[-5:]
        if name in names:
            index = names.index(name)
            mon = self._dataSet.ix[index, :]
            return monster(*list(map(lambda x:mon[x], label)))
        else:
            print("No such monster")
            return None

class gui(object):
    
    def __init__(self, game):
        self.game = game
        self.monster_label = list(self.game._dataSet.columns)[:9] + list(self.game._dataSet.columns)[-5:]
        self.current_monster = self.game.findMonster("武圣关云长")
        self.root = Tk()
        self.root.title("MonsterBook")
        self.root.geometry("350x420+500+100")
        self.root.resizable(False,False)
        self.searchVariable = StringVar()
        self.canvas = Canvas(self.root, width=350, height=420)
        self.bulidBasicLayout()
        self.bulidDisplayFramework()
        self.canvas.pack()
        self.root.mainloop()

    def bulidBasicLayout(self):
        self.searchEntry = Entry(width=10, textvariable=self.searchVariable)
        self.searchEntry.place(x=100, y=10)
        self.searchVariable.set("武圣关云长")
        Button(text=" 查 询  ", command=self.searchByName).place(x=200, y=10)
        Button(text=">", command=self.nextMonster, width=1, height=15).place(x=310, y=110)
        Button(text="<", command=self.previousMonster, width=1, height=15).place(x=10, y=110)

    def bulidDisplayFramework(self):
        self.canvas.create_rectangle(50, 50, 300, 400 , fill="#F8EED2")
        self.defaultImage = ImageTk.PhotoImage(file="pic_gif/image0.gif")
        self.monsterImage = ImageTk.PhotoImage(file="pic_gif/image{id}.gif".format(id=self.current_monster._monster_id))
        self.picLabel = Label(self.canvas, image=self.monsterImage, borderwidth=0)
        self.picLabel.place(x=110, y=70)
        self.attrList = [Label(self.canvas, text="test", borderwidth=0, bg="#B0A995", fg="#5E4E3F", font=20, width=8, height=1, justify="left") for i in range(6)]
        self.attrList[0].place(x=70, y=230)
        self.attrList[1].place(x=141, y=230)
        self.attrList[2].place(x=212, y=230)
        self.attrList[3].place(x=70, y=253)
        self.attrList[4].place(x=141, y=253)
        self.attrList[5].place(x=212, y=253)
        self.attrList[0]["text"] = "力{:>5}".format(str(self.current_monster._strength))
        self.attrList[1]["text"] = "智{:>5}".format(str(self.current_monster._intelligence))
        self.attrList[2]["text"] = "速{:>5}".format(str(self.current_monster._speed))
        self.attrList[3]["text"] = "魅{:>5}".format(str(self.current_monster._glamour))
        self.attrList[4]["text"] = "运{:>5}".format(str(self.current_monster._lucky))
        self.attrList[5]["text"] = "技{:>5}".format(str(self.current_monster._technique))
        self.defaultElementImage = ImageTk.PhotoImage(file="ele/0.gif")
        self.elementImage = ImageTk.PhotoImage(file="ele/{ele}.gif".format(ele=self.current_monster._attribute))
        self.eleLabel = Label(self.canvas, image=self.elementImage, borderwidth=0)
        self.eleLabel.place(x=70, y=60)
        self.nameItem = self.canvas.create_text((80, 140), text="\n".join(list(i for i in self.current_monster._name)), font="Monaco 15 bold", fill="#5E4E3F")
        if isinstance(self.current_monster._skill3, str):
            self.showSkillList(3)
        elif isinstance(self.current_monster._skill2, str):
            self.showSkillList(2)
        elif isinstance(self.current_monster._skill1, str):
            self.showSkillList(1)
        else:
            self.showSkillList(0)
        if isinstance(self.current_monster._special, str):
            self.special = Label(self.canvas, text=str(self.current_monster._special), borderwidth=0, bg="#F74851", fg="#4BAEA4", font=20, width=26, height=1, justify="center")
            self.special.place(x=70, y=356)
            if not isinstance(self.current_monster._specialSkill, str):
                self.current_monster._specialSkill = ""
            self.specialSkill = Label(self.canvas, text=str(self.current_monster._specialSkill), borderwidth=0, bg="#F74851", fg="#5E4E3F", font=20, width=26, height=1, justify="left")
            self.specialSkill.place(x=70, y=371)


    def showSkillList(self, n):
        if n == 0:
            return
        self.skillList = [Label(self.canvas, text="", borderwidth=0, bg="#B0A995", fg="#5E4E3F", font=20, width=26, height=2) for i in range(n)]
        if n >= 1:
            self.skillList[0].place(x=70, y=276)
            self.skillList[0]["text"] = self.current_monster._skill1
        if n >= 2:
            self.skillList[1].place(x=70, y=316)
            self.skillList[1]["text"] = self.current_monster._skill2
        if n >= 3:
            self.skillList[2].place(x=70, y=356)
            self.skillList[2]["text"] = self.current_monster._skill3

    def searchByName(self):
        self.current_monster = self.game.findMonster(self.searchVariable.get())
        self.searchVariable.set("")
        self.displayCurrentMonster()

    def nextMonster(self):
        if int(self.current_monster._monster_id) < 1046:
            nextMonster_id = int(self.current_monster._monster_id)
            mon = self.game._dataSet.ix[nextMonster_id, :]
            self.current_monster = monster(*list(map(lambda x:mon[x], self.monster_label)))
        self.displayCurrentMonster()

    def previousMonster(self):
        if int(self.current_monster._monster_id) > 1:
            nextMonster_id = int(self.current_monster._monster_id) - 2
            mon = self.game._dataSet.ix[nextMonster_id, :]
            self.current_monster = monster(*list(map(lambda x:mon[x], self.monster_label)))
        self.displayCurrentMonster()

    def reset(self):
        for skillItem in self.skillList:
            skillItem["text"] = ""
            skillItem["bg"] = "#F8EED2"
        self.picLabel["image"] = self.defaultImage
        self.eleLabel["image"] = self.defaultElementImage
        self.special["bg"] = "#F8EED2"
        self.special["text"] = ""
        self.specialSkill["bg"] = "#F8EED2"
        self.specialSkill["text"] = ""

    def displayCurrentMonster(self):
        self.reset()
        if self.current_monster is None:
            self.current_monster = self.game.findMonster("妈蛋")
        self.bulidDisplayFramework()         


def changeName():
    # change pgn into gif and change the background into (248, 238, 210)
    fileList = list(os.walk("pic"))[0][2][1:]
    for file in fileList:
        im = Image.open("pic/" + file)
        x,y = im.size 
        p = Image.new('RGBA', im.size, (248,238,210))
        p.paste(im, (0, 0, x, y), im)
        newFile = file.split(".")[0] + ".gif"
        p.save('pic_gif/' + newFile)
        print("Done!:\t"+ file)

def checkPicPixels():
    import matplotlib.image as mping
    fileList = list(os.walk("pic_gif"))[0][2][1:]
    a, b, c = (142, 142, 4)
    differentList = [file for file in fileList if mping.imread("pic_gif/" + file).shape != (a, b, c)]
    return differentList

def unifyPicPixels():
    import matplotlib.image as mpimg
    from scipy import misc
    differentList = checkPicPixels()
    for file in differentList:
        fileName = "pic_gif/" + file
        arrayToChanged = mpimg.imread(fileName)
        arrayToSaved = misc.imresize(arrayToChanged, (142, 142, 4))
        misc.imsave(fileName, arrayToSaved)
    print("Done!")

gui(game())



