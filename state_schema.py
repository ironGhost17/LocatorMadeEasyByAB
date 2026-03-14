def create_initial_state(url):

    return {
        "url": url,
        "dom": None,
        "screenshot_path": None,
        "interactive_elements": [],
        "analysis": [],
        "final_output": []
    }