from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
import spacy
from nltk import word_tokenize

nlp = spacy.load('en_core_web_sm')

# chrome_driver = webdriver.Chrome()
locator = 'div.ytd-rich-grid-media ytd-thumbnail a.ytd-thumbnail'







class find_about():

    def remove_html(self,text):
        pattern = r'\<.*?\>'
        string = re.sub(pattern, '', text)
        return string.lower()

    def remove_txt(self,text):
        pattern1 = r'\[.*?\]'
        pattern2 = r'\([^()]*\)'
        string = re.sub(pattern1, '', text)
        string = re.sub(pattern2, '', string)
        return string.lower()

    def chrome_search(self, text):


        self.chrome_driver = webdriver.Chrome()
        self.chrome_driver.get('https://www.google.com/')
        element = self.chrome_driver.find_element(By.CLASS_NAME, "gLFyf")
        # print(element.get_attribute('innerHTML'))
        element.clear()
        element.send_keys(text)
        # element.send_keys(Keys.RETURN)

        search_q = "+".join(text.split(" "))

        self.chrome_driver.get('https://www.google.com/search?q={}'.format(search_q))

        text_box = self.chrome_driver.find_element(By.CLASS_NAME, 'LGOjhe').get_attribute('innerHTML')
        text_box = self.remove_html(text_box)
        text_box = self.remove_html(text_box)
        print(text_box)
        return text_box

    def youtube_song(self, text):


        self.chrome_driver = webdriver.Chrome()
        self.chrome_driver.get('https://www.youtube.com/')
        search_box = self.chrome_driver.find_element(By.NAME, "search_query")
        search_box.clear()
        search_box.send_keys(text)
        time.sleep(2.2)
        search_box.send_keys(Keys.ENTER)

        search_q = "+".join(text.split(" "))
        self.chrome_driver.get('https://www.youtube.com/results?search_query={}'.format(search_q))

        img_box = self.chrome_driver.find_element(By.ID, "video-title").get_attribute('href')
        self.chrome_driver.get(img_box)

        print(img_box)
        return img_box

    def youtube_search(self, text):


        self.chrome_driver = webdriver.Chrome()
        try:
            self.chrome_driver.get('https://www.youtube.com/')
            search_box = self.chrome_driver.find_element(By.NAME, "search_query")
            search_box.send_keys(text)
            time.sleep(2)
            search_box.send_keys(Keys.ENTER)

            search_q = "+".join(text.split(" "))
            self.chrome_driver.get('https://www.youtube.com/results?search_query={}'.format(search_q))

            text_box = self.chrome_driver.find_element(By.ID, "main-link").get_attribute('href')

            self.chrome_driver.get(text_box + '/about')
            para = self.chrome_driver.find_element(By.CLASS_NAME,"style-scope.ytd-channel-about-metadata-renderer").text

            pattern = re.compile(r"[a-zA-Z0-9. ]")
            check = "".join(pattern.findall(para))
            final = nlp(check)
            print(final)

            print(check)

            # about = chrome_driver.find_elements(By.ID, "description")

        except:
            print('found nothing')

    def search_wiki(self, text):


        self.chrome_driver = webdriver.Chrome()

        try:

            self.chrome_driver.get('https://en.wikipedia.org/wiki/')
            search_box = self.chrome_driver.find_element(By.NAME, "search")
            input_box = self.chrome_driver.find_element(By.NAME, "go")
            search_box.send_keys(text)
            input_box.click()

            search_q = "_".join(text.split(" "))
            search_q = search_q.title()

            self.chrome_driver.get('https://en.wikipedia.org/wiki/{}'.format(search_q))
            para = self.chrome_driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[5]/div[1]/p[2]').text
            if para == '':
                para = self.chrome_driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[5]/div[1]/p[3]').text

                check = self.remove_txt(para)
                print(check)
                return check
                # final = nlp(check)
                # print(final)

            else:

                check = self.remove_txt(para)
                print(check)
                return check



        except:
            print('Found Nothing')

    def search_weather(self, text):
        try:
            self.chrome_driver = webdriver.Chrome()
            self.chrome_driver.get('https://www.google.com/')

            lang = self.chrome_driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div/a").text

            if lang == "English":
                self.chrome_driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div/a").click()
                element = self.chrome_driver.find_element(By.CLASS_NAME, "gLFyf")
                print(element.get_attribute('innerHTML'))
                element.clear()
                element.send_keys(text)
                # element.send_keys(Keys.RETURN)

                search_q = "+".join(text.split(" "))

                self.chrome_driver.get('https://www.google.com/search?q={}'.format(search_q))

                text_box1 = self.chrome_driver.find_element(By.CLASS_NAME, 'UQt4rd').text
                text_box2 = str(self.chrome_driver.find_element(By.CLASS_NAME, 'VQF4g').text)

                text_box1 = str(nlp(text_box1))

                text_box2 = str(nlp(text_box2))
                if text_box1 != '' and text_box2 != '':
                    text_box1 = word_tokenize(text_box1)
                    text_box1 = " ".join(text_box1)

                    text_box1 = text_box1.replace('°F', '')
                    text_box1 = text_box1.replace('°', ' degree')
                    text_box1 = text_box1.replace('C', ' Celsius,')
                    text_box1 = text_box1.replace('km/h', 'kilometer per hour')
                    text_box1 = text_box1.replace(' %', '%,')
                    text_box1 = text_box1.replace(text_box1[0:8], 'And the temperature is, ' + text_box1[0:8])

                    text_box2 = word_tokenize(text_box2)
                    text_box2 = " ".join(text_box2)
                    text_box2 = text_box2.replace(text_box2[0:4],'Right now in '+text_box2[0:4])


                    # text_box = pd.concat(text_box2,text_box1)
                    print(text_box2)
                    print(text_box1)

                    return text_box2, text_box1
                else:
                    print('Found Nothing')
            else:

                element = self.chrome_driver.find_element(By.CLASS_NAME, "gLFyf")
                print(element.get_attribute('innerHTML'))
                element.clear()
                element.send_keys(text)
                # element.send_keys(Keys.RETURN)

                search_q = "+".join(text.split(" "))

                self.chrome_driver.get('https://www.google.com/search?q={}'.format(search_q))

                text_box1 = self.chrome_driver.find_element(By.CLASS_NAME, 'UQt4rd').text
                text_box2 = str(self.chrome_driver.find_element(By.CLASS_NAME, 'VQF4g').text)

                text_box1 = str(nlp(text_box1))
                text_box2 = str(nlp(text_box2.replace('°', 'degree')))

                if text_box1 != '' and text_box2 != '':
                    text_box1 = word_tokenize(text_box1)
                    text_box1 = " ".join(text_box1)

                    text_box1 = text_box1.replace('°F', '')
                    text_box1 = text_box1.replace('°', ' degree')
                    text_box1 = text_box1.replace('C', ' Celsius')
                    text_box1 = text_box1.replace('km/h', 'kilometer per hour')
                    text_box1 = text_box1.replace(' % ', '%,')
                    text_box1 = text_box1.replace(text_box1[0:8], 'And the temperature is ' + text_box1[0:8])

                    text_box2 = word_tokenize(text_box2)
                    text_box2 = " ".join(text_box2)
                    text_box2 = text_box2.replace(text_box2[0:4], 'Right now in ' + text_box2[0:4])

                    # text_box = pd.concat(text_box2,text_box1)
                    print(text_box2)
                    print(text_box1)
                    return text_box2, text_box1
                else:
                    print('Found Nothing')
                # text_box = pd.concat(text_box2,text_box1)
                return text_box1, text_box2
        except:
            print('search again')

    def close_window(self):

        self.chrome_driver.quit()



#item = find_about()
#item.search_weather('what is the weather')
# youtube_search('rakazone')
#item.chrome_search('what is google home mini')
#item.youtube_song('love me like you do')

# string = 'what is this'
# print(string.replace('this', 'that'))
