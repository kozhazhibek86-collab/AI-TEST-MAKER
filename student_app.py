import streamlit as st
import json
import os
import requests

# ============================================================
# GOOGLE SHEETS WEB APP
# ============================================================

GOOGLE_SHEETS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbwgJoktoyeeNtlmFrNKWD6kTwBeDVDnKbriNrEZ0Aa_1EdaCVq4OuXs2YcigxhpQikU/"
    "exec"
)


# ============================================================
# БЕТ БАПТАУ
# ============================================================

st.set_page_config(
    page_title="AI Test Maker - Оқушы",
    page_icon="🎓",
    layout="centered"
)


# ============================================================
# СТИЛЬ
# ============================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 25px;
}

.question-box {
    background-color: #f5f7fa;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.result-box {
    background-color: #f0f8ff;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TESTS.JSON ЖҮКТЕУ
# ============================================================

def load_tests():

    file_path = "tests.json"

    if not os.path.exists(file_path):

        st.error(
            "❌ tests.json файлы табылмады!"
        )

        st.info(
            "student_app.py және tests.json "
            "бір репозиторийде болуы керек."
        )

        st.stop()

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except json.JSONDecodeError:

        st.error(
            "❌ tests.json ішінде қате бар."
        )

        st.stop()

    except Exception as e:

        st.error(
            f"❌ tests.json оқу қатесі: {e}"
        )

        st.stop()


tests = load_tests()


# ============================================================
# СЫНЫПТАРДЫ АНЫҚТАУ
# ============================================================

grades = []

for key in tests.keys():

    if str(key).strip().isdigit():

        grades.append(str(key))


grades = sorted(
    grades,
    key=lambda x: int(x)
)


if not grades:

    st.error(
        "❌ tests.json файлынан сыныптар табылмады."
    )

    st.stop()


# ============================================================
# БАСТЫ БЕТ
# ============================================================

st.markdown(
    '<div class="main-title">🎓 AI Test Maker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Оқушыға арналған тест жүйесі</div>',
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "test_started" not in st.session_state:
    st.session_state.test_started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "saved_to_sheets" not in st.session_state:
    st.session_state.saved_to_sheets = False


# ============================================================
# СЫНЫП ТАҢДАУ
# ============================================================

if not st.session_state.test_started:

    grade_options = [
        "— Сыныпты таңдаңыз —"
    ] + grades

    selected_grade = st.selectbox(
        "🏫 Сыныбыңызды таңдаңыз:",
        grade_options
    )

    if selected_grade == "— Сыныпты таңдаңыз —":

        st.info(
            "☝️ Алдымен сыныпты таңдаңыз."
        )

        st.stop()


    # ========================================================
    # ТАҢДАЛҒАН СЫНЫПТЫҢ ТАҚЫРЫПТАРЫ
    # ========================================================

    class_data = tests[selected_grade]

    if not isinstance(class_data, dict):

        st.error(
            "❌ Таңдалған сыныптың деректері дұрыс емес."
        )

        st.stop()


    topics = []

    for topic_name, topic_data in class_data.items():

        if isinstance(topic_data, dict):

            if topic_name not in [
                "grade",
                "subject"
            ]:

                topics.append(topic_name)


    if not topics:

        st.warning(
            "⚠️ Бұл сыныпта тест тақырыптары жоқ."
        )

        st.stop()


    # ========================================================
    # ТАҚЫРЫП ТАҢДАУ
    # ========================================================

    topic_options = [
        "— Тақырыпты таңдаңыз —"
    ] + topics

    selected_topic = st.selectbox(
        "📚 Тақырыпты таңдаңыз:",
        topic_options
    )


    if selected_topic == "— Тақырыпты таңдаңыз —":

        st.info(
            "☝️ Тақырыпты таңдаңыз."
        )

        st.stop()


    # ========================================================
    # ТЕСТ АҚПАРАТЫ
    # ========================================================

    test = class_data[selected_topic]

    subject = test.get(
        "subject",
        "Информатика"
    )

    questions = test.get(
        "questions",
        []
    )


    st.info(
        f"""
📚 Пән: **{subject}**

🏫 Сынып: **{selected_grade}**

📖 Тақырып: **{selected_topic}**

📝 Сұрақ саны: **{len(questions)}**
"""
    )


    # ========================================================
    # ОҚУШЫ АТЫ
    # ========================================================

    student_name = st.text_input(
        "👤 Оқушының аты-жөні:",
        placeholder="Аты-жөніңізді енгізіңіз"
    )


    # ========================================================
    # ТЕСТ БАСТАУ
    # ========================================================

    if st.button(
        "▶️ Тестті бастау",
        use_container_width=True
    ):

        if student_name.strip() == "":

            st.warning(
                "⚠️ Алдымен аты-жөніңізді енгізіңіз."
            )

        else:

            st.session_state.student_name = (
                student_name.strip()
            )

            st.session_state.selected_grade = (
                selected_grade
            )

            st.session_state.selected_topic = (
                selected_topic
            )

            st.session_state.test_started = True

            st.session_state.finished = False

            st.session_state.answers = {}

            st.session_state.saved_to_sheets = False

            st.rerun()


# ============================================================
# ТЕСТ БАСТАЛҒАН КЕЗ
# ============================================================

if (
    st.session_state.test_started
    and not st.session_state.finished
):

    selected_grade = (
        st.session_state.selected_grade
    )

    selected_topic = (
        st.session_state.selected_topic
    )

    student_name = (
        st.session_state.student_name
    )

    class_data = tests[selected_grade]

    test = class_data[selected_topic]

    questions = test.get(
        "questions",
        []
    )


    st.markdown("---")

    st.subheader(
        f"👤 Оқушы: {student_name}"
    )

    st.write(
        f"🏫 Сынып: **{selected_grade}**"
    )

    st.write(
        f"📚 Тақырып: **{selected_topic}**"
    )

    st.markdown("---")


    # ========================================================
    # СҰРАҚТАР
    # ========================================================

    for i, question_data in enumerate(
        questions
    ):

        question_text = question_data.get(
            "question",
            f"{i + 1}-сұрақ"
        )

        options_data = question_data.get(
            "options",
            {}
        )


        # ----------------------------------------------------
        # ВАРИАНТТАР
        # ----------------------------------------------------

        if isinstance(
            options_data,
            dict
        ):

            option_keys = list(
                options_data.keys()
            )

            option_values = []

            for key in option_keys:

                option_values.append(
                    f"{key}) {options_data[key]}"
                )


        elif isinstance(
            options_data,
            list
        ):

            option_keys = []

            option_values = []

            for j, value in enumerate(
                options_data
            ):

                letter = chr(65 + j)

                option_keys.append(
                    letter
                )

                option_values.append(
                    f"{letter}) {value}"
                )


        else:

            option_keys = []

            option_values = []


        st.markdown(
            f"""
            <div class="question-box">
                <b>{i + 1}. {question_text}</b>
            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # БОС НҰСҚА
        # ----------------------------------------------------

        choices = [
            "— Жауапты таңдаңыз —"
        ] + option_values


        selected_answer = st.radio(
            "Жауап:",
            choices,
            key=f"question_{i}",
            index=0
        )


        # ----------------------------------------------------
        # ЖАУАПТЫ САҚТАУ
        # ----------------------------------------------------

        if (
            selected_answer
            != "— Жауапты таңдаңыз —"
        ):

            selected_letter = (
                selected_answer
                .split(")")[0]
                .strip()
                .upper()
            )

            st.session_state.answers[i] = (
                selected_letter
            )

        else:

            if i in st.session_state.answers:

                del st.session_state.answers[i]


        st.markdown("---")


    # ========================================================
    # ЖАУАП САНЫ
    # ========================================================

    answered_count = len(
        st.session_state.answers
    )

    st.write(
        f"📊 Жауап берілді: "
        f"**{answered_count} / {len(questions)}**"
    )


    # ========================================================
    # ТЕСТІ АЯҚТАУ
    # ========================================================

    if st.button(
        "✅ Тестті аяқтау",
        use_container_width=True
    ):

        if answered_count < len(questions):

            unanswered = []

            for i in range(
                len(questions)
            ):

                if i not in st.session_state.answers:

                    unanswered.append(
                        i + 1
                    )

            st.warning(
                "⚠️ Барлық сұрақтарға жауап беріңіз.\n\n"
                "Жауап берілмеген сұрақтар: "
                + ", ".join(
                    map(
                        str,
                        unanswered
                    )
                )
            )

        else:

            st.session_state.finished = True

            st.rerun()


# ============================================================
# НӘТИЖЕ
# ============================================================

if st.session_state.finished:

    selected_grade = (
        st.session_state.selected_grade
    )

    selected_topic = (
        st.session_state.selected_topic
    )

    student_name = (
        st.session_state.student_name
    )

    class_data = tests[selected_grade]

    test = class_data[selected_topic]

    questions = test.get(
        "questions",
        []
    )


    # ========================================================
    # ҰПАЙ
    # ========================================================

    score = 0

    total = len(questions)


    for i, question_data in enumerate(
        questions
    ):

        correct_answer = str(
            question_data.get(
                "answer",
                ""
            )
        ).strip().upper()


        student_answer = str(
            st.session_state.answers.get(
                i,
                ""
            )
        ).strip().upper()


        if student_answer == correct_answer:

            score += 1


    # ========================================================
    # ПАЙЫЗ
    # ========================================================

    if total > 0:

        percentage = round(
            score / total * 100
        )

    else:

        percentage = 0


    # ========================================================
    # БАҒА
    # ========================================================

    if percentage >= 90:

        grade_mark = 5

    elif percentage >= 70:

        grade_mark = 4

    elif percentage >= 50:

        grade_mark = 3

    else:

        grade_mark = 2


    # ========================================================
    # НӘТИЖЕНІ КӨРСЕТУ
    # ========================================================

    st.markdown("---")

    st.markdown(
        f"""
        <div class="result-box">

        <h2>🎉 Тест аяқталды!</h2>

        <h3>👤 {student_name}</h3>

        <p>
        🏫 Сынып:
        <b>{selected_grade}</b>
        </p>

        <p>
        📚 Тақырып:
        <b>{selected_topic}</b>
        </p>

        <p>
        ✅ Дұрыс жауап:
        <b>{score}/{total}</b>
        </p>

        <p>
        📊 Нәтиже:
        <b>{percentage}%</b>
        </p>

        <p>
        🏆 Баға:
        <b>{grade_mark}</b>
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    if percentage >= 90:

        st.success(
            "🏆 Өте жақсы!"
        )

    elif percentage >= 70:

        st.info(
            "👍 Жақсы нәтиже!"
        )

    elif percentage >= 50:

        st.warning(
            "🙂 Қанағаттанарлық."
        )

    else:

        st.error(
            "📚 Тақырыпты қайта қарау қажет."
        )


    # ========================================================
    # GOOGLE SHEETS-КЕ ЖІБЕРУ
    # ========================================================

    if not st.session_state.saved_to_sheets:

        result_data = {

            "student": student_name,

            "grade": selected_grade,

            "topic": selected_topic,

            "score": score,

            "total": total,

            "percentage": percentage

        }


        try:

            response = requests.post(
                GOOGLE_SHEETS_URL,
                json=result_data,
                timeout=15
            )


            if response.status_code == 200:

                try:

                    response_data = (
                        response.json()
                    )

                    if response_data.get(
                        "success",
                        False
                    ):

                        st.session_state.saved_to_sheets = True

                        st.success(
                            "☁️ Нәтиже мұғалімге жіберілді."
                        )

                    else:

                        st.warning(
                            "⚠️ Нәтиже жіберілді, "
                            "бірақ сервер жауабын тексеру қажет."
                        )

                except Exception:

                    st.session_state.saved_to_sheets = True

                    st.success(
                        "☁️ Нәтиже жіберілді."
                    )

            else:

                st.error(
                    "❌ Нәтижені Google Sheets-ке "
                    "жіберу кезінде қате шықты."
                )


        except Exception as e:

            st.error(
                f"❌ Интернет/сервер қатесі: {e}"
            )


    # ========================================================
    # ЖАУАПТАРДЫ ТЕКСЕРУ
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📋 Жауаптарды тексеру"
    )


    for i, question_data in enumerate(
        questions
    ):

        correct_answer = str(
            question_data.get(
                "answer",
                ""
            )
        ).strip().upper()


        student_answer = str(
            st.session_state.answers.get(
                i,
                ""
            )
        ).strip().upper()


        if student_answer == correct_answer:

            st.success(
                f"№{i + 1} — Дұрыс ✅"
            )

        else:

            st.error(
                f"""
№{i + 1} — Қате ❌

Сіздің жауабыңыз: **{student_answer}**

Дұрыс жауап: **{correct_answer}**
"""
            )


    # ========================================================
    # ҚАЙТА БАСТАУ
    # ========================================================

    st.markdown("---")

    if st.button(
        "🔄 Басқа тестті тапсыру",
        use_container_width=True
    ):

        st.session_state.test_started = False

        st.session_state.finished = False

        st.session_state.answers = {}

        st.session_state.saved_to_sheets = False

        st.rerun()

