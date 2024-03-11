import pytest
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        yield browser
        browser.close()

def test_login(browser):
    page = browser.new_page()
    page.goto("http://localhost:5000/login")
    page.fill("input[name=username]", "test")
    page.fill("input[name=password]", "test123")

    page.click("button[type=submit]")

    # Assert login success or failure
    assert page.title() == "Mindsight - Dashboard"

def test_add_record(browser):
    page = browser.new_page()
    page.goto("http://localhost:5000/login")

    page.click("#toggleConfirmation")

    page.inner_html('#toggleConfirmation')

    page.click('button.swal2-confirm')

    page.click("button#toggleConfirmation")

    assert page.title() == "Mindsight - Add Record"