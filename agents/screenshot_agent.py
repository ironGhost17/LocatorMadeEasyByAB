from playwright.sync_api import sync_playwright
from utils.agent_decorator import agent


@agent("Screenshot Agent")
def screenshot_agent(state):

    url = state["url"]

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url, wait_until="domcontentloaded")

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        path = "debug/page.png"

        page.screenshot(path=path, full_page=True)

        state["screenshot_path"] = path

        browser.close()

    return state