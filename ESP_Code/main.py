from machine import Pin, I2C
import ssd1306
import network
import time
import urequests

ip = "192.168.214.167"
table = 5

# OLED setup
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Adjust pins if needed
display = ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

# WiFi credentials
ssid = 'ssid'
password = 'password'

# Buttons
BTN1 = Pin(26, Pin.IN, Pin.PULL_UP)
BTN2 = Pin(25, Pin.IN, Pin.PULL_UP)
BTN3 = Pin(33, Pin.IN, Pin.PULL_UP)
BTN4 = Pin(32, Pin.IN, Pin.PULL_UP)

# Menu
menuItems = ["Burger", "Pizza", "Pasta", "Soda"]
menuSize = len(menuItems)
btn2Pressed = False
btn2PressStartTime = 0
btn2Handled = False


# States
HOME_SCREEN = -1
MENU_SCREEN = 0
QUANTITY_SCREEN = 1

currentScreen = HOME_SCREEN
selectedIndex = 0
quantity = 1

btn2PressStart = 0
btn2LongPressSent = False
btn2Pressed = False
btn2PressStartTime = 0
btn2Handled = False


# Cart now as Dictionary
cart = {}

def connectWiFi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    display.fill(0)
    display.text('Connecting WiFi...', 0, 0)
    display.show()
    
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("Connected!")
    return wlan

def showHomeScreen():
    global currentScreen
    currentScreen = HOME_SCREEN
    display.fill(0)
    display.text('BISTRO 92', 20, 25)  # Centered
    display.show()

def showMainMenu():
    global currentScreen
    currentScreen = MENU_SCREEN
    display.fill(0)
    display.text('Select Item:', 0, 0)
    for i in range(menuSize):
        if i == selectedIndex:
            display.text('> ' + menuItems[i], 0, 10 + i * 10)
        else:
            display.text('  ' + menuItems[i], 0, 10 + i * 10)
    display.show()

def showQuantityScreen():
    global currentScreen
    currentScreen = QUANTITY_SCREEN
    display.fill(0)
    display.text('Set Quantity:', 0, 0)
    display.text(str(quantity), 50, 30)
    display.show()

def resetCart():
    global cart, selectedIndex, quantity
    cart = {}
    selectedIndex = 0
    quantity = 1
    showHomeScreen()
    print("Cart cleared.")

def addToCart(item, qty):
    global cart
    if item in cart:
        cart[item] += qty
    else:
        cart[item] = qty
    print("Cart updated:", cart)

def sendOrderToCloud():
    global cart
    
    print("Sending order...")
    try:
        url = f"http://{ip}:8000/order"  # Replace with your server URL
        headers = {"Content-Type": "application/json"}
        # Prepare JSON
        json_data = {
            "table": table,
            "order": cart
        }
        print(json_data)
        response = urequests.post(url, json=json_data, headers=headers)
        print("Order sent:", response.status_code)
        response.close()
    except Exception as e:
        print("Error:", e)

    display.fill(0)
    display.text('Order Sent!', 0, 0)
    display.show()
    time.sleep(2)
    resetCart()

def handleMenuNavigation():
    global selectedIndex, quantity
    if not BTN3.value():  # DOWN / +
        selectedIndex = (selectedIndex + 1) % menuSize
        showMainMenu()
        time.sleep(0.2)
    if not BTN4.value():  # UP / -
        selectedIndex = (selectedIndex - 1 + menuSize) % menuSize
        showMainMenu()
        time.sleep(0.2)
    if not BTN2.value():  # SELECT
        quantity = 1
        showQuantityScreen()
        time.sleep(0.2)

def handleQuantitySelection():
    global quantity
    if not BTN3.value():  # +
        quantity += 1
        showQuantityScreen()
        time.sleep(0.2)
    if not BTN4.value():  # -
        if quantity > 1:
            quantity -= 1
        showQuantityScreen()
        time.sleep(0.2)
    if not BTN2.value():  # Confirm
        addToCart(menuItems[selectedIndex], quantity)
        showMainMenu()
        time.sleep(0.2)

def handleHomeScreen():
    if not BTN2.value():
        showMainMenu()
        time.sleep(0.2)

def updateBtn2State():
    global btn2Pressed, btn2PressStartTime, btn2Handled

    if not BTN2.value():  # Button is held down
        if not btn2Pressed:
            btn2Pressed = True
            btn2PressStartTime = time.ticks_ms()
            btn2Handled = False
        else:
            # Still held down
            if not btn2Handled:
                if time.ticks_diff(time.ticks_ms(), btn2PressStartTime) > 1200:
                    sendOrderToCloud()
                    btn2Handled = True
    else:
        if btn2Pressed:
            if not btn2Handled:
                pressDuration = time.ticks_diff(time.ticks_ms(), btn2PressStartTime)
                if pressDuration < 1200:
                    handleBtn2ShortPress()
            btn2Pressed = False
            btn2Handled = False


def handleBtn2ShortPress():
    global currentScreen, quantity

    if currentScreen == HOME_SCREEN:
        showMainMenu()
    elif currentScreen == MENU_SCREEN:
        quantity = 1
        showQuantityScreen()
    elif currentScreen == QUANTITY_SCREEN:
        addToCart(menuItems[selectedIndex], quantity)
        showMainMenu()



# Main setup
wlan = connectWiFi()
showHomeScreen()

# Main loop
while True:
    if not BTN1.value():  # Reset
        resetCart()
        time.sleep(0.2)

    if currentScreen == MENU_SCREEN:
        if not BTN3.value():  # Down
            selectedIndex = (selectedIndex + 1) % menuSize
            showMainMenu()
            time.sleep(0.2)
        if not BTN4.value():  # Up
            selectedIndex = (selectedIndex - 1 + menuSize) % menuSize
            showMainMenu()
            time.sleep(0.2)

    elif currentScreen == QUANTITY_SCREEN:
        if not BTN3.value():  # Increase quantity
            quantity += 1
            showQuantityScreen()
            time.sleep(0.2)
        if not BTN4.value():  # Decrease quantity
            if quantity > 1:
                quantity -= 1
            showQuantityScreen()
            time.sleep(0.2)

    updateBtn2State()  # Always check BTN2 last
    time.sleep(0.01)

