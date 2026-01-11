
from playwright.sync_api import sync_playwright
import time

GAME_URL = "https://www.linkedin.com/games/view/pinpoint/desktop/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page.goto(GAME_URL)
    
    # Start
    try:
        page.wait_for_selector("#launch-footer-start-button", timeout=10000).click()
        page.wait_for_selector(".pinpoint__card--clue", timeout=10000)
    except:
        print("Failed to start or find clues.")
        browser.close()
        exit(1)

    # Get clues
    clues = page.locator(".pinpoint__card--clue").all_inner_texts()
    print(f"CLUES: {clues}")
    
    browser.close()
