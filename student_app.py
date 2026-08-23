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
    margin-top: 10px;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.question-box {
    background-color: #f5f7fa;
    padding: 18px;
    border-radius: 12px;
    margin-top: 10px;
    margin-bottom: 10px;
}

.result-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #f0f8ff;
    margin-top: 20px;
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
            "GitHub репозиторийде student_app.py және "
            "tests.json файлдары бір папкада болуы керек."
        )

        return {}

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data

    except json.JSONDecodeError:

        st.error("❌ tests.json ішінде қате бар.")

        return {}

    except Exception as e:

        st.error(
            f"❌ Файлды оқу кезінде қате шықты: {e}"
        )

        return {}


# ============================================================
# ТЕСТТЕРДІ ЖҮКТЕУ
# ============================================================

tests_data = load_tests()

if not tests_data:
    st.stop()


# ============================================================
# ТАҚЫРЫПТАРДАН СЫНЫПТАРДЫ АВТОМАТТЫ ЖИНАУ
# ============================================================

grades = []

for topic_name, test_data in tests_data.items():

    if isinstance(test_data, dict):

        grade = test_data.get("grade", "")

        if grade:

            grade = str(grade).strip()

            if grade not in grades:

                grades.append(grade)


# Сыныптарды реттеу

def grade_sort_key(value):

    try:
        return int(value)
    except:
        return 999


grades = sorted(
    grades,
    key=grade_sort_key
)


# ============================================================
# ТАҚЫРЫПТАРДЫҢ СЫНЫПТАРЫ ТАБЫЛМАСА
# ============================================================

if not grades:

    st.error(
        "❌ tests.json файлынан сыныптар табылмады."
    )

    st.info(
        'Әр тесттің ішінде "grade": "5" сияқты сынып көрсетілуі керек.'
    )

    st.stop()


# ============================================================
# БАС ТАҚЫРЫП
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
# СЫНЫП ТАҢДАУ
# ============================================================

st.markdown(
    "### 🏫 Сыныбыңызды таңдаңыз:"
)

grade_options = [
    "-- Сыныпты таңдаңыз --"
] + grades

selected_grade = st.selectbox(
    "Сынып",
    grade_options,
    key="student_grade"
)


# ============================================================
# СЫНЫП ТАҢДАЛМАСА
# ============================================================

if selected_grade == "-- Сыныпты таңдаңыз --":

    st.warning(
        "⚠️ Алдымен сыныпты таңдаңыз."
    )

    st.stop()


# ============================================================
# ТАҢДАЛҒАН СЫНЫПҚА ТИЕСІЛІ ТАҚЫРЫПТАР
# ============================================================

available_topics = []

for topic_name, test_data in tests_data.items():

    if not isinstance(test_data, dict):
        continue

    test_grade = str(
        test_data.get("grade", "")
    ).strip()

    if test_grade == str(selected_grade):

        available_topics.append(topic_name)


# ============================================================
# ТАҚЫРЫП ЖОҚ БОЛСА
# ============================================================

if not available_topics:

    st.warning(
        f"⚠️ {selected_grade}-сыныпқа арналған тесттер табылмады."
    )

    st.stop()


# ============================================================
# ТАҚЫРЫП ТАҢДАУ
# ============================================================

st.markdown(
    "### 📚 Тест тақырыбын таңдаңыз:"
)

topic_options = [
    "-- Тақырыпты таңдаңыз --"
] + available_topics

selected_topic = st.selectbox(
    "Тақырып",
    topic_options,
    key=f"student_topic_{selected_grade}"
)


# ============================================================
# ТАҚЫРЫП ТАҢДАЛМАСА
# ============================================================

if selected_topic == "-- Тақырыпты таңдаңыз --":

    st.info(
        "📚 Тестті бастау үшін алдымен тақырыпты таңдаңыз."
    )

    st.stop()


# ============================================================
# ТАҢДАЛҒАН ТЕСТ
# ============================================================

test = tests_data[selected_topic]

subject = test.get(
    "subject",
    "Информатика"
)

grade = test.get(
    "grade",
    selected_grade
)

questions = test.get(
    "questions",
    []
)


# ============================================================
# ТЕСТ АҚПАРАТЫ
# ============================================================

st.info(
    f"""
📚 *Пән:* {subject}

🎓 *Сынып:* {grade}

📖 *Тақырып:* {selected_topic}

📝 *Сұрақ саны:* {len(questions)}
"""
)


# ============================================================
# ОҚУШЫНЫҢ АТЫ
# ============================================================

student_name = st.text_input(
    "👤 Оқушының аты-жөні:",
    placeholder="Аты-жөніңізді енгізіңіз",
    key="student_name"
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


# ============================================================
# ТЕСТТІ БАСТАУ
# ============================================================

if not st.session_state.test_started:

    if st.button(
        "▶️ Тестті бастау",
        use_container_width=True
    ):

        if student_name.strip() == "":

            st.warning(
                "⚠️ Алдымен аты-жөніңізді енгізіңіз."
            )

        else:

            st.session_state.test_started = True

            st.session_state.finished = False

            st.session_state.answers = {}

            st.rerun()


# ============================================================
# ТЕСТ
# ============================================================

if (
    st.session_state.test_started
    and not st.session_state.finished
):

    st.markdown("---")

    st.subheader(
        f"👤 Оқушы: {student_name}"
    )

    st.write(
        f"🏫 Сынып: *{grade}*"
    )

    st.write(
        f"📖 Тақырып: *{selected_topic}*"
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

        if isinstance(options_data, dict):

            option_keys = list(
                options_data.keys()
            )

            option_values = []

            for key in option_keys:

                option_values.append(
                    f"{key}) {options_data[key]}"
                )


        elif isinstance(options_data, list):

            option_keys = []

            option_values = []

            for j, option in enumerate(
                options_data
            ):

                letter = chr(
                    65 + j
                )

                option_keys.append(
                    letter
                )

                option_values.append(
                    f"{letter}) {option}"
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


        selected_answer = st.radio(
            "Жауап:",
            choices,
            key=f"question_{selected_topic}_{i}",
            index=0
        )


        # ----------------------------------------------------
        # ЖАУАПТЫ САҚТАУ
        # ----------------------------------------------------

        if (
            selected_answer
            != "-- Жауапты таңдаңыз --"
        ):

            selected_letter = (
                selected_answer
                .split(")", 1)[0]
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
        f"*{answered_count} / {len(questions)}*"
    )


    # ========================================================
    # ТЕСТІ АЯҚТАУ
    # ========================================================

    if st.button(
        "✅ Тестті аяқтау",
        use_container_width=True
    ):

        if (
            len(st.session_state.answers)
            < len(questions)
        ):

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
                f"Жауап берілмеген сұрақтар: "
                f"{', '.join(map(str, unanswered))}"
            )

        else:

            st.session_state.finished = True

            st.rerun()


# ============================================================
# НӘТИЖЕ
# ============================================================

if st.session_state.finished:

    st.markdown("---")

    st.success(
        "🎉 Тест аяқталды!"
    )


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
            == correct_answer
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
            score / total * 100
        )


    # ========================================================
    # НӘТИЖЕ БЛОГЫ
    # ========================================================

    st.markdown(
        f"""
        <div class="result-box">

            <h2>📊 Нәтиже</h2>

            <h3>👤 {student_name}</h3>

            <p>🏫 Сынып:
            <b>{grade}</b>
            </p>

            <p>📖 Тақырып:
            <b>{selected_topic}</b>
            </p>

            <p>✅ Дұрыс жауап:
            <b>{score} / {total}</b>
            </p>

            <p>📈 Нәтиже:
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
            "📚 Тақырыпты қайта қарау қажет. Баға: 2"
        )


    # ========================================================
    # ЖАУАПТАРДЫ КӨРСЕТУ
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
                f"№{i + 1} — Дұрыс ✅"
            )

        else:

            st.error(
                f"""
№{i + 1} — Қате ❌

Сіздің жауабыңыз: {result["student_answer"]}

Дұрыс жауап: {result["correct_answer"]}
"""
            )


    # ========================================================
    # ҚАЙТА ТАПСЫРУ
    # ========================================================

    st.markdown("---")

    if st.button(
        "🔄 Тестті қайта бастау",
        use_container_width=True
    ):

        st.session_state.test_started = False

        st.session_state.finished = False

        st.session_state.answers = {}

        st.rerun()
