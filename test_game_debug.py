
from playwright.sync_api import sync_playwright
import time

GAME_URL = "https://www.linkedin.com/games/view/pinpoint/desktop/"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
            "--no-sandbox"
        ]
    )
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        locale="en-US",
        timezone_id="Asia/Kolkata"
    )
    # Stealth
    context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    page = context.new_page()
    print(f"Navigating to {GAME_URL}...")
    try:
        page.goto(GAME_URL)
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception as e:
        print(f"Navigation error: {e}")

    time.sleep(5)
    print(f"Current URL: {page.url}")
    print(f"Page Title: {page.title()}")

    page.screenshot(path="debug_page.png", full_page=True)
    print("Saved debug_page.png")

    # Check for Start Button
    selector = "#launch-footer-start-button"
    if page.locator(selector).is_visible():
        print(f"Element '{selector}' is VISIBLE.")
        try:
            page.click(selector)
            print("Clicked Start Game button.")
            time.sleep(2)
            page.screenshot(path="debug_game_started.png")
            print("Saved debug_game_started.png")
        except Exception as e:
            print(f"Failed to click: {e}")
    else:
        print(f"Element '{selector}' is NOT visible.")
        
        # Check frames
        print("Checking frames...")
        for frame in page.frames:
            print(f"Frame name: {frame.name}, URL: {frame.url}")
            try:
                if frame.locator(selector).is_visible():
                    print(f"FOUND button in frame: {frame.name}")
            except:
                pass
        
        # Check if generic 'Start' or 'Play' text exists
        print("Checking for text 'Start game' or 'Play'...")
        if page.get_by_text("Start game").is_visible():
            print("Text 'Start game' found.")
        elif page.get_by_text("Play").is_visible():
            print("Text 'Play' found.")
        else:
            print("No 'Start game' or 'Play' text found visible.")

    browser.close()
