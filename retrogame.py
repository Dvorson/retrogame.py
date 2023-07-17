import uinput
import gpiozero
import time

# Map of GPIO pin to keyboard key
button_map = {
    22: uinput.KEY_LEFT,
    20: uinput.KEY_RIGHT,
    7: uinput.KEY_UP,
    12: uinput.KEY_DOWN,
    19: uinput.KEY_LEFTCTRL,
    5: uinput.KEY_LEFTALT,
    6: uinput.KEY_Z,
    13: uinput.KEY_X,
    26: uinput.KEY_RIGHTSHIFT,
    16: uinput.KEY_ENTER,
    18: uinput.KEY_A,
    27: uinput.KEY_S,
    15: uinput.KEY_Q,
    17: uinput.KEY_W,
}

# Create a list of the device capabilities
device = uinput.Device(button_map.values())

# Create buttons for all the pins, with a debounce time of 0.1 seconds
buttons = {pin: gpiozero.Button(pin, debounce_time=0.1) for pin in button_map}

def make_press_handler(button):
    def handler():
        device.emit(button, 1)
    return handler

def make_release_handler(button):
    def handler():
        device.emit(button, 0)
    return handler

# Make each button press and release the corresponding keyboard button
for pin, button in button_map.items():
    buttons[pin].when_pressed = make_press_handler(button)
    buttons[pin].when_released = make_release_handler(button)

# ESC button logic
esc_sequence = [16, 26]  # Press ENTER then RIGHTSHIFT for ESC
esc_state = [False, False]

def make_esc_handler(index, button):
    def handler():
        esc_state[index] = True
        if all(esc_state):
            device.emit_click(uinput.KEY_ESC)
            # Reset the sequence
            for i in range(len(esc_state)):
                esc_state[i] = False
        else:
            device.emit(button, 1)  # emit the button's own event
    return handler

# Clean up old handlers
for pin in esc_sequence:
    buttons[pin].when_pressed = None

# Create new handlers
for i, pin in enumerate(esc_sequence):
    buttons[pin].when_pressed = make_esc_handler(i, button_map[pin])
    buttons[pin].when_released = make_release_handler(button_map[pin])

# Sleep forever to keep the script running
while True:
    time.sleep(1)

