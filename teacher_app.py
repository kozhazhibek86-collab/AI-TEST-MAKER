import streamlit as st
import json
import os

# ============================================================
# БЕТ БАПТАУ
# ============================================================

st.set_page_config(
    page_title="AI Test Maker - Мұғалім",
    page_icon="👩‍🏫",
    layout="wide"
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
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    font-size: 20px;
    color: #666;
    margin-bottom: 30px;
}

.test-card {
    background-color: #f5f7fa;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}

.question-card {
    background-color: #ffffff;
    border: 1px solid #dddddd;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# ТЕСТТЕРДІ ЖҮКТЕУ
# ============================================================

def load_tests():

    file_path = "tests.json"

    if not os.path.exists(file_path):

        st.error("❌ tests.json файлы табылмады!")

        st.info(
            "GitHub репозиторийде мына файлдар болуы керек:\n\n"
            "• student_app.py\n"
            "• teacher_app.py\n"
            "• tests.json"
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

        st.error(
            "❌ tests.json файлының ішінде JSON қатесі бар."
        )

        return {}

    except Exception as e:

        st.error(
            f"❌ Файлды оқу кезінде қате шықты: {e}"
        )

        return {}


# ============================================================
# ДЕРЕКТЕРДІ ЖҮКТЕУ
# ============================================================

tests_data = load_tests()

if not tests_data:
    st.stop()


# ============================================================
# ТАҚЫРЫПТАРДЫ ЖИНАУ
# ============================================================

all_tests = []

for topic_name, test_data in tests_data.items():

    if not isinstance(test_data, dict):
        continue

    subject = test_data.get(
        "subject",
        "Информатика"
    )

    grade = str(
        test_data.get(
            "grade",
            ""
        )
    )

    questions = test_data.get(
        "questions",
        []
    )

    all_tests.append({

        "topic": topic_name,

        "subject": subject,

        "grade": grade,

        "questions": questions

    })


# ============================================================
# ТАҚЫРЫП ЖОҚ БОЛСА
# ============================================================

if len(all_tests) == 0:

    st.error(
        "❌ tests.json ішінде тесттер табылмады."
    )

    st.stop()


# ============================================================
# ТАҚЫРЫПТАРДЫҢ БАРЛЫҚ СЫНЫПТАРЫН АЛУ
# ============================================================

grades = sorted(
    list(
        set(
            test["grade"]
            for test in all_tests
            if test["grade"] != ""
        )
    )
)


# ============================================================
# ТАҚЫРЫПТАР
# ============================================================

topics = sorted(
    list(
        set(
            test["topic"]
            for test in all_tests
        )
    )
)


# ============================================================
# БАСТЫ БЕТ
# ============================================================

st.markdown(
    '<div class="main-title">👩‍🏫 AI Test Maker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Мұғалімнің басқару панелі'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ЖАЛПЫ АҚПАРАТ
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📚 Барлық тест",
        len(all_tests)
    )

with col2:

    st.metric(
        "🎓 Сынып саны",
        len(grades)
    )

with col3:

    st.metric(
        "📝 Тақырып саны",
        len(topics)
    )


st.markdown("---")


# ============================================================
# СҮЗГІЛЕР
# ============================================================

st.subheader("🔎 Тесттерді іздеу")


col1, col2 = st.columns(2)


with col1:

    grade_options = [
        "Барлық сыныптар"
    ] + grades

    selected_grade = st.selectbox(
        "🎓 Сыныпты таңдаңыз:",
        grade_options
    )


with col2:

    topic_options = [
        "Барлық тақырыптар"
    ] + topics

    selected_topic = st.selectbox(
        "📚 Тақырыпты таңдаңыз:",
        topic_options
    )


# ============================================================
# СҮЗГІЛЕУ
# ============================================================

filtered_tests = []

for test in all_tests:

    grade_match = (
        selected_grade == "Барлық сыныптар"
        or test["grade"] == selected_grade
    )

    topic_match = (
        selected_topic == "Барлық тақырыптар"
        or test["topic"] == selected_topic
    )

    if grade_match and topic_match:

        filtered_tests.append(test)


# ============================================================
# НӘТИЖЕ САНЫ
# ============================================================

st.markdown("---")

st.write(
    f"📊 Табылған тест саны: *{len(filtered_tests)}*"
)


# ============================================================
# ТЕСТТЕРДІ КӨРСЕТУ
# ============================================================

for number, test in enumerate(
    filtered_tests,
    start=1
):

    topic = test["topic"]

    subject = test["subject"]

    grade = test["grade"]

    questions = test["questions"]


    # ========================================================
    # ТЕСТ ТУРАЛЫ АҚПАРАТ
    # ========================================================

    with st.expander(
        f"📚 {number}. {topic} — {grade}-сынып",
        expanded=False
    ):

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write(
                f"📚 *Пән:* {subject}"
            )

        with col2:

            st.write(
                f"🎓 *Сынып:* {grade}"
            )

        with col3:

            st.write(
                f"📝 *Сұрақ саны:* {len(questions)}"
            )


        st.markdown("---")


        # ====================================================
        # СҰРАҚТАР
        # ====================================================

        if len(questions) == 0:

            st.warning(
                "Бұл тестте сұрақтар жоқ."
            )

        else:

            for i, question_data in enumerate(
                questions,
                start=1
            ):

                question_text = question_data.get(
                    "question",
                    ""
                )

                options = question_data.get(
                    "options",
                    {}
                )

                correct_answer = question_data.get(
                    "answer",
                    ""
                )


                st.markdown(
                    f"### {i}. {question_text}"
                )


                # ------------------------------------------------
                # ВАРИАНТТАР
                # ------------------------------------------------

                if isinstance(options, dict):

                    for key, value in options.items():

                        if str(key).upper() == str(
                            correct_answer
                        ).upper():

                            st.success(
                                f"*{key}) {value}* ✅ Дұрыс жауап"
                            )

                        else:

                            st.write(
                                f"{key}) {value}"
                            )


                elif isinstance(options, list):

                    for j, value in enumerate(
                        options
                    ):

                        letter = chr(
                            65 + j
                        )

                        if letter == str(
                            correct_answer
                        ).upper():

                            st.success(
                                f"*{letter}) {value}* "
                                f"✅ Дұрыс жауап"
                            )

                        else:

                            st.write(
                                f"{letter}) {value}"
                            )


                st.markdown("---")


# ============================================================
# ТӨМЕНГІ АҚПАРАТ
# ============================================================

st.markdown("---")

st.info(
    "👩‍🏫 Бұл — мұғалім режимі. "
    "Мұнда барлық сыныптар, тақырыптар, "
    "сұрақтар және дұрыс жауаптар көрінеді."
)
