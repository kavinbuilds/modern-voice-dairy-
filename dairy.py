import json
import os
import tempfile
from datetime import datetime

import streamlit as st

try:
    import whisper
except ImportError:
    whisper = None

try:
    from gtts import gTTS
except ImportError:
    gTTS = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="VocaDiary AI",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed",
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
AUDIO_FOLDER = "generated_audio"

os.makedirs(DIARY_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)


# ============================================================
# CSS
# IMPORTANT:
# HTML MUST START AT COLUMN 0 INSIDE THE TRIPLE QUOTES.
# ============================================================

st.markdown(
    """
<style>

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

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

.block-container {
    max-width: 850px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}


/* ============================================================
   HEADER
   ============================================================ */

.brand {
    text-align: center;
    margin-bottom: 10px;
}

.brand-small {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
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


/* ============================================================
   GLASS CARD
   ============================================================ */

.glass-card {
    background: rgba(15, 23, 42, 0.72);

    border: 1px solid rgba(148, 163, 184, 0.15);

    border-radius: 24px;

    padding: 24px;

    box-shadow:
        0 20px 50px rgba(0, 0, 0, 0.28),
        inset 0 1px 0 rgba(255, 255, 255, 0.04);

    backdrop-filter: blur(18px);

    margin-bottom: 20px;
}


/* ============================================================
   SECTION
   ============================================================ */

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 5px;
}

.section-description {
    color: #94a3b8;
    font-size: 14px;
}


/* ============================================================
   FEATURE BADGES
   ============================================================ */

.feature-row {
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;

    margin-top: 18px;
    margin-bottom: 28px;
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


/* ============================================================
   TABS
   ============================================================ */

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


/* ============================================================
   SELECT BOX
   ============================================================ */

div[data-baseweb="select"] > div {
    background: rgba(15, 23, 42, 0.85) !important;

    border:
        1px solid rgba(148, 163, 184, 0.20)
        !important;

    border-radius: 14px !important;

    color: white !important;
}


/* ============================================================
   AUDIO INPUT
   ============================================================ */

[data-testid="stAudioInput"] {
    background: rgba(30, 41, 59, 0.45);

    border:
        1px dashed rgba(129, 140, 248, 0.55);

    border-radius: 20px;

    padding: 16px;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    border-radius: 14px !important;

    border:
        1px solid rgba(148, 163, 184, 0.18)
        !important;

    background:
        rgba(30, 41, 59, 0.8)
        !important;

    color: #f8fafc !important;

    font-weight: 700 !important;

    min-height: 46px;
}

.stButton > button:hover {
    border-color:
        rgba(129, 140, 248, 0.6)
        !important;
}

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
        0 8px 25px
        rgba(79, 70, 229, 0.28);
}


/* ============================================================
   TEXT AREA
   ============================================================ */

textarea {
    background:
        rgba(15, 23, 42, 0.80)
        !important;

    color:
        #f8fafc
        !important;

    border:
        1px solid rgba(148, 163, 184, 0.18)
        !important;

    border-radius:
        16px
        !important;

    font-size:
        15px
        !important;

    line-height:
        1.7
        !important;
}

input {
    color: #f8fafc !important;
}


/* ============================================================
   ALERTS
   ============================================================ */

[data-testid="stAlert"] {
    border-radius: 14px !important;

    border:
        1px solid rgba(148, 163, 184, 0.15)
        !important;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;

    color: #64748b;

    font-size: 12px;

    margin-top: 35px;
}


/* ============================================================
   MOBILE
   ============================================================ */

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

    .feature {
        font-size: 11px;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# LOAD WHISPER
# ============================================================

@st.cache_resource(show_spinner=False)
def load_model():

    if whisper is None:
        raise RuntimeError(
            "Whisper is not installed. "
            "Add openai-whisper to requirements.txt."
        )

    return whisper.load_model("base")


# ============================================================
# SESSION STATE
# ============================================================

if "audio_key" not in st.session_state:
    st.session_state.audio_key = 0

if "diary_editor" not in st.session_state:
    st.session_state.diary_editor = ""

if "diary_note" not in st.session_state:
    st.session_state.diary_note = ""

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"

if "loaded_date" not in st.session_state:
    st.session_state.loaded_date = None

if "loaded_language" not in st.session_state:
    st.session_state.loaded_language = "English"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_filename(date_value):

    return os.path.join(
        DIARY_FOLDER,
        f"{date_value.strftime('%d-%m-%y')}.json"
    )


def save_diary(
    date_value,
    text,
    language
):

    data = {
        "date": date_value.strftime("%d-%m-%y"),
        "language": language,
        "text": text
    }

    filename = get_filename(date_value)

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


def load_diary(date_value):

    filename = get_filename(date_value)

    if not os.path.exists(filename):
        return None

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        OSError,
        json.JSONDecodeError
    ):

        return None


def delete_file(filename):

    try:

        if os.path.exists(filename):
            os.remove(filename)

    except OSError:
        pass


def make_tts(
    text,
    language_name
):

    if gTTS is None:

        raise RuntimeError(
            "gTTS is not installed. "
            "Add gTTS to requirements.txt."
        )

    output_file = os.path.join(
        AUDIO_FOLDER,
        "diary_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
        + ".mp3"
    )

    gTTS(
        text=text,
        lang=LANGUAGES[
            language_name
        ]["tts"]
    ).save(output_file)

    return output_file


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
        "✦ Add Diary",
        "⌕ Search Diary"
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


    language_names = list(
        LANGUAGES.keys()
    )


    language_name = st.selectbox(
        "🌍 Diary language",

        language_names,

        index=language_names.index(
            st.session_state.selected_language
        ),

        key="record_language"
    )


    st.session_state.selected_language = (
        language_name
    )


    st.caption(
        f"{LANGUAGES[language_name]['flag']} "
        f"Recording language: **{language_name}**"
    )


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # ========================================================
    # AUDIO RECORDING
    # ========================================================

    audio_file = st.audio_input(
        "🎙️ Tap to record your diary",

        key=(
            f"audio_input_"
            f"{st.session_state.audio_key}"
        )
    )


    if audio_file is not None:

        st.audio(audio_file)


        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        col1, col2 = st.columns(2)


        # ====================================================
        # CLEAR
        # ====================================================

        with col1:

            if st.button(
                "🗑️ Clear",

                key=(
                    f"clear_"
                    f"{st.session_state.audio_key}"
                ),

                width="stretch"
            ):

                st.session_state.audio_key += 1

                st.session_state.diary_editor = ""

                st.rerun()


        # ====================================================
        # CONVERT
        # ====================================================

        with col2:

            if st.button(
                "✨ Convert with AI",

                key=(
                    f"convert_"
                    f"{st.session_state.audio_key}"
                ),

                type="primary",

                width="stretch"
            ):

                temp_path = None

                try:

                    with st.spinner(
                        f"AI is understanding your "
                        f"{language_name} voice..."
                    ):

                        # Create a unique temporary audio file
                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=".wav"
                        ) as temp_file:

                            temp_file.write(
                                audio_file.getvalue()
                            )

                            temp_path = (
                                temp_file.name
                            )


                        # Load Whisper
                        model = load_model()


                        # Transcribe
                        result = model.transcribe(

                            temp_path,

                            language=LANGUAGES[
                                language_name
                            ]["whisper"],

                            fp16=False
                        )


                    text = result.get(
                        "text",
                        ""
                    ).strip()


                    if text:

                        st.session_state.diary_editor = (
                            text
                        )

                        st.success(
                            "Your diary entry is ready! ✨"
                        )

                    else:

                        st.warning(
                            "No speech was detected. "
                            "Please record again."
                        )


                except Exception as error:

                    st.error(
                        "Unable to process the recording."
                    )

                    with st.expander(
                        "Technical details"
                    ):

                        st.exception(error)


                finally:

                    if temp_path:

                        delete_file(
                            temp_path
                        )


    # ========================================================
    # DIARY EDITOR
    # ========================================================

    if st.session_state.diary_editor:

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


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

            key="diary_editor",

            height=260,

            label_visibility="collapsed"
        )


        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        # ====================================================
        # SAVE
        # ====================================================

        if st.button(
            "💾 Save to My Diary",

            type="primary",

            width="stretch",

            key="save_diary"
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


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # ========================================================
    # FIND
    # ========================================================

    if st.button(
        "🔍 Find Diary",

        type="primary",

        width="stretch",

        key="find_diary"
    ):

        diary_data = load_diary(
            search_date
        )


        if diary_data:

            st.session_state.diary_note = (
                diary_data.get(
                    "text",
                    ""
                )
            )


            st.session_state.loaded_date = (
                search_date
            )


            st.session_state.loaded_language = (
                diary_data.get(
                    "language","English"
                )
            )


            st.success(
                "Memory found ✨"
            )

        else:

            st.session_state.diary_note = ""

            st.session_state.loaded_date = None

            st.warning(
                "No diary entry found for this date."
            )


    # ========================================================
    # DISPLAY DIARY
    # ========================================================

    if (
        st.session_state.diary_note
        and
        st.session_state.loaded_date
        == search_date
    ):

        saved_language = (
            st.session_state.loaded_language
        )


        if saved_language not in LANGUAGES:

            saved_language = "English"


        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


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


        st.text_area(

            "Saved diary entry",

            value=st.session_state.diary_note,

            height=280,

            disabled=True,

            label_visibility="collapsed"
        )


        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        col1, col2 = st.columns(2)


        # ====================================================
        # PLAY DIARY
        # ====================================================

        with col1:

            if st.button(
                "🔊 Play Diary",

                width="stretch",

                key="play_diary"
            ):

                try:

                    with st.spinner(
                        "Creating voice playback..."
                    ):

                        audio_path = make_tts(

                            st.session_state.diary_note,

                            saved_language
                        )


                    with open(
                        audio_path,
                        "rb"
                    ) as audio:

                        st.audio(
                            audio.read(),
                            format="audio/mp3"
                        )


                except Exception as error:

                    st.error(
                        "Voice playback could not "
                        "be generated."
                    )

                    with st.expander(
                        "Technical details"
                    ):

                        st.exception(error)


        # ====================================================
        # DELETE DIARY
        # ====================================================

        with col2:

            if st.button(
                "🗑️ Delete Entry",

                width="stretch",

                key="delete_diary"
            ):

                delete_file(
                    get_filename(
                        search_date
                    )
                )


                st.session_state.diary_note = ""

                st.session_state.loaded_date = None


                st.success(
                    "Diary entry deleted."
                )


                st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
    VocaDiary AI • Your voice. Your memories. Your story.
</div>
""",
    unsafe_allow_html=True
)