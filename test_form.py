import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_successful_login(driver):
   driver.get("https://the-internet.herokuapp.com/login")

   username_input = driver.find_element(By.ID, "username")
   username_input.clear()
   username_input.send_keys("tomsmith")

   password_input = driver.find_element(By.ID, "password")
   password_input.clear()
   password_input.send_keys("SuperSecretPassword!")
   
   driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

   flash_message = driver.find_element(By.ID, "flash").text
   assert "You logged into a secure area!" in flash_message


def test_unsuccessful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    
    invalid_username = driver.find_element(By.ID, "username")
    invalid_username.clear()
    invalid_username.send_keys("invalid_username")
    
    invalid_password = driver.find_element(By.ID, "password")
    invalid_password.clear()
    invalid_password.send_keys("SuperSecretPassword!")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    flash_message = driver.find_element(By.ID, "flash").text
    assert "Your username is invalid!" in flash_message
    