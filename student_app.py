
import streamlit as st
import json
import os

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
    font-size: 36px;
    font-weight: bold;
}

.sub-title {
    text-align: center;
    font-size: 20px;
    color: #666;
    margin-bottom: 30px;
}

.question-box {
    background: #f5f7fa;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.result-box {
    background: #f0f8ff;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# TESTS.JSON
# ============================================================

def load_tests():

    path = "tests.json"

    if not os.path.exists(path):
        st.error("❌ tests.json файлы табылмады.")
        st.stop()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    except Exception as e:
        st.error(f"❌ tests.json оқу қатесі: {e}")
        st.stop()


tests = load_tests()


# ============================================================
# БЕТ
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
# СЫНЫПТАР
# ============================================================

# Сіздің tests.json құрылымы:
#
# {
#   "5": {...},
#   "6": {...},
#   "7": {...}
# }

if not isinstance(tests, dict):

    st.error("❌ tests.json құрылымы дұрыс емес.")
    st.stop()


grades = []

for key in tests.keys():

    # "5", "6", "7" сияқты кілттерді аламыз
    if str(key).strip().isdigit():

        grades.append(str(key))


# Сыныптарды реттеу
grades = sorted(
    grades,
    key=lambda x: int(x)
)


if len(grades) == 0:

    st.error(
        "❌ tests.json файлынан сыныптар табылмады."
    )

    st.stop()


# ============================================================
# СЫНЫП ТАҢДАУ
# ============================================================

grade_options = [
    "— Сыныпты таңдаңыз —"
] + grades


selected_grade = st.selectbox(
    "🏫 Сыныбыңызды таңдаңыз:",
    grade_options
)


if selected_grade == "— Сыныпты таңдаңыз —":

    st.info("☝️ Алдымен сыныпты таңдаңыз.")

    st.stop()


# ============================================================
# ТАҢДАЛҒАН СЫНЫП
# ============================================================

class_data = tests[selected_grade]


if not isinstance(class_data, dict):

    st.error(
        f"❌ {selected_grade}-сыныптың деректері дұрыс емес."
    )

    st.stop()


# ============================================================
# ТАҚЫРЫПТАР
# ============================================================

topics = list(class_data.keys())


if len(topics) == 0:

    st.warning(
        f"⚠️ {selected_grade}-сыныпта тесттер жоқ."
    )

    st.stop()


# ============================================================
# ТАҚЫРЫП ТАҢДАУ
# ============================================================

topic_options = [
    "— Тақырыпты таңдаңыз —"
] + topics


selected_topic = st.selectbox(
    "📚 Тақырыпты таңдаңыз:",
    topic_options
)


if selected_topic == "— Тақырыпты таңдаңыз —":

    st.info("☝️ Енді тақырыпты таңдаңыз.")

    st.stop()


# ============================================================
# ТЕСТ
# ============================================================

test = class_data[selected_topic]


subject = test.get(
    "subject",
    "Информатика"
)

questions = test.get(
    "questions",
    []
)


# ============================================================
# АҚПАРАТ
# ============================================================

st.info(
    f"""
📚 Пән: *{subject}*

🏫 Сынып: *{selected_grade}*

📖 Тақырып: *{selected_topic}*

📝 Сұрақ саны: *{len(questions)}*
"""
)


# ============================================================
# ОҚУШЫ АТЫ
# ============================================================

student_name = st.text_input(
    "👤 Оқушының аты-жөні:",
    placeholder="Аты-жөніңізді енгізіңіз"
)


# ============================================================
# SESSION STATE
# ============================================================

if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "answers" not in st.session_state:
    st.session_state.answers = {}


# ============================================================
# ТЕСТТІ БАСТАУ
# ============================================================

if not st.session_state.started:

    if st.button(
        "▶️ Тестті бастау",
        use_container_width=True
    ):

        if student_name.strip() == "":

            st.warning(
                "⚠️ Аты-жөніңізді енгізіңіз."
            )

        else:

            st.session_state.started = True
            st.session_state.finished = False
            st.session_state.answers = {}

            st.rerun()


# ============================================================
# ТЕСТ
# ============================================================

if (
    st.session_state.started
    and not st.session_state.finished
):

    st.markdown("---")

    st.subheader(
        f"👤 {student_name}"
    )

    for i, q in enumerate(questions):

        question = q.get(
            "question",
            f"{i + 1}-сұрақ"
        )

        options = q.get(
            "options",
            {}
        )


        st.markdown(
            f"""
            <div class="question-box">
            <b>{i + 1}. {question}</b>
            </div>
            """,
            unsafe_allow_html=True
        )


        # -----------------------------------------------
        # ВАРИАНТТАР
        # -----------------------------------------------

        if isinstance(options, dict):

            option_list = []

            for letter, text in options.items():

                option_list.append(
                    f"{letter}) {text}"
                )

        else:

            option_list = []

            for j, text in enumerate(options):

                letter = chr(65 + j)

                option_list.append(
                    f"{letter}) {text}"
                )


        choices = [
            "— Жауапты таңдаңыз —"
        ] + option_list


        answer = st.radio(
            "Жауап:",
            choices,
            key=f"q_{i}"
        )


        if answer != "— Жауапты таңдаңыз —":

            letter = answer.split(")")[0]

            st.session_state.answers[i] = letter


        st.markdown("---")


    # ========================================================
    # ЖАУАП САНЫ
    # ========================================================

    answered = len(
        st.session_state.answers
    )

    st.write(
        f"📊 Жауап берілді: *{answered}/{len(questions)}*"
    )


    # ========================================================
    # АЯҚТАУ
    # ========================================================

    if st.button(
        "✅ Тестті аяқтау",
        use_container_width=True
    ):

        if answered != len(questions):

            st.warning(
                "⚠️ Барлық сұрақтарға жауап беріңіз."
            )

        else:

            st.session_state.finished = True

            st.rerun()


# ============================================================
# НӘТИЖЕ
# ============================================================

if st.session_state.finished:

    score = 0

    total = len(questions)


    for i, q in enumerate(questions):

        correct = str(
            q.get("answer", "")
        ).strip().upper()

        student = str(
            st.session_state.answers.get(i, "")
        ).strip().upper()


        if student == correct:

            score += 1


    percentage = round(
        score / total * 100
    ) if total else 0


    # ========================================================
    # НӘТИЖЕ
    # ========================================================

    st.markdown(
        f"""
        <div class="result-box">

        <h2>📊 Тест нәтижесі</h2>

        <h3>👤 {student_name}</h3>

        <p>🏫 Сынып: <b>{selected_grade}</b></p>

        <p>📚 Тақырып: <b>{selected_topic}</b></p>

        <p>✅ Дұрыс жауап:
        <b>{score}/{total}</b></p>

        <p>📈 Нәтиже:
        <b>{percentage}%</b></p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # БАҒА
    # ========================================================

    if percentage >= 90:

        st.success("🏆 Өте жақсы! Баға: 5")

    elif percentage >= 70:

        st.info("👍 Жақсы! Баға: 4")

    elif percentage >= 50:

        st.warning("🙂 Қанағаттанарлық. Баға: 3")

    else:

        st.error(
            "📚 Тақырыпты қайта қарау қажет. Баға: 2"
        )


    # ========================================================
    # ҚАЙТА ТАПСЫРУ
    # ========================================================

    st.markdown("---")

    if st.button(
        "🔄 Басқа тестті тапсыру",
        use_container_width=True
    ):

        st.session_state.started = False
        st.session_state.finished = False
        st.session_state.answers = {}

        st.rerun()
