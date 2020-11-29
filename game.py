# Þórður Ingi 29.11

import random
import arcade
import csv


# set skjá stærðina í 1000x600

screen_width = 1000
screen_height = 600

veiwport_margin = 150
MOVEMENT_SPEED = 4
enemy_movement_speed = 5
enemy_count = 10
sprite_scaling_skot = 0.004
skot_hradi = 10




#physics

gravity = 1
Player_jump_speed = 15



# geari fallsem les csv skrá á breytir því lista sem forritð getur lesið til að gera mapið
def readcsv():
    with open("data/map.csv") as csvfile:
        readCSV = csv.reader(csvfile,delimiter=",")
        cord_listi2 = []
        for x in readCSV:
            cord_listi2.append(list(x))
        cord_listi2.reverse()
        x1 = 0
        y1 = 0
        cord_listi = []
        for x in cord_listi2:
            y1 +=50
            for item in x:
                x1+=50
                cord_listi.append([x1,y1,item])
            x1 = 0
    return cord_listi

# fall sem les skrá og returnar lista af texture og texture sem er spegluð
def load_texture_pair(filename):

    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

# gera klassa fyrir spilara sem erfðir sprite klassan  
class Player(arcade.Sprite):
    def __init__(self, player_lives=3):
        super().__init__()

        self.player_lives = player_lives
        self.change_x = 0
        self.change_y = 0
        
        self.textures = load_texture_pair("data/hermadur.png")
        self.texture = self.textures[1]
        self.scale = 0.15
    def update(self):

        # checka hvort notendi fer af skjánum og snú honum við
        if self.center_x<0:
            self.center_x += 5
        if self.center_x>2000:
            self.center_x -= 5
        # eftir hvernig spilarinn snýr breytist texture
        if self.change_x < 0:
            self.texture  = self.textures[0]
        elif self.change_x > 0:
            self.texture  = self.textures[1]
        
        self.center_x += self.change_x

        self.center_y += self.change_y
# enemy klass er  alveg eins og player klassin nema enemy_lives er alltaf það sama
class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.enemy_lives = 1
        self.change_x = 0
        self.change_y = 0
        
        self.textures = load_texture_pair("data/adolf-hitler.png")
        self.texture = self.textures[1]
        self.scale = 0.05
    def update(self):



        if self.center_x<0:
            self.center_x += 5
        if self.center_x>2000:
            self.center_x -= 5

        if self.change_x < 0:
            self.texture  = self.textures[0]
        elif self.change_x > 0:
            self.texture  = self.textures[1]
        
        self.center_x += self.change_x

        self.center_y += self.change_y
   
            

# gera klassa fyrir ovini

class Leikur(arcade.Window): # klassi fyrir leikinn
    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(screen_width, screen_height, "Byssumaður - Þórður Ingi")
        
        self.score = 0

        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
        arcade.set_viewport(200,200 + screen_width - 1, 0, screen_height - 1)
        
        self.wall_list = None
        self.skot_list = None
        self.ovina_list = None
        self.peninga_list = None
        
        
        self.player = None

        self.text_x = 20
        self.text_change = 0

        self.physics_engine = None

        self.view_left = 0
        self.view_bottom = 0  

        #geri boolean breytur fyrir leikja states
        self.start = True
        self.game = False
        self.dead = False
        self.vann = False
        self.menu = False

        self.erfidleiki = [0,1,2,4]
        self.erfidleiki_text = ""

        self.skothljod = arcade.load_sound("data/skot.mp3")

        self.val = 0
        self.val2 = 0

        self.full = False

    def setup(self):

        
        # geri lista fyrir sprites
        self.wall_list = arcade.SpriteList()
        self.skot_list = arcade.SpriteList()
        self.ovina_list = arcade.SpriteList()
        self.peninga_list = arcade.SpriteList()

        # stig
        self.score = 0

        self.player = Player()
        self.player.center_x = 10
        self.player.center_y = 70

        # set up ákveðið marga ovini og set þá í lista 

        for x in range(self.erfidleiki[1]):
            enemy = Enemy()
            enemy.center_x = random.randint(500,550)
            enemy.center_y = 82
            enemy.change_x = random.randint(2,3)
            self.ovina_list.append(enemy)

        for x in range(self.erfidleiki[2]):
            enemy = Enemy()
            enemy.center_x = random.randint(800,1000)
            enemy.center_y = 82
            enemy.change_x = random.randint(2,5)
            self.ovina_list.append(enemy)
        for x in range(self.erfidleiki[3]):
            enemy = Enemy()
            enemy.center_x = random.randint(1200,1800)
            enemy.center_y = 82
            enemy.change_x = random.randint(2,5)
            self.ovina_list.append(enemy)
        
        # geri physics engine 
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,self.wall_list,gravity)

        # geri nota csv fallið
        cord_listi = readcsv()

        # bí til veggi og set þá í lista
        for x in cord_listi:
            if x[2]=="0":
                wall = arcade.Sprite("data/floor.png", 1)
                wall.center_x = x[0]-25
                wall.center_y = x[1]-25

                self.wall_list.append(wall)
        endi = arcade.Sprite("data/end.png")
        endi.center_x = 2000-25
        endi.center_y = 50-25
        self.wall_list.append(endi)


      
        # geri 3 peninga
        star = arcade.Sprite("data/peningur.png")
        star.center_x = 250-25
        star.center_y = 450-25
        self.peninga_list.append(star)

        star = arcade.Sprite("data/peningur.png")
        star.center_x = 900-25
        star.center_y = 100-25
        self.peninga_list.append(star)

        star = arcade.Sprite("data/peningur.png")
        star.center_x = 1950-25
        star.center_y = 450-25
        self.peninga_list.append(star)

        # set upp veiw 
        self.view_left = 0
        self.view_bottom = 0

    
    def on_draw(self):
        arcade.start_render()
        # ef  game er True þá tekinar forritið allt sem þarf fyrir leikinn
        if self.game:
            arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)

            # tekna öll sprites
            self.player.draw()
            self.wall_list.draw()
            self.skot_list.draw()
            self.peninga_list.draw()
            self.ovina_list.draw()
            
            # tekna texta sem þarf að sýna og nota text_x sem hreifst með veiwinu 
            arcade.draw_text("ESC - Heim", self.text_x, 560, arcade.color.WHITE, 20)
            output = f"Stig: {self.score}"
            arcade.draw_text(output, self.text_x, 530, arcade.color.WHITE, 20)
            lif = f"Líf: {self.player.player_lives} "

            arcade.draw_text(lif, self.text_x, 500, arcade.color.WHITE, 20)


        # ef start abreytan er true
        if self.start:
            # forritið teiknar main menu
            arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
            if self.val == 0:
                arcade.draw_text("--> Spila",3400, 300, arcade.color.BLUE, 30)
                arcade.draw_text("Stillingar",3400, 200, arcade.color.LIGHT_BLUE, 30)
                arcade.draw_text("Hætta",3400, 100, arcade.color.LIGHT_BLUE, 30)
            if self.val == 1:
                arcade.draw_text("Spila",3400, 300, arcade.color.LIGHT_BLUE, 30)
                arcade.draw_text("--> Stillingar",3400, 200, arcade.color.BLUE, 30)
                arcade.draw_text("Hætta",3400, 100, arcade.color.LIGHT_BLUE, 30)
            if self.val == 2:
                arcade.draw_text("Spila",3400, 300, arcade.color.LIGHT_BLUE, 30)
                arcade.draw_text("Stillingar",3400, 200, arcade.color.LIGHT_BLUE, 30)
                arcade.draw_text("--> Hætta",3400, 100, arcade.color.BLUE, 30)

            arcade.draw_text("Skot Leikur",3400, 500, arcade.color.BLUE, 40)
        
        # ef leikmaður deyr eða vinnur þá skrifar forritð það
        elif self.dead:
            arcade.set_background_color(arcade.color.RED)
            arcade.draw_text("ESC - Heim",4020, 560, arcade.color.WHITE, 20)
            arcade.draw_text("R - byrja upp á nýtt",4020, 530, arcade.color.WHITE, 20)
            arcade.draw_text("Þú Dóst!",4400, 500, arcade.color.WHITE, 40)
            arcade.draw_text(f"stig {self.score}",5400, 400, arcade.color.WHITE, 40)
        elif self.vann:
            arcade.set_background_color(arcade.color.FRESH_AIR)
            arcade.draw_text("ESC - Heim",5020, 560, arcade.color.WHITE, 20)
            arcade.draw_text("R - byrja upp á nýtt",5020, 530, arcade.color.WHITE, 20)
            arcade.draw_text("Þú vannst",5400, 500, arcade.color.WHITE, 40)
            arcade.draw_text(f"stig {self.score}",5400, 400, arcade.color.WHITE, 40)
            
            
        
        # ef menu er true teiknar forritð menu sem maður getur kveikt á full screen og breytt erfið leika
        elif self.menu:
            arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
            if self.val2 == 0:
                arcade.draw_text(f"Fullur Skjár: {self.fullscreen}",6400, 300, arcade.color.BLUE, 30)
                arcade.draw_text(f"Erfiðleiki: <{self.erfidleiki_text}>",6400, 200, arcade.color.LIGHT_BLUE, 30)
                arcade.draw_text("Til Baka",6400, 100, arcade.color.LIGHT_BLUE, 30)
            if self.val2 == 1:
                arcade.draw_text(f"Fullur Skjár: {self.fullscreen}",6400, 300, arcade.color.LIGHT_BLUE, 30)
                arcade.draw_text(f"Erfiðleiki: <{self.erfidleiki_text}>",6400, 200, arcade.color.BLUE, 30)
                arcade.draw_text("Til Baka",6400, 100, arcade.color.LIGHT_BLUE, 30)
            if self.val2 == 2:
                arcade.draw_text(f"Fullur Skjár: {self.fullscreen}",6400, 300, arcade.color.LIGHT_BLUE, 30)
                arcade.draw_text(f"Erfiðleiki: <{self.erfidleiki_text}>",6400, 200, arcade.color.LIGHT_BLUE, 30)
                arcade.draw_text("Til Baka",6400, 100, arcade.color.BLUE, 30)
            arcade.draw_text("Stillingar",6400, 500, arcade.color.BLUE, 40)


    def on_key_press(self, key, modifiers):
        if self.game:
            if key == arcade.key.SPACE or key == arcade.key.W or key == arcade.key.UP:
                if self.physics_engine.can_jump():
                    self.player.change_y = Player_jump_speed
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.player.change_x = -MOVEMENT_SPEED
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player.change_x = MOVEMENT_SPEED
            elif key == arcade.key.ESCAPE:
                self.start = True
                self.game = False
        
        elif self.start:
            if key == arcade.key.DOWN:
                if self.val >=2:
                    self.val = 0
                else:
                    self.val+=1

            if key == arcade.key.UP:
                if self.val <= 0:
                    self.val = 2
                else:
                    self.val -= 1

            if key == arcade.key.ENTER:
                if self.val == 0:
                    self.game = True
                    self.start = False
                    self.player.center_x = 50
                    self.player.center_y = 70
                elif self.val == 1:
                    self.menu = True
                    self.start = False
                elif self.val == 2:
                    arcade.close_window()
        elif self.dead:
            if key == arcade.key.ESCAPE:
                self.start = True 
                self.dead = False
                self.player.player_lives = 3
            if key == arcade.key.R:
                self.game = True
                self.dead = False
                self.player.center_x = 50
                self.player.center_y = 70
                self.player.player_lives = 3

        elif self.vann:
            if key == arcade.key.ESCAPE:
                self.start = True 
                self.vann = False
                self.player.player_lives = 3
                self.score = 0
            if key == arcade.key.R:
                self.game = True
                self.vinn = False
                self.player.center_x = 50
                self.player.center_y = 70
                self.player.player_lives = 3
                self.score = 0

        elif self.menu:
            if key == arcade.key.DOWN:
                if self.val2 >=2:
                    self.val2 = 0
                else:
                    self.val2+=1

            elif key == arcade.key.UP:
                if self.val2 <= 0:
                    self.val2 = 2
                else:
                    self.val2 -= 1

            elif key == arcade.key.ENTER:
                if self.val2 == 0:
                    self.set_fullscreen(not self.fullscreen)

                elif self.val2 == 1:
                    pass
                elif self.val2 == 2:
                    self.menu = False
                    self.start = True

            elif key == arcade.key.RIGHT:
                if self.erfidleiki[0] >=3:
                    self.erfidleiki[0] = 0
                else:
                    self.erfidleiki[0]+=1

            if key == arcade.key.LEFT:
                if self.erfidleiki[0] <= 0:
                    self.erfidleiki[0] = 3
                else:
                    self.erfidleiki[0] -= 1

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game:
            arcade.play_sound(self.skothljod)
            bullet = arcade.Sprite("data/skot.png", sprite_scaling_skot)

            bullet.center_x = self.player.center_x
            bullet.center_y = self.player.center_y

            if self.player.texture  == self.player.textures[0]:
                bullet.change_x = -skot_hradi
                bullet.angle = 0
                self.skot_list.append(bullet)

            elif self.player.texture  == self.player.textures[1]:
                bullet.change_x = skot_hradi
                bullet.angle = 0
                self.skot_list.append(bullet)
            else:
                bullet.change_x = -skot_hradi
                bullet.angle = 0
                self.skot_list.append(bullet)
        if self.start:
            pass


    # fall em updatar allt
    def update(self, delta_time):
        if self.game:
            self.player.update()
            self.skot_list.update()
            self.physics_engine.update()
            for enemy in self.ovina_list:
                enemy.update()
                if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                        enemy.change_x *= -1

            # checka hvort leikmaður hreyfist úr boundery þá hreyfist skjárinn
            changed = False

            self.text_change = 0
            left_boundary = self.view_left + veiwport_margin
            if self.player.left < left_boundary:
                self.view_left -= left_boundary - self.player.left
                self.text_change = 1
                changed = True


            right_boundary = self.view_left + screen_width - veiwport_margin
            if self.player.right > right_boundary:
                self.view_left += self.player.right - right_boundary
                self.text_change = 2
                changed = True

            top_boundary = self.view_bottom + screen_height - veiwport_margin
            if self.player.top > top_boundary:
                self.view_bottom += self.player.top - top_boundary

            bottom_boundary = self.view_bottom + veiwport_margin
            if self.player.bottom < bottom_boundary:
                self.view_bottom -= bottom_boundary - self.player.bottom
                changed = True

            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)
            if self.view_left <0:
                self.view_left = 0
            if self.view_left >2000:
                self.view_left = 2000
            if changed:
                arcade.set_viewport(self.view_left,
                                    screen_width + self.view_left - 1,
                                    0,
                                    screen_height + 0 - 1)
                self.text_x = self.view_left+20
            

            for skot in self.skot_list:

                hit_list = arcade.check_for_collision_with_list(skot, self.wall_list)
                hit_list2 = arcade.check_for_collision_with_list(skot,self.ovina_list)
                
                if len(hit_list) > 0:
                    skot.remove_from_sprite_lists()

                for enemy in hit_list2:
                    enemy.remove_from_sprite_lists()
                    skot.remove_from_sprite_lists()
                    self.score += 1
                if skot.bottom > screen_width:
                    skot.remove_from_sprite_lists()
                if skot.bottom  <0:
                    skot.remove_from_sprite_lists()
            if len(arcade.check_for_collision_with_list(self.player, self.ovina_list)) > 0:
                self.player.player_lives -= 1
                self.player.center_x = 50
                self.player.center_y = 70
            if self.player.player_lives <=0:
                self.game = False
                self.dead = True
            for coin in self.peninga_list:
                hit_list3 = arcade.check_for_collision_with_list(self.player,self.peninga_list)
                if len(hit_list3):
                    coin.remove_from_sprite_lists()
                    self.score += 10
            if self.player.center_x > 1950:
                self.vann = True
                self.game = False
        elif self.start:
            arcade.set_viewport(3000,4000,
                                    0,
                                    600)
        elif self.dead:
            arcade.set_viewport(4000,5000,
                                    0,
                                    600)
        elif self.vann:
            arcade.set_viewport(5000,6000,
                                    0,
                                    600)
            
        elif self.menu:
            arcade.set_viewport(6000,7000,
                                    0,
                                    600)

            if self.erfidleiki[0] == 0:
                self.erfidleiki = [0,1,2,4]
                self.erfidleiki_text = "Létt"
            elif self.erfidleiki[0] == 1:
                self.erfidleiki = [1,2,5,8]
                self.erfidleiki_text = "Miðlungs"
            elif self.erfidleiki[0] == 2:
                self.erfidleiki = [2,4,8,20]
                self.erfidleiki_text = "Erfitt"
            elif self.erfidleiki[0] == 3:
                self.erfidleiki = [3,10,50,100]
                self.erfidleiki_text = "Extreme"



        if self.start or self.vann or self.dead:
            self.skot_list = arcade.SpriteList()
            self.ovina_list = arcade.SpriteList()
            self.peninga_list = arcade.SpriteList()
            for x in range(self.erfidleiki[1]):
                enemy = Enemy()
                enemy.center_x = random.randint(500,550)
                enemy.center_y = 82
                enemy.change_x = random.randint(2,3)
                self.ovina_list.append(enemy)

            for x in range(self.erfidleiki[2]):
                enemy = Enemy()
                enemy.center_x = random.randint(800,1000)
                enemy.center_y = 82
                enemy.change_x = random.randint(2,5)
                self.ovina_list.append(enemy)
            for x in range(self.erfidleiki[3]):
                enemy = Enemy()
                enemy.center_x = random.randint(1200,1800)
                enemy.center_y = 82
                enemy.change_x = random.randint(2,5)
                self.ovina_list.append(enemy)


            star = arcade.Sprite("data/peningur.png")
            star.center_x = 250-25
            star.center_y = 450-25
            self.peninga_list.append(star)

            star = arcade.Sprite("data/peningur.png")
            star.center_x = 900-25
            star.center_y = 100-25
            self.peninga_list.append(star)

            star = arcade.Sprite("data/peningur.png")
            star.center_x = 1950-25
            star.center_y = 450-25
            self.peninga_list.append(star)
        

# main breyta sem runar arcade og gerir leikur klassan
def main():
    """ Main method """

    window = Leikur()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
