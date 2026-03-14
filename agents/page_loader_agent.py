from playwright.sync_api import sync_playwright
from utils.agent_decorator import agent


@agent("Page Loader Agent")
def page_loader_agent(state):

    url = state["url"]

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url, wait_until="domcontentloaded")

        html = page.content()

        state["dom"] = html

        browser.close()
    with open("debug/dom.html","w",encoding="utf-8") as f:
        f.write(html)
    return state