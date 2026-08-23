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
    font-size: 38px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    font-size: 20px;
    color: #666;
    margin-bottom: 30px;
}

.mode-box {
    background-color: #f5f7fa;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 20px;
}

.card {
    background-color: #f8f9fb;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

.big-number {
    font-size: 30px;
    font-weight: bold;
}

.question-box {
    background-color: #f5f7fa;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TESTТЕРДІ ЖҮКТЕУ
# ============================================================

def load_tests():

    file_path = "tests.json"

    if not os.path.exists(file_path):

        st.error("❌ tests.json файлы табылмады!")

        st.info(
            "teacher_app.py және tests.json файлдары "
            "бір репозиторийде болуы керек."
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
            "❌ tests.json файлында JSON қатесі бар."
        )

        return {}

    except Exception as e:

        st.error(
            f"❌ Қате: {e}"
        )

        return {}


tests_data = load_tests()

if not tests_data:
    st.stop()


# ============================================================
# ТАҚЫРЫПТАР МЕН СЫНЫПТАР
# ============================================================

all_tests = []

for grade_key, grade_data in tests_data.items():

    if isinstance(grade_data, dict):

        for topic_name, test_data in grade_data.items():

            if isinstance(test_data, dict):

                all_tests.append({
                    "grade": str(
                        test_data.get(
                            "grade",
                            grade_key
                        )
                    ),
                    "topic": topic_name,
                    "subject": test_data.get(
                        "subject",
                        "Информатика"
                    ),
                    "questions": test_data.get(
                        "questions",
                        []
                    )
                })


# ============================================================
# БАСТЫ БӨЛІК
# ============================================================

st.markdown(
    '<div class="main-title">👩‍🏫 AI Test Maker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Мұғалімнің басқару панелі</div>',
    unsafe_allow_html=True
)


# ============================================================
# РЕЖИМДЕР
# ============================================================

st.markdown(
    '<div class="mode-box">',
    unsafe_allow_html=True
)

mode = st.radio(
    "Жүйеге кіру режимін таңдаңыз:",
    [
        "👩‍🏫 Мұғалім",
        "🎓 Оқушы",
        "📊 Нәтижелер"
    ],
    horizontal=True
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# МҰҒАЛІМ РЕЖИМІ
# ============================================================

if mode == "👩‍🏫 Мұғалім":

    st.header("👩‍🏫 Мұғалім режимі")

    st.write(
        "Бұл бөлімде барлық сыныптар, тақырыптар және тесттер көрінеді."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # ЖАЛПЫ СТАТИСТИКА
    # --------------------------------------------------------

    total_tests = len(all_tests)

    total_questions = sum(
        len(test["questions"])
        for test in all_tests
    )

    grades = sorted(
        list(
            set(
                test["grade"]
                for test in all_tests
            )
        )
    )

    topics = sorted(
        list(
            set(
                test["topic"]
                for test in all_tests
            )
        )
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📚 Сыныптар",
            len(grades)
        )

    with col2:

        st.metric(
            "📖 Тақырыптар",
            len(topics)
        )

    with col3:

        st.metric(
            "📝 Тесттер",
            total_tests
        )

    with col4:

        st.metric(
            "❓ Сұрақтар",
            total_questions
        )


    st.markdown("---")

    # --------------------------------------------------------
    # СЫНЫПТЫ ТАҢДАУ
    # --------------------------------------------------------

    st.subheader("🔎 Тесттерді іздеу")

    grade_options = [
        "Барлық сыныптар"
    ] + grades

    selected_grade = st.selectbox(
        "🏫 Сыныпты таңдаңыз:",
        grade_options
    )


    # --------------------------------------------------------
    # ТАҚЫРЫПТЫ ТАҢДАУ
    # --------------------------------------------------------

    filtered_tests = all_tests

    if selected_grade != "Барлық сыныптар":

        filtered_tests = [
            test
            for test in all_tests
            if test["grade"] == selected_grade
        ]


    filtered_topics = sorted(
        list(
            set(
                test["topic"]
                for test in filtered_tests
            )
        )
    )

    topic_options = [
        "Барлық тақырыптар"
    ] + filtered_topics

    selected_topic = st.selectbox(
        "📚 Тақырыпты таңдаңыз:",
        topic_options
    )


    # --------------------------------------------------------
    # ҚОСЫМША СҮЗГІ
    # --------------------------------------------------------

    if selected_topic != "Барлық тақырыптар":

        filtered_tests = [
            test
            for test in filtered_tests
            if test["topic"] == selected_topic
        ]


    st.markdown("---")

    st.subheader("📋 Тесттер тізімі")


    # --------------------------------------------------------
    # ТЕСТТЕРДІ КӨРСЕТУ
    # --------------------------------------------------------

    if not filtered_tests:

        st.warning(
            "Бұл таңдауға сәйкес тест табылмады."
        )

    else:

        for number, test in enumerate(
            filtered_tests,
            start=1
        ):

            with st.expander(
                f"📝 {number}. {test['topic']} — {test['grade']} сынып"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"📚 *Пән:* {test['subject']}"
                    )

                    st.write(
                        f"🏫 *Сынып:* {test['grade']}"
                    )

                with col2:

                    st.write(
                        f"📖 *Тақырып:* {test['topic']}"
                    )

                    st.write(
                        f"❓ *Сұрақ саны:* "
                        f"{len(test['questions'])}"
                    )

                st.markdown("---")

                st.write("*Сұрақтар:*")

                for i, question in enumerate(
                    test["questions"],
                    start=1
                ):

                    question_text = question.get(
                        "question",
                        ""
                    )

                    st.markdown(
                        f"""
                        <div class="question-box">
                        <b>{i}. {question_text}</b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


# ============================================================
# ОҚУШЫ РЕЖИМІ
# ============================================================

elif mode == "🎓 Оқушы":

    st.header("🎓 Оқушы режимі")

    st.info(
        "Оқушыларға арналған тест жүйесі."
    )

    st.markdown("---")

    st.write(
        "Оқушы режимі жеке сілтемеде жұмыс істейді:"
    )

    st.code(
        "student_app.py"
    )

    st.success(
        "Оқушыларға student_app.py арқылы жасалған "
        "сілтемені жіберіңіз."
    )


# ============================================================
# НӘТИЖЕЛЕР РЕЖИМІ
# ============================================================

elif mode == "📊 Нәтижелер":

    st.header("📊 Нәтижелер")

    st.info(
        "Оқушылардың тест нәтижелері осы бөлімде көрсетіледі."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # НӘТИЖЕ ФАЙЛЫН ТЕКСЕРУ
    # --------------------------------------------------------

    if os.path.exists("results.json"):

        try:

            with open(
                "results.json",
                "r",
                encoding="utf-8"
            ) as file:

                results_data = json.load(file)


            if results_data:

                st.subheader(
                    "📋 Оқушылардың нәтижелері"
                )

                for result in results_data:

                    st.markdown(
                        f"""
                        <div class="card">
                            <h3>
                            👤 {result.get("student_name", "Оқушы")}
                            </h3>

                            <p>
                            🏫 Сынып:
                            <b>{result.get("grade", "-")}</b>
                            </p>

                            <p>
                            📚 Тақырып:
                            <b>{result.get("topic", "-")}</b>
                            </p>

                            <p>
                            ✅ Дұрыс жауап:
                            <b>{result.get("score", 0)}</b>
                            /
                            <b>{result.get("total", 0)}</b>
                            </p>

                            <p>
                            📊 Нәтиже:
                            <b>{result.get("percentage", 0)}%</b>
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.warning(
                    "Әзірге нәтижелер жоқ."
                )

        except Exception as e:

            st.error(
                f"Нәтижелерді оқу кезінде қате: {e}"
            )

    else:

        st.warning(
            "📊 Әзірге оқушылардың нәтижелері жоқ."
        )

        st.write(
            "Оқушылар тест тапсырғаннан кейін "
            "нәтижелер осы бөлімде көрсетілетіндей "
            "жүйені байланыстыруға болады."
        )


# ============================================================
# ТӨМЕНГІ АҚПАРАТ
# ============================================================

st.markdown("---")

st.caption(
    "AI Test Maker • Информатика пәніне арналған тест жүйесі"
)
