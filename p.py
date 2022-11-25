import pygame
from math import ceil
import matplotlib.pyplot as plt

class Throttle:
    def __init__(self, x, y, w, h):
        self.throttleRect = pygame.Rect(x, y, w, h)
        w = w//2
        x = x + w
        self.x = x
        self.value = 0
        self.sliderRect = pygame.Rect(x - h//2, y, w + h//2, h)
        self.sliderRect2 = pygame.Rect(x - w, y, w + h//2, h)
        self.sliderBox = pygame.Rect(x - h//2, y, h, h)
        self.accelerator = pygame.Rect(x, y, 0, h)
    
    def get_value(self):
        return self.value

    def set_value(self, num):
        w = num / 100 * float(self.sliderRect.w - self.sliderBox.w)
        if w > 0:
            self.accelerator.w = ceil(w)
        else:
            self.accelerator.w = w // 1
        self.value = num
        self.sliderBox.x = self.accelerator.w + self.sliderRect.x

    def update_value(self, pos, click):
        if click and self.throttleRect.collidepoint(pos):
            x = pos[0]
            if x < self.sliderRect2.x + self.sliderBox.w//2:
                self.x = self.sliderRect2.x + self.sliderBox.w//2
            elif x > self.sliderRect.right - self.sliderBox.w//2:
                self.x = self.sliderRect.right - self.sliderBox.w//2
            else:
                self.x = x
            
            self.sliderBox.x = self.x - self.sliderBox.w//2
            self.accelerator.w = self.sliderBox.x - self.sliderRect.x

            if self.sliderBox.x < self.sliderRect.x + self.sliderBox.w//2 and self.sliderBox.right > self.sliderRect2.right - self.sliderBox.w//2:
                self.sliderBox.x = self.sliderRect.x
                self.accelerator.w = 0

            self.value = int((self.accelerator.w) / float(self.sliderRect.w - self.sliderBox.w) * 100)

    def draw(self, screen):
        pygame.draw.rect(screen, (70, 70, 70), self.sliderRect)
        pygame.draw.rect(screen, (70, 70, 70), self.sliderRect2)

        if self.value > 0:
            pygame.draw.rect(screen, pygame.Color('dodgerblue'), self.accelerator)
        else:
            pygame.draw.rect(screen, (255, 60, 60), (self.accelerator.x - abs(self.accelerator.w), self.accelerator.y, abs(self.accelerator.w), self.accelerator.h))
        
        pygame.draw.rect(screen, (255, 255, 255), self.sliderBox)

class Car():
    def __init__(self, velocity1, velocity2, distance):
        self.velocity1 = velocity1
        self.velocity2 = velocity2
        self.distance1 = 0
        self.acceleration1 = 0
        self.acceleration2 = 0
        self.relative_distance = distance
        self.relative_velocity = velocity1 - velocity2
        self.relative_acceleration = 0
        self.time = 0
        self.time_diff = 1/30

        self.velocity1_points = [velocity1]
        self.velocity2_points = [velocity2]
        self.relative_velocity_points = [velocity1 - velocity2]
        self.distance1_points = [0]
        self.relative_distance_points = [distance]
        self.acceleration1_points = [0]
        self.acceleration2_points = [0]
        self.relative_acceleration_points = [self.relative_acceleration]
        self.time_points = [0]
    
    def car(self, acceleration1, acceleration2):
        # Uses Velocity, Acceleration and Distance formula
        # v = u + at
        # d = ut + 1/2at²
        # v² - u² = 2ad
        self.acceleration1 = acceleration1
        self.acceleration2 = acceleration2

        self.distance1 = self.distance1 + 1000 / 3600 * self.velocity1 * self.time_diff + 0.5 * self.acceleration1 * self.time_diff * self.time_diff

        self.velocity1 = max(0, 1000 / 3600 * self.velocity1 + self.acceleration1 * self.time_diff)
        self.velocity2 = max(0, 1000 / 3600 * self.velocity2 + self.acceleration2 * self.time_diff)

        self.relative_acceleration = self.acceleration1 - self.acceleration2
        self.relative_distance = self.relative_distance - (1000 / 3600 * self.relative_velocity * self.time_diff + 0.5 * self.relative_acceleration * self.time_diff * self.time_diff)

        # Convert m/s to kmph
        self.velocity1 = 3.6 * self.velocity1
        self.velocity2 = 3.6 * self.velocity2
        self.relative_velocity = self.velocity1 - self.velocity2

        self.time = self.time + self.time_diff

        self.velocity1_points.append(round(self.velocity1, 2))
        self.velocity2_points.append(round(self.velocity2, 2))
        self.relative_velocity_points.append(round(self.relative_velocity, 2))
        self.distance1_points.append(round(self.distance1, 2))
        self.relative_distance_points.append(round(self.relative_distance, 2))
        self.acceleration1_points.append(round(self.acceleration1, 2))
        self.acceleration2_points.append(round(self.acceleration2,2 ))
        self.relative_acceleration_points.append(round(self.relative_acceleration, 2))
        self.time_points.append(round(self.time, 2))

    def car_data(self):
        print(f'\nVelocity1: {self.velocity1}kmph, Distance1: {self.distance1}m')
        print(f'Velocity2: {self.velocity2}kmph')
        print(f'Acceleration1: {self.acceleration1}m/s2, Acceleration2: {self.acceleration2}m/s2')
        print(f'Relative Velocity: {self.relative_velocity}kmph, Relative Acceleration: {self.relative_acceleration}m/s2, Relative Distance: {self.relative_distance}m\n')

class AutomaticBraking:
    def __init__(self):
        self.velocity = 0
        self.relative_velocity = 0
        self.relative_acceleration = 0
        self.relative_distance = 0
        self.safe_distance = 0
        self.time_to_collision = 30
        self.time_to_collision_prev = self.time_to_collision
        self.brake = False
        self.braking_power = 0
        self.braking_power_prev = 0
        self.braking_power_extra = 0
        self.braking_power_points = [self.braking_power]
        self.time_to_collision_points = [self.time_to_collision]
    
    def autobrake(self, velocity, relative_velocity, relative_acceleration, relative_distance):
        self.velocity = 1000 / 3600 * velocity
        self.relative_velocity = 1000 / 3600 * relative_velocity
        self.relative_acceleration = relative_acceleration
        self.relative_distance = relative_distance
        self.safe_distance = (self.velocity * self.velocity) / (2 * 7 * 2)

        self.time_to_collision = self.calculate_ttc()

        # Partial Braking for time to collision between 2.5 and 5 sec
        if self.time_to_collision < 5 and self.time_to_collision > 2.5:
            self.brake = True
            if self.time_to_collision < self.time_to_collision_prev:
                self.braking_power = min(100, self.braking_power + 2)
            else:
                self.braking_power = self.braking_power
            self.braking_power_prev = self.braking_power
            self.braking_power_extra = 0
        
        # Full Braking for time to collision less than 2.5 sec
        elif self.time_to_collision <= 2.5 and self.time_to_collision > 0:
            self.brake = True
            self.braking_power = 100
            self.braking_power_prev = self.braking_power
            self.braking_power_extra = 0
        
        # Once Automated Braking Activated and time to collision greater than 5 sec
        # Need to make Relative Acceleration 0,
        # Relative Velocity 0 and
        # Relative Distance greater than safe distance
        # Release Brake
        elif self.brake:
            if self.relative_acceleration > 0 and self.relative_distance < self.safe_distance * 2:
                self.braking_power_extra = 0
                self.braking_power = min(100, self.braking_power + 1)
                self.braking_power_prev = self.braking_power
            elif self.relative_velocity > 0:
                self.braking_power_extra = min(15, self.braking_power_extra + 1)
                self.braking_power = min(100, self.braking_power_prev + self.braking_power_extra)
            elif self.relative_distance < self.safe_distance / 2:
                self.braking_power_extra = 0
                self.braking_power = self.braking_power
                self.braking_power_prev = self.braking_power
            else:
                self.braking_power_extra = 0
                self.braking_power = max(0, self.braking_power - 2)
                self.braking_power_prev = self.braking_power
        
        if not self.braking_power:
            self.brake = False
            self.braking_power_prev = 0
            self.braking_power_extra = 0
        
        self.time_to_collision_prev = self.time_to_collision
        self.braking_power_points.append(self.braking_power)
        self.time_to_collision_points.append(self.time_to_collision)
    
    def calculate_ttc(self):
        # For a ≠ 0
        # d = ut + 1/2at²
        if self.relative_acceleration:
            a = self.relative_acceleration
            b = self.relative_velocity
            c = -self.relative_distance

            d = b * b - 2 * a * c

            time = (-b + d ** 0.5) / a

            if isinstance(time, complex):
                return 30
            if time < 0:
                return 30
            return round(time, 2)

        elif not self.relative_acceleration:
            # For a = 0
            # Time = Distance / Velocity
            if not self.relative_velocity:
                return 30
            
            time = round(self.relative_distance / self.relative_velocity, 2)
            if time < 0:
                return 30
            return time


pygame.init()
screen = pygame.display.set_mode((750, 500))
cars = Car(100, 100, 50)
car1_image = pygame.image.load('car1.png')
car2_image = pygame.image.load('car2.png')
# To prevent car from going out of screen
max_left = 50
max_right = 600
autobrake = AutomaticBraking()
car1_throttle = Throttle(125, 400, 200, 20)
car2_throttle = Throttle(425, 400, 200, 20)

clock = pygame.time.Clock()

font = pygame.font.SysFont('Calibri', 25)
font2 = pygame.font.SysFont('Calibri', 20)
run = True

lines_rect = []
x = 0
for i in range(6):
    lines_rect.append(pygame.Rect(x, 305, 100, 3))
    x = x + 150

while run:
    screen.fill((30,30,30))
    car1_pos = max(max_left, max_right - 100 - cars.relative_distance * 5)
    screen.blit(car1_image, (car1_pos, 270))
    screen.blit(car2_image, (max_right, 270))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        car1_throttle.set_value(max(-100, car1_throttle.get_value() - 5))
    elif keys[pygame.K_d]:
        car1_throttle.set_value(min(100, car1_throttle.get_value() + 5))
    elif keys[pygame.K_s]:
        car1_throttle.set_value(0)
    if keys[pygame.K_LEFT]:
        car2_throttle.set_value(max(-100, car2_throttle.get_value() - 5))
    elif keys[pygame.K_RIGHT]:
        car2_throttle.set_value(min(100, car2_throttle.get_value() + 5))
    elif keys[pygame.K_DOWN]:
        car2_throttle.set_value(0)
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    car1_throttle.update_value(mouse, click[0])
    car2_throttle.update_value(mouse, click[0])

    autobrake.autobrake(cars.velocity1, cars.relative_velocity, cars.relative_acceleration, cars.relative_distance)

    if autobrake.brake:
        value = min(-autobrake.braking_power, car1_throttle.get_value() + 2)
        if value == -2 or value == -1:
            value = 0
        acceleration1 = 7 * value / 100
        car1_throttle.set_value(value)

    # To prevent car from going reverse when velocity is 0
    if car1_throttle.get_value() < 0 and not cars.velocity1:
        acceleration1 = 0
    else:
        acceleration1 = 7 * car1_throttle.get_value() / 100
    
    if car2_throttle.get_value() < 0 and not cars.velocity2:
        acceleration2 = 0
    else:
        acceleration2 = 7 * car2_throttle.get_value() / 100
    
    cars.car(acceleration1, acceleration2)
    car1_throttle.draw(screen)
    car2_throttle.draw(screen)

    car2_distance = 1000 / 3600 * cars.velocity2 * cars.time_diff + 0.5 * cars.acceleration2 * cars.time_diff * cars.time_diff
    lines_rect[0].x = lines_rect[0].x - int(car2_distance * 15)
    if lines_rect[0].right < 0:
        lines_rect[0].x = 50
    pygame.draw.rect(screen, (255, 255, 255), lines_rect[0])

    for i in range(1, 6):
        lines_rect[i].x = lines_rect[i-1].x + 150
        pygame.draw.rect(screen, (255, 255, 255), lines_rect[i])

    line = font2.render('Car 1', 1, (255, 255, 255))
    line2 = font2.render(f'Velocity: {round(cars.velocity1, 0)} kmph', 1, (255, 255, 255))
    line3 = font2.render(f'Acceleration: {round(cars.acceleration1, 2)} m/s2', 1, (255, 255, 255))

    line4 = font2.render('Car 2', 1, (255, 255, 255))
    line5 = font2.render(f'Velocity: {round(cars.velocity2, 0)} kmph', 1, (255, 255, 255))
    line6 = font2.render(f'Acceleration: {round(cars.acceleration2, 2)} m/s2', 1, (255, 255, 255))

    line7 = font2.render(f'Relative Velocity: {round(cars.relative_velocity, 1)} kmph', 1, (255, 255, 255))
    line8 = font2.render(f'Relative Acceleration: {round(cars.relative_acceleration, 2)} m/s2', 1, (255, 255, 255))
    line9 = font2.render(f'Relative Distance: {round(cars.relative_distance, 1)} m', 1, (255, 255, 255))

    screen.blit(line, (125, 50))
    screen.blit(line2, (125, 100))
    screen.blit(line3, (125, 150))
    screen.blit(line4, (425, 50))
    screen.blit(line5, (425, 100))
    screen.blit(line6, (425, 150))
    screen.blit(line7, (125, 200))
    screen.blit(line8, (425, 200))
    screen.blit(line9, (375 - line9.get_width()//2, 350))

    throttle1_value = font.render(str(car1_throttle.get_value()), 1, (255, 255, 255))
    screen.blit(throttle1_value, (car1_throttle.sliderRect.x + car1_throttle.sliderBox.w//2 - throttle1_value.get_width()//2, car1_throttle.sliderRect.y + 30))

    throttle2_value = font.render(str(car2_throttle.get_value()), 1, (255, 255, 255))
    screen.blit(throttle2_value, (car2_throttle.sliderRect.x + car2_throttle.sliderBox.w//2 - throttle2_value.get_width()//2, car2_throttle.sliderRect.y + 30))

    pygame.display.update()
    clock.tick(30)

pygame.quit()

cars.car_data()

figure, graph = plt.subplots(2, 2)

graph[0][0].plot(cars.time_points, cars.velocity1_points, label='Velocity1')
graph[0][0].plot(cars.time_points, cars.velocity2_points, label='Velocity2', color='green')
graph[0][0].set_title('Velocity vs Time')
graph[0][0].set_xlabel('Time (s)')
graph[0][0].set_ylabel('Velocity (km/h)')
graph[0][0].legend()

graph[0][1].plot(cars.time_points, autobrake.braking_power_points)
graph[0][1].set_ylim(bottom=0, top=105)
graph[0][1].set_title('Braking Power vs Time')
graph[0][1].set_xlabel('Time (s)')
graph[0][1].set_ylabel('Braking Power (%)')

graph[1][0].plot(cars.time_points, autobrake.time_to_collision_points)
graph[1][0].set_ylim(bottom=0, top=7)
graph[1][0].set_title('Time to collision vs Time')
graph[1][0].set_xlabel('Time (s)')
graph[1][0].set_ylabel('Time to collision (s)')

graph[1][1].plot(cars.time_points, cars.relative_distance_points)
graph[1][1].set_title('Relative Distance vs Time')
graph[1][1].set_xlabel('Time (s)')
graph[1][1].set_ylabel('Relative Distance (m)')

figure.tight_layout()
plt.show()
exit()
