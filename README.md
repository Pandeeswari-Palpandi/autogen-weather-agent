# Weather Agent

A Streamlit weather app that uses an AutoGen AI agent to look up and summarize
current weather information for a city.

## Setup

1. Add your OpenAI API key to a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   The app also accepts a file named `env`. If both files exist, values in
   `.env` take precedence over values in `env`. Variables already set in the
   process environment take precedence over both files.

2. Install the dependencies:
   ```bash
   pip install -r requirements.txy
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

Enter a city and select **Get Weather** to view the generated weather summary.
