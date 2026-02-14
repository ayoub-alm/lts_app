from playwright.sync_api import sync_playwright
import time
import os

def run():
    print("Starting Playwright verification for Google Style UI...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Test Index
        print("Navigating to index.html...")
        page.goto("http://localhost:3000/index.html")
        page.wait_for_load_state("networkidle")

        title = page.title()
        print(f"Index Title: {title}")

        # Verify Google Fonts
        content = page.content()
        if "Google Sans" in content or "Roboto" in content:
            print("PASS: Google Fonts linked.")
        else:
            print("FAIL: Google Fonts missing.")

        # Verify New CSS Classes
        if page.locator(".formation-card").count() > 0:
            print("PASS: New .formation-card class found.")
        else:
            print("FAIL: .formation-card class not found.")

        if page.locator(".glass-panel").count() == 0:
            print("PASS: Old .glass-panel class removed from index (as expected).")
        else:
            print("WARNING: .glass-panel class found (might be intended for details pages).")

        page.screenshot(path="verification_google_index.png", full_page=True)
        print("Screenshot saved: verification_google_index.png")

        # Test Formation Page
        print("Navigating to marketing.html...")
        page.goto("http://localhost:3000/formations/marketing.html")
        page.wait_for_load_state("networkidle")

        if "Marketing Digital" in page.title():
            print("PASS: Formation page title correct.")

        # Verify Hero Section
        if page.locator(".hero-section").count() > 0:
             print("PASS: Hero section found.")

        page.screenshot(path="verification_google_marketing.png", full_page=True)
        print("Screenshot saved: verification_google_marketing.png")

        browser.close()

if __name__ == "__main__":
    run()
