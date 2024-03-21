from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
opts=webdriver.ChromeOptions()
opts.headless=True
# using selenium 4:
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import requests

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = "https://www.costco.com/"
driver.get(url)
search_box = driver.find_element(By.ID, "search-field")  # Adjust this ID based on your findings
search_box.send_keys("toilet paper")
search_box.submit()

product_name_elements = driver.find_elements(By.XPATH, "//input[starts-with(@id,'product_name_')]")
# Iterate through each product element
for index, element in enumerate(product_name_elements):
    try:
        product_name = element.get_attribute('value')
        print(product_name)
        link = driver.find_element(By.LINK_TEXT, product_name)
        link.click()
        ##### getting data  #######
        image_element = driver.find_element(By.CSS_SELECTOR, "img[id*='richfx_id_']")  # This selector is an example
        # Get the URL of the image
        image_url = image_element.get_attribute('src')
        try:
            response = requests.get(image_url, timeout=30, headers=headers)
            if response.status_code == 200:
                # Open a local file with wb (write binary) permission.
                with open(f"item{index}.jpg", "wb") as file:
                    # Write the content of the response to the file
                    file.write(response.content)
                print("Image downloaded successfully.")
        except:
            print("Failed to download image.")
        #######
        driver.back()
    except:
        print("not valid item, next!")


