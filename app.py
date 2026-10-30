import asyncio
from datetime import datetime
from html import escape

import streamlit as st

from agents.weather_agent import get_weather_report


st.set_page_config(
    page_title="Weather Buddy",
    page_icon="🌤️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp {
        min-height: 100vh;
        background: #ffffff;
    }

    .block-container {
        max-width: 760px;
        padding: 3rem 1rem;
    }

    .st-key-weather_card {
        max-width: 440px;
        margin: 0 auto;
        padding: 2rem 2.25rem;
        border-radius: 22px;
        background: linear-gradient(120deg, #39a978 0%, #2799ca 100%);
        box-shadow: 0 18px 45px rgba(27, 75, 91, 0.18);
    }

    .st-key-weather_card > div {
        background: #f3f8fa;
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
    }

    .weather-brand {
        margin: 0;
        color: #168a35;
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.04em;
    }

    .weather-subtitle {
        margin: 0.2rem 0 1.2rem;
        color: #25313a;
        font-size: 1.05rem;
        font-weight: 600;
    }

    .st-key-weather_card div[data-baseweb="input"] {
        border-radius: 7px;
    }

    .st-key-weather_card div[data-baseweb="input"] input {
        text-align: left;
    }

    .st-key-weather_card .stForm {
        border: 0;
        padding: 0;
    }

    .st-key-weather_card .stButton > button {
        min-height: 2.5rem;
        padding: 0.45rem 1.2rem;
        border: 0;
        border-radius: 5px;
        background: #168bd1;
        color: white;
        font-weight: 600;
    }

    .st-key-weather_card .stButton > button:hover {
        background: #0878bb;
        color: white;
    }

    .weather-city {
        margin: 1.1rem 0 0.15rem;
        color: #182129;
        font-size: 1.35rem;
        font-weight: 750;
        text-align: center;
    }

    .weather-date {
        margin-bottom: 0.8rem;
        color: #d9534f;
        font-size: 0.78rem;
        text-align: center;
    }

    .weather-icon {
        margin: 0.5rem 0;
        font-size: 2.7rem;
        line-height: 1.2;
        text-align: center;
    }

    .weather-report {
        margin-top: 0.8rem;
        color: #39434a;
        font-size: 0.9rem;
        line-height: 1.6;
        text-align: center;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    @media (max-width: 480px) {
        .block-container {
            padding: 1.5rem 0.75rem;
        }

        .st-key-weather_card {
            padding: 1rem;
        }

        .st-key-weather_card > div {
            padding: 1.25rem 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.container(key="weather_card"):
    st.markdown(
        """
        <h1 class="weather-brand">SkyMate</h1>
        <p class="weather-subtitle">Weather Buddy</p>
        """,
        unsafe_allow_html=True,
    )

    with st.form("weather_form"):
        city = st.text_input(
            "City",
            placeholder="Enter city name",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Get Weather", type="primary")

    if submitted:
        if not city.strip():
            st.warning("Please enter a city name.")
        else:
            with st.spinner("Getting weather information..."):
                try:
                    report = asyncio.run(get_weather_report(city.strip()))
                    report_lower = report.lower()

                    if "storm" in report_lower:
                        icon = "⛈️"
                    elif "rain" in report_lower:
                        icon = "🌧️"
                    elif "snow" in report_lower:
                        icon = "❄️"
                    elif "cloud" in report_lower:
                        icon = "☁️"
                    elif "wind" in report_lower:
                        icon = "🌬️"
                    else:
                        icon = "☀️"

                    st.markdown(
                        f'<h2 class="weather-city">{escape(city.strip())}</h2>'
                        f'<p class="weather-date">'
                        f'{datetime.now().strftime("%A, %d %B %Y, %I:%M %p")}'
                        "</p>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="weather-icon">{icon}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="weather-report">'
                        f'{escape(report).replace(chr(10), "<br>")}'
                        "</div>",
                        unsafe_allow_html=True,
                    )
                except Exception as error:
                    st.error(f"Unable to get weather information: {error}")
