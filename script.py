from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup as bs
import time
import datetime
from datetime import date

#Options
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

#DRIVER_PATH
DRIVER_PATH = 'c:/Users/Admin/Desktop/Python/Practice/Web scraping/chromedriver.exe'

driver = webdriver.Chrome(options=options, executable_path = DRIVER_PATH)

#Login to ncov.moh.gov.vn
url = 'https://ncov.moh.gov.vn/'
driver.get(url)
print('Accessing url: https://ncov.moh.gov.vn/')
time.sleep(5)
msg = ''

def get_info(msg, country, xpath1, xpath2):
    msg+=country
    info = driver.find_elements_by_xpath(xpath2)
    info = info[0].get_attribute('innerHTML')
    info_soup = bs(info, 'html.parser')
    tags_div = info_soup('div')
    for tag in tags_div:
        text = tag.text
        msg = msg + text.strip() + '\n'
    msg += '==================\n'
    return msg
xpath1 = '//*[@id="portlet_corona_trangchu_top_CoronaTrangchuTopPortlet_INSTANCE_RrVAbIFIPL7v"]/div/div[2]/div/section[1]/div[2]/div[2]/div/div[3]/div/span[1]'
xpath2 = '//*[@id="portlet_corona_trangchu_top_CoronaTrangchuTopPortlet_INSTANCE_RrVAbIFIPL7v"]/div/div[2]/div/section[1]/div[2]/div[2]/div/div[3]/div/div[1]'
msg1 = get_info(msg,"Việt Nam\n", xpath1, xpath2)
xpath1 = '//*[@id="portlet_corona_trangchu_top_CoronaTrangchuTopPortlet_INSTANCE_RrVAbIFIPL7v"]/div/div[2]/div/section[1]/div[2]/div[2]/div/div[3]/div/span[2]'
xpath2 = '//*[@id="portlet_corona_trangchu_top_CoronaTrangchuTopPortlet_INSTANCE_RrVAbIFIPL7v"]/div/div[2]/div/section[1]/div[2]/div[2]/div/div[3]/div/div[2]'
msg2 = get_info(msg,'Thế giới\n', xpath1, xpath2)
text = msg1+msg2

#Get the news
url = 'https://ncov.moh.gov.vn/dong-thoi-gian'
driver.get(url)
print('Accessing:', url)

#get today's date
today = date.today()
today = today.strftime("%d/%m/%Y")
today = datetime.datetime.strptime(today, '%d/%m/%Y')

text += 'Timeline\n'

#get news within 3-days range
timeline = driver.find_elements_by_class_name('timeline-detail')
for item in timeline:
    time = item.find_element_by_class_name('timeline-head')
    formated_time = datetime.datetime.strptime(time.text.split()[1], '%d/%m/%Y')
    range = today - formated_time
    if range.days <=2:
        content = item.find_element_by_class_name('timeline-content')
        text = text + time.text + '\n' + content.text + '\n'
        text +='==================\n'

driver.close()

# set up the SMTP server
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login('cuong.bot.72@gmail.com', 'khca18111999')

sender = 'cuong.bot.72@gmail.com'
receiver = 'ttcuong18111999@gmail.com'

# Create message container
msg = MIMEMultipart()
msg['Subject'] = "New messages"
msg['From'] = sender
msg['To'] = receiver

# add in the message body
msg.attach(MIMEText(text, 'plain'))

# send the message via the server set up earlier.
s.send_message(msg)
s.quit()
print('Done')

