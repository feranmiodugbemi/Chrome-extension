from selenium import webdriver
import time
import re
import imaplib
import email

try:
    # Step 1: Connect to email account and search for email with specific subject
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('your_email@gmail.com', 'your_email_password')
    mail.select('inbox')
    typ, data = mail.search(None, 'SUBJECT "specific subject line"')
    mail_ids = data[0]
    id_list = mail_ids.split()

    # Step 2: Extract URL from email and open in new tab
    for i in id_list:
        typ, data = mail.fetch(i, '(RFC822)' )
        msg = email.message_from_bytes(data[0][1])
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg.get_payload())
        if urls:
            driver = webdriver.Chrome()
            driver.get(urls[0])
            time.sleep(5)  # wait for page to load

            # Step 3: Click on specific button in opened website
            button = driver.find_element_by_xpath('//button[@id="specific-button"]')
            button.click()

            # Close the tab and quit the driver
            driver.close()
            driver.quit()
except Exception as e:
    print('An error occurred:', e)
