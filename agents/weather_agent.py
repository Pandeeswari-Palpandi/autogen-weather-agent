from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from ddgs import DDGS
import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_environment() -> None:
    """Load environment variables from the project root without overriding the process environment."""
    for env_file in (PROJECT_ROOT / ".env", PROJECT_ROOT / "env"):
        if env_file.exists():
            load_dotenv(env_file)


load_environment()


def get_openai_api_key() -> str:
    """Return the configured API key or an empty string when it is missing."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        return ""

    placeholder_values = {
        "your api key",
        "your-api-key",
        "your key",
        "changeme",
    }

    normalized = api_key.lower()
    if normalized in placeholder_values or normalized.startswith("your "):
        return ""

    return api_key


def search_weather(city: str) -> str:
    """
    Search the web for the latest weather information
    and weather-related news for a given city.
    """

    query = f"{city} weather today latest"

    results = DDGS().text(
        query,
        max_results=5
    )

    if not results:
        return f"No weather information found for {city}."

    output = []

    for result in results:
        title = result.get("title", "")
        body = result.get("body", "")
        href = result.get("href", "")

        output.append(
            f"Title: {title}\n"
            f"Summary: {body}\n"
            f"URL: {href}"
        )

    return "\n\n".join(output)


def build_weather_agent(model_client: OpenAIChatCompletionClient):
    """Create a weather agent for the supplied model client."""
    return AssistantAgent(
        name="weather_news_agent",
        model_client=model_client,
        tools=[search_weather],
        system_message="""
            You are a weather news assistant.

            Your job is to provide the latest weather information
            for the city requested by the user.

            Use the search_weather tool whenever the user asks
            about weather.

            After getting the search results, summarize the
            useful information.

            Always respond in exactly 3 short lines:

            Line 1: Current weather summary.
            Line 2: Important weather condition or forecast.
            Line 3: One useful weather-related note.

            Do not mention the tool or the search process.
            """,
        reflect_on_tool_use=True,
    )


async def get_weather_report(city: str) -> str:
    """
    Get a weather report for a city using the AutoGen agent.
    """

    api_key = get_openai_api_key()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing or invalid. Add a valid key to a .env or env "
            "file in the project root before using the app."
        )

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=api_key,
    )
    try:
        weather_agent = build_weather_agent(model_client)
        result = await weather_agent.run(
            task=f"Give me the latest weather report for {city}."
        )

        return result.messages[-1].content
    finally:
        await model_client.close()
