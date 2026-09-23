import os
import json
import tempfile
from datetime import datetime

import streamlit as st
import whisper
from gtts import gTTS


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DIGITAL DIARY",
    page_icon="🗣️",
    layout="centered"
)


# ============================================================
# LANGUAGE CONFIGURATION
# ============================================================

LANGUAGES = {
    "English": {
        "whisper": "en",
        "tts": "en"
    },
    "Hindi": {
        "whisper": "hi",
        "tts": "hi"
    },
    "Marathi": {
        "whisper": "mr",
        "tts": "mr"
    },
    "Tamil": {
        "whisper": "ta",
        "tts": "ta"
    },
    "Telugu": {
        "whisper": "te",
        "tts": "te"
    },
    "Bengali": {
        "whisper": "bn",
        "tts": "bn"
    },
    "Gujarati": {
        "whisper": "gu",
        "tts": "gu"
    },
    "Kannada": {
        "whisper": "kn",
        "tts": "kn"
    },
    "Malayalam": {
        "whisper": "ml",
        "tts": "ml"
    },
    "Punjabi": {
        "whisper": "pa",
        "tts": "pa"
    }
}


# ============================================================
# DIRECTORIES
# ============================================================

DIARY_FOLDER = "diary_notes"

os.makedirs(DIARY_FOLDER, exist_ok=True)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    [data-testid="stAppViewContainer"] {
        background-color: #f0f0f0;
    }

    [data-testid="stHeader"] {
        background-color: #f0f0f0;
    }

    .title {
        text-align: center;
        color: #ff6600;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        color: #555555;
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

if "selected_date" not in st.session_state:
    st.session_state.selected_date = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_filename(selected_date):
    """
    Returns the JSON filename for a diary date.
    """

    date_string = selected_date.strftime("%d-%m-%y")

    return os.path.join(
        DIARY_FOLDER,
        f"{date_string}.json"
    )


def save_diary(date, text, language):
    """
    Save diary text and language information.
    """

    filename = get_filename(date)

    diary_data = {
        "date": date.strftime("%d-%m-%y"),
        "language": language,
        "text": text
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            diary_data,
            file,
            ensure_ascii=False,
            indent=4
        )

    return filename


def load_diary(date):
    """
    Load diary from JSON file.
    """

    filename = get_filename(date)

    if not os.path.exists(filename):
        return None

    try:
        with open(filename, "r", encoding="utf-8") as file:
            diary_data = json.load(file)

        return diary_data

    except (json.JSONDecodeError, OSError):
        return None


def delete_audio_file(filename):
    """
    Safely delete temporary audio file.
    """

    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError:
            pass


# ============================================================
# HEADER
# ============================================================

st.markdown(
    "<h5 class='title'>AI POWERED</h5>",
    unsafe_allow_html=True
)

st.markdown(
    "<h1 class='title'>VOICE TO DIARY</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Record your thoughts and turn them into diary entries.</p>",
    unsafe_allow_html=True
)


# ============================================================
# TABS
# ============================================================

tab1, tab2 = st.tabs(
    [
        "➕ Add Diary",
        "🔎 Search Diary"
    ]
)


# ============================================================
# ADD DIARY TAB
# ============================================================

with tab1:

    st.markdown(
        "<h3 class='title'>🎙️ RECORD YOUR VOICE</h3>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # --------------------------------------------------------
    # LANGUAGE SELECTION
    # --------------------------------------------------------

    language_name = st.selectbox(
        "Select the language you will speak",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(
            st.session_state.selected_language
        ),
        key="record_language"
    )

    st.session_state.selected_language = language_name

    whisper_language = LANGUAGES[language_name]["whisper"]

    st.info(
        f"Selected language: **{language_name}**"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # AUDIO RECORDING
    # --------------------------------------------------------

    audio_file = st.audio_input(
        "RECORD HERE",
        key=f"audio_input_{st.session_state.audio_key}"
    )

    st.markdown("---")

    if audio_file is not None:

        # Save uploaded recording temporarily
        audio_path = "audio.wav"

        with open(audio_path, "wb") as file:
            file.write(audio_file.getvalue())

        st.audio(audio_file)

        # ----------------------------------------------------
        # CLEAR AUDIO BUTTON
        # ----------------------------------------------------

        if st.button(
            "🗑️ Clear Audio",
            key=f"clear_audio_{st.session_state.audio_key}",
            width="stretch"
        ):

            delete_audio_file(audio_path)

            st.session_state.audio_key += 1
            st.session_state.edit_area = ""

            st.rerun()

        st.markdown("---")

        # ----------------------------------------------------
        # TRANSCRIBE BUTTON
        # ----------------------------------------------------

        if st.button(
            "📝 Convert to Diary",
            key="convert",
            type="primary",
            width="stretch"
        ):

            try:

                with st.spinner(
                    f"Converting your {language_name} voice to text..."
                ):

                            result=model.transcribe(
    audio_path,
    language=whisper_language,
    task="transcribe",
    fp16=False,
    temperature=0,
    condition_on_previous_text=False,
    initial_prompt=(
        f"Personal diary entry in {language_name}. "
        "Transcribe exactly what the speaker says. "
        "Do not translate."
    )
)

 transcribed_text = result["text"].strip()

                transcribed_text = result["text"].strip()

                if transcribed_text:

                    st.session_state.edit_area = transcribed_text

                    st.success(
                        "Voice converted successfully! ✅"
                    )

                else:

                    st.warning(
                        "No speech was detected in the recording."
                    )

            except Exception as error:

                st.error(
                    "Something went wrong while converting the audio."
                )

                st.exception(error)

        # ----------------------------------------------------
        # EDIT DIARY NOTE
        # ----------------------------------------------------

        if st.session_state.edit_area:

            st.markdown("---")

            st.subheader("📖 Check Your Diary Note")

            edited_text = st.text_area(
                "Your diary note",
                value=st.session_state.edit_area,
                height=250,
                key="diary_editor"
            )

            st.session_state.edit_area = edited_text

            # ------------------------------------------------
            # SAVE DIARY
            # ------------------------------------------------

            if st.button(
                "💾 Save Diary Note",
                key="save_diary",
                type="primary",
                width="stretch"
            ):

                if not edited_text.strip():

                    st.warning(
                        "Your diary note is empty."
                    )

                else:

                    today = datetime.now()

                    filename = save_diary(
                        today,
                        edited_text.strip(),
                        language_name
                    )

                    st.success(
                        f"Diary saved successfully! ✅"
                    )

                    st.info(
                        f"Date: {today.strftime('%d-%m-%y')}"
                    )

                    st.info(
                        f"Language: {language_name}"
                    )


# ============================================================
# SEARCH DIARY TAB
# ============================================================

with tab2:

    st.markdown(
        "<h2 class='title'>🔎 SEARCH DIARY</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # --------------------------------------------------------
    # DATE SELECTION
    # --------------------------------------------------------

    search_date = st.date_input(
        "Select date",
        value=datetime.now().date(),
        key="search_date"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # SEARCH BUTTON
    # --------------------------------------------------------

    if st.button(
        "🔍 Search",
        key="search",
        type="primary",
        width="stretch"
    ):

        diary_data = load_diary(search_date)

        if diary_data:

            st.session_state.diary_note = diary_data.get(
                "text",
                ""
            )

            saved_language = diary_data.get(
                "language",
                "English"
            )

            st.session_state.selected_language = saved_language

            st.session_state.selected_date = search_date

            st.success(
                "Diary note found! ✅"
            )

        else:

            st.session_state.diary_note = ""

            st.warning(
                "No diary note found for the selected date."
            )

    # --------------------------------------------------------
    # DISPLAY DIARY
    # --------------------------------------------------------

    if st.session_state.diary_note:

        st.markdown("---")

        diary_data = load_diary(search_date)

        if diary_data:

            saved_language = diary_data.get(
                "language",
                "English"
            )

        else:

            saved_language = "English"

        st.subheader(
            f"📖 Diary — {search_date.strftime('%d-%m-%y')}"
        )

        st.info(
            f"Language: **{saved_language}**"
        )

        # ----------------------------------------------------
        # EDIT LOADED DIARY
        # ----------------------------------------------------

        edited_diary = st.text_area(
            "Diary Note",
            value=st.session_state.diary_note,
            height=250,
            key="search_diary_editor"
        )

        st.session_state.diary_note = edited_diary

        st.markdown("---")

        # ----------------------------------------------------
        # SAVE CHANGES
        # ----------------------------------------------------

        if st.button(
            "💾 Save Changes",
            key="update_diary",
            width="stretch"
        ):

            save_diary(
                search_date,
                edited_diary.strip(),
                saved_language
            )

            st.success(
                "Diary updated successfully! ✅"
            )

        # ----------------------------------------------------
        # READ DIARY
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader("🔊 Listen to Your Diary")

        # Automatically use the language stored with the diary
        tts_language = LANGUAGES.get(
            saved_language,
            LANGUAGES["English"]
        )["tts"]

        st.caption(
            f"The diary will be read in {saved_language}."
        )

        if st.button(
            "🔊 Read Diary",
            key="read_diary",
            type="primary",
            width="stretch"
        ):

            if not st.session_state.diary_note.strip():

                st.warning(
                    "There is no text to read."
                )

            else:

                try:

                    with st.spinner(
                        "Generating audio..."
                    ):

                        tts = gTTS(
                            text=st.session_state.diary_note,
                            lang=tts_language,
                            slow=False
                        )

                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=".mp3"
                        ) as temp_file:

                            audio_path = temp_file.name

                        tts.save(audio_path)

                    with open(
                        audio_path,
                        "rb"
                    ) as audio_file:

                        audio_bytes = audio_file.read()

                    st.audio(
                        audio_bytes,
                        format="audio/mp3"
                    )

                    # Clean up temporary file
                    delete_audio_file(audio_path)

                except Exception as error:

                    st.error(
                        "Unable to generate the audio."
                    )

                    st.exception(error)