from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()
    page.goto("http://localhost:5000/login")

    page.click("#toggleConfirmation")

    page.click('button.swal2-confirm')

    # Basic Information
    page.fill("input[name=first_name]", "Ludwig")
    page.fill("input[name=last_name]", "Ahgren")

    page.fill("input[name=student_id]", "2012-000007")

    page.select_option("#collegeDropDown", "CEA")
    page.select_option("#courseDropDown", "Bachelor of Science in Electrical Engineering")

    page.select_option("#campusDropDown", "Boni")

    page.fill("input[name=year_level]", "3")
    page.fill("input[name=date_of_birth]", "2024-03-10")
    page.fill("input[name=age]", "21")
    page.fill("input[name=gender]", "Male")
    page.select_option("#civil", "Single")

    page.fill("input[name=nationality]", "American")
    page.fill("input[name=religion]", "Goblin")
    page.fill("input[name=residence]", "United States")
    page.fill("input[name=phone_number]", "123-123")
    page.fill("input[name=email_address]", "thor@pirate.com")
    page.fill("input[name=contact_number]", "09165137684")

    # Referral Source
    page.fill("input[name=referral_source]", "Twitch ig idk honestly")

    # Emergency Contact Information
    page.fill("input[name=emergency_name]", "Odin")
    page.fill("input[name=emergency_relationship]", "Father")
    page.fill("input[name=emergency_address]", "Asgard")
    page.fill("input[name=emergency_contact]", "091200000")

    # History Information
    page.click("#client")

    page.fill("input[name=current_problem]", "Annoying ass goblins D:")
    page.fill("input[name=problem_length]", "Since a few months ago.")
    page.fill("input[name=stressors]", "The goblins.")


    page.click("#substance_abuse")
    page.click("#addiction")

    # to be continued yung iba

    page.click("#prevtreatmentyes")

    # Previous Treatment

    

    page.wait_for_timeout(50000)

