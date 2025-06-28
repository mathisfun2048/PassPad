# PassPAD 

![Initial Sketch](https://github.com/user-attachments/assets/1e8a41a7-2f07-4a86-a2f1-a32b6212f76f)

## Description and Exigence

This is my fourth attempt at hardware design, and it's been so much fun!

One thing I've been dreading about starting college is moving away from my mac to use a windows laptop for my engineering degree. One of my key contentions was not being able to use the in-built password manger to hold large, secure passwords that I would have otherwise not been able to memorize. This project aims to help me in this problem. 

This device is going to hold passwords with a nickname. The encoder will be able to rotate between saved passwords, with the nickname appearing on the OLED dispaly. The password can be "typed" by repeatedly pressing the switch, which will dynamically change to the charachter next in the password. As a password is being typed, a completion bar will appear on the OLED> After the password is typed, a "completed" message will appear on the oled.

While the hardware for this is pretty simple, the software was not. Instead of being able to use the KMK or QMK frameworks, I learned circuitpython to make this hardware truly custom. I havn't seen a physical password transporter anywhere on the market, so it was really cool building this from scratch. (I submitted it as a 4-point project as my BOM ~$50 , but if you think it may warrent 6 points, please upgrade it :3 )

The design philosophy behind the CAD case for this is similar to my PaperCAM project: I wanted it to be sleek and minimal, in part not to draw attention. This, after all, contains my passwords! I do not want it to be flashy. That's why the case looks quite non-descrcipt. I wanted to add some custimizations, though, so I engraved my logo and a text that reads "PassPad v1". 

In line with keeping things simple (and affordable), I chose a very minimalistic BOM. Here it is below! It is also copied at the end of this README. 

NOTE: I know some items can be found cheaper through other retailars: the only problem is that my parents will only let me buy from the retailors below. If the cost goes above teh allocated cost for my project, I will hapilly pay out of my own pocket. I am grateful to have the opportunity to build this, and I cannot do so if I don't buy the parts from the retailors below.



|Item               |Quantity|Cost |Link                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|-------------------|--------|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|0.91 OLED Display  |1       |5.99 |https://www.amazon.com/gp/product/B08F9F8BYB/ref=ewc_pr_img_3?smid=A3CX4TQNUXMB0L&th=1                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|EC11 Rotary Encoder|1       |0 |n/a I should have spares from the Hackpad kit                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|MX-Style Switch    |1       |0 |n/a I should have spares from the Hackpad kit                               |
|White DSA Keycap   |1       |0 |n/a I should have spares from the Hackpad kit|
|1N4148 Diodes      |2       |0 |n/a I should have spares from the Hackpad kit                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|XIAO Microprocessor|1       |9.99 |https://www.amazon.com/gp/product/B09NNVNW7M/ref=ox_sc_act_title_1?smid=A1YP59NGBNBZUR&psc=1                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|Custom PCB         |1       |2  + shipping  |https://jlcpcb.com                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|2.5M x 4mm Screws  |8       |0    |n/a, self-provided                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|                   |        |~$38|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |


## Schematic and PCB Design

For this project, I kept pretty much exactly to my initial sketch. Here's some images!


### Schematic
<img width="500" alt="Schematic" src="https://github.com/user-attachments/assets/b0ecda9c-f120-4939-ac24-98550749557e" />


### PCB
<img width="825" alt="PCB" src="https://github.com/user-attachments/assets/e2679079-3262-4a04-a8f0-c0a9bd23986b" />


## Firmware

Custom firmware! It was super fun to make. If you want a detailed view into my mindset, check out my journal! The runtime script is also included in this repo under the firmware and production directories. 

The code for this project was signficantly longer than teh code for my other projects (being ~600ish lines). I think that's a record for me! I experienced a lot of growth as a dev in this project as I was really able to exercise skills in error handeling and encryption. It was really satisfying to know that the code I have is for a project that I will use rather than something for a test. 

## CAD

The CAD case, like I said above, is simple by design: it is meant to be non-descript so people don't want to steal my passwords (litteraly). Here's some pretty renders of how everything looked at the end. Also, like the PaperCAM, as there is no wiring outside the PCB, no pretty sketch :(. However, I did annotate some of teh images below!





![CAD_Case_Together_Front](https://github.com/user-attachments/assets/3ce90b22-2e43-4edc-9fc3-8d764a0f1538)
![CAD_Case_Together_Back](https://github.com/user-attachments/assets/6b5c2d84-0318-4890-8999-3d445e6dff87)
![CAD_Case_Seperated_Front](https://github.com/user-attachments/assets/ebca11eb-30dd-4e7a-9033-3800136454c2)


## BOM

NOTE: I know some items can be found cheaper through other retailars: the only problem is that my parents will only let me buy from the retailors below. If the cost goes above teh allocated cost for my project, I will hapilly pay out of my own pocket. I am grateful to have the opportunity to build this, and I cannot do so if I don't buy the parts from the retailors below.


|Item               |Quantity|Cost |Link                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|-------------------|--------|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|0.91 OLED Display  |1       |5.99 |https://www.amazon.com/gp/product/B08F9F8BYB/ref=ewc_pr_img_3?smid=A3CX4TQNUXMB0L&th=1                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|EC11 Rotary Encoder|1       |0 |n/a I should have spares from the Hackpad kit                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|MX-Style Switch    |1       |0 |n/a I should have spares from the Hackpad kit                               |
|White DSA Keycap   |1       |0 |n/a I should have spares from the Hackpad kit|
|1N4148 Diodes      |2       |0 |n/a I should have spares from the Hackpad kit                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|XIAO Microprocessor|1       |9.99 |https://www.amazon.com/gp/product/B09NNVNW7M/ref=ox_sc_act_title_1?smid=A1YP59NGBNBZUR&psc=1                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|Custom PCB         |1       |2  + shipping  |https://jlcpcb.com                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|2.5M x 4mm Screws  |8       |0    |n/a, self-provided                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|                   |        |~$38|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
