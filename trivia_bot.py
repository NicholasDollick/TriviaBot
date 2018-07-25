import time
import pytesseract
import sys
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import PIL.ImageGrab
import msvcrt
from ctypes import windll, Structure, c_long, byref
import ascii


class POINT(Structure):
    _fields_ = [('x', c_long), ('y', c_long)]


def get_mouse_position():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return (pt.x, pt.y)


def save_position(initial, offset):
    with open('position.txt', mode = 'w') as file:
        file.write("x1 = " + str(initial[0]) + "\n" +
                   "y1 = " + str(initial[1]) + "\n" +
                   "x2 = " + str(offset[0]) + "\n" +
                   "y2 = " + str(offset[1]))


def start_browser():
    print("[*] Starting browser")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-accelerated-video-decode')
    browser = webdriver.Chrome('E:\Downloads\chromedriver_win32\chromedriver.exe', chrome_options=options)
    browser.get("https://www.google.com/")
    return browser


def close_browser(browser):
    browser.close()


def search(browser, search_term):
    search_box = browser.find_element_by_name('q')
    search_box.clear()
    search_box.send_keys(search_term)
    search_box.submit()
    hits = browser.find_elements_by_css_selector('.st')
    results = ""
    for hit in hits:
        results += hit.text
    return results


def check_answers(hits, a, b, c):
    count = 0
    maxCount = 0
    answer = 'A'

    maxCount = hits.count(a)
    count = hits.count(b)
    if(count > maxCount):
        maxCount = count
        answer = 'B'
    else:
        count = 0
    count = hits.count(c)
    if(count > maxCount):
        maxCount = count
        answer = 'C'
    else:
        count = 0
    return answer


ascii.splash()
print('              HQ Bot v2.0')
print('[*] Press "S" to enter setup')
print('[*] Press "I" to initialize search engine (takes the most time)')
print('[*] Press "G" to run')
print('[*] Press "C" to close')
print("WARNING: Search engine must have been initialized for the script to successfully run\n")

while(True):
    pos = get_mouse_position()
    ansFlag = False
    quesFlag = False
    keyPressed = msvcrt.getch().decode('utf-8').lower()

    if(keyPressed == 's'):
        print('[+] Entering Setup')
        print('[/] Place cursor in the top left corner of play area.\n    Press "Q" to capture position of cursor.')
        print('[\] Place cursor in the bottom right corner of play area.\n    Press "A" to capture position of cursor.')



        while(True):
            keyPressed = msvcrt.getch().decode('utf-8').lower()

            if(keyPressed == 'q'):
                initialPos = get_mouse_position()  # stores as (x,y). Sets position of origin
                #print(initialPos)
                quesFlag = True
                print('[+] Region Saved')

            if(keyPressed == 'a'):
                offsetPos = get_mouse_position()  # stores as (x,y). Records offset in position
                #print(offsetPos)
                ansFlag = True
                print('[+]  Region Saved')

            if(ansFlag and quesFlag):
                save_position(initialPos, offsetPos)
                break

        print('[+] Setup Complete')

    if(keyPressed == 'i'):
        search_engine = start_browser()
        print("[+] Browser Running")

    if(keyPressed == 'c'):
        close_browser(search_engine)
        sys.exit(0)

    if(keyPressed == 'g'):
        questionZone = PIL.ImageGrab.grab(bbox=(initialPos[0],  # bbox values: (x, y, x + x offset, y + y offset)
                                                initialPos[1],
                                                initialPos[0] + abs(initialPos[0] - offsetPos[0]),
                                                initialPos[1] + abs(initialPos[1] - offsetPos[1])))
        questionZone.save('question.png')
        print('[+] Reading Image')

        data = pytesseract.image_to_string(Image.open('question.png')).split('\n')  # raw input data
        answers = list(filter(None, data))[-3:]  # takes the last 3 lines, which contain the answers
        question = ""

        for i in range(0, (len(data) - len(answers) - 2)):  # assembles question by omitting answers from data string
            question += data[i] + " "

        question = question.encode('utf-8')  # might not need?

        try:
            print('Question: ' + question.decode('utf-8'))
        except UnicodeEncodeError:
            print('Error Reading Image')

        a = answers[0]

        b = answers[1]

        c = answers[2]

        print('Correct answer is: ' + check_answers(search(search_engine, question.decode('utf-8')), a, b, c))

    continue
