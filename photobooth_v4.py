from gpiozero import Button
from picamera import PiCamera
import pygame
import time
from pygame import QUIT, KEYDOWN, K_ESCAPE
from time import sleep
import config
from os import system

### Init buttons ###
buttonRed = Button(2)
buttonBlue = Button(3)

### Init camera ###
camera = PiCamera()
camera.resolution = (1366, 768)

### Init pygames ###
pygame.init()
infoObject = pygame.display.Info()
print(infoObject.current_w)
print(infoObject.current_h)
pygame.display.set_mode((config.monitor_w, config.monitor_h))
screen = pygame.display.get_surface()
pygame.display.set_caption('Photobooth')
pygame.mouse.set_visible(False)
pygame.display.toggle_fullscreen()

###################
#### FUNCTIONS ####
###################

# Handle quit events
def input(events):
  for event in events:
    if (event.type == QUIT or
        (event.type == KEYDOWN and event.key == K_ESCAPE)):
      pygame.quit()

# Display a blank screen
def clear_screen():
  screen.fill( (0,0,0) )
  pygame.display.flip()
  
def show_image(path):
  screen.fill( (0,0,0) )

  img = pygame.image.load(path)
  img = img.convert()
  screen.blit(img,(0,0))
  pygame.display.flip()

def start_photobooth():
  input(pygame.event.get())
  show_image("screen_01.jpg")

  if buttonBlue.is_pressed:
    camera.start_preview()
    sleep(2)
    try:
      now = time.strftime("%Y%m%d-%H-%M-%S")
      filename = "/media/usb1/Photobooth/image_"+now+".jpg"
      camera.capture(filename)
    finally:
      camera.stop_preview()
      input(pygame.event.get())
      show_image(filename)
      sleep(5)

  if buttonRed.is_pressed:
    camera.start_preview()
    sleep(2)
    try:
      now = time.strftime("%Y%m%d-%H-%M-%S")
      for i in range(5):
        camera.capture('image{0:02d}.jpg'.format(i))
        sleep(1)
      print("building the gif")
      camera.stop_preview()
      show_image("screen_02.jpg")
      filename = "/media/usb1/Photobooth/image_"+now+".gif"
      system('convert -delay 50 -loop 0 image*.jpg '+filename)
    finally:
      input(pygame.event.get())
      for i in range(2):
        show_image("image00.jpg")
        sleep(1)
        show_image("image01.jpg")
        sleep(1)
        show_image("image02.jpg")
        sleep(1)
        show_image("image03.jpg")
        sleep(1)
        show_image("image04.jpg")
        sleep(1)
      

while True:
  input(pygame.event.get())
  start_photobooth()
