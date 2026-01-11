
from playwright.sync_api import sync_playwright
import time
import random

GAME_URL = "https://www.linkedin.com/games/view/pinpoint/desktop/"

def human_type(page, selector, text):
    page.focus(selector)
    for char in text:
        page.keyboard.type(char)
        time.sleep(random.uniform(0.05, 0.1))

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=["--disable-blink-features=AutomationControlled", "--start-maximized", "--no-sandbox"]
    )
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="en-US",
        timezone_id="Asia/Kolkata"
    )
    page = context.new_page()
    
    # 1. Start Game
    print(f"Navigating...")
    page.goto(GAME_URL)
    
    start_selector = "#launch-footer-start-button"
    try:
        print("Waiting for start button...")
        page.wait_for_selector(start_selector, timeout=10000)
        page.click(start_selector)
        print("Clicked Start.")
    except Exception as e:
        print(f"Start failed: {e}")
        page.screenshot(path="fail_start.png")
        browser.close()
        exit(1)

    # 2. Verify Input
    input_selector = "input.pinpoint__input"
    try:
        print("Waiting for input...")
        # Wait for clue first to be sure game loaded
        page.wait_for_selector(".pinpoint__card--clue", timeout=10000)
        print("Clue visible.")
        
        page.wait_for_selector(input_selector, timeout=5000)
        print("Input field visible.")
        
        print("Typing 'TEST'...")
        page.click(input_selector)
        human_type(page, input_selector, "TEST")
        time.sleep(1)
        
        # Verify value
        val = page.locator(input_selector).input_value()
        print(f"Input value is: '{val}'")
        
        if val == "TEST":
            print("SUCCESS: Typed correctly.")
        else:
            print("FAILURE: Text not matched.")
            
        page.screenshot(path="success_type.png")
        
    except Exception as e:
        print(f"Input interaction failed: {e}")
        page.screenshot(path="fail_input.png")
        browser.close()
        exit(1)

    browser.close()
