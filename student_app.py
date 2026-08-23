import streamlit as st
import json
import os

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
    margin-top: 15px;
    margin-bottom: 10px;
    font-size: 18px;
}

.result-box {
    padding: 25px;
    border-radius: 15px;
    background-color: #f0f8ff;
    margin-top: 20px;
    text-align: center;
}

.big-score {
    font-size: 42px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TESTS.JSON ФАЙЛЫН ОҚУ
# ============================================================

def load_tests():

    file_path = "tests.json"

    if not os.path.exists(file_path):

        st.error("❌ tests.json файлы табылмады!")

        st.info(
            "GitHub-та student_app.py және tests.json "
            "бір папкада болуы керек."
        )

        return {}

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except json.JSONDecodeError:

        st.error(
            "❌ tests.json ішінде JSON қатесі бар."
        )

        return {}

    except Exception as e:

        st.error(
            f"❌ Файлды оқу қатесі: {e}"
        )

        return {}


# ============================================================
# ДЕРЕКТЕР
# ============================================================

tests_data = load_tests()

if not tests_data:
    st.stop()


# ============================================================
# ТАҚЫРЫПТАРДЫ ДАЙЫНДАУ
# ============================================================

all_tests = []

for topic_name, test_data in tests_data.items():

    if not isinstance(test_data, dict):
        continue

    grade = str(
        test_data.get("grade", "")
    ).strip()

    subject = test_data.get(
        "subject",
        "Информатика"
    )

    questions = test_data.get(
        "questions",
        []
    )

    all_tests.append({
        "topic": topic_name,
        "grade": grade,
        "subject": subject,
        "questions": questions
    })


if not all_tests:

    st.error(
        "❌ tests.json ішінде тесттер табылмады."
    )

    st.stop()


# ============================================================
# ТАҚЫРЫПТАРДЫҢ СЫНЫПТАРЫН АНЫҚТАУ
# ============================================================

grades = []

for test in all_tests:

    grade = test["grade"]

    if grade and grade not in grades:
        grades.append(grade)


# Сыныптарды реттеу
def grade_sort_key(value):

    try:
        return int(
            ''.join(
                ch for ch in value
                if ch.isdigit()
            )
        )

    except:
        return 999


grades = sorted(
    grades,
    key=grade_sort_key
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

if "selected_grade" not in st.session_state:
    st.session_state.selected_grade = ""

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""

if "student_name" not in st.session_state:
    st.session_state.student_name = ""


# ============================================================
# ТАҚЫРЫП ТАҢДАУ БӨЛІМІ
# ============================================================

if not st.session_state.test_started:

    st.markdown(
        '<div class="main-title">🎓 AI Test Maker</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'Оқушыға арналған тест жүйесі'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ========================================================
    # СЫНЫП
    # ========================================================

    grade_options = [
        "-- Сыныпты таңдаңыз --"
    ] + grades

    selected_grade = st.selectbox(
        "🏫 Сыныбыңызды таңдаңыз:",
        grade_options
    )


    # ========================================================
    # ТАҚЫРЫП
    # ========================================================

    if selected_grade != "-- Сыныпты таңдаңыз --":

        available_topics = []

        for test in all_tests:

            if test["grade"] == selected_grade:

                available_topics.append(
                    test["topic"]
                )


        if available_topics:

            topic_options = [
                "-- Тақырыпты таңдаңыз --"
            ] + available_topics

            selected_topic = st.selectbox(
                "📚 Тест тақырыбын таңдаңыз:",
                topic_options
            )

        else:

            selected_topic = (
                "-- Тақырып табылмады --"
            )

            st.warning(
                "⚠️ Бұл сыныпқа тест тақырыбы "
                "әлі қосылмаған."
            )

    else:

        selected_topic = (
            "-- Алдымен сыныпты таңдаңыз --"
        )


    # ========================================================
    # ТАҢДАЛҒАН ТЕСТ ТУРАЛЫ
    # ========================================================

    selected_test = None

    if (
        selected_grade != "-- Сыныпты таңдаңыз --"
        and
        selected_topic != "-- Тақырыпты таңдаңыз --"
        and
        selected_topic != "-- Тақырып табылмады --"
    ):

        for test in all_tests:

            if (
                test["grade"] == selected_grade
                and
                test["topic"] == selected_topic
            ):

                selected_test = test
                break


    if selected_test:

        st.info(
            f"📚 Пән: *{selected_test['subject']}*\n\n"
            f"🏫 Сынып: *{selected_test['grade']}*\n\n"
            f"📖 Тақырып: *{selected_test['topic']}*\n\n"
            f"📝 Сұрақ саны: "
            f"*{len(selected_test['questions'])}*"
        )


    # ========================================================
    # ОҚУШЫ АТЫ
    # ========================================================

    student_name = st.text_input(
        "👤 Аты-жөніңіз:",
        placeholder="Аты-жөніңізді енгізіңіз"
    )


    # ========================================================
    # ТЕСТТІ БАСТАУ
    # ========================================================

    if st.button(
        "▶️ Тестті бастау",
        use_container_width=True
    ):

        if selected_grade == "-- Сыныпты таңдаңыз --":

            st.warning(
                "⚠️ Алдымен сыныпты таңдаңыз."
            )

        elif selected_topic in [
            "-- Тақырыпты таңдаңыз --",
            "-- Тақырып табылмады --"
        ]:

            st.warning(
                "⚠️ Тақырыпты таңдаңыз."
            )

        elif not student_name.strip():

            st.warning(
                "⚠️ Аты-жөніңізді енгізіңіз."
            )

        elif selected_test is None:

            st.error(
                "❌ Тест табылмады."
            )

        else:

            st.session_state.selected_grade = (
                selected_grade
            )

            st.session_state.selected_topic = (
                selected_topic
            )

            st.session_state.student_name = (
                student_name.strip()
            )

            st.session_state.test_started = True

            st.session_state.finished = False

            st.session_state.answers = {}

            st.rerun()


# ============================================================
# ТЕСТТІ ТАБУ
# ============================================================

current_test = None

if st.session_state.test_started:

    for test in all_tests:

        if (
            test["grade"]
            == st.session_state.selected_grade
            and
            test["topic"]
            == st.session_state.selected_topic
        ):

            current_test = test
            break


if (
    st.session_state.test_started
    and
    not st.session_state.finished
    and
    current_test
):

    questions = current_test["questions"]


    # ========================================================
    # ТЕСТ БАСЫ
    # ========================================================

    st.markdown(
        '<div class="main-title">📝 AI Test Maker</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'Тест тапсырмасы'
        '</div>',
        unsafe_allow_html=True
    )

    st.success(
        f"👤 Оқушы: "
        f"*{st.session_state.student_name}*"
    )

    st.info(
        f"🏫 Сынып: *{st.session_state.selected_grade}*  \n"
        f"📚 Тақырып: *{st.session_state.selected_topic}*"
    )

    st.markdown("---")


    # ========================================================
    # СҰРАҚТАР
    # ========================================================

    for i, question_data in enumerate(questions):

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

                key = chr(
                    65 + j
                )

                option_keys.append(key)

                option_values.append(
                    f"{key}) {value}"
                )

        else:

            option_keys = []

            option_values = []


        # ----------------------------------------------------
        # СҰРАҚ
        # ----------------------------------------------------

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
            "-- Жауапты таңдаңыз --"
        ] + option_values


        selected = st.radio(
            "Жауабыңыз:",
            choices,
            key=f"question_{i}",
            index=0
        )


        # ----------------------------------------------------
        # ЖАУАПТЫ САҚТАУ
        # ----------------------------------------------------

        if (
            selected
            !=
            "-- Жауапты таңдаңыз --"
        ):

            selected_letter = (
                selected.split(")")[0]
            )

            st.session_state.answers[i] = (
                selected_letter
            )

        else:

            if i in st.session_state.answers:

                del st.session_state.answers[i]


        st.markdown("---")


    # ========================================================
    # ПРОГРЕСС
    # ========================================================

    answered_count = len(
        st.session_state.answers
    )

    total_questions = len(
        questions
    )

    st.write(
        f"📊 Жауап берілді: "
        f"*{answered_count} / {total_questions}*"
    )


    progress = 0

    if total_questions > 0:

        progress = (
            answered_count
            /
            total_questions
        )

    st.progress(progress)


    # ========================================================
    # ТЕСТІ АЯҚТАУ
    # ========================================================

    if st.button(
        "✅ Тестті аяқтау",
        use_container_width=True
    ):

        if answered_count < total_questions:

            unanswered = []

            for i in range(
                total_questions
            ):

                if (
                    i
                    not in
                    st.session_state.answers
                ):

                    unanswered.append(
                        i + 1
                    )


            st.warning(
                "⚠️ Барлық сұрақтарға "
                "жауап беріңіз.\n\n"
                "Жауап берілмеген сұрақтар: "
                +
                ", ".join(
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

if (
    st.session_state.finished
    and
    current_test
):

    questions = current_test["questions"]

    score = 0

    total = len(questions)

    results = []


    # ========================================================
    # ЖАУАПТАРДЫ ТЕКСЕРУ
    # ========================================================

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


        is_correct = (
            student_answer
            ==
            correct_answer
        )


        if is_correct:

            score += 1


        results.append({

            "question":
                question_data.get(
                    "question",
                    ""
                ),

            "student_answer":
                student_answer,

            "correct_answer":
                correct_answer,

            "is_correct":
                is_correct

        })


    # ========================================================
    # ПАЙЫЗ
    # ========================================================

    percentage = 0

    if total > 0:

        percentage = round(
            score
            /
            total
            *
            100
        )


    # ========================================================
    # НӘТИЖЕ
    # ========================================================

    st.markdown(
        '<div class="main-title">'
        '🎉 Тест аяқталды!'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="result-box">

            <h2>📊 Нәтиже</h2>

            <h3>
                👤 {st.session_state.student_name}
            </h3>

            <p>
                🏫 Сынып:
                <b>
                {st.session_state.selected_grade}
                </b>
            </p>

            <p>
                📚 Тақырып:
                <b>
                {st.session_state.selected_topic}
                </b>
            </p>

            <div class="big-score">
                {score} / {total}
            </div>

            <p>
                Нәтиже:
                <b>{percentage}%</b>
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # БАҒА
    # ========================================================

    if percentage >= 90:

        st.success(
            "🏆 Өте жақсы! Баға: 5"
        )

    elif percentage >= 70:

        st.info(
            "👍 Жақсы! Баға: 4"
        )

    elif percentage >= 50:

        st.warning(
            "🙂 Қанағаттанарлық. Баға: 3"
        )

    else:

        st.error(
            "📚 Тақырыпты қайта қарау қажет. "
            "Баға: 2"
        )


    # ========================================================
    # ЖАУАПТАРДЫ ТЕКСЕРУ
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📋 Жауаптарды тексеру"
    )


    for i, result in enumerate(
        results
    ):

        if result["is_correct"]:

            st.success(
                f"№{i + 1} — "
                f"Дұрыс жауап ✅"
            )

        else:

            st.error(
                f"№{i + 1} — "
                f"Қате ❌\n\n"
                f"Сіздің жауабыңыз: "
                f"{result['student_answer']}\n\n"
                f"Дұрыс жауап: "
                f"{result['correct_answer']}"
            )


    # ========================================================
    # ҚАЙТА ТАПСЫРУ
    # ========================================================

    st.markdown("---")

    if st.button(
        "🔄 Басқа тест тапсыру",
        use_container_width=True
    ):

        st.session_state.test_started = False

        st.session_state.finished = False

        st.session_state.answers = {}

        st.session_state.selected_grade = ""

        st.session_state.selected_topic = ""

        st.session_state.student_name = ""

        st.rerun()
