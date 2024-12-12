import pygame
import sys 
import random
import math



pygame.init()
info = pygame.display.Info()
w, h = info.current_w, info.current_h
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
pygame.display.set_caption('physics, math, code & fun')

pygame.mixer.init()
beep = pygame.mixer.Sound("beep.mp3")
font = pygame.font.SysFont('Arial', 50)
clock = pygame.time.Clock()

t = 0
delta_time = 0.0


class Particles:
    def __init__(self, x, y, radius):
        self.pos =  [x, y]
        self.radius = radius
        self.visible = True
        self.enable = False
        self.color = [random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)]
        self.velocity = [5*random.uniform(-1.0,1.0), 5*random.uniform(-1.0,1.0)]
        self.n_coll = 0
        self.mass = 0.01 * self.radius
        if self.radius <= 0:
            self.mass = 0.01

    def draw(self, screen):
        if self.visible:
            pygame.draw.circle(screen, self.color, self.pos, self.radius)
    def move(self):
        isCollide = False
        last_pos = self.pos
        
        if self.pos[0] - self.radius <= 0 or self.pos[0] + self.radius >= w:
            self.pos[0] = last_pos[0]
            self.velocity[0] = -self.velocity[0] 
            isCollide = True            
        if self.pos[1] - self.radius <= 0 or self.pos[1] + self.radius >= h:
            self.pos[1] = last_pos[1]
            self.velocity[1] = -self.velocity[1] 
            isCollide = True            

        self.pos[0] += self.velocity[0]          
        self.pos[1] += self.velocity[1]

        return isCollide        

particles = []
pixels = []

        
particles.append(Particles(450,450,400))        
particles.append(Particles(w - 450,h - 450,400)) 

def collision(l1):
    global particles
    
    ret = -1

    for l2 in range(0, len(particles)):
        if l2 != l1 and particles[l2].visible:
            m1 = particles[l1].mass
            m2 = particles[l2].mass
            
            v1i = particles[l1].velocity
            v2i = particles[l2].velocity
            
            n = [particles[l1].pos[0] - particles[l2].pos[0], particles[l1].pos[1] - particles[l2].pos[1]]         
            dist = math.sqrt(n[0]**2 + n[1]**2)
                  
            if dist != 0.0:
                n[0] = n[0] / dist
                n[1] = n[1] / dist
             
            v_dot_n = (v1i[0] - v2i[0]) * n[0] + (v1i[1] - v2i[1]) * n[1]
            
            if dist < particles[l1].radius + particles[l2].radius and v_dot_n < 0 and dist != 0.0:
                
                e = 1
                I_n = -(1+e) * ((m1*m2) / (m1 + m2)) * v_dot_n
               
                particles[l1].velocity[0] = v1i[0] + (I_n / m1) * n[0]
                particles[l1].velocity[1] = v1i[1] + (I_n / m1) * n[1]
                
                particles[l2].velocity[0] = v2i[0] - (I_n / m2) * n[0]
                particles[l2].velocity[1] = v2i[1] - (I_n / m2) * n[1]
            
                ret = l2
            
            if dist < particles[l1].radius + particles[l2].radius:
                particles[l1].n_coll += 1
                particles[l2].n_coll += 1
            else:
                particles[l1].n_coll = 0
                particles[l2].n_coll = 0

            
    return ret            
  
            
           
def Update(screen):
    global t
    global delta_time

    screen.fill((0,0,0))

    for l1 in range(0, len(particles)):
        if particles[l1].visible:
            particles[l1].draw(screen) 
           
            l2 = collision(l1) # circle-circle collision 

            if l2 != -1: # one per collision
                if particles[l1].n_coll <= 1:
                    beep.play() 
                    
                    if particles[l1].radius > 20: 
                        new_r1 = particles[l1].radius // 2
                        p = Particles(particles[l1].pos[0], particles[l1].pos[1], new_r1) 
                        p.velocity = [5*random.uniform(-1.0,1.0), 5*random.uniform(-1.0,1.0)]
                        particles.append(p)
                        particles[l1].radius = new_r1
                        
                        particles[l1].velocity = [5*random.uniform(-1.0,1.0), 5*random.uniform(-1.0,1.0)]
                        particles[l1].mass = 0.01 * new_r1
                        
                    if particles[l2].radius > 20: 
                        new_r2 = particles[l2].radius // 2
                        p = Particles(particles[l2].pos[0], particles[l2].pos[1], new_r2) 
                        p.velocity = [5*random.uniform(-1.0,1.0), 5*random.uniform(-1.0,1.0)]
                        particles.append(p)
                        particles[l2].radius = new_r2
                        particles[l2].velocity = [5*random.uniform(-1.0,1.0), 5*random.uniform(-1.0,1.0)]
                        particles[l2].mass = 0.01 * new_r2
                    
                    


            particles[l1].move() # move and wall collision



    text = font.render('github.com/PhysicsMathCodeAndFun', True, (255,255,255))
    screen.blit(text, pygame.Rect(100, 0, 400,300))

    t += 1
    
    delta_time = clock.tick(60) / 1000
    pygame.display.flip()
    


isEnd = False
while not isEnd:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isEnd = True
            
    Update(screen)
    
pygame.quit()
sys.exit()
