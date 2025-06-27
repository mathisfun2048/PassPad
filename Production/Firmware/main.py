import time
import board
import busio
import digitalio
import rotaryio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import supervisor
import gc

CONFIG = {
    "os_type": "windows",
    "typing_delay": 0.02,
    "auto_lock_timeout": 300,
    "screen_brightness": 1.0,
}

DEVICE_KEY = 0xA5

def obfuscate_password(password):
    return ''.join(chr(ord(c) ^ DEVICE_KEY) for c in password)

def deobfuscate_password(obfuscated):
    return ''.join(chr(ord(c) ^ DEVICE_KEY) for c in obfuscated)

PASSWORDS = [
    {"name": "Password_1", "password": obfuscate_password("1234!")},
    {"name": "Password_2", "password": obfuscate_password("password")},
    {"name": "Password_3", "password": obfuscate_password("very-secure")},
    {"name": "Password_4", "password": obfuscate_password("passwordpassword")},
    {"name": "Password_5", "password": obfuscate_password("drowssap")},
]

class PasswordManagerError(Exception):
    pass

class PasswordManager:
    def __init__(self):
        self.error_count = 0
        self.max_errors = 5
        self.error_state = False
        self.last_error = None
        self.config_mode = False
        self.locked = False
        self.last_activity = time.monotonic()

        try:
            self.initialize_system()
        except Exception as e:
            self.handle_critical_error(f"Initialization failed: {e}")
            raise

    def initialize_system(self):
        print("Initializing Password Manager...")

        self.initialize_display()

        self.setup_hardware()

        self.initialize_hid()

        self.initialize_state()

        self.update_display()
        print("Password Manager initialization complete")

    def initialize_display(self):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                displayio.release_displays()
                time.sleep(0.1)

                i2c = busio.I2C(board.P29, board.P6)
                display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
                self.display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

                self.splash = displayio.Group()
                self.display.show(self.splash)
                return

            except Exception as e:
                print(f"Display init attempt {attempt+1} failed: {e}")
                if attempt == max_retries - 1:
                    raise PasswordManagerError(f"Display initialization failed after {max_retries} attempts")
                time.sleep(0.5)

    def setup_hardware(self):
        try:
            self.switch = digitalio.DigitalInOut(board.P1)
            self.switch.direction = digitalio.Direction.INPUT
            self.switch.pull = digitalio.Pull.DOWN

            try:
                self.encoder = rotaryio.IncrementalEncoder(board.P26, board.P28)
                self.encoder_available = True
            except Exception as e:
                print(f"Encoder initialization failed: {e}")
                self.encoder = None
                self.encoder_available = False

            self.encoder_switch = digitalio.DigitalInOut(board.P27)
            self.encoder_switch.direction = digitalio.Direction.INPUT
            self.encoder_switch.pull = digitalio.Pull.DOWN

        except Exception as e:
            raise PasswordManagerError(f"Hardware setup failed: {e}")

    def initialize_hid(self):
        self.keyboard = None
        self.hid_available = False

        try:
            if not usb_hid.devices:
                print("Warning: No USB HID devices found")
                return

            self.keyboard = Keyboard(usb_hid.devices)
            self.hid_available = True

        except Exception as e:
            print(f"USB HID initialization failed: {e}")
            self.keyboard = None
            self.hid_available = False

    def initialize_state(self):
        self.current_password_index = 0
        self.current_char_index = 0
        self.password_transmitted = False
        self.last_encoder_position = self.encoder.position if self.encoder_available else 0

        self.config_option = 0
        self.config_options = ["OS Type", "Typing Delay", "Auto Lock"]

        self.last_switch_time = 0
        self.debounce_delay = 0.3

    def update_activity(self):
        self.last_activity = time.monotonic()

    def check_auto_lock(self):
        if CONFIG["auto_lock_timeout"] > 0 and not self.locked:
            if time.monotonic() - self.last_activity > CONFIG["auto_lock_timeout"]:
                self.locked = True
                self.safe_display_update(self.update_display)

    def unlock_device(self):
        self.locked = False
        self.update_activity()
        self.safe_display_update(self.update_display)

    def secure_clear_password(self, password_data):
        try:
            if isinstance(password_data, str):
                password_data = "0" * len(password_data)
            gc.collect()
        except:
            pass

    def handle_error(self, error_msg):
        self.error_count += 1
        self.last_error = error_msg
        print(f"Error {self.error_count}: {error_msg}")

        if self.error_count >= self.max_errors:
            self.error_state = True
            self.show_error_screen("Too many errors", "Device in safe mode")
            return False

        if "display" in error_msg.lower():
            self.recover_display()
        elif "hid" in error_msg.lower():
            self.recover_hid()
        elif "encoder" in error_msg.lower():
            self.recover_encoder()

        return True

    def handle_critical_error(self, error_msg):
        print(f"CRITICAL ERROR: {error_msg}")
        try:
            if self.display:
                self.show_error_screen("CRITICAL ERROR", "Restarting...")
                time.sleep(3)
        except:
            pass
        supervisor.reload()

    def recover_display(self):
        try:
            self.initialize_display()
            self.update_display()
            return True
        except Exception as e:
            print(f"Display recovery failed: {e}")
            return False

    def recover_hid(self):
        try:
            time.sleep(1)
            self.initialize_hid()
            return self.hid_available
        except Exception as e:
            print(f"HID recovery failed: {e}")
            return False

    def recover_encoder(self):
        try:
            self.encoder = rotaryio.IncrementalEncoder(board.P26, board.P28)
            self.encoder_available = True
            self.last_encoder_position = self.encoder.position
            return True
        except Exception as e:
            print(f"Encoder recovery failed: {e}")
            self.encoder_available = False
            return False

    def show_error_screen(self, title, message):
        try:
            if not self.display:
                return

            self.display.show(None)
            group = displayio.Group()

            text1 = label.Label(terminalio.FONT, text=title, color=0xFFFFFF, x=5, y=8)
            text2 = label.Label(terminalio.FONT, text=message, color=0xFFFFFF, x=5, y=18)
            text3 = label.Label(terminalio.FONT, text="Press encoder to retry", color=0xFFFFFF, x=2, y=28)

            group.append(text1)
            group.append(text2)
            group.append(text3)

            self.display.show(group)
        except Exception as e:
            print(f"Error displaying error screen: {e}")

    def safe_display_update(self, update_func):
        try:
            update_func()
        except Exception as e:
            if not self.handle_error(f"Display update failed: {e}"):
                return False
        return True

    def update_display(self):
        try:
            if self.display:
                self.display.show(None)

            gc.collect()
            self.splash = displayio.Group()

            if self.locked:
                text1 = label.Label(terminalio.FONT, text="DEVICE LOCKED", color=0xFFFFFF, x=15, y=8)
                text2 = label.Label(terminalio.FONT, text="Press encoder", color=0xFFFFFF, x=18, y=18)
                text3 = label.Label(terminalio.FONT, text="to unlock", color=0xFFFFFF, x=25, y=28)
                self.splash.append(text1)
                self.splash.append(text2)
                self.splash.append(text3)

            elif self.config_mode:
                self.display_config_screen()

            elif self.error_state:
                text1 = label.Label(terminalio.FONT, text="SAFE MODE", color=0xFFFFFF, x=25, y=8)
                text2 = label.Label(terminalio.FONT, text="Multiple errors", color=0xFFFFFF, x=8, y=18)
                text3 = label.Label(terminalio.FONT, text="Hold encoder: reset", color=0xFFFFFF, x=2, y=28)
                self.splash.append(text1)
                self.splash.append(text2)
                self.splash.append(text3)

            elif not self.hid_available:
                text1 = label.Label(terminalio.FONT, text="USB HID ERROR", color=0xFFFFFF, x=15, y=8)
                text2 = label.Label(terminalio.FONT, text="Check USB connection", color=0xFFFFFF, x=5, y=18)
                self.splash.append(text1)
                self.splash.append(text2)

            elif self.password_transmitted:
                text1 = label.Label(terminalio.FONT, text="SUCCESS!", color=0xFFFFFF, x=30, y=8)
                text2 = label.Label(terminalio.FONT, text="Password sent", color=0xFFFFFF, x=15, y=18)
                text3 = label.Label(terminalio.FONT, text="Press encoder: reset", color=0xFFFFFF, x=2, y=28)
                self.splash.append(text1)
                self.splash.append(text2)
                self.splash.append(text3)
            else:
                password_info = PASSWORDS[self.current_password_index]

                name = password_info["name"]
                if len(name) > 18:
                    name = name[:15] + "..."
                text1 = label.Label(terminalio.FONT, text=name, color=0xFFFFFF, x=5, y=8)

                actual_password = deobfuscate_password(password_info["password"])

                progress = f"{self.current_char_index}/{len(actual_password)}"
                os_status = f"OS: {CONFIG['os_type']}"
                text2 = label.Label(terminalio.FONT, text=f"{progress}  {os_status}", color=0xFFFFFF, x=5, y=18)

                text3 = label.Label(terminalio.FONT, text="Switch+Enc: config", color=0xFFFFFF, x=5, y=28)

                self.splash.append(text1)
                self.splash.append(text2)
                self.splash.append(text3)

                self.secure_clear_password(actual_password)

            if self.display:
                self.display.show(self.splash)

        except Exception as e:
            print(f"Display update error: {e}")
            self.handle_error(f"Display update failed: {e}")

    def display_config_screen(self):
        global value, value
        option_name = self.config_options[self.config_option]

        if self.config_option == 0:
            value = CONFIG["os_type"]
        elif self.config_option == 1:
            value = f"{CONFIG['typing_delay']:.3f}s"
        elif self.config_option == 2:
            value = f"{CONFIG['auto_lock_timeout']}s" if CONFIG['auto_lock_timeout'] > 0 else "OFF"

        text1 = label.Label(terminalio.FONT, text="CONFIG MODE", color=0xFFFFFF, x=20, y=8)
        text2 = label.Label(terminalio.FONT, text=f"{option_name}: {value}", color=0xFFFFFF, x=5, y=18)
        text3 = label.Label(terminalio.FONT, text="Rotate: change, Press: next", color=0xFFFFFF, x=2, y=28)

        self.splash.append(text1)
        self.splash.append(text2)
        self.splash.append(text3)

    def handle_encoder(self):
        if self.locked or self.error_state or not self.encoder_available:
            return

        try:
            current_position = self.encoder.position
            if current_position != self.last_encoder_position:
                difference = current_position - self.last_encoder_position
                self.update_activity()

                if self.config_mode:
                    self.handle_config_rotation(difference)
                else:
                    if difference > 0:
                        self.current_password_index = (self.current_password_index + 1) % len(PASSWORDS)
                    else:
                        self.current_password_index = (self.current_password_index - 1) % len(PASSWORDS)

                    self.reset_transmission()

                self.last_encoder_position = current_position
                self.safe_display_update(self.update_display)
                time.sleep(0.1)

        except Exception as e:
            print(f"Encoder handling error: {e}")
            if not self.handle_error(f"Encoder error: {e}"):
                self.encoder_available = False

    def handle_config_rotation(self, difference):
        if self.config_option == 0:
            os_types = ["windows", "macos", "linux"]
            current_index = os_types.index(CONFIG["os_type"])
            if difference > 0:
                current_index = (current_index + 1) % len(os_types)
            else:
                current_index = (current_index - 1) % len(os_types)
            CONFIG["os_type"] = os_types[current_index]

        elif self.config_option == 1:
            if difference > 0:
                CONFIG["typing_delay"] = min(0.2, CONFIG["typing_delay"] + 0.01)
            else:
                CONFIG["typing_delay"] = max(0.0, CONFIG["typing_delay"] - 0.01)

        elif self.config_option == 2:
            if difference > 0:
                if CONFIG["auto_lock_timeout"] == 0:
                    CONFIG["auto_lock_timeout"] = 60
                else:
                    CONFIG["auto_lock_timeout"] = min(1800, CONFIG["auto_lock_timeout"] + 60)
            else:
                if CONFIG["auto_lock_timeout"] <= 60:
                    CONFIG["auto_lock_timeout"] = 0
                else:
                    CONFIG["auto_lock_timeout"] = max(0, CONFIG["auto_lock_timeout"] - 60)

    def get_key_mapping(self):
        mapping = {
            '!': (Keycode.SHIFT, Keycode.ONE),
            '@': (Keycode.SHIFT, Keycode.TWO),
            '#': (Keycode.SHIFT, Keycode.THREE),
            '$': (Keycode.SHIFT, Keycode.FOUR),
            '%': (Keycode.SHIFT, Keycode.FIVE),
            '^': (Keycode.SHIFT, Keycode.SIX),
            '&': (Keycode.SHIFT, Keycode.SEVEN),
            '*': (Keycode.SHIFT, Keycode.EIGHT),
            '(': (Keycode.SHIFT, Keycode.NINE),
            ')': (Keycode.SHIFT, Keycode.ZERO),
            '_': (Keycode.SHIFT, Keycode.MINUS),
            '+': (Keycode.SHIFT, Keycode.EQUALS),
            ':': (Keycode.SHIFT, Keycode.SEMICOLON),
            '"': (Keycode.SHIFT, Keycode.QUOTE),
            '<': (Keycode.SHIFT, Keycode.COMMA),
            '>': (Keycode.SHIFT, Keycode.PERIOD),
            '?': (Keycode.SHIFT, Keycode.FORWARD_SLASH),
            '-': (Keycode.MINUS,),
            '=': (Keycode.EQUALS,),
            ';': (Keycode.SEMICOLON,),
            "'": (Keycode.QUOTE,),
            ',': (Keycode.COMMA,),
            '.': (Keycode.PERIOD,),
            '/': (Keycode.FORWARD_SLASH,),
            ' ': (Keycode.SPACE,),
        }

        if CONFIG["os_type"] == "macos":
            mapping['['] = (Keycode.LEFT_BRACKET,)
            mapping[']'] = (Keycode.RIGHT_BRACKET,)
            mapping['\\'] = (Keycode.BACKSLASH,)
            mapping['~'] = (Keycode.SHIFT, Keycode.GRAVE_ACCENT)
            mapping['`'] = (Keycode.GRAVE_ACCENT,)
        else:
            mapping['['] = (Keycode.LEFT_BRACKET,)
            mapping[']'] = (Keycode.RIGHT_BRACKET,)
            mapping['\\'] = (Keycode.BACKSLASH,)
            mapping['~'] = (Keycode.SHIFT, Keycode.GRAVE_ACCENT)
            mapping['`'] = (Keycode.GRAVE_ACCENT,)

        return mapping

    def send_next_character(self):
        if not self.hid_available or self.error_state or self.locked:
            return

        obfuscated_password = PASSWORDS[self.current_password_index]["password"]
        password = deobfuscate_password(obfuscated_password)

        if self.current_char_index >= len(password):
            self.secure_clear_password(password)
            return

        char = password[self.current_char_index]
        key_mapping = self.get_key_mapping()

        try:
            if char in key_mapping:
                self.keyboard.send(*key_mapping[char])
            elif char.isalpha():
                if char.isupper():
                    self.keyboard.send(Keycode.SHIFT, getattr(Keycode, char))
                else:
                    self.keyboard.send(getattr(Keycode, char.upper()))
            elif char.isdigit():
                digit_map = {
                    '0': Keycode.ZERO, '1': Keycode.ONE, '2': Keycode.TWO,
                    '3': Keycode.THREE, '4': Keycode.FOUR, '5': Keycode.FIVE,
                    '6': Keycode.SIX, '7': Keycode.SEVEN, '8': Keycode.EIGHT,
                    '9': Keycode.NINE
                }
                self.keyboard.send(digit_map[char])
            else:
                print(f"Unhandled character: {char}")

            self.current_char_index += 1

            if CONFIG["typing_delay"] > 0:
                time.sleep(CONFIG["typing_delay"])

            if self.current_char_index >= len(password):
                self.password_transmitted = True

            self.secure_clear_password(password)

        except Exception as e:
            self.secure_clear_password(password)
            self.handle_error(f"Failed to send character: {e}")

    def reset_transmission(self):
        self.current_char_index = 0
        self.password_transmitted = False

    def factory_reset(self):
        try:
            self.error_state = False
            self.error_count = 0
            self.last_error = None
            self.config_mode = False
            self.locked = False
            self.reset_transmission()
            self.update_activity()

            CONFIG["os_type"] = "windows"
            CONFIG["typing_delay"] = 0.02
            CONFIG["auto_lock_timeout"] = 300

            self.initialize_hid()
            if not self.encoder_available:
                self.recover_encoder()

            self.safe_display_update(self.update_display)

        except Exception as e:
            self.handle_critical_error("Factory reset failed")

    def run(self):
        print("Password Manager Started")
        print(f"Loaded {len(PASSWORDS)} passwords")
        print(f"HID Available: {self.hid_available}")
        print(f"Encoder Available: {self.encoder_available}")

        consecutive_errors = 0
        max_consecutive_errors = 10
        encoder_press_start = None
        long_press_duration = 1.5
        config_combo_start = None
        config_combo_duration = 2.0

        while True:
            try:
                self.check_auto_lock()

                self.handle_encoder()

                if self.switch.value and not self.password_transmitted and not self.config_mode and not self.locked:
                    current_time = time.monotonic()
                    if current_time - self.last_switch_time > self.debounce_delay:
                        self.send_next_character()
                        self.last_switch_time = current_time
                        self.safe_display_update(self.update_display)
                        self.update_activity()

                if self.encoder_switch.value:
                    if encoder_press_start is None:
                        encoder_press_start = time.monotonic()
                    else:
                        press_duration = time.monotonic() - encoder_press_start

                        if press_duration >= long_press_duration and not self.locked:
                            self.factory_reset()
                            encoder_press_start = None

                        elif self.switch.value and press_duration >= config_combo_duration and not self.locked:
                            self.config_mode = not self.config_mode
                            self.safe_display_update(self.update_display)
                            encoder_press_start = None
                else:
                    if encoder_press_start is not None:
                        press_duration = time.monotonic() - encoder_press_start

                        if press_duration < long_press_duration:
                            if self.locked:
                                self.unlock_device()
                            elif self.config_mode:
                                self.config_option = (self.config_option + 1) % len(self.config_options)
                                self.safe_display_update(self.update_display)
                            else:
                                self.reset_transmission()
                                self.safe_display_update(self.update_display)

                        encoder_press_start = None
                        self.update_activity()

                    config_combo_start = None

                consecutive_errors = 0
                time.sleep(0.01)

            except Exception as e:
                consecutive_errors += 1
                print(f"Runtime error {consecutive_errors}: {e}")

                if consecutive_errors >= max_consecutive_errors:
                    self.handle_critical_error(f"Too many consecutive errors")
                    break

                time.sleep(0.1)

if __name__ == "__main__":
    max_restart_attempts = 3
    restart_count = 0

    while restart_count < max_restart_attempts:
        try:
            print(f"Starting Password Manager (attempt {restart_count + 1})")
            password_manager = PasswordManager()
            password_manager.run()
            break

        except KeyboardInterrupt:
            print("Shutting down...")
            break

        except Exception as e:
            restart_count += 1
            print(f"Startup failed (attempt {restart_count}): {e}")

            if restart_count >= max_restart_attempts:
                print("Maximum restart attempts reached. Entering safe mode.")
                try:
                    displayio.release_displays()
                    i2c = busio.I2C(board.P29, board.P6)
                    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
                    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

                    group = displayio.Group()
                    text1 = label.Label(terminalio.FONT, text="SYSTEM FAILURE", color=0xFFFFFF, x=10, y=12)
                    text2 = label.Label(terminalio.FONT, text="Check hardware", color=0xFFFFFF, x=8, y=22)
                    group.append(text1)
                    group.append(text2)
                    display.show(group)

                    while True:
                        time.sleep(1)

                except:
                    print("Complete system failure. Hardware check required.")
                    while True:
                        time.sleep(1)
            else:
                print("Retrying in 2 seconds...")
                time.sleep(2)