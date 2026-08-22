import streamlit as st
import json
import os

# ============================================================
# БЕТ БАПТАУЛАРЫ
# ============================================================

st.set_page_config(
    page_title="AI Test Maker - Оқушы",
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
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 10px;
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
        margin-bottom: 15px;
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
# ТЕСТТЕРДІ ЖҮКТЕУ
# ============================================================

def load_tests():
    file_path = "tests.json"

    if not os.path.exists(file_path):
        st.error("❌ tests.json файлы табылмады!")
        st.info(
            "GitHub репозиторийде student_app.py және tests.json "
            "файлдары бір папкада болуы керек."
        )
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        st.error("❌ tests.json ішінде қате бар.")
        return {}

    except Exception as e:
        st.error(f"❌ Файлды оқу кезінде қате шықты: {e}")
        return {}


# ============================================================
# ТЕСТТІ ЖҮКТЕУ
# ============================================================

tests_data = load_tests()

if not tests_data:
    st.stop()


# ============================================================
# ТАҚЫРЫПТЫ ТАҢДАУ
# ============================================================

st.markdown(
    '<div class="main-title">📝 AI Test Maker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Оқушыға арналған тест жүйесі</div>',
    unsafe_allow_html=True
)

topics = list(tests_data.keys())

if len(topics) == 0:
    st.error("Тест тақырыптары табылмады.")
    st.stop()

selected_topic = st.selectbox(
    "📚 Тест тақырыбын таңдаңыз:",
    topics
)


# ============================================================
# ТАҢДАЛҒАН ТЕСТ
# ============================================================

test = tests_data[selected_topic]

subject = test.get("subject", "Информатика")
grade = test.get("grade", "")

questions = test.get("questions", [])


# ============================================================
# ТЕСТ АҚПАРАТЫ
# ============================================================

st.info(
    f"📚 Пән: *{subject}*  \n"
    f"🎓 Сынып: *{grade}*  \n"
    f"📝 Сұрақ саны: *{len(questions)}*"
)


# ============================================================
# ОҚУШЫНЫҢ АТЫ
# ============================================================

student_name = st.text_input(
    "👤 Оқушының аты-жөні:",
    placeholder="Аты-жөніңізді енгізіңіз"
)


# ============================================================
# ТЕСТ БАСТАУ
# ============================================================

if "test_started" not in st.session_state:
    st.session_state.test_started = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "finished" not in st.session_state:
    st.session_state.finished = False


if not st.session_state.test_started:

    if st.button("▶️ Тестті бастау", use_container_width=True):

        if student_name.strip() == "":
            st.warning("⚠️ Алдымен аты-жөніңізді енгізіңіз.")
        else:
            st.session_state.test_started = True
            st.session_state.finished = False
            st.session_state.answers = {}

            st.rerun()


# ============================================================
# ТЕСТ
# ============================================================

if st.session_state.test_started and not st.session_state.finished:

    st.markdown("---")

    st.subheader(
        f"👤 Оқушы: {student_name}"
    )

    st.markdown("---")


    # --------------------------------------------------------
    # ӘР СҰРАҚ
    # --------------------------------------------------------

    for i, question_data in enumerate(questions):

        question_text = question_data.get(
            "question",
            f"{i + 1}-сұрақ"
        )

        options_data = question_data.get(
            "options",
            {}
        )

        # Егер options dict болса
        if isinstance(options_data, dict):

            option_keys = list(options_data.keys())

            option_values = [
                f"{key}) {options_data[key]}"
                for key in option_keys
            ]

        # Егер options list болса
        elif isinstance(options_data, list):

            option_keys = [
                chr(65 + j)
                for j in range(len(options_data))
            ]

            option_values = [
                f"{option_keys[j]}) {options_data[j]}"
                for j in range(len(options_data))
            ]

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


        # ====================================================
        # ЕҢ МАҢЫЗДЫ БӨЛІК
        # ====================================================
        # Алғашқы нұсқа автоматты түрде белгіленбеуі үшін
        # "Жауапты таңдаңыз" деген бос нұсқа қосылады.
        # ====================================================

        choices = ["-- Жауапты таңдаңыз --"] + option_values

        selected = st.radio(
            "Жауап:",
            choices,
            key=f"question_{i}",
            index=0
        )


        # ----------------------------------------------------
        # ОҚУШЫНЫҢ ЖАУАБЫН САҚТАУ
        # ----------------------------------------------------

        if selected != "-- Жауапты таңдаңыз --":

            selected_letter = selected.split(")")[0]

            st.session_state.answers[i] = selected_letter

        else:

            # Таңдалмаса, жауапты өшіреміз
            if i in st.session_state.answers:
                del st.session_state.answers[i]


        st.markdown("---")


    # ========================================================
    # ЖАУАП БЕРІЛГЕН СҰРАҚ САНЫ
    # ========================================================

    answered_count = len(st.session_state.answers)

    st.write(
        f"📊 Жауап берілді: *{answered_count} / {len(questions)}*"
    )


    # ========================================================
    # ТЕСТІ АЯҚТАУ
    # ========================================================

    if st.button(
        "✅ Тестті аяқтау",
        use_container_width=True
    ):

        if len(st.session_state.answers) < len(questions):

            unanswered = []

            for i in range(len(questions)):

                if i not in st.session_state.answers:
                    unanswered.append(i + 1)

            st.warning(
                "⚠️ Барлық сұрақтарға жауап беріңіз.\n\n"
                f"Жауап берілмеген сұрақтар: {', '.join(map(str, unanswered))}"
            )

        else:

            st.session_state.finished = True

            st.rerun()


# ============================================================
# НӘТИЖЕ
# ============================================================

if st.session_state.finished:

    st.markdown("---")

    st.success("🎉 Тест аяқталды!")

    score = 0
    total = len(questions)

    results = []


    # --------------------------------------------------------
    # ДҰРЫС ЖАУАПТАРДЫ ТЕКСЕРУ
    # --------------------------------------------------------

    for i, question_data in enumerate(questions):

        correct_answer = str(
            question_data.get("answer", "")
        ).strip().upper()

        student_answer = str(
            st.session_state.answers.get(i, "")
        ).strip().upper()

        is_correct = (
            student_answer == correct_answer
        )

        if is_correct:
            score += 1

        results.append({
            "question": question_data.get(
                "question",
                ""
            ),
            "student_answer": student_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })


    # ========================================================
    # НӘТИЖЕ КӨРСЕТУ
    # ========================================================

    percentage = 0

    if total > 0:
        percentage = round(
            score / total * 100
        )


    st.markdown(
        f"""
        <div class="result-box">
            <h2>📊 Нәтиже</h2>
            <h3>👤 {student_name}</h3>
            <p>Дұрыс жауап: <b>{score}</b> / {total}</p>
            <p>Нәтиже: <b>{percentage}%</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # БАҒА
    # ========================================================

    if percentage >= 90:

        grade_mark = 5
        st.success("🏆 Өте жақсы! Баға: 5")

    elif percentage >= 70:

        grade_mark = 4
        st.info("👍 Жақсы! Баға: 4")

    elif percentage >= 50:

        grade_mark = 3
        st.warning("🙂 Қанағаттанарлық. Баға: 3")

    else:

        grade_mark = 2
        st.error("📚 Тақырыпты қайта қарау қажет. Баға: 2")


    # ========================================================
    # ЖАУАПТАРДЫ КӨРСЕТУ
    # ========================================================

    st.markdown("---")
    st.subheader("📋 Жауаптарды тексеру")


    for i, result in enumerate(results):

        if result["is_correct"]:

            st.success(
                f"№{i + 1} — Дұрыс ✅"
            )

        else:

            st.error(
                f"№{i + 1} — Қате ❌  \n"
                f"Сіздің жауабыңыз: {result['student_answer']}  \n"
                f"Дұрыс жауап: {result['correct_answer']}"
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
