from bs4 import BeautifulSoup
from utils.agent_decorator import agent


@agent("DOM Filter Agent")
def filter_agent(state):

    html = state["dom"]

    soup = BeautifulSoup(html, "html.parser")

    elements = soup.find_all([
        "button",
        "input",
        "textarea",
        "select",
        "a",
        "label"
    ])

    snippets = []

    for el in elements:
        snippets.append(str(el)[:500])

    state["interactive_elements"] = snippets

    return state