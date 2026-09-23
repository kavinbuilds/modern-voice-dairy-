import os
import json
import tempfile
from datetime import datetime

import streamlit as st
import whisper
from gtts import gTTS


# ============================================================
# PAGE CONFIG
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
    "English": {"whisper": "en", "tts": "en", "flag": "🇬🇧"},
    "Hindi": {"whisper": "hi", "tts": "hi", "flag": "🇮🇳"},
    "Marathi": {"whisper": "mr", "tts": "mr", "flag": "🇮🇳"},
    "Tamil": {"whisper": "ta", "tts": "ta", "flag": "🇮🇳"},
    "Telugu": {"whisper": "te", "tts": "te", "flag": "🇮🇳"},
    "Bengali": {"whisper": "bn", "tts": "bn", "flag": "🇮🇳"},
    "Gujarati": {"whisper": "gu", "tts": "gu", "flag": "🇮🇳"},
    "Kannada": {"whisper": "kn", "tts": "kn", "flag": "🇮🇳"},
    "Malayalam": {"whisper": "ml", "tts": "ml", "flag": "🇮🇳"},
    "Punjabi": {"whisper": "pa", "tts": "pa", "flag": "🇮🇳"},
}


# ============================================================
# FOLDERS
# ============================================================

DIARY_FOLDER = "diary_notes"

os.makedirs(DIARY_FOLDER, exist_ok=True)


# ============================================================
# MODERN UI / CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(124, 58, 237, 0.22),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(37, 99, 235, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(14, 165, 233, 0.12),
                transparent 35%
            ),
            #080b18;
        color: #f8fafc;
    }

    /* Hide Streamlit default decorations */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* Main content */

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =====================================================
       HEADER
       ===================================================== */

    .brand {
        text-align: center;
        margin-bottom: 8px;
    }

    .brand-small {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #a78bfa;
        margin-bottom: 8px;
    }

    .brand-title {
        font-size: 48px;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -2px;

        background: linear-gradient(
            90deg,
            #c084fc,
            #818cf8,
            #38bdf8
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        margin: 0;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: 15px;
        margin-top: 12px;
    }


    /* =====================================================
       GLASS CARD
       ===================================================== */

    .glass-card {
        background: rgba(15, 23, 42, 0.72);

        border: 1px solid rgba(148, 163, 184, 0.15);

        border-radius: 24px;

        padding: 28px;

        box-shadow:
            0 20px 50px rgba(0, 0, 0, 0.28),
            inset 0 1px 0 rgba(255, 255, 255, 0.04);

        backdrop-filter: blur(18px);

        margin-bottom: 20px;
    }


    /* =====================================================
       SECTION TITLES
       ===================================================== */

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .section-description {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 20px;
    }


    /* =====================================================
       FEATURE BADGES
       ===================================================== */

    .feature-row {
        display: flex;
        justify-content: center;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 20px;
        margin-bottom: 30px;
    }

    .feature {
        background: rgba(139, 92, 246, 0.10);
        border: 1px solid rgba(139, 92, 246, 0.20);
        color: #c4b5fd;

        border-radius: 999px;

        padding: 7px 13px;

        font-size: 12px;
        font-weight: 600;
    }


    /* =====================================================
       TABS
       ===================================================== */

    button[data-baseweb="tab"] {
        background: transparent !important;
        color: #94a3b8 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
        background: rgba(139, 92, 246, 0.15) !important;
    }

    [data-baseweb="tab-highlight"] {
        background: linear-gradient(
            90deg,
            #8b5cf6,
            #3b82f6
        ) !important;
    }


    /* =====================================================
       SELECT BOX
       ===================================================== */

    div[data-baseweb="select"] > div {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(148, 163, 184, 0.20) !important;
        border-radius: 14px !important;
        color: white !important;
    }


    /* =====================================================
       AUDIO INPUT
       ===================================================== */

    [data-testid="stAudioInput"] {
        background: rgba(30, 41, 59, 0.45);
        border: 1px dashed rgba(129, 140, 248, 0.55);
        border-radius: 20px;
        padding: 20px;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        border-radius: 14px !important;

        border: 1px solid rgba(148, 163, 184, 0.18) !important;

        background: rgba(30, 41, 59, 0.8) !important;

        color: #f8fafc !important;

        font-weight: 700 !important;

        min-height: 48px;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 10px 25px rgba(0, 0, 0, 0.25);

        border-color: rgba(129, 140, 248, 0.6) !important;
    }

    /* Primary buttons */

    .stButton > button[kind="primary"] {
        background:
            linear-gradient(
                135deg,
                #7c3aed,
                #4f46e5,
                #2563eb
            ) !important;

        border: none !important;

        box-shadow:
            0 8px 25px rgba(79, 70, 229, 0.28);
    }

    .stButton > button[kind="primary"]:hover {
        box-shadow:
            0 12px 32px rgba(79, 70, 229, 0.40);
    }


    /* =====================================================
       TEXT AREA
       ===================================================== */

    textarea {
        background: rgba(15, 23, 42, 0.80) !important;

        color: #f8fafc !important;

        border:
            1px solid rgba(148, 163, 184, 0.18)
            !important;

        border-radius: 16px !important;

        font-size: 15px !important;

        line-height: 1.7 !important;
    }


    /* =====================================================
       DATE INPUT
       ===================================================== */

    input {
        color: #f8fafc !important;
    }


    /* =====================================================
       INFO / SUCCESS / WARNING
       ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 14px !important;
        border: 1px solid rgba(148, 163, 184, 0.15) !important;
        background: rgba(15, 23, 42, 0.70) !important;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {
        border-color: rgba(148, 163, 184, 0.10) !important;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        margin-top: 35px;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 600px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .brand-title {
            font-size: 36px;
        }

        .glass-card {
            padding: 20px;
            border-radius: 20px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD WHISPER
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
# HEADER
# ============================================================

st.markdown(
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
    """,
    unsafe_allow_html=True
)


# ============================================================
# FEATURES
# ============================================================

st.markdown(
    """
    <div class="feature-row">

        <div class="feature">
            🎙️ Voice Powered
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
    """,
    unsafe_allow_html=True
)


# ============================================================
# TABS
# ============================================================

tab1, tab2 = st.tabs(
    [
        "✦  Add Diary",
        "⌕  Search Diary"
    ]
)


# ============================================================
# ADD DIARY
# ============================================================

with tab1:

    st.markdown(
        """
        <div class="glass-card">

            <div class="section-title">
                🎙️ Capture your moment
            </div>

            <div class="section-description">
                Speak naturally and let AI turn your voice
                into a beautiful diary entry.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

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
        f"Recording language: **{language_name}**"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    audio_file = st.audio_input(
        "🎙️ Tap to record your diary",
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

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

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

        with col2:

            if st.button(
                "✨ Convert with AI",
                key="convert",
                type="primary",
                width="stretch"
            ):

                try:

                    with st.spinner(
                        f"AI is understanding your "
                        f"{language_name} voice..."
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
                            "Your diary entry is ready! ✨"
                        )

                    else:

                        st.warning(
                            "No speech was detected."
                        )

                except Exception as error:

                    st.error(
                        "Unable to process the recording."
                    )

                    st.exception(error)

        # ----------------------------------------------------
        # EDITOR
        # ----------------------------------------------------

        if st.session_state.edit_area:

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                """
                <div class="glass-card">

                    <div class="section-title">
                        📝 Your diary
                    </div>

                    <div class="section-description">
                        Review and edit your entry before saving.
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            edited_text = st.text_area(
                "Diary entry",
                value=st.session_state.edit_area,
                height=260,
                label_visibility="collapsed"
            )

            st.session_state.edit_area = edited_text

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button(
                "💾 Save to My Diary",
                type="primary",
                width="stretch"
            ):

                if edited_text.strip():

                    today = datetime.now()

                    save_diary(
                        today,
                        edited_text.strip(),
                        language_name
                    )

                    st.success(
                        "Diary saved successfully 💜"
                    )

                    st.caption(
                        f"Saved on "
                        f"{today.strftime('%d %B %Y')} "
                        f"• {language_name}"
                    )

                else:

                    st.warning(
                        "Your diary entry is empty."
                    )


# ============================================================
# SEARCH DIARY
# ============================================================

with tab2:

    st.markdown(
        """
        <div class="glass-card">

            <div class="section-title">
                🔎 Revisit a memory
            </div>

            <div class="section-description">
                Select a date to rediscover what you recorded.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    search_date = st.date_input(
        "Choose a date",
        value=datetime.now().date(),
        key="search_date"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "🔍 Find Diary",
        type="primary",
        width="stretch"
    ):

        diary_data = load_diary(
            search_date
        )

        if diary_data:

            st.session_state.diary_note = diary_data.get(
                "text",
                ""
            )

            st.session_state.selected_language = diary_data.get(
                "language",
                "English"
            )

            st.success(
                "Memory found ✨"
            )

        else:

            st.session_state.diary_note = ""

            st.warning(
                "No diary entry found for this date."
            )


    # --------------------------------------------------------
    # DISPLAY DIARY
    # --------------------------------------------------------

    if st.session_state.diary_note:

        diary_data = load_diary(
            search_date
        )

        saved_language = "English"

        if diary_data:

            saved_language = diary_data.get(
                "language",
                "English"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="glass-card">

                <div class="section-title">
                    📖 {search_date.strftime('%d %B %Y')}
                </div>

                <div class="section-description">
                    {LANGUAGES[saved_language]['flag']}
                    Recorded in {saved_language}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )
   edited_diary = st.text_area(
            "Diary",
            value=st.session_state.diary_note,
            height=280,
            label_visibility="collapsed"
        )

        st.session_state.diary_note = edited_diary

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # SAVE CHANGES
        # ----------------------------------------------------

        with col1:

            if st.button(
                "💾 Save Changes",
                width="stretch"
            ):

                save_diary(
                    search_date,
                    edited_diary.strip(),
                    saved_language
                )

                st.success(
                    "Diary updated!"
                )

        # ----------------------------------------------------
        # READ DIARY
        # ----------------------------------------------------

        with col2:

            if st.button(
                "🔊 Read Aloud",
                type="primary",
                width="stretch"
            ):

                if not edited_diary.strip():

                    st.warning(
                        "There is nothing to read."
                    )

                else:

                    try:

                        tts_language = LANGUAGES.get(
                            saved_language,
                            LANGUAGES["English"]
                        )["tts"]

                        with st.spinner(
                            "Creating your audio memory..."
                        ):

                            tts = gTTS(
                                text=edited_diary,
                                lang=tts_language,
                                slow=False
                            )

                            with tempfile.NamedTemporaryFile(
                                delete=False,
                                suffix=".mp3"
                            ) as temp_file:

                                audio_path = temp_file.name

                            tts.save(
                                audio_path
                            )

                        with open(
                            audio_path,
                            "rb"
                        ) as audio:

                            audio_bytes = audio.read()

                        st.audio(
                            audio_bytes,
                            format="audio/mp3"
                        )

                        delete_file(
                            audio_path
                        )

                    except Exception as error:

                        st.error(
                            "Unable to create the voice playback."
                        )

                        st.exception(error)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        ✦ VocaDiary AI &nbsp;•&nbsp;
        Your memories, beautifully preserved.
    </div>
    """,
    unsafe_allow_html=True
)