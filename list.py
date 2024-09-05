#selenium imports
from selenium  import  webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium .webdriver.common.by import  By

#general imports
import time
import requests
import smtplib , ssl ,email
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np

#email imports
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pymupdf

from PIL import Image







def get_driver():
    service = Service("/home/priya/Learning/selenium/chromedriver")
    driver = webdriver.Chrome(service=service)
    driver.get('https://jharkhandhighcourt.nic.in/')
    return driver


def sending_gmail(filename):
    
    port = 465
    passsowrd=os.getenv("PASSWORD")
    print(passsowrd)
    smtp_server = "smtp.gmail.com"
    sender_email= "tstgmlwrld@gmail.com"
    receiver_email ="tsanjaykumar533@gmail.com"
    context = ssl.create_default_context()
    subject = "Dear Customer Here is Your listing accordingly please Check"
    body="Thank you for  Subscribing to Anshu Automation Services"

    message = MIMEMultipart()
    message["From"]= sender_email
    message["To"]= receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body,"plain"))

    with open (filename , "rb") as attachment:
       part = MIMEBase("application","octet-stream")
       part.set_payload(attachment.read())
    
    encoders.encode_base64(part)

    part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()

    with smtplib.SMTP_SSL(smtp_server,port,context=context) as server:
       server.login(sender_email,password=passsowrd)
       server.sendmail(sender_email,receiver_email,text)
       print("mail was send")
    






def downloading_content():
    #Loading Driver
    driver = get_driver()
    
    entire_cause_list=driver.find_element(By.XPATH,value='//*[@id="main_content"]/div/div[2]/div[5]/ul/li[2]/a')
    print(entire_cause_list.text)
    entire_cause_list.click()
    
    time.sleep(2)
    
    suppl_cause_list= driver.find_element(By.PARTIAL_LINK_TEXT,"DAILY CAUSELIST For Wednesday The 19th June 2024")
    print(driver.current_window_handle)
    print(suppl_cause_list.text)
    
    time.sleep(2)
    
    suppl_cause_list.click() 
    
    # Till this old window
    orignail_window = driver.current_window_handle
    all_windows=driver.window_handles

    for window in all_windows:
        if window !=orignail_window:
         new_window = window
         break

    driver.switch_to.window(new_window)

    
    time.sleep(2)
    iframe = driver.find_element(By.TAG_NAME,"iframe")
    result_url = iframe.get_attribute("src")
    file_name = result_url.split("/")[-1]
    print(file_name)

    #Downladong Pdf 
    respose = requests.get(result_url)
    if respose.status_code == 200:
       with open("{name}".format(name=file_name),'wb') as file:
        file.write(respose.content)

    time.sleep(2)
    return file_name;


def filter_content():

  with pymupdf.open("PDF.js viewer.pdf") as doc:
    for  page in doc:  # Assuming you want the first page
        text_locations = page.search_for(search_text, quads=True)

        for x0, y0, x1, y1 in text_locations:
         rect = pymupdf.Rect(x0, y0, x1, y1)
         extracted_text = get_text_from_rect(pdf_path, rect)
         print(f"Extracted text: {extracted_text}")

         # Modify output filename if needed
         crop_image(pdf_path, rect, output_filename=f"cropped_{search_text}.png")

def main():
    load_dotenv()
    #filename = downloading_content()
    # sending_gmail(filename)
    filter_content()
    

main()
