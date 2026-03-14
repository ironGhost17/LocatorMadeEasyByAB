from state_schema import create_initial_state

from agents.page_loader_agent import page_loader_agent
from agents.scroll_agent import scroll_agent
from agents.screenshot_agent import screenshot_agent
from agents.filter_agent import filter_agent
from agents.vision_locator_agent import vision_locator_agent
from agents.validation_agent import validation_agent
from agents.aggregator_agent import aggregator_agent


def run_pipeline(url):

    state = create_initial_state(url)

    pipeline = [
        page_loader_agent,
        scroll_agent,
        screenshot_agent,
        filter_agent,
        vision_locator_agent,
        validation_agent,
        aggregator_agent
    ]

    for agent in pipeline:
        try:
            state = agent(state)

        except Exception as e:
            print(f"\n❌ Pipeline failed at {agent.__name__}")
            print(f"Error: {e}")
            break

    return state


def main():

    url = input("Enter webpage URL: ").strip()

    if not url.startswith("http"):
        url = "https://" + url

    final_state = run_pipeline(url)

    print("\n✅ Pipeline completed")

    if "validated_output" in final_state:
        print("\nTop Locator Candidates:\n")

        for item in final_state["validated_output"][:5]:

            name = item.get("element_name")
            locator = item.get("css_locator")
            score = item.get("reliability_score")

            print(f"{name} → {locator} (score={score})")

    print("\n📁 Results saved to validated_locators.json\n")


if __name__ == "__main__":
    main()