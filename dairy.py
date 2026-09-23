import os
import json
import tempfile
import textwrap
from datetime import datetime

import streamlit as st
import whisper
from gtts import gTTS


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VocaDiary AI",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# LANGUAGE CONFIGURATION
# ============================================================

LANGUAGES = {
    "English": {
        "whisper": "en",
        "tts": "en",
        "flag": "🇬🇧"
    },
    "Hindi": {
        "whisper": "hi",
        "tts": "hi",
        "flag": "🇮🇳"
    },
    "Marathi": {
        "whisper": "mr",
        "tts": "mr",
        "flag": "🇮🇳"
    },
    "Tamil": {
        "whisper": "ta",
        "tts": "ta",
        "flag": "🇮🇳"
    },
    "Telugu": {
        "whisper": "te",
        "tts": "te",
        "flag": "🇮🇳"
    },
    "Bengali": {
        "whisper": "bn",
        "tts": "bn",
        "flag": "🇮🇳"
    },
    "Gujarati": {
        "whisper": "gu",
        "tts": "gu",
        "flag": "🇮🇳"
    },
    "Kannada": {
        "whisper": "kn",
        "tts": "kn",
        "flag": "🇮🇳"
    },
    "Malayalam": {
        "whisper": "ml",
        "tts": "ml",
        "flag": "🇮🇳"
    },
    "Punjabi": {
        "whisper": "pa",
        "tts": "pa",
        "flag": "🇮🇳"
    }
}


# ============================================================
# APPLICATION SETTINGS
# ============================================================

DIARY_FOLDER = "diary_notes"

os.makedirs(DIARY_FOLDER, exist_ok=True)


# ============================================================
# HELPER FOR HTML
#
# This fixes the problem where Streamlit was displaying
# <div> and </div> as visible text.
# ============================================================

def render_html(html):
    st.markdown(
        textwrap.dedent(html).strip(),
        unsafe_allow_html=True
    )


# ============================================================
# PREMIUM MOBILE-FIRST CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL APP
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(124, 58, 237, 0.20),
            transparent 28%
        ),
        radial-gradient(
            circle at 100% 15%,
            rgba(59, 130, 246, 0.16),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(6, 182, 212, 0.08),
            transparent 35%
        ),
        #070a14;

    color: #f8fafc;
}


/* ============================================================
   REMOVE DEFAULT STREAMLIT ELEMENTS
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ============================================================
   MAIN CONTAINER
   ============================================================ */

.block-container {
    max-width: 760px !important;

    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;

    padding-left: 1rem !important;
    padding-right: 1rem !important;
}


/* ============================================================
   BRAND
   ============================================================ */

.brand {
    text-align: center;

    padding-top: 10px;
    padding-bottom: 12px;
}

.brand-small {
    color: #a78bfa;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 3px;

    text-transform: uppercase;

    margin-bottom: 8px;
}

.brand-title {
    font-size: clamp(38px, 11vw, 58px);

    line-height: 1;

    font-weight: 900;

    letter-spacing: -2px;

    background:
        linear-gradient(
            100deg,
            #d8b4fe,
            #8b5cf6,
            #60a5fa,
            #22d3ee
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    background-clip: text;

    margin: 0;
}

.brand-subtitle {
    margin-top: 12px;

    color: #94a3b8;

    font-size: 14px;

    line-height: 1.5;
}


/* ============================================================
   FEATURE PILLS
   ============================================================ */

.feature-row {
    display: flex;

    justify-content: center;

    flex-wrap: wrap;

    gap: 7px;

    margin-top: 16px;
    margin-bottom: 24px;
}

.feature {
    padding: 7px 11px;

    border-radius: 999px;

    background: rgba(139, 92, 246, 0.08);

    border:
        1px solid
        rgba(139, 92, 246, 0.20);

    color: #c4b5fd;

    font-size: 11px;

    font-weight: 700;

    white-space: nowrap;
}


/* ============================================================
   GLASS CARD
   ============================================================ */

.glass-card {
    width: 100%;
    box-sizing: border-box;

    background:
        linear-gradient(
            145deg,
            rgba(22, 28, 52, 0.88),
            rgba(10, 15, 30, 0.82)
        );

    border:
        1px solid
        rgba(148, 163, 184, 0.13);

    border-radius: 22px;

    padding: 20px;

    margin-bottom: 16px;

    box-shadow:
        0 18px 45px rgba(0, 0, 0, 0.24),
        inset 0 1px 0 rgba(255,255,255,0.04);

    backdrop-filter: blur(18px);
}


/* ============================================================
   CARD ICON
   ============================================================ */

.card-icon {
    width: 48px;
    height: 48px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 15px;

    background:
        linear-gradient(
            135deg,
            rgba(139, 92, 246, 0.25),
            rgba(59, 130, 246, 0.18)
        );

    border:
        1px solid
        rgba(167, 139, 250, 0.20);

    font-size: 22px;

    margin-bottom: 14px;
}


/* ============================================================
   CARD TITLES
   ============================================================ */

.section-title {
    color: #f8fafc;

    font-size: 20px;

    font-weight: 800;

    letter-spacing: -0.3px;
}

.section-description {
    color: #94a3b8;

    font-size: 13px;

    line-height: 1.6;

    margin-top: 6px;
}


/* ============================================================
   TABS
   ============================================================ */

div[data-baseweb="tab-list"] {
    gap: 8px;

    background:
        rgba(15, 23, 42, 0.65);

    border:
        1px solid
        rgba(148, 163, 184, 0.10);

    border-radius: 15px;

    padding: 5px;

    margin-bottom: 18px;
}

button[data-baseweb="tab"] {
    border-radius: 11px !important;

    color: #64748b !important;

    font-size: 13px !important;

    font-weight: 700 !important;

    padding: 9px 12px !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background:
        linear-gradient(
            135deg,
            rgba(124, 58, 237, 0.28),
            rgba(59, 130, 246, 0.20)
        ) !important;

    color: #ffffff !important;
}

div[data-baseweb="tab-highlight"] {
    background:
        linear-gradient(
            90deg,
            #8b5cf6,
            #3b82f6
        ) !important;
}


/* ============================================================
   LABELS
   ============================================================ */

label {
    color: #cbd5e1 !important;

    font-size: 13px !important;

    font-weight: 600 !important;
}


/* ============================================================
   SELECTBOX
   ============================================================ */

div[data-baseweb="select"] > div {
    background:
        rgba(15, 23, 42, 0.86) !important;

    border:
        1px solid
        rgba(148, 163, 184, 0.16) !important;

    border-radius: 13px !important;

    min-height: 46px !important;

    color: #f8fafc !important;
}


/* ============================================================
   DATE INPUT
   ============================================================ */

div[data-testid="stDateInput"] input {
    background:
        rgba(15, 23, 42, 0.86) !important;

    border:
        1px solid
        rgba(148, 163, 184, 0.16) !important;

    border-radius: 13px !important;

    color: #f8fafc !important;
}


/* ============================================================
   AUDIO INPUT
   ============================================================ */

[data-testid="stAudioInput"] {
    background:
        linear-gradient(
            145deg,
            rgba(30, 41, 70, 0.70),
            rgba(15, 23, 42, 0.65)
        );

    border:
        1px dashed
        rgba(129, 140, 248, 0.55);

    border-radius: 20px;

    padding: 14px;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.03);
}


/* ============================================================
   AUDIO PLAYER
   ============================================================ */

audio {
    width: 100% !important;

    border-radius: 12px;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    min-height: 46px !important;

    border-radius: 13px !important;

    background:
        rgba(30, 41, 59, 0.85) !important;

    color: #f8fafc !important;

    border:
        1px solid
        rgba(148, 163, 184, 0.16) !important;

    font-size: 13px !important;

    font-weight: 750 !important;

    transition:
        transform 0.15s ease,
        box-shadow 0.15s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);

    border-color:
        rgba(129, 140, 248, 0.50) !important;

    box-shadow:
        0 8px 22px
        rgba(0,0,0,0.22);
}


/* ============================================================
   PRIMARY BUTTON
   ============================================================ */

.stButton > button[kind="primary"] {
    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #5b4ce6,
            #2563eb
        ) !important;

    border: none !important;

    color: white !important;

    box-shadow:
        0 8px 25px
        rgba(99, 72, 220, 0.28);
}

.stButton > button[kind="primary"]:hover {
    box-shadow:
        0 12px 30px
        rgba(99, 72, 220, 0.40);
}


/* ============================================================
   TEXT AREA
   ============================================================ */

textarea {
    background:
        rgba(8, 13, 27, 0.82) !important;

    color:
        #f8fafc !important;

    border:
        1px solid
        rgba(148, 163, 184, 0.15) !important;

    border-radius:
        16px !important;

    font-size:
        15px !important;

    line-height:
        1.75 !important;

    padding:
        14px !important;
}


/* ============================================================
   INFO / SUCCESS / WARNING
   ============================================================ */

[data-testid="stAlert"] {
    border-radius: 14px !important;

    background:
        rgba(15, 23, 42, 0.75) !important;

    border:
        1px solid
        rgba(148, 163, 184, 0.12) !important;
}


/* ============================================================
   CAPTION
   ============================================================ */

[data-testid="stCaptionContainer"] {
    color: #64748b !important;
}


/* ============================================================
   DIVIDER
   ============================================================ */

hr {
    border-color:
        rgba(148, 163, 184, 0.08) !important;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;

    color: #475569;

    font-size: 11px;

    margin-top: 28px;

    padding-bottom: 10px;
}


/* ============================================================
   MOBILE OPTIMIZATION
   ============================================================ */

@media (max-width: 600px) {

    .block-container {
        padding-top: 0.8rem !important;

        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }

    .brand-title {
        font-size: 40px;
    }

    .brand-subtitle {
        font-size: 13px;
    }

    .feature-row {
        gap: 5px;
    }

    .feature {
        font-size: 10px;
        padding: 6px 9px;
    }

    .glass-card {
        padding: 17px;

        border-radius: 19px;
    }

    .section-title {
        font-size: 18px;
    }

    .section-description {
        font-size: 12px;
    }

    .stButton > button {
        min-height: 48px !important;
    }

}


/* ============================================================
   EXTRA SMALL PHONES
   ============================================================ */

@media (max-width: 380px) {

    .brand-title {
        font-size: 35px;
    }

    .feature {
        font-size: 9px;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# LOAD WHISPER MODEL
# ============================================================

@st.cache_resource
def load_model():
    return whisper.load_model("base")


model = load_model()


# ============================================================
# SESSION STATE
# ============================================================

if "audio_key" not in st.session_state:
    st.session_state.audio_key = 0

if "edit_area" not in st.session_state:
    st.session_state.edit_area = ""

if "diary_note" not in st.session_state:
    st.session_state.diary_note = ""

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_filename(date):
    date_string = date.strftime("%d-%m-%y")

    return os.path.join(
        DIARY_FOLDER,
        f"{date_string}.json"
    )


def save_diary(date, text, language):

    data = {
        "date": date.strftime("%d-%m-%y"),
        "language": language,
        "text": text
    }

    filename = get_filename(date)

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )

    return filename


def load_diary(date):

    filename = get_filename(date)

    if not os.path.exists(filename):
        return None

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:
        return None


def delete_file(filename):

    if os.path.exists(filename):

        try:
            os.remove(filename)

        except OSError:
            pass


# ============================================================
# BRAND HEADER
# ============================================================

render_html(
    """
    <div class="brand">

        <div class="brand-small">
            ✦ AI POWERED
        </div>

        <div class="brand-title">
            VocaDiary
        </div>

        <div class="brand-subtitle">
            Your voice. Your memories. Your story.
        </div>

    </div>
    """
)


# ============================================================
# FEATURE PILLS
# ============================================================

render_html(
    """
    <div class="feature-row">

        <div class="feature">
            🎙️ Voice
        </div>

        <div class="feature">
            🌍 10 Languages
        </div>

        <div class="feature">
            🤖 AI Transcription
        </div>

        <div class="feature">
            🔊 Voice Playback
        </div>

    </div>
    """
)


# ============================================================
# TABS
# ============================================================

tab_add, tab_search = st.tabs(
    [
        "✦  Add Diary",
        "⌕  Search Diary"
    ]
)


# ============================================================
# ADD DIARY
# ============================================================

with tab_add:

    render_html(
        """
        <div class="glass-card">

            <div class="card-icon">
                🎙️
            </div>

            <div class="section-title">
                Capture your moment
            </div>

            <div class="section-description">
                Speak naturally and let AI transform
                your voice into a diary entry.
            </div>

        </div>
        """
    )

    # --------------------------------------------------------
    # LANGUAGE
    # --------------------------------------------------------

    language_name = st.selectbox(
        "🌍 Diary language",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(
            st.session_state.selected_language
        ),
        key="record_language"
    )

    st.session_state.selected_language = language_name

    whisper_language = LANGUAGES[
        language_name
    ]["whisper"]

    st.caption(
        f"{LANGUAGES[language_name]['flag']} "
        f"Recording in {language_name}"
    )

    # --------------------------------------------------------
    # RECORDING
    # --------------------------------------------------------

    audio_file = st.audio_input(
        "🎙️ Tap below to record",
        key=f"audio_input_{st.session_state.audio_key}"
    )

    if audio_file is not None:

        audio_path = "audio.wav"

        with open(
            audio_path,
            "wb"
        ) as file:

            file.write(
                audio_file.getvalue()
            )

        st.audio(audio_file)

        st.write("")

        col1, col2 = st.columns(
            2,
            gap="small"
        )

        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        with col1:

            if st.button(
                "🗑️ Clear",
                key=f"clear_{st.session_state.audio_key}",
                width="stretch"
            ):

                delete_file(audio_path)

                st.session_state.audio_key += 1

                st.session_state.edit_area = ""

                st.rerun()

        # ----------------------------------------------------
        # CONVERT
        # ----------------------------------------------------

        with col2:

            if st.button(
                "✨ Convert",
                key="convert",
                type="primary",
                width="stretch"
            ):

                try:

                    with st.spinner(
                        "AI is processing your voice..."
                    ):

                        result = model.transcribe(
                            audio_path,
                            language=whisper_language,
                            fp16=False
                        )

                    text = result[
                        "text"
                    ].strip()

                    if text:

                        st.session_state.edit_area = text

                        st.success(
                            "Your diary entry is ready ✨"
                        )

                    else:

                        st.warning(
                            "No speech was detected."
                        )

                except