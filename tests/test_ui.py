import os

import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_LOCAL_DRIVER = os.path.join(_REPO_ROOT, "drivers", "msedgedriver.exe")


@pytest.fixture
def driver():
    opts = EdgeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,720")

    service = EdgeService(
        executable_path=_LOCAL_DRIVER if os.path.isfile(_LOCAL_DRIVER) else None
    )
    drv = webdriver.Edge(service=service, options=opts)
    try:
        yield drv
    finally:
        drv.quit()


def test_page_loads_and_shows_heading(driver, base_url):
    driver.get(base_url + "/index.html")
    assert "Лабораторная 11" in driver.title
    heading = driver.find_element(By.TAG_NAME, "h1")
    assert "Форма обратной связи" in heading.text


def test_submit_button_is_visible(driver, base_url):
    driver.get(base_url + "/index.html")
    btn = driver.find_element(By.ID, "submit-btn")
    assert btn.is_displayed()
    assert "Отправить сообщение" in btn.text


def test_form_fields_accept_input(driver, base_url):
    driver.get(base_url + "/index.html")
    name = driver.find_element(By.ID, "name")
    email = driver.find_element(By.ID, "email")
    comment = driver.find_element(By.ID, "comment")

    name.send_keys("Тест Пользователь")
    email.send_keys("test@example.org")
    comment.send_keys("Проверка ввода")

    assert name.get_attribute("value") == "Тест Пользователь"
    assert email.get_attribute("value") == "test@example.org"
    assert comment.get_attribute("value") == "Проверка ввода"


def test_submit_shows_thank_you_message(driver, base_url):
    driver.get(base_url + "/index.html")
    driver.find_element(By.ID, "name").send_keys("Мария")
    driver.find_element(By.ID, "submit-btn").click()

    msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert "Спасибо" in msg.text
    assert "Мария" in msg.text
