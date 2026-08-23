
import streamlit as st
import json
import os
import requests
from datetime import datetime


# =========================================================
# БЕТ БАПТАУ
# =========================================================

st.set_page_config(
    page_title="AI Test Maker - Оқушы",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# GOOGLE SHEETS
# =========================================================

GOOGLE_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbwgJoktoyeeNtlmFrNKWD6kTwBeDVDnKbriNrEZ0Aa_1EdaCVq4OuXs2YcigxhpQikU/"
    "exec"
)


# =========================================================
# SESSION STATE
# =========================================================

DEFAULTS = {
    "selected_grade": "",
    "selected_topic": "",
    "student_name": "",
    "test_started": False,
    "test_finished": False,
    "score": 0,
    "answers": {},
    "questions": [],
    "result_saved": False
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# СТИЛЬ
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #666;
        margin-bottom: 35px;
    }

    .student-card {
        background: #f8f9fa;
        border-radius: 18px;
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
    }

    .question-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .result-card {
        background: #f0fdf4;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        border: 2px solid #86efac;
        margin-top: 25px;
    }

    .big-score {
        font-size: 55px;
        font-weight: 800;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# JSON ФАЙЛЫН ОҚУ
# =========================================================

@st.cache_data
def load_tests():

    file_path = "tests.json"

    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    except Exception as e:
        st.error(f"tests.json файлын оқу кезінде қате шықты: {e}")
        return {}


tests_data = load_tests()


# =========================================================
# ТЕСТ ҚҰРЫЛЫМЫН ТҮСІНУ
# =========================================================

def get_grades(data):

    grades = []

    if isinstance(data, dict):

        for key, value in data.items():

            # Мысалы:
            # "5": {...}
            # "6": {...}

            if isinstance(value, dict):

                grade = str(key)

                if grade not in grades:
                    grades.append(grade)

    return grades


def get_topics(data, grade):

    topics = []

    if not isinstance(data, dict):
        return topics

    grade_data = data.get(grade)

    if not isinstance(grade_data, dict):
        return topics

    for topic, topic_data in grade_data.items():

        if isinstance(topic_data, dict):
            topics.append(topic)

    return topics


def get_questions(data, grade, topic):

    if not isinstance(data, dict):
        return []

    grade_data = data.get(grade)

    if not isinstance(grade_data, dict):
        return []

    topic_data = grade_data.get(topic)

    if not isinstance(topic_data, dict):
        return []

    questions = topic_data.get("questions", [])

    if not isinstance(questions, list):
        return []

    return questions


# =========================================================
# GOOGLE SHEETS-ке НӘТИЖЕ ЖІБЕРУ
# =========================================================

def save_result_to_google_sheets(
    student_name,
    grade,
    topic,
    score,
    total_questions
):

    try:

        if total_questions == 0:
            percent = 0
        else:
            percent = round(
                score / total_questions * 100,
                1
            )

        data = {
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "student": student_name,
            "grade": grade,
            "topic": topic,
            "correct": score,
            "total": total_questions,
            "percent": percent
        }

        response = requests.post(
            GOOGLE_SCRIPT_URL,
            json=data,
            timeout=15
        )

        if response.status_code == 200:
            return True

        return False

    except Exception:
        return False


# =========================================================
# БАСТЫ ТАҚЫРЫП
# =========================================================

st.markdown(
    '<div class="main-title">🎓 AI Test Maker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Оқушыға арналған тест жүйесі</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# НӘТИЖЕ ШЫҚҚАННАН КЕЙІН
# =========================================================

if st.session_state.test_finished:

    score = st.session_state.score
    questions = st.session_state.questions

    total = len(questions)

    if total > 0:
        percent = round(score / total * 100)
    else:
        percent = 0

    st.success("🎉 Тест аяқталды!")

    st.markdown(
        f"""
        <div class="result-card">

        <div style="font-size:24px;">
        👤 {st.session_state.student_name}
        </div>

        <div style="font-size:20px; margin-top:10px;">
        🎒 {st.session_state.selected_grade}-сынып
        </div>

        <div style="font-size:20px; margin-top:5px;">
        📚 {st.session_state.selected_topic}
        </div>

        <div class="big-score">
        {score} / {total}
        </div>

        <div style="font-size:30px; font-weight:700;">
        {percent}%
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if percent >= 90:
        st.balloons()
        st.success("🏆 Өте жақсы нәтиже!")

    elif percent >= 70:
        st.success("👏 Жақсы нәтиже!")

    elif percent >= 50:
        st.warning("👍 Жаман емес. Тағы да қайталап көріңіз.")

    else:
        st.error("📚 Тақырыпты қайта қарап шыққаныңыз дұрыс.")

    st.write("")

    if not st.session_state.result_saved:

        saved = save_result_to_google_sheets(
            st.session_state.student_name,
            st.session_state.selected_grade,
            st.session_state.selected_topic,
            score,
            total
        )

        if saved:
            st.session_state.result_saved = True
            st.success("✅ Нәтиже мұғалімнің нәтижелер кестесіне сақталды.")

        else:
            st.warning(
                "⚠️ Нәтиже кестеге жіберілмеді. "
                "Бірақ тест нәтижесі экранда сақталды."
            )

    else:
        st.success("☁️ Нәтиже Google Sheets-те сақталған.")

    st.write("")

    if st.button(
        "🔄 Жаңа тест бастау",
        use_container_width=True
    ):

        st.session_state.selected_grade = ""
        st.session_state.selected_topic = ""
        st.session_state.student_name = ""
        st.session_state.test_started = False
        st.session_state.test_finished = False
        st.session_state.score = 0
        st.session_state.answers = {}
        st.session_state.questions = []
        st.session_state.result_saved = False

        st.rerun()

    st.stop()


# =========================================================
# СЫНЫПТАРДЫ АЛУ
# =========================================================

grades = get_grades(tests_data)


if not grades:

    st.error("❌ tests.json файлынан сыныптар табылмады.")

    st.info(
        'Әр тесттің ішінде "grade": "5" сияқты сынып көрсетілуі керек.'
    )

    st.stop()


# =========================================================
# ОҚУШЫ АҚПАРАТЫ
# =========================================================

st.markdown("### 👤 Оқушы туралы ақпарат")

student_name = st.text_input(
    "Оқушының аты-жөні:",
    value=st.session_state.student_name,
    placeholder="Мысалы: Айдана Ермекова"
)

st.session_state.student_name = student_name


# =========================================================
# СЫНЫП ТАҢДАУ
# =========================================================

st.markdown("### 🎒 Сыныбыңызды таңдаңыз")

grade_options = ["-- Сыныпты таңдаңыз --"] + grades

selected_grade = st.selectbox(
    "Сынып:",
    grade_options,
    key="selected_grade_box"
)

if selected_grade == "-- Сыныпты таңдаңыз --":

    st.session_state.selected_grade = ""

else:

    st.session_state.selected_grade = selected_grade


# =========================================================
# ТАҚЫРЫП ТАҢДАУ
# =========================================================

if st.session_state.selected_grade:

    topics = get_topics(
        tests_data,
        st.session_state.selected_grade
    )

    st.markdown("### 📚 Тақырыпты таңдаңыз")

    if not topics:

        st.warning(
            "⚠️ Бұл сыныпқа арналған тақырыптар табылмады."
        )

        st.stop()

    topic_options = ["-- Тақырыпты таңдаңыз --"] + topics

    selected_topic = st.selectbox(
        "Тақырып:",
        topic_options,
        key="selected_topic_box"
    )

    if selected_topic == "-- Тақырыпты таңдаңыз --":

        st.session_state.selected_topic = ""

    else:

        st.session_state.selected_topic = selected_topic


# =========================================================
# ТЕСТТІ БАСТАУ
# =========================================================

st.write("")

if st.button(
    "▶️ Тестті бастау",
    use_container_width=True,
    type="primary"
):

    if not st.session_state.student_name.strip():

        st.warning(
            "⚠️ Алдымен оқушының аты-жөнін енгізіңіз."
        )

        st.stop()

    if not st.session_state.selected_grade:

        st.warning(
            "⚠️ Алдымен сыныпты таңдаңыз."
        )

        st.stop()

    if not st.session_state.selected_topic:

        st.warning(
            "⚠️ Алдымен тақырыпты таңдаңыз."
        )

        st.stop()

    questions = get_questions(
        tests_data,
        st.session_state.selected_grade,
        st.session_state.selected_topic
    )

    if not questions:

        st.error(
            "❌ Бұл тақырып бойынша сұрақтар табылмады."
        )

        st.stop()

    st.session_state.questions = questions
    st.session_state.answers = {}
    st.session_state.score = 0
    st.session_state.test_started = True
    st.session_state.test_finished = False
    st.session_state.result_saved = False

    st.rerun()


# =========================================================
# ТЕСТ СҰРАҚТАРЫ
# =========================================================

if st.session_state.test_started:

    questions = st.session_state.questions

    st.divider()

    st.markdown(
        f"""
        ### 📝 Тест

        *Сынып:* {st.session_state.selected_grade}

        *Тақырып:* {st.session_state.selected_topic}

        *Оқушы:* {st.session_state.student_name}

        *Сұрақ саны:* {len(questions)}
        """
    )

    st.write("")

    with st.form("test_form"):

        answers = {}

        for index, question_data in enumerate(questions):

            question_text = question_data.get(
                "question",
                f"{index + 1}-сұрақ"
            )

            options = question_data.get(
                "options",
                {}
            )

            st.markdown(
                f"""
                <div class="question-card">

                <b>{index + 1}. {question_text}</b>

                </div>
                """,
                unsafe_allow_html=True
            )

            if isinstance(options, dict):

                option_keys = list(options.keys())

                option_labels = [
                    f"{key}) {options[key]}"
                    for key in option_keys
                ]

                selected_option = st.radio(
                    "Жауабыңызды таңдаңыз:",
                    option_labels,
                    key=f"question_{index}",
                    index=None
                )

                answers[index] = selected_option

            elif isinstance(options, list):

                selected_option = st.radio(
                    "Жауабыңызды таңдаңыз:",
                    options,
                    key=f"question_{index}",
                    index=None
                )

                answers[index] = selected_option

        st.write("")

        submit_test = st.form_submit_button(
            "✅ Тестті аяқтау",
            use_container_width=True,
            type="primary"
        )


    # =====================================================
    # ТЕСТ НӘТИЖЕСІН ЕСЕПТЕУ
    # =====================================================

    if submit_test:

        score = 0

        unanswered = 0

        for index, question_data in enumerate(questions):

            selected = answers.get(index)

            if selected is None:
                unanswered += 1
                continue

            correct_answer = question_data.get(
                "answer",
                ""
            )

            # ---------------------------------------------
            # Егер жауап A/B/C/D форматында болса
            # ---------------------------------------------

            if isinstance(selected, str):

                selected_key = selected[:1].upper()

                correct_key = str(
                    correct_answer
                ).strip().upper()

                if selected_key == correct_key:
                    score += 1

        # ---------------------------------------------
        # Жауаптарды сақтау
        # ---------------------------------------------

        st.session_state.answers = answers
        st.session_state.score = score

        st.session_state.test_started = False
        st.session_state.test_finished = True

        st.rerun()
