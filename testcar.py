import pygame
import os
import random

WIDTH = 500
HEIGHT = 500
FPS = 30

BLACK = (0,0,0)
WHITE =(255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

#ส่วนหน้าต่างเกมเริ่มต้น
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Shooting Tank')
clock = pygame.time.Clock()

# สร้างรถถัง
# = C:\Users\Knab\Desktop\tank
game_folder = os.path.dirname(__file__)
# = C:\Users\Knab\Desktop\tank\img
img_folder = os.path.join(game_folder, 'img')

print(game_folder)

#ตัวแสดงคะแนน
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

    
class Tank(pygame.sprite.Sprite):  #ฟังชั่นตัวละคร
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((50,40))
        tank_img = os.path.join(img_folder,'carofgun.png')
        self.image = pygame.image.load(tank_img).convert()
        self.image.set_colorkey(BLACK)
        
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT -10

        self.speedx = 0
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
            
        self.rect.x += self.speedx
        
        if self.rect.right > WIDTH:
             self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
        #print(self.rect.centerx)
    def shoot(self):
        Bullet = bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(Bullet)
        Bullets.add(Bullet)
#ฝ่ายตรงข้าม            
class enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        enemy_img = os.path.join(img_folder,'killingcar.png')
        
        self.image = pygame.image.load(enemy_img).convert()
        self.image.set_colorkey(BLACK)
        
        #self.image = pygame.Surface((30,40))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1,5)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,5)
            

class bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        bullet_img = os.path.join(img_folder,'bulletforgun.png')
        self.image = pygame.image.load(bullet_img).convert()
        self.image.set_colorkey(BLACK)
        #self.image = pygame.Surface((10,20))
        #self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
            
       
#สร้างผู้เล่น
all_sprites = pygame.sprite.Group()
tank = Tank()
all_sprites.add(tank)

enemys = pygame.sprite.Group()
Bullets = pygame.sprite.Group()        
for i in range(10):
    em = enemy()
    all_sprites.add(em)
    enemys.add(em)

score = 0

running = True

#เช็คเพื่อปิด
while running:
    clock.tick(FPS)
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tank.shoot()

    all_sprites.update()

    #การยิง
    hits = pygame.sprite.groupcollide(enemys ,Bullets, True, True)
    if hits:
        score += 1
        em = enemy()
        all_sprites.add(em)
        enemys.add(em)

   
        
    hits = pygame.sprite.spritecollide(tank ,enemys, False)
    if hits:
        running = False
    
    screen.fill(BLUE)  #สีพื่นหลังดึงมาจากการตั้งค่าสีข้างบน
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH /2,10)

    
    pygame.display.flip()
    

pygame.quit()
