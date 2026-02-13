
import threading
import http.server
import socketserver
import os
import time
from playwright.sync_api import sync_playwright

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

def verify_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # 1. Verify Index Page
        print("Navigating to Index...")
        page.goto(f"http://localhost:{PORT}/index.html")
        page.wait_for_selector(".navbar-brand")

        # Check for 'Nos Pôles' link
        poles_link = page.get_by_role("link", name="Nos Pôles")
        if poles_link.count() > 0:
             print("SUCCESS: 'Nos Pôles' link found on Index.")
        else:
             print("FAILURE: 'Nos Pôles' link NOT found on Index.")

        page.screenshot(path="verification_index.png")
        print("Screenshot saved: verification_index.png")

        # 2. Verify Poles Page
        print("Navigating to Poles page...")
        poles_link.first.click()
        page.wait_for_url(f"http://localhost:{PORT}/poles.html")
        page.wait_for_selector("h1.hero-title")

        if "Nos Pôles de Formation" in page.content():
            print("SUCCESS: Poles page loaded with correct title.")
        else:
             print("FAILURE: Poles page title incorrect.")

        page.screenshot(path="verification_poles.png")
        print("Screenshot saved: verification_poles.png")

        # 3. Verify a New Formation Page (Marketing)
        print("Navigating to Marketing Digital...")
        # Find the card or link for Marketing Digital. It might be under 'Gestion & Management'
        # based on my poles.html content, it's a card with text "Marketing Digital" inside an anchor
        marketing_card = page.locator("text=Marketing Digital")
        marketing_card.first.click()

        page.wait_for_url(f"http://localhost:{PORT}/formations/marketing.html")
        page.wait_for_selector("h1")

        title = page.locator("h1").inner_text()
        if "Marketing Digital" in title:
             print("SUCCESS: Marketing Digital page loaded.")
        else:
             print(f"FAILURE: Expected 'Marketing Digital', got '{title}'")

        page.screenshot(path="verification_marketing.png")
        print("Screenshot saved: verification_marketing.png")

        browser.close()

if __name__ == "__main__":
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Give server a moment to start
    time.sleep(2)

    try:
        verify_ui()
    except Exception as e:
        print(f"An error occurred: {e}")
