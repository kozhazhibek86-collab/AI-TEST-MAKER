import streamlit as st
import json
import os
from datetime import datetime


# ============================================================
# БЕТ БАПТАУ
# ============================================================

st.set_page_config(
    page_title="AI Test Maker",
    page_icon="📝",
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
    margin-bottom: 12px;
}

.result-box {
    background-color: #f0f8ff;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TEST ФАЙЛЫН ЖҮКТЕУ
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

        st.error("❌ tests.json файлында JSON қатесі бар.")

        return {}

    except Exception as e:

        st.error(
            f"❌ Файлды оқу кезінде қате шықты: {e}"
        )

        return {}


# ============================================================
# НӘТИЖЕЛЕРДІ ЖҮКТЕУ
# ============================================================

def load_results():

    file_path = "results.json"

    if not os.path.exists(file_path):
        return []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:
        return []


# ============================================================
# НӘТИЖЕНІ САҚТАУ
# ============================================================

def save_result(result):

    results = load_results()

    results.append(result)

    try:

        with open(
            "results.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                results,
                file,
                ensure_ascii=False,
                indent=4
            )

        return True

    except Exception:

        return False


# ============================================================
# DATA
# ============================================================

tests_data = load_tests()

if not tests_data:
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "mode" not in st.session_state:
    st.session_state.mode = None

if "test_started" not in st.session_state:
    st.session_state.test_started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "selected_class" not in st.session_state:
    st.session_state.selected_class = ""

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ============================================================
# ТАҚЫРЫПТЫ ҚАЙТА БАСТАУ
# ============================================================

def reset_test():

    st.session_state.test_started = False
    st.session_state.finished = False
    st.session_state.answers = {}
    st.session_state.last_result = None


# ============================================================
# БАС ТАҚЫРЫП
# ============================================================

st.markdown(
    '<div class="main-title">📝 AI Test Maker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Информатика пәнінен онлайн тест жүйесі</div>',
    unsafe_allow_html=True
)


# ============================================================
# РЕЖИМ ТАҢДАУ
# ============================================================

mode = st.radio(
    "🔐 Жүйеге кіру режимін таңдаңыз:",
    [
        "👨‍🏫 Мұғалім",
        "🎓 Оқушы",
        "📊 Нәтижелер"
    ],
    horizontal=True
)


# ============================================================
# ============================================================
# 👨‍🏫 МҰҒАЛІМ РЕЖИМІ
# ============================================================
# ============================================================

if mode == "👨‍🏫 Мұғалім":

    st.header("👨‍🏫 Мұғалім режимі")

    st.info(
        "Бұл жерде жүйеде бар сыныптар мен тақырыптарды "
        "көруге болады."
    )

    classes = list(tests_data.keys())

    st.subheader("📚 Сыныптар")

    for class_name in classes:

        topics = tests_data[class_name]

        st.markdown(
            f"### 🎓 {class_name}"
        )

        for topic_name, topic_data in topics.items():

            questions = topic_data.get(
                "questions",
                []
            )

            st.write(
                f"📖 {topic_name} — "
                f"{len(questions)} сұрақ"
            )

    st.markdown("---")

    st.success(
        "Жаңа сынып немесе тақырып қосу үшін "
        "tests.json файлына жаңа бөлім қосылады."
    )


# ============================================================
# ============================================================
# 🎓 ОҚУШЫ РЕЖИМІ
# ============================================================
# ============================================================

elif mode == "🎓 Оқушы":

    # --------------------------------------------------------
    # ЕГЕР ТЕСТ АЯҚТАЛСА
    # --------------------------------------------------------

    if st.session_state.finished:

        result = st.session_state.last_result

        if result:

            st.success("🎉 Тест аяқталды!")

            st.markdown(
                f"""
                <div class="result-box">

                <h2>📊 Тест нәтижесі</h2>

                <h3>👤 {result['student_name']}</h3>

                <p>
                🎓 Сынып:
                <b>{result['class_name']}</b>
                </p>

                <p>
                📚 Тақырып:
                <b>{result['topic_name']}</b>
                </p>

                <h2>
                {result['score']} / {result['total']}
                </h2>

                <h3>
                Нәтиже: {result['percentage']}%
                </h3>

                <h3>
                Баға: {result['grade']}
                </h3>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("---")

            st.subheader("📋 Жауаптарды тексеру")

            for i, answer in enumerate(
                result["details"]
            ):

                if answer["is_correct"]:

                    st.success(
                        f"№{i + 1}. "
                        f"{answer['question']}  \n"
                        f"Сіздің жауабыңыз: "
                        f"{answer['student_answer']} ✅"
                    )

                else:

                    st.error(
                        f"№{i + 1}. "
                        f"{answer['question']}  \n"
                        f"Сіздің жауабыңыз: "
                        f"{answer['student_answer']} ❌  \n"
                        f"Дұрыс жауап: "
                        f"{answer['correct_answer']}"
                    )

            st.markdown("---")

            if st.button(
                "🔄 Басқа тест тапсыру",
                use_container_width=True
            ):

                reset_test()

                st.rerun()

        st.stop()


    # --------------------------------------------------------
    # ОҚУШЫНЫҢ АТЫ
    # --------------------------------------------------------

    student_name = st.text_input(
        "👤 Оқушының аты-жөні:",
        value=st.session_state.student_name,
        placeholder="Мысалы: Айдана Нұрлан"
    )

    st.session_state.student_name = student_name


    # --------------------------------------------------------
    # 1. СЫНЫП ТАҢДАУ
    # --------------------------------------------------------

    st.subheader("🎓 1. Сыныбыңызды таңдаңыз")

    classes = list(tests_data.keys())

    selected_class = st.selectbox(
        "Сынып:",
        ["-- Сыныпты таңдаңыз --"] + classes
    )


    # --------------------------------------------------------
    # 2. ТАҚЫРЫП ТАҢДАУ
    # --------------------------------------------------------

    if selected_class != "-- Сыныпты таңдаңыз --":

        st.session_state.selected_class = selected_class

        st.subheader(
            "📚 2. Тақырыпты таңдаңыз"
        )

        class_topics = tests_data[
            selected_class
        ]

        topics = list(class_topics.keys())

        selected_topic = st.selectbox(
            "Тақырып:",
            ["-- Тақырыпты таңдаңыз --"] + topics
        )


        # ----------------------------------------------------
        # ТЕСТ АҚПАРАТЫ
        # ----------------------------------------------------

        if selected_topic != "-- Тақырыпты таңдаңыз --":

            st.session_state.selected_topic = selected_topic

            test = class_topics[selected_topic]

            subject = test.get(
                "subject",
                "Информатика"
            )

            grade = test.get(
                "grade",
                selected_class
            )

            questions = test.get(
                "questions",
                []
            )

            st.info(
                f"📚 Пән: *{subject}*  \n"
                f"🎓 Сынып: *{grade}*  \n"
                f"📖 Тақырып: *{selected_topic}*  \n"
                f"📝 Сұрақ саны: *{len(questions)}*"
            )


            # ------------------------------------------------
            # ТЕСТ БАСТАУ
            # ------------------------------------------------

            if not st.session_state.test_started:

                if st.button(
                    "▶️ Тестті бастау",
                    use_container_width=True
                ):

                    if student_name.strip() == "":

                        st.warning(
                            "⚠️ Алдымен аты-жөніңізді енгізіңіз."
                        )

                    elif len(questions) == 0:

                        st.warning(
                            "⚠️ Бұл тақырыпта сұрақ жоқ."
                        )

                    else:

                        st.session_state.test_started = True
                        st.session_state.finished = False
                        st.session_state.answers = {}

                        st.rerun()


    # --------------------------------------------------------
    # ТЕСТ
    # --------------------------------------------------------

    if (
        st.session_state.test_started
        and not st.session_state.finished
    ):

        selected_class = st.session_state.selected_class

        selected_topic = st.session_state.selected_topic

        test = tests_data[
            selected_class
        ][
            selected_topic
        ]

        questions = test.get(
            "questions",
            []
        )

        st.markdown("---")

        st.subheader(
            f"👤 {student_name}"
        )

        st.write(
            f"🎓 {selected_class} | "
            f"📚 {selected_topic}"
        )

        st.markdown("---")


        # ----------------------------------------------------
        # СҰРАҚТАР
        # ----------------------------------------------------

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


            # --------------------------------------------
            # ВАРИАНТТАР
            # --------------------------------------------

            if isinstance(
                options_data,
                dict
            ):

                option_keys = list(
                    options_data.keys()
                )

                option_values = [
                    f"{key}) {options_data[key]}"
                    for key in option_keys
                ]

            elif isinstance(
                options_data,
                list
            ):

                option_keys = [
                    chr(65 + j)
                    for j in range(
                        len(options_data)
                    )
                ]

                option_values = [
                    f"{option_keys[j]}) "
                    f"{options_data[j]}"
                    for j in range(
                        len(options_data)
                    )
                ]

            else:

                option_keys = []
                option_values = []


            # --------------------------------------------
            # СҰРАҚ
            # --------------------------------------------

            st.markdown(
                f"""
                <div class="question-box">
                <b>{i + 1}. {question_text}</b>
                </div>
                """,
                unsafe_allow_html=True
            )


            # --------------------------------------------
            # БОС НҰСҚА
            # --------------------------------------------

            choices = [
                "-- Жауапты таңдаңыз --"
            ] + option_values


            selected = st.radio(
                "Жауап:",
                choices,
                key=f"question_{i}"
            )


            # --------------------------------------------
            # ЖАУАПТЫ САҚТАУ
            # --------------------------------------------

            if (
                selected
                != "-- Жауапты таңдаңыз --"
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


        # ----------------------------------------------------
        # ЖАУАП САНЫ
        # ----------------------------------------------------

        answered_count = len(
            st.session_state.answers
        )

        st.write(
            f"📊 Жауап берілді: "
            f"*{answered_count} / {len(questions)}*"
        )


        # ----------------------------------------------------
        # ТЕСТІ АЯҚТАУ
        # ----------------------------------------------------

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

                    if (
                        i
                        not in
                        st.session_state.answers
                    ):

                        unanswered.append(
                            i + 1
                        )

                st.warning(
                    "⚠️ Барлық сұрақтарға жауап беріңіз.\n\n"
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

                # ----------------------------------------
                # НӘТИЖЕ ЕСЕПТЕУ
                # ----------------------------------------

                score = 0

                details = []

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


                    details.append(
                        {
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
                        }
                    )


                # ----------------------------------------
                # ПРОЦЕНТ
                # ----------------------------------------

                total = len(questions)

                percentage = round(
                    score / total * 100
                )


                # ----------------------------------------
                # БАҒА
                # ----------------------------------------

                if percentage >= 90:

                    grade_mark = 5

                elif percentage >= 70:

                    grade_mark = 4

                elif percentage >= 50:

                    grade_mark = 3

                else:

                    grade_mark = 2


                # ----------------------------------------
                # НӘТИЖЕ ОБЪЕКТІСІ
                # ----------------------------------------

                result = {

                    "student_name":
                        student_name,

                    "class_name":
                        selected_class,

                    "topic_name":
                        selected_topic,

                    "score":
                        score,

                    "total":
                        total,

                    "percentage":
                        percentage,

                    "grade":
                        grade_mark,

                    "date":
                        datetime.now().strftime(
                            "%d.%m.%Y %H:%M"
                        ),

                    "details":
                        details
                }


                # ----------------------------------------
                # SESSION-ҒА САҚТАУ
                # ----------------------------------------

                st.session_state.last_result = (
                    result
                )

                st.session_state.finished = True


                # ----------------------------------------
                # RESULTS.JSON-ҒА САҚТАУ
                # ----------------------------------------

                save_result(result)


                st.rerun()


# ============================================================
# ============================================================
# 📊 НӘТИЖЕЛЕР РЕЖИМІ
# ============================================================
# ============================================================

elif mode == "📊 Нәтижелер":

    st.header("📊 Нәтижелер")

    results = load_results()


    if not results:

        st.info(
            "Әзірге ешқандай нәтиже жоқ."
        )

    else:

        st.success(
            f"Барлығы {len(results)} нәтиже табылды."
        )


        # ----------------------------------------------------
        # СЫНЫП ФИЛЬТРІ
        # ----------------------------------------------------

        result_classes = sorted(
            list(
                set(
                    r["class_name"]
                    for r in results
                )
            )
        )


        selected_result_class = st.selectbox(
            "🎓 Сынып:",
            ["Барлық сыныптар"]
            + result_classes
        )


        # ----------------------------------------------------
        # ФИЛЬТР
        # ----------------------------------------------------

        filtered_results = results


        if (
            selected_result_class
            != "Барлық сыныптар"
        ):

            filtered_results = [
                r
                for r in results
                if r["class_name"]
                == selected_result_class
            ]


        # ----------------------------------------------------
        # ТАҚЫРЫП ФИЛЬТРІ
        # ----------------------------------------------------

        result_topics = sorted(
            list(
                set(
                    r["topic_name"]
                    for r in filtered_results
                )
            )
        )


        selected_result_topic = st.selectbox(
            "📚 Тақырып:",
            ["Барлық тақырыптар"]
            + result_topics
        )


        if (
            selected_result_topic
            != "Барлық тақырыптар"
        ):

            filtered_results = [
                r
                for r in filtered_results
                if r["topic_name"]
                == selected_result_topic
            ]


        # ----------------------------------------------------
        # НӘТИЖЕЛЕР
        # ----------------------------------------------------

        st.markdown("---")

        if not filtered_results:

            st.warning(
                "Бұл таңдауға сәйкес нәтиже жоқ."
            )

        else:

            for i, result in enumerate(
                reversed(filtered_results)
            ):

                if result["percentage"] >= 90:
                    icon = "🏆"

                elif result["percentage"] >= 70:
                    icon = "👍"

                elif result["percentage"] >= 50:
                    icon = "🙂"

                else:
                    icon = "📚"


                with st.expander(
                    f"{icon} "
                    f"{result['student_name']} — "
                    f"{result['percentage']}%"
                ):

                    st.write(
                        f"🎓 Сынып: "
                        f"*{result['class_name']}*"
                    )

                    st.write(
                        f"📚 Тақырып: "
                        f"*{result['topic_name']}*"
                    )

                    st.write(
                        f"📊 Дұрыс жауап: "
                        f"**{result['score']} / "
                        f"{result['total']}**"
                    )

                    st.write(
                        f"📈 Нәтиже: "
                        f"*{result['percentage']}%*"
                    )

                    st.write(
                        f"🎯 Баға: "
                        f"*{result['grade']}*"
                    )

                    st.write(
                        f"🕐 Уақыты: "
                        f"*{result['date']}*"
                    )
