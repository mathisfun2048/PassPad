title: PassPad

author: Arya C. 

description: Convinent way to physically transport a password! (I love my password manager but what if I need to log into a public device where I don't want to link that?)

created_at: 06-26-2025

time spent (so far): 19 hours

# June 26

## 2PM -> 3PM (1 hour)

Spent this time researching possible parts and drawing a sketch of what I want this to look like. After, I wrote out the explicit objectives of this project. 

### Initial Sketch
![Initial Sketch](https://github.com/user-attachments/assets/45d1da0c-0bc1-4e0a-940c-a1a77d4ac390)

### Interem BOM
- 0.91 OLED Display
- EC11 Rotary Encoder
- MX-Style Switch
- White DSA Keycap
- 1N4148 Diodes
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

<img width="500" alt="Schematic" src="https://github.com/user-attachments/assets/dca50135-9fe8-40f4-b07f-57827bb4835d" />




### GPIO Guide
- 3.3v -> 3.3V (-> implicitly attached to VCC on display)
- GND -> GND (-> implicitly attached to GND on display, C pin on encoder, switch on encoder, and switch)
- Pin 1 -> diode -> one side of switch (other side is grounded)
- Pin 26 -> A pin on encoder
- Pin 27 -> diode -> one side of switch on encoder (other switch on encoder is grounded)
- Pin 28 -> B pin on encoder
- Pin 29 -> SCL on display
- Pin 6 -> SDA on display

now onto the PCB design!


## 8PM -> 9PM (1 hour)

Finished the PCB!

<img width="500" alt="Screenshot 2025-06-27 at 2 07 22 AM" src="https://github.com/user-attachments/assets/bd968576-1681-4c4e-a822-2cde2b15ebe1" />


Now time for the beast: coding it. I remember last time I used micropython with this controler and it wasn't the worst... lets see how this goes. This project, in my opinion, is more complex algorithmically than the hackpad (which has a lot of open keyboard examples online which I could directly learn from). This is me operating it all on my own! I hope it'll be fun though...


# June 27

## 9PM -> 5AM 7AM -> 2PM (15 hours)

Finished my code! 

Who could have thought this would be so complicated! 

Okay so here was my process:
At first I started with micropython, becasue I thought it would be a similar proccess as to my hackpad. I was wrong....

Because my device is not purely a keybaord, I could not use KMK libraries... fun fun

So I went searching for soemthing that would be a tad bit more usable per my skill level, and I discovered circuit python! Which had a LOT of libraries I could use to not work in low-level code! YAY!


Here is everything I was able to import to help with the code:

<img width="500" alt="Screenshot 2025-06-27 at 1 36 20 PM" src="https://github.com/user-attachments/assets/7aef729a-e7fc-4eb9-81b2-444c015e834f" />

One thing that I saw that made my code more rohbust was me being able to incorporate error handeling! I first truly learned the neccesity of it while making my PaperCAM project, and it was nice being able to see my learning and apply it to this. Error handeling is present primarily if the host device does not support HID, in which case the OLED pannel will display an error message. 

I wanted to incorporate a "copy" mode but then was lazy and forgot to do it. However, I was able to implement OS detection, so it will be reletivily easy to implmement that in the future. The reason I need OS detection is because I use a Mac which does not interpret CTRL+C as CMD+C. 

Overall, this was pretty fun, and you can see the full code in main.py under the firmware folder. 

I don't know really what else to add here, because my code is just a representation of my desgin statements that I made earlier in this journal. 


Now, onto the CAD!


## 2PM -> 4PM (2 Hours)

Finished the CAD case!

![CAD_Case_Together_Front](https://github.com/user-attachments/assets/228d2c02-e028-4f4e-8cc3-ea4853b50542)
![CAD_Case_Together_Back](https://github.com/user-attachments/assets/43eb18e7-db4d-464b-b2cc-3e35ed215d83)
![CAD_Case_Seperated_Front](https://github.com/user-attachments/assets/0bc24ce7-933c-4a87-96e0-afb060655d69)


## 4PM -> 5PM (1 Hour)

Put the repo all together for submission!











