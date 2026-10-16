# BuildPilot

**Turn a rough software idea into a clear first build plan.**

BuildPilot is a small Streamlit prototype for shaping a project idea into a realistic first version, starter tasks, risks, and an optional test checklist.

## What it does

- Collects a project idea and basic scope settings.
- Builds a plan using a deterministic local Python planner, even without internet access or API credentials.
- Optionally sends the idea to a separately configured Nebius-hosted model through an OpenAI-compatible API.
- Shows the plan and progress checklist in two side-by-side work areas.
- Keeps checklist progress in the current Streamlit session and includes completed items in the JSON export.
- Falls back to the local planner when hosted model configuration is missing or a request fails.

**Streamlit is the app framework and user interface; it is not the AI.** The local planner is fixed Python logic. Hosted AI is a separate model/API integration and may send the entered idea to the configured provider when enabled.

## Requirements

- Python 3.10 or newer
- Packages in `requirements.txt`
- Internet access to install packages, and separately to call a hosted model

## Run locally

### Windows (quick start)

1. Install Python 3.10 or newer if it is not already installed. During Python setup, enable **Add Python to PATH**.
2. Extract the ZIP to a folder you can find again, such as `Documents\\BuildPilot`.
3. Open that folder and double-click `run_windows.bat`.
4. The first run creates a private `.venv` folder and installs the app packages. This needs an internet connection. A browser tab should open with BuildPilot; keep the terminal window open while using the app.
5. To stop the app, close the terminal window or press `Ctrl+C` in it.

### macOS/Linux or manual setup

From this folder:

```bash
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit. The app works in local mode without any model account or key. On Windows, the equivalent manual command is `py -m streamlit run app.py` after activating the virtual environment.

## Optional hosted model setup

The prototype can call a Nebius model using its OpenAI-compatible API. Verify the current endpoint and model ID with your provider before use. Keep credentials private; never paste them into the idea field or commit them to version control.

One option is to set environment variables before starting the app:

```bash
# macOS/Linux
export NEBIUS_API_KEY="your-key"
export NEBIUS_BASE_URL="https://api.tokenfactory.nebius.com/v1/"
export NEBIUS_MODEL="meta-llama/Meta-Llama-3.1-8B-Instruct"

# Windows PowerShell
$env:NEBIUS_API_KEY="your-key"
$env:NEBIUS_BASE_URL="https://api.tokenfactory.nebius.com/v1/"
$env:NEBIUS_MODEL="meta-llama/Meta-Llama-3.1-8B-Instruct"
```

Alternatively, create a private `.streamlit/secrets.toml` file next to `app.py`:

```toml
NEBIUS_API_KEY = "your-key"
NEBIUS_BASE_URL = "https://api.tokenfactory.nebius.com/v1/"
NEBIUS_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"
```

Do not commit `secrets.toml`. The `.gitignore` excludes it. Turn on **Use a hosted AI model** in the app to attempt a request. If no key is available or the provider request fails, the app explains that it is showing the local plan instead.

## Deploy from GitHub

For a simple hosted demo, push this folder to a GitHub repository, then sign in to [Streamlit Community Cloud](https://share.streamlit.io/), choose **Create app**, and select the repository, branch, and `app.py` entrypoint. Keep `app.py` and `requirements.txt` at the repository root (or select the correct app path if you keep them in a subfolder). After deployment, pushes to the selected branch are reflected in the app automatically. If you use hosted model mode, add the API values in the app's Streamlit secrets settings; never commit a real key. See the [official deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

## Current limits and future work

- This is a prototype, not a production agent; local planning follows fixed rules and is not generative AI.
- Hosted model output depends on provider access, model availability, network access, and valid credentials. Live access was not verified as part of this package.
- Checklist progress lasts for the current Streamlit session. It is not stored in a database and may be lost when the session ends. Download the JSON to keep a copy.
- There is no authentication, multi-user storage, or account connection.
- Gmail, Google Calendar, and reminder delivery are **not implemented**. They are possible future integrations that would require explicit user opt-in, secure OAuth, and a clear permission/scope design.
- Hosted mode sends the submitted idea text to the configured model provider. Do not include sensitive information unless you are comfortable sharing it with that provider.

Possible next steps: validate plans with users, add durable project storage, add editable tasks and saved examples, verify a live hosted model configuration, then explore opt-in calendar/reminder integrations.

## Sharing and attribution

This ZIP provides an AI-assisted prototype. Before presenting it, be ready to explain which parts you built, which tools assisted, how the local planner and optional API path work, and what remains incomplete. Describe your own contribution accurately.
