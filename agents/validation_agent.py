from playwright.sync_api import sync_playwright
from utils.agent_decorator import agent


def stability_score(locator):
    """
    Estimate locator stability based on attribute type.
    Inspired by Playwright locator preference.
    """

    if not locator:
        return 0

    locator = locator.lower()

    if "#" in locator:
        return 1.0

    if "data-testid" in locator:
        return 0.95

    if "name=" in locator:
        return 0.9

    if "aria" in locator:
        return 0.85

    if "placeholder" in locator:
        return 0.85

    if "text" in locator:
        return 0.8

    return 0.6


def uniqueness_score(matches):
    """
    Score locator based on how unique it is.
    """

    if matches == 1:
        return 1.0

    if matches in [2, 3]:
        return 0.6

    if matches > 3:
        return 0.3

    return 0


@agent("Locator Validation Agent")
def validation_agent(state):

    locators = state.get("final_output", [])
    url = state["url"]

    validated = []

    # If LLM returned string accidentally
    if isinstance(locators, str):
        print("⚠️ LLM output was string, skipping validation")
        state["validated_output"] = []
        return state

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url, wait_until="domcontentloaded")

        for item in locators:

            # Skip malformed items
            if not isinstance(item, dict):
                continue

            css = item.get("css_locator")

            matches = 0
            exists = False

            if css:
                try:
                    matches = page.locator(css).count()
                    exists = matches > 0
                except:
                    matches = 0
                    exists = False

            stability = stability_score(css)
            uniqueness = uniqueness_score(matches)

            reliability = round(stability * uniqueness, 2)

            item["valid"] = exists
            item["matches"] = matches
            item["stability_score"] = stability
            item["reliability_score"] = reliability

            validated.append(item)

        browser.close()

    # Rank locators by reliability
    validated.sort(
        key=lambda x: x.get("reliability_score", 0),
        reverse=True
    )

    state["validated_output"] = validated

    return state