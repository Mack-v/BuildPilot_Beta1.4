"""BuildPilot: a small, session-based project planning prototype."""

import json
import os
import re
from typing import Any

import streamlit as st


st.set_page_config(
    page_title="BuildPilot | Your first build plan",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root { --ink:#172b3b; --muted:#637585; --teal:#087e82; --line:#dfe8e7; --wash:#f3f8f6; }
    .stApp { background: #fbfcfa; color: var(--ink); }
    /* Streamlit's fixed top toolbar sits above the app content. Leave enough
       clearance so the first brand row is never tucked under that toolbar. */
    .block-container { max-width: 1220px; padding-top: 5.25rem !important; padding-bottom: 4rem; }
    [data-testid="stSidebar"] { background: #f1f6f4; border-right: 1px solid var(--line); }
    .brand { display:flex; align-items:center; gap:.8rem; margin:0 0 1.1rem; }
    .brand-mark { width:42px; height:42px; border-radius:14px; display:grid; place-items:center;
        color:white; background:linear-gradient(145deg,#0b9291,#075c70); font-size:22px; box-shadow:0 5px 16px #087e8230; }
    .brand-name { font-size:1.05rem; font-weight:800; letter-spacing:-.02em; color:#183344; }
    .brand-tag { display:block; color:#70818d; font-size:.72rem; letter-spacing:.12em; text-transform:uppercase; font-weight:700; }
    .hero { padding:1.4rem 1.6rem 1.55rem; border:1px solid #dce8e5; border-radius:22px;
        background:radial-gradient(ellipse at 90% 0%,#d7eeea 0,transparent 40%),linear-gradient(120deg,#f3f9f7,#fff 66%); }
    .eyebrow { color:#087e82; text-transform:uppercase; letter-spacing:.12em; font-size:.75rem; font-weight:800; }
    .hero h1 { margin:.42rem 0 .38rem; font-size:clamp(2rem,4vw,3rem); line-height:1.08; letter-spacing:-.045em; color:#173245; }
    .hero p { max-width:670px; color:#536a78; font-size:1.07rem; margin:0; }
    .section-kicker { color:#087e82; font-size:.75rem; text-transform:uppercase; letter-spacing:.11em; font-weight:800; margin-bottom:.35rem; }
    .panel { border:1px solid var(--line); border-radius:18px; background:white; padding:1.1rem 1.2rem; min-height:100%; }
    .panel-note { color:var(--muted); font-size:.91rem; }
    .metric { border:1px solid var(--line); border-radius:14px; padding:.8rem 1rem; background:var(--wash); }
    div[data-testid="stTextArea"] textarea { border-radius:14px; line-height:1.55; }
    div.stButton > button[kind="primary"] { background:#087e82; border-color:#087e82; border-radius:12px; font-weight:700; min-height:3rem; }
    div.stButton > button[kind="primary"]:hover { background:#066b70; border-color:#066b70; }
    div[data-testid="stCheckbox"] { padding:.24rem 0; }
    @media (max-width: 700px) { .block-container{padding:4.5rem 1rem 3rem !important;} .hero{padding:1.1rem;} }
    </style>
    """,
    unsafe_allow_html=True,
)


def local_plan(idea: str, project_type: str, experience: str, timeline: str, include_tests: bool) -> dict[str, Any]:
    """Return a deterministic starter plan; this does not call an AI model."""
    cleaned = " ".join(idea.strip().split())
    title = cleaned.split(".")[0][:62].strip() or "Untitled project"
    if len(title) == 62 and len(cleaned) > 62:
        title = title.rsplit(" ", 1)[0] + "…"

    if project_type == "Game":
        mvp = ["A playable loop from start to win or lose", "One core mechanic", "A restart flow"]
    elif project_type == "Automation":
        mvp = ["One input format", "One useful transformation", "A clear output and error message"]
    elif project_type == "AI tool":
        mvp = ["A focused user input", "One model-assisted result", "A way to review or copy the result"]
    elif project_type == "Mobile app":
        mvp = ["One primary screen", "One complete user action", "A clear confirmation or result"]
    else:
        mvp = ["A simple input screen", "One complete core workflow", "A result with a useful next action"]

    if timeline == "A few hours":
        tasks = [
            ("Choose one user and one problem", "15 min"),
            ("Build only the core happy path", "90 min"),
            ("Try three realistic inputs", "30 min"),
            ("Write setup notes and capture a demo", "30 min"),
        ]
    elif timeline == "A weekend":
        tasks = [
            ("Set the scope and define what done means", "45 min"),
            ("Implement one end-to-end happy path", "3–4 h"),
            ("Add input checks and useful error states", "1–2 h"),
            ("Try five inputs and fix the biggest issues", "1–2 h"),
            ("Document setup and capture a demo", "1 h"),
        ]
    elif timeline == "One week":
        tasks = [
            ("Define the user, problem, and success criteria", "1–2 h"),
            ("Sketch the main screens and data flow", "2 h"),
            ("Build a runnable first version", "Half day"),
            ("Implement the core workflow", "1–2 days"),
            ("Add validation and handle failure cases", "Half day"),
            ("Test, revise, and document the prototype", "1 day"),
        ]
    else:
        tasks = [
            ("Define the user, problem, and success criteria", "1–2 h"),
            ("Sketch the main screens and data flow", "Half day"),
            ("Build a runnable first version", "1 day"),
            ("Implement and refine the core workflow", "3–5 days"),
            ("Add validation and handle failure cases", "1–2 days"),
            ("Test with users, revise, and document", "2–3 days"),
        ]

    plan: dict[str, Any] = {
        "title": title,
        "summary": f"A first {project_type.lower()} prototype based on your idea: {cleaned}",
        "goals": [
            "Describe the problem and name the person who has it.",
            "Choose the smallest useful outcome someone can complete.",
            "Finish one end-to-end happy path before adding extras.",
        ],
        "mvp": mvp,
        "tasks": [{"step": i, "task": task, "estimate": estimate} for i, (task, estimate) in enumerate(tasks, 1)],
        "risks": [
            "Scope creep: defer features that do not support the main workflow.",
            "Unclear value: ask a new person what they think the prototype helps them do.",
            "Unverified output: label assumptions and check important results.",
        ],
        "experience_note": f"Starter scope calibrated for {experience.lower()} experience and {timeline.lower()} available time.",
    }
    if include_tests:
        plan["tests"] = [
            "Empty input is handled without crashing.",
            "A typical input produces a useful, readable result.",
            "A long or unusual input does not break the workflow.",
            "A new user can follow the setup instructions.",
        ]
    return plan


def try_llm_plan(idea: str, project_type: str, experience: str, timeline: str, include_tests: bool):
    """Call the optional OpenAI-compatible hosted model, if configured."""
    def setting(name: str, default: str) -> str:
        try:
            return st.secrets.get(name, os.getenv(name, default))
        except Exception:
            # Streamlit raises when no secrets file is present; environment-only setup is valid.
            return os.getenv(name, default)

    api_key = setting("NEBIUS_API_KEY", "")
    if not api_key:
        return None, "No hosted model key is configured. BuildPilot used its built-in local planner."
    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url=setting("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/"),
            timeout=30.0,
            max_retries=1,
        )
        model = setting("NEBIUS_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct")
        prompt = f"""Create a realistic first-build plan. Return valid JSON only, no markdown, using keys: title, summary, goals (3 strings), mvp (3 strings), tasks (objects with step/task/estimate), risks (3 strings){', tests (4 strings)' if include_tests else ''}.
Keep the plan achievable and do not invent requirements. Mention uncertainty rather than assuming details.
Idea: {idea}
Project type: {project_type}
Developer experience: {experience}
Available time: {timeline}"""
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Return concise valid JSON only. No markdown fences."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1400,
        )
        content = response.choices[0].message.content or "{}"
        data = json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.IGNORECASE))
        if not isinstance(data, dict) or not isinstance(data.get("tasks"), list) or not data["tasks"]:
            raise ValueError("The model response did not contain a usable task list")
        data.setdefault("goals", [])
        data.setdefault("mvp", [])
        data.setdefault("risks", [])
        if not include_tests:
            data.pop("tests", None)
        return data, f"Generated with the configured hosted model: {model}. Review the suggestions before relying on them."
    except Exception as exc:
        return None, f"Hosted model was unavailable or returned an unusable plan ({type(exc).__name__}). Showing the local plan instead."


def render_brand() -> None:
    st.markdown(
        '<div class="brand"><div class="brand-mark">⌁</div><div><span class="brand-name">BuildPilot</span>'
        '<span class="brand-tag">From idea to first build</span></div></div>',
        unsafe_allow_html=True,
    )


render_brand()
st.markdown(
    '<section class="hero"><div class="eyebrow">A calmer way to get started</div>'
    '<h1>Turn a rough software idea into a clear first build plan.</h1>'
    '<p>Shape the smallest useful version, see what to do first, and keep track of your progress as you build.</p></section>',
    unsafe_allow_html=True,
)

with st.sidebar:
    render_brand()
    st.markdown("### Project settings")
    project_type = st.selectbox("What are you making?", ["Web app", "AI tool", "Game", "Automation", "Mobile app", "Other"])
    experience = st.selectbox("Your current experience", ["Beginner", "Intermediate", "Advanced"])
    timeline = st.selectbox("Time available", ["A few hours", "A weekend", "One week", "A month"])
    include_tests = st.checkbox("Include a test checklist", value=True)
    st.divider()
    st.caption("Your plans and checklist are kept in this browser session. They are not saved to an account or database.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-kicker">Start with the idea</div>', unsafe_allow_html=True)
st.markdown("### What do you want to build?")
st.caption("A few rough sentences are enough. Include who it is for, what they need, and what a first version should let them do.")
idea = st.text_area(
    "Idea description",
    value=st.session_state.get("idea_text", ""),
    height=190,
    placeholder="For example: A simple web app for student clubs to plan events. Organizers can create an event, share a signup link, and see who is coming. The first version should work well on a phone.",
    label_visibility="collapsed",
    key="idea_text",
)

ai_col, local_col = st.columns([1, 1], vertical_alignment="center")
with ai_col:
    use_ai = st.toggle(
        "Use a hosted AI model",
        value=False,
        help="Optional: sends the idea text to the configured Nebius model API. BuildPilot's built-in local planner works without any account or API key.",
    )
with local_col:
    st.markdown('<div class="panel-note">ⓘ Streamlit is the app framework and user interface. It is not the AI. Hosted AI is a separate model/API connection; the local planner is a simple built-in fallback.</div>', unsafe_allow_html=True)

with st.expander("ⓘ How to configure hosted model access", expanded=False):
    st.markdown(
        "The hosted option uses a compatible Nebius API endpoint and is completely optional. **Do not paste a key into the idea box or commit it to the project.** Set these values in your shell before starting Streamlit, or add them to a local `.streamlit/secrets.toml` file that stays private:"
    )
    st.code(
        'NEBIUS_API_KEY = "your-key"\nNEBIUS_BASE_URL = "https://api.tokenfactory.nebius.com/v1/"\nNEBIUS_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"',
        language="toml",
    )
    st.caption("The model ID and endpoint may change; verify them with your provider. The optional OpenAI Python package must be installed. With no key, or if the request fails, BuildPilot uses its local planner.")

if st.button("Create my first build plan", type="primary", use_container_width=True):
    if len(idea.strip()) < 12:
        st.error("Add a little more detail so the plan has something useful to work from.")
    else:
        plan = None
        note = ""
        if use_ai:
            with st.spinner("Putting your plan together…"):
                plan, note = try_llm_plan(idea, project_type, experience, timeline, include_tests)
        if plan is None:
            plan = local_plan(idea, project_type, experience, timeline, include_tests)
            note = note or "Generated by BuildPilot's built-in local planner. No AI service was called."
        st.session_state["plan"] = plan
        st.session_state["plan_note"] = note
        st.session_state["plan_id"] = st.session_state.get("plan_id", 0) + 1
        st.session_state["completed_tasks"] = set()
        st.session_state["completed_tests"] = set()

if "plan" in st.session_state:
    plan = st.session_state["plan"]
    plan_id = st.session_state.get("plan_id", 1)
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="section-kicker">Your project workspace</div>', unsafe_allow_html=True)
    st.title(plan.get("title", "Your first build plan"))
    st.write(plan.get("summary", ""))
    st.caption(st.session_state.get("plan_note", ""))

    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown('<div class="section-kicker">01 · Plan & guidance</div>', unsafe_allow_html=True)
        st.markdown("### Keep the first version small")
        st.caption(plan.get("experience_note", "Start with the essentials and check assumptions as you go."))
        st.markdown("**The first version needs**")
        for item in plan.get("mvp", []):
            st.markdown(f"- {item}")
        st.markdown("**A good place to start**")
        for item in plan.get("goals", []):
            st.markdown(f"- {item}")
        st.markdown("**Things to watch**")
        for risk in plan.get("risks", []):
            st.markdown(f"- {risk}")

    with right:
        st.markdown('<div class="section-kicker">02 · Progress checklist</div>', unsafe_allow_html=True)
        tasks = plan.get("tasks", [])
        done = st.session_state.get("completed_tasks", set())
        st.markdown("### What have you done?")
        st.progress(len(done) / len(tasks) if tasks else 0.0, text=f"{len(done)} of {len(tasks)} build steps complete")
        for index, task in enumerate(tasks):
            task_key = f"task_{plan_id}_{index}"
            checked = st.checkbox(
                f"{task.get('step', index + 1)}. {task.get('task', 'Build step')}  ·  {task.get('estimate', 'time varies')}",
                value=index in done,
                key=task_key,
            )
            if checked:
                done.add(index)
            else:
                done.discard(index)
        st.session_state["completed_tasks"] = done

        if plan.get("tests"):
            st.markdown("**Check before you share**")
            test_done = st.session_state.get("completed_tests", set())
            for index, test in enumerate(plan["tests"]):
                checked = st.checkbox(test, value=index in test_done, key=f"test_{plan_id}_{index}")
                if checked:
                    test_done.add(index)
                else:
                    test_done.discard(index)
            st.session_state["completed_tests"] = test_done

    plan_export = dict(plan)
    plan_export["progress"] = {
        "completed_task_indexes": sorted(st.session_state.get("completed_tasks", set())),
        "completed_test_indexes": sorted(st.session_state.get("completed_tests", set())),
    }
    st.download_button(
        "Download plan and progress as JSON",
        data=json.dumps(plan_export, indent=2, ensure_ascii=False),
        file_name="buildpilot_plan.json",
        mime="application/json",
    )
    st.caption("Progress stays available during this app session. Download the JSON to keep a copy after the session ends.")

with st.expander("About BuildPilot and what works in this prototype"):
    st.write(
        "Streamlit provides the app framework and interface. It does not provide the AI model. The built-in planner is deterministic local Python logic; the optional hosted mode is a separate API integration and may send your idea text to the configured provider. Plans and checklist state live only in the current Streamlit session. There is no login, database, Gmail access, Google Calendar access, reminder delivery, or multi-user persistence. Those are future product ideas and are not connected in this demo."
    )
