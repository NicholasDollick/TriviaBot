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
#this is a test

class POINT(Structure):
    _fields_ = [('x', c_long), ('y', c_long)]


def get_mouse_position():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return (pt.x, pt.y)


def start_browser():
    print("[*] Starting browser")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-accelerated-video-decode')
    browser = webdriver.Chrome('E:\Downloads\chromedriver_win32\chromedriver.exe', chrome_options = options)
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
        #print(hit.text)
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
print('              HQ Bot v1.3')
print('[*] Press "S" to enter setup')
print('[*] Press "I" to initialize search engine (takes the most time)')
print('[*] Press "G" to run')
print('[*] Press "C" to close')
print("WARNING: Search engine must have been initialized for the script to successfully run")

while(True):
    pos = get_mouse_position()
    ansFlag = False
    quesFlag = False
    keyPressed = msvcrt.getch().decode('utf-8').lower()

    if(keyPressed == 's'):
        print('[+] Entering Setup')
        print('[/] Place cursor in the top left corner of question.\n    Press "Q" to capture position of cursor.')
        print('[\] Place cursor in the top left corner of answers block.\n    Press "A" to capture position of cursor.')



        while(True):
            keyPressed = msvcrt.getch().decode('utf-8').lower()

            if(keyPressed == 'q'):
                quesPos = get_mouse_position()
                print(quesPos)
                quesFlag = True
                print('[+] Question Region Saved')

            if(keyPressed == 'a'):
                ansPos = get_mouse_position()
                print(ansPos)
                ansFlag = True
                print('[+] Answer Region Saved')

            if(ansFlag and quesFlag):
                break

        print('[+] Setup Complete')

    if(keyPressed == 'i'):
        search_engine = start_browser()
        print("[+] Browser Running")

    if(keyPressed == 'c'):
        close_browser(search_engine)
        sys.exit(0)

    if(keyPressed == 'g'):
        questionZone = PIL.ImageGrab.grab(bbox=(quesPos[0], quesPos[1], 1195, 410))
        questionZone.save('question.png')
        answerZone = PIL.ImageGrab.grab(bbox=(ansPos[0], ansPos[1], 1190, 680))
        answerZone.save('answers.png')
        print('[+] Reading Image')
        question = pytesseract.image_to_string(Image.open('question.png')).replace("\n", " ").replace("'", " ").encode('utf-8')
        answers = pytesseract.image_to_string(Image.open('answers.png')).split('\n')

        try:
            print('Question: ' + question.decode('utf-8'))
        except UnicodeEncodeError:
            print('Error Reading Image')

        a = answers[0]

        b = answers[2]

        c = answers[4]


        print('Correct answer is: ' + check_answers(search(search_engine, question.decode('utf-8')), a, b, c))

    continue
