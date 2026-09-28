import os
import time

import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")

HINDSIGHT_API_URL = os.getenv(
    "HINDSIGHT_API_URL",
    "https://api.hindsight.vectorize.io"
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BANK_ID = "memorymate-demo"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MemoryMate",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "meetings" not in st.session_state:
    st.session_state.meetings = []

if "briefing" not in st.session_state:
    st.session_state.briefing = None


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* HERO */

    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #171b2e 0%,
            #241b3d 100%
        );
        border: 1px solid #40376b;
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #aeb3c7;
        margin-top: 5px;
    }


    /* STATISTICS */

    .stat-card {
        padding: 18px;
        border-radius: 14px;
        background: #171923;
        border: 1px solid #303343;
        text-align: center;
        min-height: 110px;
    }

    .stat-number {
        font-size: 30px;
        font-weight: 800;
    }

    .stat-label {
        color: #a5a7b5;
        font-size: 14px;
        margin-top: 5px;
    }


    /* SECTION */

    .section-title {
        font-size: 25px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 15px;
    }


    /* INSIGHT */

    .insight-card {
        padding: 18px;
        border-radius: 14px;
        background: #151d2b;
        border: 1px solid #29415e;
        min-height: 150px;
    }


    /* SUCCESS */

    .success-card {
        padding: 18px;
        border-radius: 14px;
        background: #14251e;
        border: 1px solid #276749;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CHECK HINDSIGHT API KEY
# ============================================================

if not HINDSIGHT_API_KEY:

    st.error(
        "HINDSIGHT_API_KEY is missing. "
        "Please check your .env file."
    )

    st.stop()


# ============================================================
# HINDSIGHT CLIENT
# ============================================================

@st.cache_resource
def get_hindsight_client():

    return Hindsight(
        base_url=HINDSIGHT_API_URL,
        api_key=HINDSIGHT_API_KEY
    )


client = get_hindsight_client()


# ============================================================
# GROQ CLIENT
# ============================================================

@st.cache_resource
def get_groq_client():

    if not GROQ_API_KEY:
        return None

    return Groq(
        api_key=GROQ_API_KEY
    )


groq_client = get_groq_client()


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero">'
    '<div class="hero-title">🧠 MemoryMate</div>'
    '<div class="hero-subtitle">'
    'AI Meeting Intelligence Agent • Remembers • Learns • Prepares'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("👤 Contact")

    contact_name = st.text_input(
        "Contact name",
        value="Sarah"
    )

    company_name = st.text_input(
        "Company",
        value="Acme Corporation"
    )

    st.divider()

    st.header("🧠 Memory System")

    st.success("Hindsight Connected")

    st.caption(
        "MemoryMate uses Hindsight as its "
        "long-term memory layer."
    )

    st.divider()

    st.header("🎯 Demo Flow")

    st.markdown(
        """
        **1.** Add Meeting 1  
        ↓  
        **2.** Add Meeting 2  
        ↓  
        **3.** Add Meeting 3  
        ↓  
        **4.** Prepare Meeting  
        ↓  
        **5.** See cumulative memory
        """
    )


# ============================================================
# MEMORY OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">📊 Memory Overview</div>',
    unsafe_allow_html=True
)

stat1, stat2, stat3, stat4 = st.columns(4)

meeting_count = len(
    st.session_state.meetings
)


# ------------------------------------------------------------
# MEETINGS
# ------------------------------------------------------------

with stat1:

    st.markdown(
        f'<div class="stat-card">'
        f'<div class="stat-number">{meeting_count}</div>'
        f'<div class="stat-label">Meetings Remembered</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# LONG TERM MEMORY
# ------------------------------------------------------------

with stat2:

    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-number">∞</div>'
        '<div class="stat-label">Long-Term Memory</div>'
        '</div>',
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# HINDSIGHT
# ------------------------------------------------------------

with stat3:

    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-number">🧠</div>'
        '<div class="stat-label">Hindsight Powered</div>'
        '</div>',
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# AI
# ------------------------------------------------------------

with stat4:

    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-number">AI</div>'
        '<div class="stat-label">Cumulative Intelligence</div>'
        '</div>',
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# ADD MEETING + MEMORY TIMELINE
# ============================================================

left, right = st.columns([1, 1])


# ============================================================
# ADD MEETING
# ============================================================

with left:

    st.markdown(
        '<div class="section-title">📝 Add Meeting</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Give MemoryMate your meeting notes. "
        "It will remember important details "
        "for future meetings."
    )

    meeting_notes = st.text_area(
        "Meeting notes",
        height=240,
        placeholder="""Example:

Sarah needs the analytics dashboard before October 15.

She prefers email communication.

She is concerned about implementation time.

We promised to send a revised proposal.""",
        key="meeting_input"
    )


    # --------------------------------------------------------
    # REMEMBER BUTTON
    # --------------------------------------------------------

    if st.button(
        "🧠 Remember This Meeting",
        type="primary",
        use_container_width=True
    ):

        if not meeting_notes.strip():

            st.warning(
                "Please enter meeting notes first."
            )

        else:

            try:

                # ------------------------------------------------
                # CREATE MEMORY
                # ------------------------------------------------

                memory_content = f"""
Meeting with {contact_name}
from {company_name}.

{meeting_notes}
"""


                # ------------------------------------------------
                # STORE MEMORY IN HINDSIGHT
                # ------------------------------------------------

                client.retain(
                    bank_id=BANK_ID,
                    content=memory_content,
                    context=f"Meeting with {contact_name}"
                )


                # ------------------------------------------------
                # STORE FOR UI TIMELINE
                # ------------------------------------------------

                st.session_state.meetings.append(
                    {
                        "contact": contact_name,
                        "company": company_name,
                        "notes": meeting_notes
                    }
                )


                # ------------------------------------------------
                # CLEAR PREVIOUS BRIEFING
                # ------------------------------------------------

                st.session_state.briefing = None


                # ------------------------------------------------
                # REFRESH UI
                # ------------------------------------------------

                st.success(
                    "🧠 Meeting remembered successfully!"
                )

                time.sleep(0.5)

                st.rerun()


            except Exception as e:

                st.error(
                    f"Could not save meeting: {e}"
                )


# ============================================================
# MEMORY TIMELINE
# ============================================================

with right:

    st.markdown(
        '<div class="section-title">🧠 Memory Timeline</div>',
        unsafe_allow_html=True
    )


    if not st.session_state.meetings:

        st.info(
            "No meetings remembered yet. "
            "Add your first meeting to start "
            "building memory."
        )


    else:

        # Newest meeting first
        for index, meeting in enumerate(
            reversed(st.session_state.meetings)
        ):

            meeting_number = (
                len(st.session_state.meetings)
                - index
            )

            preview = meeting["notes"]


            # Keep cards compact
            if len(preview) > 220:

                preview = (
                    preview[:220]
                    + "..."
                )


            with st.container(
                border=True
            ):

                st.markdown(
                    f"### 🟣 Meeting {meeting_number}"
                )

                st.caption(
                    f"👤 {meeting['contact']}  •  "
                    f"🏢 {meeting['company']}"
                )

                st.write(preview)


# ============================================================
# MEETING INTELLIGENCE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🔮 Meeting Intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "MemoryMate combines information from "
    "previous meetings to prepare you for "
    "the next conversation."
)


# ============================================================
# GENERATE USING HINDSIGHT REFLECT
# ============================================================

def generate_with_hindsight():

    query = f"""
Prepare me for my next meeting with
{contact_name} from {company_name}.

Use relevant information from ALL previous
interactions stored in memory.

Create a professional meeting intelligence report.

Include these sections:

## Key Priorities

What does this contact care about?

## Communication Preferences

How does this person prefer to communicate?

## Concerns or Problems

What problems or risks have they mentioned?

## Open Commitments

What did we promise to do that may still
require follow-up?

## Important Deadlines

Identify dates or time-sensitive requirements.

## Suggested Talking Points

What should we discuss in the next meeting?

## Memory Insights

Mention useful information that became clear
from previous interactions.

Use only information supported by memory.
Do not invent facts.
"""


    # --------------------------------------------------------
    # RETRY HINDSIGHT REFLECT
    # --------------------------------------------------------

    last_error = None

    for attempt in range(3):

        try:

            response = client.reflect(
                bank_id=BANK_ID,
                query=query,
                budget="low",
                max_tokens=3000
            )

            if response and response.text:

                return response.text

        except Exception as e:

            last_error = e

            # Wait before retrying
            if attempt < 2:

                time.sleep(4)


    # If all Reflect attempts fail,
    # return the error so Recall fallback can run.

    raise Exception(
        f"Hindsight Reflect failed after 3 attempts: "
        f"{last_error}"
    )


# ============================================================
# FALLBACK: HINDSIGHT RECALL + GROQ
# ============================================================

def generate_with_recall_and_groq():

    if not groq_client:

        raise Exception(
            "GROQ_API_KEY is missing from .env"
        )


    # --------------------------------------------------------
    # SEARCH HINDSIGHT MEMORY
    # --------------------------------------------------------

    recall_query = f"""
Find all useful memories about my meetings
with {contact_name} from {company_name}.

Focus on:

- priorities
- communication preferences
- concerns
- problems
- deadlines
- commitments
- previous discussions
- follow-up items
- important facts
"""


    results = client.recall(
        bank_id=BANK_ID,
        query=recall_query,
        budget="low",
        max_tokens=5000
    )


    # --------------------------------------------------------
    # EXTRACT MEMORY TEXT
    # --------------------------------------------------------

    memories = []


    if hasattr(results, "results"):

        for item in results.results:

            if hasattr(item, "text"):

                if item.text:

                    memories.append(
                        item.text
                    )

            elif isinstance(item, str):

                memories.append(item)


    # --------------------------------------------------------
    # CHECK MEMORY
    # --------------------------------------------------------

    if not memories:

        raise Exception(
            "Hindsight Recall did not return "
            "any memories."
        )


    memory_text = "\n\n--- MEMORY ---\n\n".join(
        memories
    )


    # --------------------------------------------------------
    # GROQ PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are MemoryMate, an AI meeting intelligence assistant.

Prepare me for my next meeting with
{contact_name} from {company_name}.

Below are memories retrieved from Hindsight,
the long-term memory system.

IMPORTANT:
Use ONLY information contained in these memories.
Do not invent facts.

MEMORIES:

{memory_text}


Create a professional meeting briefing with
exactly these sections:

## Key Priorities

What does this contact care about?

## Communication Preferences

How does this person prefer to communicate?

## Concerns or Problems

What problems or risks have they mentioned?

## Open Commitments

What did we promise to do that may still
require follow-up?

## Important Deadlines

Identify dates or time-sensitive requirements.

## Suggested Talking Points

What should we discuss in the next meeting?

## Memory Insights

What useful information became clear from
previous interactions?

Keep the briefing concise and practical.
"""


    # --------------------------------------------------------
    # GROQ
    # --------------------------------------------------------

    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional meeting "
                    "intelligence assistant."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=2500
    )


    return completion.choices[0].message.content


# ============================================================
# PREPARE NEXT MEETING
# ============================================================

if st.button(
    "✨ Prepare My Next Meeting",
    use_container_width=True
):

    if not st.session_state.meetings:

        st.warning(
            "Please remember at least one meeting "
            "before preparing the next meeting."
        )

    else:

        with st.spinner(
            "🧠 Searching Hindsight memory..."
        ):

            try:

                # ==================================================
                # FIRST: HINDSIGHT REFLECT
                # ==================================================

                briefing = generate_with_hindsight()

                st.session_state.briefing = briefing

                st.session_state.briefing_source = (
                    "Hindsight Reflect"
                )


            except Exception as reflect_error:

                # ==================================================
                # REFLECT FAILED
                # TRY RECALL + GROQ
                # ==================================================

                try:

                    with st.spinner(
                        "🔎 Using Hindsight Recall to recover memories..."
                    ):

                        briefing = (
                            generate_with_recall_and_groq()
                        )

                        st.session_state.briefing = briefing

                        st.session_state.briefing_source = (
                            "Hindsight Recall + Groq"
                        )


                except Exception as fallback_error:

                    st.session_state.briefing = None

                    st.error(
                        "⚠️ The meeting briefing could not "
                        "be generated right now."
                    )

                    st.warning(
                        "Hindsight experienced a temporary "
                        "backend issue. Your meeting memory "
                        "has already been saved."
                    )

                    with st.expander(
                        "Technical details"
                    ):

                        st.write(
                            "Reflect error:"
                        )

                        st.code(
                            str(reflect_error)
                        )

                        st.write(
                            "Fallback error:"
                        )

                        st.code(
                            str(fallback_error)
                        )


# ============================================================
# DISPLAY BRIEFING
# ============================================================

if st.session_state.briefing:

    source = st.session_state.get(
        "briefing_source",
        "Hindsight"
    )


    st.markdown(
        '<div class="success-card">'
        '<strong>🧠 Memory Activated</strong><br>'
        f'This briefing was generated using '
        f'<strong>{source}</strong> and information '
        f'accumulated across previous interactions.'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        st.session_state.briefing
    )


else:

    st.info(
        "Click **Prepare My Next Meeting** "
        "to generate a briefing from "
        "accumulated memory."
    )


# ============================================================
# WHY MEMORYMATE IS DIFFERENT
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '💡 Why MemoryMate is Different'
    '</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)


# ------------------------------------------------------------
# REMEMBER
# ------------------------------------------------------------

with c1:

    st.markdown(
        '<div class="insight-card">'
        '<h3>🧠 Remember</h3>'
        '<p>Meeting information is stored in '
        'Hindsight instead of disappearing '
        'after the conversation.</p>'
        '</div>',
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# RECALL
# ------------------------------------------------------------

with c2:

    st.markdown(
        '<div class="insight-card">'
        '<h3>🔎 Recall</h3>'
        '<p>Previous interactions can be '
        'retrieved when they become '
        'relevant to the next conversation.</p>'
        '</div>',
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# REFLECT
# ------------------------------------------------------------

with c3:

    st.markdown(
        '<div class="insight-card">'
        '<h3>✨ Reflect</h3>'
        '<p>Hindsight reasons over accumulated '
        'memories to produce personalized '
        'meeting intelligence.</p>'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "MemoryMate • Persistent AI Memory • "
    "Powered by Hindsight"
)