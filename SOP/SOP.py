#importering af moduler
import sys
import arcade
import random
import math
import time
from threading import Timer
import os
#definering af universelle værdier
BREDDE = 800
HOEJDE = 600
TITEL = "VM CUP"
SPORLAENGDE = 200
tilskuer = random.randrange(15, 750)
spd = 200
bredde = 30
height = 80
gameover = False
#klasse menuen
class mainmenuview (arcade.View):
    # når menuen bliver vist loader den baggrunden
    def on_show_view(self):

        self.background = None
        arcade.set_background_color(arcade.color.AMAZON)
        self.background = arcade.load_texture("Meny.jpg")
    # tegner Teksten
    def on_draw(self):
        self.clear
        arcade.draw_texture_rectangle(self.window.width // 2, self.window.height // 2, self.window.width,
                                      self.window.height, self.background)
        arcade.draw_text("VM CUP SIM 2022",self.window.width/2, self.window.height/2,arcade.color.WHITE
                         , font_size=50, anchor_x="center")
        arcade.draw_text("Klik for at forstaette", self.window.width / 2, self.window.height/2-75, arcade.color.WHITE
                         , font_size=30, anchor_x="center")
    #klik for at gå videre til SpilView klassen
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        spil_View = SpilView()
        spil_View.setup()
        self.window.show_view(spil_View)
# vores maalmand klasse
class maalmand:
    #attributes blir kaldt
    def __init__(self, fast_punkt: object, retningsvektor: object, farve: object, ) -> object:
        self.retningsvektor = retningsvektor
        self.farve = farve
        self.punkt = fast_punkt
        self.tid = 0
        self.rv = math.pi * 1/2
        self.tryk = False
#Det her skal den gøre 60 gange i sekundet for at sørge for tyngdekraft og tid
    def opdater(self, delta_tid):
        if self.tryk:
            self.tid += delta_tid
            x, y = self.punkt
            vx, vy = self.retningsvektor
            #vektorfunktionen
            x = spd * math.cos(self.rv) * self.tid + 400
            y = spd * math.sin(self.rv) * self.tid - 0.5 *  150.82 * self.tid**2 + 300
            self.punkt = (x, y)
    # tegner målmanden
    def tegn(self):
        x, y = self.punkt
        arcade.draw_rectangle_filled(x, y, bredde, height, self.farve)
#Klassen bold
class Bold:
    #Boldens atributes
    def __init__(self, fast_punkt, retningsvektor, farve, sporlaengde=None):
        self.fast_punkt = fast_punkt
        self.retningsvektor = retningsvektor
        self.punkt = self.fast_punkt
        self.farve = farve
        self.sporlaengde = sporlaengde
        if self.sporlaengde:
            self.spor = list()

    def opdater(self, delta_tid):
        #Boldens spor
        self.spor.append(self.punkt)
        if len(self.spor) >= self.sporlaengde:
            self.spor.pop(0)
        #Boldens retnignsvektor med tid
        x, y = self.punkt
        vx, vy = self.retningsvektor
        x += vx * delta_tid*3/4
        y += vy * delta_tid*3/4
        self.punkt = (x, y)
    #Tegn af bold og spor
    def tegn(self):
        x, y = self.punkt
        arcade.draw_circle_filled(x, y, 5, self.farve)
        for punkt in self.spor:
            x, y = punkt
            arcade.draw_circle_filled(x, y, 2, self.farve)


class SpilView(arcade.View):
    def __init__(self):
        #Hoppets x og y kordinater
        self.hop_x = 30#int(input("x"))
        self.hop_y = 30#int(input("y"))
        # funktion der bestemmer om det nat eller dag
        natdag = 1#int(input("dag=1 nat = 0"))
        super().__init__()

        while natdag == True:
            arcade.set_background_color(arcade.csscolor.LIGHT_SKY_BLUE)
            break
        if natdag == True:
            return
            print("Dagstid")
        else:
            return
            arcade.set_background_color(arcade.csscolor.BLACK)
            print("Nattid")


    def setup(self):
        # Definering af værdier bla boldens mulige endemål
        self.mm_start_x = 400
        self.rx = self.mm_start_x
        self.mm_start_y = 300
        self.ry = self.mm_start_y
        self.bold_start_x = 400
        self.bold_start_y = 50
        self.bold_x = random.randint(250, 550)
        self.bold_y = random.randint(275, 425)
        #bolden gives værdier
        self.v_x = self.bold_x - self.bold_start_x
        self.v_y = self.bold_y - self.bold_start_y
        self.v = (self.v_x, self.v_y)
        self.bold = Bold((400, 50), self.v, arcade.csscolor.WHITE, 5)

#maalmand, gives værdier
        self.vmx = self.hop_x - self.mm_start_x
        self.vmy = self.hop_y - self.mm_start_y
        self.vm = (self.vmx, self.vmy)
        self.maalmand = maalmand((400, 300), self.vm, arcade.csscolor.RED)

    def on_key_press(self, symbol: int, modifiers: int):
        #Styring af målmanaden
        if symbol == arcade.key.Q:
            self.maalmand.rv = math.pi*5/8
            self.maalmand.tryk = True
        if symbol == arcade.key.E:
            self.maalmand.rv = math.pi * 3/8
            self.maalmand.tryk = True
        if symbol == arcade.key.A:
            self.maalmand.rv = math.pi *7/8
            self.maalmand.tryk = True
        if symbol == arcade.key.D:
            self.maalmand.rv = 2/8
            self.maalmand.tryk = True
        if symbol == arcade.key.W:
            self.maalmand.rv = math.pi*1/2
            self.maalmand.tryk = True

    def update(self, delta_tid):
        #Opdater funktionen der sørger for at bolden ikke ryger ud af målet og målmandene ikke ryger igennem jorden
        if (self.bold.punkt[0] <= self.bold_x and self.bold.punkt[1] <= self.bold_y) or (
                self.bold.punkt[0] >= self.bold_x and self.bold.punkt[1] <= self.bold_y):
            self.bold.opdater(delta_tid)
        if (self.maalmand.punkt[1] > 299):
            self.maalmand.opdater(delta_tid)
#Variabler til at beregne afstanden
        afb = (int(self.bold.punkt[0]))
        afm = (int(self.maalmand.punkt[0]))
        afby = (int(self.bold.punkt[1]))
        afmy = (int(self.maalmand.punkt[1]))
        #Beregner om maalmanden har ramt bolden, hvis den har vent 3 sekudner og vis WIN skærmen
        dist = math.sqrt((afb - afm) ** 2 + (afby - afmy) ** 2)
        if dist < 20:
            def gg():
                SpilView= WIN()
                self.window.show_view(SpilView)
            t = Timer(3.0, gg)
            t.start()

    def on_draw(self):
        self.clear()
        arcade.draw_rectangle_filled(400, 300, 800, 400, arcade.csscolor.GREY, 0)
        #tegner tilskuerne med for loops
        for tilskuer in range(17):
            arcade.draw_rectangle_filled(tilskuer * 50 + 15, 350, 15, 50, arcade.csscolor.BLACK, 0)
        for tilskuer2 in range(17):
            arcade.draw_rectangle_filled(tilskuer2 * 50 - 10, 400, 15, 50, arcade.csscolor.YELLOW, 0)
#tegner reklamebannere
        arcade.draw_rectangle_filled(400, 280, 800, 100, arcade.csscolor.MEDIUM_PURPLE, 0)
        #tegner net
        arcade.draw_rectangle_outline(400, 350, 300, 150, (255, 255, 255), 5)
#tegner græsset
        arcade.draw_rectangle_filled(400, 130, 800, 300, arcade.csscolor.GREENYELLOW, 0)
        #Kører bold tegn og maalmand tegn funktionerne
        self.bold.tegn()
        self.maalmand.tegn()
        arcade.draw_text("Klik for at give op", self.window.width / 2, self.window.height / 4, arcade.color.WHITE
                     , font_size=20, anchor_x="center")
        arcade.draw_text("a er <- , q er \, w er ^ , e er /, d er -> ", self.window.width / 2, self.window.height / 6, arcade.color.WHITE
                         , font_size=20, anchor_x="center")

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        #funktion der ved mussetryk giver os LOSS skærmen
        SpilView = LOSS()
        self.window.show_view(SpilView)

#klassen der viser WIN skærmen
class WIN(arcade.View):
    #tegn baggrunden
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("endscreen.png")

    def on_draw(self):
        #Tegn teksten
        self.clear()
        self.texture.draw_sized(BREDDE/2,HOEJDE/2,BREDDE,HOEJDE)
        arcade.draw_text("DU REDDE BOLDEN DU VADNT", self.window.width / 2, self.window.height / 2, arcade.color.WHITE
                         , font_size=20, anchor_x="center")
        arcade.draw_text("Klik for at forstaette/Q for at forlade spillet", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE
                         , font_size=15, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        # ved tryk på q forlad programmet
        if symbol== arcade.key.Q:
            print("ok")
            os._exit(1)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # ved mussetryk start spillet om
        spil_View = SpilView()
        spil_View.setup()
        self.window.show_view(spil_View)

#Klassen der viser os skærmen når man har tabt
class LOSS(arcade.View):
    #tegn baggrunden
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Loss.png")

    def on_draw(self):
        #Tegn teksten
        self.clear()
        self.texture.draw_sized(BREDDE / 2, HOEJDE / 2, BREDDE, HOEJDE)
        arcade.draw_text("LOSER", self.window.width / 2, self.window.height / 2, arcade.color.WHITE
                         , font_size=20, anchor_x="center")
        arcade.draw_text("Klik for at prøve igen/q for at exti", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE
                         , font_size=15, anchor_x="center")
    def on_key_press(self, symbol: int, modifiers: int):
        # ved tryk på q forlad programmet
        if symbol== arcade.key.Q:
            os._exit(1)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # ved mussetryk start spillet om
        spil_View = SpilView()
        spil_View.setup()
        self.window.show_view(spil_View)

def main(): #kalder klasserne i den rigitge rækkefølge
        vindue = arcade.Window(BREDDE, HOEJDE, TITEL)
        start_view = mainmenuview()
        vindue.show_view(start_view)
        arcade.run()


#kalder main funktionen
main()


