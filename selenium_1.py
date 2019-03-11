'''
A basic selenium script to automateliking posts on your instagram feed
It will like all posts, there is no filter in place; you have been warned.
I created this script as part of my selenium learning process and will not
be held responsible for any misuse of this code.

Uncomment the lines marked "details" to view an experimental graphical
representaion of the script progress.
Author: V S Sreejeet
'''


import time
import sys
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


# Time format for output log
def t():
    return time.strftime('[%A %H:%M:%S] ')


# User setup
username = 'username'
password = 'password'


# driver setup
print(t() + 'Setting up driver...')
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'geckodriver')
# driver = webdriver.Firefox()
driver.implicitly_wait(5)
errs = 0
liked = 0
try:
    to_like = int(sys.argv[1])
except IndexError as e:
    to_like = 1000
try:
    step_liked = int(sys.argv[2])
except IndexError as e:
    step_liked = 50
try:
    max_errors = int(sys.argv[3])
except IndexError as e:
    max_errors = 10


# Logging in
print(t() + 'Logging in as %s...' % (username))
tries = 0
got = False
while(not got):
    tries += 1
    if tries > 5:
        print(t() + 'Unable to login after 5 tries!!\nExiting...')
        quit()
    time.sleep(2)
    try:
        driver.get('https://instagram.com/accounts/login')
        # time.sleep(4)
        driver.find_element_by_name('username').send_keys(username)
        driver.find_element_by_name('password').send_keys(password)
        driver.find_element_by_class_name("_0mzm-.sqdOP.L3NKy").click()
        got = True
    except selenium.common.exceptions.WebDriverException as e:
        print(str(e))
        time.sleep(3)
        driver.refresh()

time.sleep(2)
try:
    # driver.find_element_by_class_name('aOOlW.HoLwm').click()
    print(t() + 'Logged in successfully')
except Exception as e:
    print(e)
    print(t() + 'Something\'s wrong!')
    print('Waiting for manual log in.')
    input('Enter to continue...')
finally:
    time.sleep(2)

try:
    # Turn on notifications? No
    driver.find_element_by_class_name('aOOlW.HoLwm').click()
except selenium.common.exceptions.NoSuchElementException:
    # Sometimes this alert is missing
    pass


# Main like engine
print(t() + 'Going to like %d posts' % (to_like))
print(t() + 'Will notify at every %d likes' % (step_liked))

tmp = step_liked
delay = 1 # delay for each like in seconds
scrolled = 0
refreshed = 0
height = 0
btn = None

try:
    while(True):
        if liked >= to_like:
            print(t() + 'Target reached.')
            break

        if errs > max_errors:
            print(t() + 'Too many errors!')
            break

        if refreshed > 5:
            print(t() + 'Refreshed too many times. Feed exhausted!')
            break

        height = int(\
            driver.execute_script('return document.body.scrollHeight'))

        if height > 1100000 or scrolled >= 600:
            # Scrolled too far
            #details# print()
            print(t() + 'Scrolled %d times without anything to like.' % scrolled)
            print(t() + 'Refreshing page in 10 minutes at height %s...' % (height), end="")
            time.sleep(600)
            print('Done')
            driver.refresh()
            refreshed += 1
            height = 0
            scrolled = 0
            time.sleep(3)
            continue
        
        try:
            like_btn = driver.find_element_by_xpath('//section/span/button/span[@aria-label="Like"]')
            like_btn.click()
            liked += 1
            scrolled = 0 # Reset scrolled because new posts found
            # if liked >= step_liked:
            #     print(t() + 'Liked', liked)
            #     step_liked += tmp
            #details# print('X', end='')
            time.sleep(delay)
        except selenium.common.exceptions.NoSuchElementException:
            # No posts to like, scrolling ahead
            # driver.execute_script(\
            #     "window.scrollTo(0, document.body.scrollHeight);")
            driver.execute_script("window.scrollBy(0,4000);")
            #details# print('_', end='')
            scrolled += 1
            continue


        except selenium.common.exceptions.StaleElementReferenceException as e:
            print('Stale element', like_btn)
            print(e)
            pass


        except Exception as e:
            print(t() + 'Unexpected exception: ' + str(e))
            errs += 1
            continue


except KeyboardInterrupt:
    print('')
    print(t() + 'Ctrl-C was pressed...')

except Exception as e:
    print('')
    print(t() + 'Unexpected exception: ' + str(e))


print('')
print(t() + 'Driver stopped')
print('Target likes:'.ljust(13), to_like)
print('Actual likes:'.ljust(13), liked)
print('Errors:'.ljust(13), errs)

driver.quit() # Manually close browser if .quit() doesn't work
