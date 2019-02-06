'''
A basic selenium script to automate liking posts on your instagram feed
It will like all posts, there is no filter in place; you have been warned.
I created this script as part of my selenium learning process and will not
be held responsible for any misuse of this code.
Author: V S Sreejeet
'''


import time
import sys
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Time format for output log
def t():
    return time.strftime('[%A %H:%M:%S] ')

# User setup
username = 'username'
password = 'password'


# driver setup
print(t() + 'Setting up driver...')
driver = webdriver.Firefox()
driver.implicitly_wait(5)
errs = 0
liked = 0
try:
    to_like = int(sys.argv[1])
except IndexError as e:
    to_like = 20
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
delay = 5 # delay for each like in seconds
scrolled = 0
refreshed = 0
btn = None

try:
    while(liked < to_like):
        if errs > max_errors:
            # Stop if too many errors
            print(t() + 'Too many errors!!')
            break

        try:
            # Avoid that button on the top bar by only selecting span elements
            # with aria-label == 'like'
            like_list = driver.find_elements_by_class_name(\
                'glyphsSpriteHeart__outline__24__grey_9.u-__7')
            like_list = [x for x in like_list\
                if x.get_attribute('aria-label') == 'Like']

            if len(like_list) < 1:
                # No posts to like, scrolling ahead
                print('Scrolled down %d times without anything to like.' % scrolled)
                driver.execute_script(\
                    "window.scrollTo(0, document.body.scrollHeight);")
                scrolled += 1
                time.sleep(3)
                height = int(\
                    driver.execute_script('return document.body.scrollHeight'))
            
                if scrolled > 20 or height > 1000000:
                    # Scrolled far but still no posts to like, refresh page
                    if refreshed > 5:
                        print(t() + 'Nothing to like at the moment.')
                        break
                    print('Refreshing page at height', height)
                    driver.refresh()
                    refreshed += 1 
                    scrolled = 0
                    time.sleep(3)

            # Reset scrolled because new posts found
            scrolled = 0
            for btn in like_list:
                btn.click()
                liked += 1
                # Like notification
                if liked >= step_liked:
                    print(t() + 'liked', liked)
                    step_liked += tmp
                time.sleep(delay)

        except selenium.common.exceptions.StaleElementReferenceException as e:
            # print('Stale element', like_list.index(btn))
            # print(e)
            pass
        
        except Exception as e:
            print(t() + 'Unexpected exception')
            print(e)
            errs += 1
            continue

except KeyboardInterrupt:
    print(t() + 'Ctrl-C was pressed...')

except Exception as e:
    print(t() + str(e))


print(t() + '\nDriver stopped')
print('Target likes:'.ljust(14), to_like)
print('Actual likes:'.ljust(14), liked)
print('Refreshes:'.ljust(14), refreshed)
print('Errors:'.ljust(14), errs)

driver.quit() # Manually close browser if .quit() doesn't work
