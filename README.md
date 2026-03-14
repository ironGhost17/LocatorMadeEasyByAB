# LocatorMadeEasyByAB

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Playwright](https://img.shields.io/badge/Automation-Playwright-green)
![OpenAI](https://img.shields.io/badge/AI-OpenAI-orange)


AI-powered locator discovery system that analyzes webpages using DOM + vision reasoning to generate reliable automation locators.



# LocatorMadeEasyByAB

AI-powered locator discovery system that analyzes webpages using **DOM parsing + vision reasoning** to automatically generate, validate, and rank UI locators for automation testing.

This project demonstrates an **agentic architecture** combining browser automation, LLM reasoning, and locator validation.

---

# Overview

Modern automation testing relies heavily on stable UI locators.  
However, manually identifying reliable selectors can be time-consuming and brittle.

LocatorMadeEasyByAB solves this by:

1. Loading a webpage
2. Extracting interactive DOM elements
3. Analyzing the page using screenshot + DOM context
4. Generating stable automation locators
5. Validating those locators using Playwright
6. Ranking them based on reliability

The result is a structured dataset of **automation-ready locators**.

---

# Features

- AI-powered locator discovery
- DOM + vision reasoning
- Agentic pipeline architecture
- Playwright-based locator validation
- Locator stability scoring
- Locator reliability scoring
- Ranked locator output
- Structured JSON dataset for automation pipelines

---

# Architecture

The system follows an **agent pipeline architecture**.

```mermaid
flowchart TD

A[User URL] --> B[Page Loader Agent]
B --> C[Auto Scroll Agent]
C --> D[Screenshot Agent]
D --> E[DOM Filter Agent]
E --> F[Vision Locator Agent]
F --> G[Locator Validation Agent]
G --> H[Aggregator Agent]
H --> I[validated_locators.json]
