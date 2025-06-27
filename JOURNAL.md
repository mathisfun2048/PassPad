title: PassPad
author: Arya C. 
description: Convinent way to physically transport a password! (I love my password manager but what if I need to log into a public device where I don't want to link that?)
created_at: 06-26-2025

# June 26

## 2PM -> 3PM (1 hour)

Spent this time researching possible parts and drawing a sketch of what I want this to look like. After, I wrote out the explicit objectives of this project. 

### Initial Sketch
![Initial Sketch](https://github.com/user-attachments/assets/45d1da0c-0bc1-4e0a-940c-a1a77d4ac390)

### Interem BOM
- 0.91 OLED Display
- EC11 Rotary Encoders
- MX-Style Switch
- White DSA Keycap
- XIAO Microprocessor
- Custom PCB
- 3D Printed Case
- 2.5M x 4mm Screws

### Required Functionality
This project is meant to be a compact password transporter to where you need to have a secure password but don't want to log into your password manager. 

- This device should be able to store multiple passwords which the encoder should be able to rotate between
- The OLED pannel should display a short codename for the password (e.x. "password 1")
- The switch should then be repeatedly pressed until the password in its entierity is transmitted
- After the password is transmitted, no new data should be pushed even if the switch is pressed. The OLED pannel should communicate that the password has been transmitted (e.x. "successful")


sidenote: i've been going into a slump over desiging and itterating complex designs so I thought making this would be a fun in-between project. 


## 6PM -> 8PM (2 hours)

While making the schematic, went into a deep-dive on how microprocessors work! In the past, I only really worked with full on machines (raspberri pi zeros, 3b+) so seeing how this worked in a custom project was pretty cool. 

After looking into that, I started on my PCB schematic. This is, compared to my other projects, stupidly simple. But it was cool nonetheless--I have never seen a similar device in the wild and it feels really cool being able to build something. 
