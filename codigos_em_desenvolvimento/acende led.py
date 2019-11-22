import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
led=27
GPIO.setup(led,GPIO.OUT)
##Ligar
GPIO.output(led,GPIO.HIGH)
sleep(5)
##Desligar
GPIO.output(led,GPIO.LOW)
