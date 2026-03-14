from playwright.sync_api import sync_playwright
from utils.agent_decorator import agent


@agent("Auto Scroll Agent")
def scroll_agent(state):

    url = state["url"]

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url, wait_until="domcontentloaded")

        page.evaluate("""
        async () => {
            await new Promise(resolve => {
                let totalHeight = 0;
                let distance = 300;

                let timer = setInterval(() => {
                    window.scrollBy(0, distance);
                    totalHeight += distance;

                    if(totalHeight >= document.body.scrollHeight){
                        clearInterval(timer);
                        resolve();
                    }
                }, 200);
            });
        }
        """)

        state["scrolled"] = True

        browser.close()

    return state