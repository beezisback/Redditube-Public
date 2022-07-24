from cleantext import clean
from cv2 import imread
from os import chdir
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def getComments(driver, minCommentLength, maxCommentLength, amountOfComments, picturePath):
    
    #Required variables
    commentTexts = []
    counter = 1
    verified = 0
    number = 5

    #Check parameters surrounding the post
    try:
        text = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, '_2jpm-rNr0Hniw6BX3NWMVe'))).text
        if type(text) == list:
            text = ' '.join(text)
        if 'contest mode' in text:
            return False
    except TimeoutException:
        pass

    #Get all the comments
    while(verified < amountOfComments):
        try:
            comment = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="overlayScrollContainer"]/div[2]/div[1]/div[2]/div['+str(number)+']/div/div/div/div['+str(counter)+']')))
            commentLevel = (comment.text).split('\n')
        except StaleElementReferenceException: #If page isn't fully loaded this error pops up
            continue
        except TimeoutException:
            try:
                comment.click()
                counter = counter + 1
                continue
            except UnboundLocalError:
                try:
                    number = 6
                    comment = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="overlayScrollContainer"]/div[2]/div[1]/div[2]/div['+str(number)+']/div/div/div/div['+str(counter)+']')))
                    commentLevel = (comment.text).split('\n')
                except TimeoutException:
                    print("No more parent comments. Returning "+str(len(commentTexts))+" comments")
                    return commentTexts

        if (commentLevel[0]) == 'level 1':
            driver.execute_script('arguments[0].scrollIntoView({block: "center"});', comment)
            try:
                commentText = comment.find_element(By.CLASS_NAME, '_3cjCphgls6DH-irkVaA0GM').text
            except NoSuchElementException:
                counter = counter + 1
                continue
            if (len(commentText) > minCommentLength) and (len(commentText) < maxCommentLength):
                if 'Stickied comment' not in comment.find_element(By.CLASS_NAME, '_1a_HxF03jCyxnx706hQmJR').text:
                    chdir(picturePath)
                    comment.screenshot('comment'+str(verified+1)+'.png')
                    commentSize = imread('comment'+str(verified+1)+'.png')
                    commentSize = commentSize.shape
                    if (commentSize[0] > 900) or (commentSize[1] > 1740):
                        counter = counter + 1
                        continue
                    else:
                        if verified == (amountOfComments-1):
                            print("Parent comments found: "+str(verified+1)+" (last comment)")
                        else:
                            print("Parent comments found: "+str(verified+1))
                        commentText = clean(commentText, no_emoji=True)
                        commentTexts.append(commentText)
                        verified = verified + 1
                else:
                    pass
            else:
                pass
        else:
            pass    
        counter = counter + 1
    
    print("\nVideo rendering will begin soon. Please standby.\n")
    return commentTexts