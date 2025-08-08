import board
import digitalio
import displayio
import adafruit_displayio_ssd1306
import terminalio
from adafruit_display_text import label
import time
import i2cdisplaybus

displayio.release_displays()

i2c = board.I2C()
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

switch = digitalio.DigitalInOut(board.D7)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

enc_a = digitalio.DigitalInOut(board.D0)
enc_a.direction = digitalio.Direction.INPUT
enc_a.pull = digitalio.Pull.UP

enc_b = digitalio.DigitalInOut(board.D2)
enc_b.direction = digitalio.Direction.INPUT
enc_b.pull = digitalio.Pull.UP

codes = {
    "gmail": "ABC123XYZ",
    "discord": "DEF456UVW", 
    "reddit": "GHI789RST",
    "jetbrains": "JKL012MNO"
}

keys = list(codes.keys())
current_index = 0
last_enc_a_state = enc_a.value
switch_pressed = False
display_needs_update = True

splash = displayio.Group()
display.root_group = splash

text_area = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=64, y=16)
text_area.anchor_point = (0.5, 0.5)
text_area.anchored_position = (64, 16)
splash.append(text_area)

def update_display():
    global display_needs_update
    if not switch_pressed:
        text_area.text = keys[current_index]
    else:
        text_area.text = codes[keys[current_index]]
    display_needs_update = False

def check_rotary_encoder():
    global current_index, last_enc_a_state, display_needs_update
    
    current_a_state = enc_a.value
    
    if last_enc_a_state and not current_a_state:
        if enc_b.value:
            current_index = (current_index + 1) % len(keys)
        else:
            current_index = (current_index - 1) % len(keys)
        display_needs_update = True
    
    last_enc_a_state = current_a_state

while True:
    if display_needs_update:
        update_display()
    
    check_rotary_encoder()
    
    if not switch.value and not switch_pressed:
        switch_pressed = True
        display_needs_update = True
    
    if switch.value and switch_pressed:
        switch_pressed = False
        display_needs_update = True

