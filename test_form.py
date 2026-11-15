
import pytest
import allure
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


@allure.title("Успешная авторизация пользователя")
@allure.description(
    "Проверка успешного входа на сайт с корректными учетными данными. "
    "После авторизации должно появиться сообщение об успешном входе."
)
def test_successful_login(driver):

    with allure.step("Открыть страницу авторизации"):
        driver.get("https://the-internet.herokuapp.com/login")

    with allure.step("Ввести корректный логин"):
        username_input = driver.find_element(By.ID, "username")
        username_input.clear()
        username_input.send_keys("tomsmith")

    with allure.step("Ввести корректный пароль"):
        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys("SuperSecretPassword!")

    with allure.step("Нажать кнопку входа"):
        driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        ).click()

    with allure.step("Проверить сообщение об успешной авторизации"):
        flash_message = driver.find_element(By.ID, "flash").text
        assert "You logged into a secure area!" in flash_message

        
@allure.title("Авторизация с неправильным логином")
@allure.description(
    "Проверка реакции сайта на ввод неправильного логина "
    "при корректном пароле. Должно появиться сообщение об ошибке."
)
def test_unsuccessful_login(driver):

    with allure.step("Открыть страницу авторизации"):
        driver.get("https://the-internet.herokuapp.com/login")

    with allure.step("Ввести неправильный логин"):
        invalid_username = driver.find_element(By.ID, "username")
        invalid_username.clear()
        invalid_username.send_keys("invalid_username")

    with allure.step("Ввести корректный пароль"):
        invalid_password = driver.find_element(By.ID, "password")
        invalid_password.clear()
        invalid_password.send_keys("SuperSecretPassword!")

    with allure.step("Нажать кнопку входа"):
        driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        ).click()

    with allure.step("Проверить сообщение об ошибке авторизации"):
        flash_message = driver.find_element(By.ID, "flash").text
        assert "Your username is invalid!" in flash_message
