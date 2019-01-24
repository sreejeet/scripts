'''
A basic selenium script to automateliking posts on your instagram feed
This program was created as part of my selenium learning process. I will not be
held responsible for any misuse of this code.
'''

import time
import sys
import selenium
from selenium import webdriver


# User setup
username = 'username'
password = 'password'


# Bot setup
print('Setting up bot...')
bot         = webdriver.Firefox()
bot.implicitly_wait(5)
# bot.set_page_load_timeout(10)
errs        = 0
b_page_height = 0
a_page_height = 1
liked       = 0
try:
    to_like = int(sys.argv[1])
except IndexError as e:
    to_like = 20
try:
    step_liked = int(sys.argv[2])
except IndexError as e:
    step_liked = 5
try:
    max_retries = int(sys.argv[3])
except IndexError as e:
    max_retries = 10

def click_element(browser, element, tryNum=0):
    try:
        element.click()
    except Exception:
        if tryNum == 0:
            # try scrolling the element into view
            browser.execute_script(
                "document.getElementsByClassName('" + element.get_attribute(
                    "class") + "')[0].scrollIntoView({ inline: 'center' });")
        elif tryNum == 1:
            # well, that didn't work, try scrolling to the top and then
            # clicking again
            browser.execute_script("window.scrollTo(0,0);")
        elif tryNum == 2:
            # that didn't work either, try scrolling to the bottom and then
            # clicking again
            browser.execute_script(
                "window.scrollTo(0,document.body.scrollHeight);")
        else:
            # try `execute_script` as a last resort
            # print("attempting last ditch effort for click, `execute_script`")
            browser.execute_script(
                "document.getElementsByClassName('" + element.get_attribute(
                    "class") + "')[0].click()")
            # end condition for the recursive function
            return
        tryNum += 1
        # try again!
        click_element(browser, element, tryNum)

# Logging in
print('Logging in as %s...' % (username))
tries = 0
got = False
while(not got):
    tries += 1

    if tries > 5:
        print('Unable to login after 5 tries!!\nExiting...')
        quit()

    time.sleep(2)
    try:
        bot.get('https://instagram.com/accounts/login')
        # time.sleep(4)
        bot.find_element_by_name('username').send_keys(username)
        bot.find_element_by_name('password').send_keys(password)
        bot.find_element_by_class_name("_0mzm-.sqdOP.L3NKy").click()
        got = True
    except selenium.common.exceptions.WebDriverException as e:
        print(str(e))
        time.sleep(3)
        bot.refresh()

time.sleep(2)
try:
    bot.find_element_by_class_name('aOOlW.HoLwm').click()
    print('Logged in successfully')
except Exception as e:
    print(e)
    print('Something\'s wrong!')
    print('Waiting for manual log in.')
    input('Enter to continue...')
finally:
    time.sleep(1)

try:
    # Turn on notifications? No
    bot.find_element_by_class_name('aOOlW.HoLwm').click()
except selenium.common.exceptions.NoSuchElementException:
    # Sometimes this alert is missing, So nothing to do here
    pass

# like engine
print('Going to like %d posts...' % (to_like))
print('Will notify at every %d likes...' % (step_liked))

tmp = step_liked
a_page_height = int(bot.execute_script('return document.body.scrollHeight'))
try:
    while(liked < to_like):
        # Stop if too many errors
        if errs > max_retries:
            print('Too many errors!!')
            break

        like_list = bot.find_elements_by_class_name(\
            'glyphsSpriteHeart__outline__24__grey_9.u-__7')
        like_list = [x for x in like_list if x.get_attribute('aria-label')=='Like']

        # Nothing to like at this position, scroll ahead
        if len(like_list) < 1:
            # print('Nothing to like here, moving forward.')
            b_page_height = int(bot.execute_script('return document.body.scrollHeight'))
            bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            a_page_height = int(bot.execute_script('return document.body.scrollHeight'))

            if not b_page_height < a_page_height:
                # Average page max height = 1118000
                print(b_page_height, a_page_height)
                # Infinite scroll exhausted, refresh and wait
                print('Page exhausted. Refreshing...')
                bot.refresh()
                time.sleep(2)
            continue

        try:
            # for x in [x for x in like_list if x.get_attribute('aria-label')=='Like']:
            for like_btn in like_list:
                bot.execute_script( "document.getElementsByClassName('"\
                    + like_btn.get_attribute("class")\
                    + "')[0].scrollIntoView({ inline: 'center' });")
                click_element(bot, like_btn)
                liked += 1
                # Like notification
                if liked > step_liked:
                    print('liked', liked)
                    step_liked += tmp

                # errs -= 1
                time.sleep(3)

        except selenium.common.exceptions.StaleElementReferenceException as e:
            print('Stale elem', like_list.index(like_btn))
            print(e)
            pass
        except Exception as e:
            print('Unexpected excep')
            print(e)
            errs += 1
            continue

except KeyboardInterrupt as e:
    print(e)
    print('Ctrl-C was pressed...')

except Exception as e:
    print(e)

finally:
    print('\nBot stopped')
    print('to_like', to_like)
    print('liked', liked)
    print('errors', errs)
    # bot.quit()
    input('Press any key to contine...')
