import simplegui
import math

# Global vars
tenth = int()
second = int()
minute = int()
attempt = 0
hit = 0

width = 400
height = 200
interval = 100

radius = 55
radius_p = 40
alpha = -90
px = int(100)
py = int(60)

stopped = 1
cheat = 0
att = 0

# Start messages
message = "00:00.0"
result = "0 hits from 0 attempts"
accuracy = "Accuracy rate: 0.00 %"

# "Zero" function before rendered time result
def add_zero(value):
    number = str(value)
    if value <= 9:
        number = "0" + str(value)
    return number

# Plural function for the result message
def plural(val, word):
    ress = str(val) + " " + word
    if val != 1 :
        ress = str(val) + " " + word + "s"
    return ress

# Clock function for the rendered clock arrow
def clock_function():
    global px, py, alpha
    alpha = (alpha + 0.6) % 360
    px = 100 + (radius_p * math.cos(alpha/180.0 * math.pi))
    py = 100 + (radius_p * math.sin(alpha/180.0 * math.pi))
    
# Accuracy rate function
def acc_rate():
    global accuracy
    if attempt == 0:
        accuracy = accuracy
    else:
        acc_number = 100 * (float(hit) / float(attempt))
        if acc_number == 100:
            accuracy = "Accuracy rate: " + (str(acc_number)[0:5]) + " %"
        elif 0 < acc_number < 100:
            accuracy = "Accuracy rate: " + (str(acc_number)[0:4]) + " %"
        else:
            accuracy = accuracy
        return accuracy

# Seconds and minutes increasing (cycled in 60)
# Applied "zero" function as a message result
def time():
    global second, minute, message
    if tenth == 0:
        second += 1
    second = second % 60
    if second == 0 and tenth == 0:
        minute += 1
    minute = minute % 60
    seconds = add_zero(second)
    minutes = add_zero(minute)
    message = minutes + ":" + seconds + "." + str(tenth)

# Timing function - the tenth (cycled in 10) increasing by the timer
# and influencing the seconds and minutes parameters
# Imported clock function for correct rotation of the clock arrow
def timing():
    global tenth
    tenth += 1
    tenth = tenth % 10
    clock_function()
    time()

# Start button handler
def start():
    global stopped, cheat, att
    cheat = 0
    att = 0
    stopped = 0
    timer.start()

# Stop button handler; displaying the results of the hit attempts and accuracy rate
# Disabled cheating and multi-failed attempts over one unit of digits
def stop():
    global attempt, hit, result, stopped, accuracy, cheat, att
    stopped = 1
    if tenth == 0 and cheat == 1:
        hit += 0
        attempt += 0
    elif tenth == 0 and cheat == 0 and second != 0:
        cheat = 1
        hit += 1
        attempt += 1
    elif tenth != 0 and att == 1:
        attempt += 0
    elif tenth != 0 and att == 0:
        att = 1
        attempt += 1
    hits = plural(hit, "hit")
    attempts = plural(attempt, "attempt")
    result = hits + " from " + attempts
    acc_rate()
    timer.stop()

# Restart button handler restarting the initial values of the global vars
def res():
    global tenth, second, minute, message, attempt, hit, result, alpha, px, py, stopped, accuracy, cheat, att
    stopped = 1
    alpha = -90
    px = int(100)
    py = int(60)
    tenth = int()
    second = int()
    minute = int()
    attempt = int()
    hit = int()
    message = "00:00.0"
    result = "0 hits from 0 attempts"
    accuracy = "Accuracy rate: 0.00 %"
    cheat = 0
    att = 0
    timer.stop()

# The draw handler, which draws the preferred variaty and amount of objects
def draw(canvas):
    canvas.draw_text(message, [185, ((height // 2) - 11)], 42, "Red")
    canvas.draw_text(result, [187, ((height // 2) + 12)], 18, "White")
    canvas.draw_text(accuracy, [187, ((height // 2) + 34)], 18, "#999999")
    canvas.draw_circle([100,100], radius, 2, "White")
    canvas.draw_line([100, 100], [px, py], 3, 'Red')
    canvas.draw_line([145, 100], [150, 100], 2, 'White')
    canvas.draw_line([100, 145], [100, 150], 2, 'White')
    canvas.draw_line([50, 100], [55, 100], 2, 'White')
    canvas.draw_line([100, 50], [100, 55], 2, 'White')
    if stopped == 1:
        canvas.draw_line([90, 35], [110, 35], 6, 'Red')
    else:
        canvas.draw_line([90, 35], [110, 35], 6, 'White')

# Frame and timer definitions
frame = simplegui.create_frame("Clock", width, height)
timer = simplegui.create_timer(interval, timing)

# Registering the different event handlers
frame.set_draw_handler(draw)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Restart", res, 100)

# Start frame
frame.start()