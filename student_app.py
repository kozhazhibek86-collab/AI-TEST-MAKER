import streamlit as st
import json
import os

# =========================================================
# БЕТ ПАРАМЕТРЛЕРІ
# =========================================================

st.set_page_config(
    page_title="AI Test Maker - Оқушы",
    page_icon="📝",
    layout="centered"
)

# =========================================================
# ТЕСТТЕРДІ ЖҮКТЕУ
# =========================================================

def load_tests():
    file_path = "tests.json"

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Егер tests.json ішінде тікелей тізім болса
        if isinstance(data, list):
            return data

        # Егер {"tests": [...]} түрінде болса
        if isinstance(data, dict):
    if "tests" in data:
        return data["tests"]

    tests = []

    for title, test in data.items():
        if isinstance(test, dict):
            test = dict(test)
            test.setdefault("title", title)
            tests.append(test)

    return tests

    except Exception:
        return []


tests = load_tests()

# =========================================================
# SESSION STATE
# =========================================================

if "student_started" not in st.session_state:
    st.session_state.student_started = False

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "student_class" not in st.session_state:
    st.session_state.student_class = ""

if "selected_test" not in st.session_state:
    st.session_state.selected_test = None

if "finished" not in st.session_state:
    st.session_state.finished = False

if "score" not in st.session_state:
    st.session_state.score = 0

if "total" not in st.session_state:
    st.session_state.total = 0


# =========================================================
# ТАҚЫРЫП
# =========================================================

st.title("📝 ОҚУШЫ БӨЛІМІ")

st.write(
    "AI Test Maker жүйесіне қош келдіңіз!"
)

st.divider()


# =========================================================
# 1. ОҚУШЫНЫҢ ДЕРЕКТЕРІ
# =========================================================

if not st.session_state.student_started:

    st.subheader("👤 Оқушы туралы ақпарат")

    student_name = st.text_input(
        "Аты-жөніңіз",
        placeholder="Мысалы: Айдана Қасымова"
    )

    student_class = st.text_input(
        "Сыныбыңыз",
        placeholder="Мысалы: 7А"
    )

    st.divider()

    # =====================================================
    # ТЕСТ ТАҢДАУ
    # =====================================================

    if len(tests) == 0:

        st.warning(
            "⚠️ Қазіргі уақытта дайын тесттер жоқ."
        )

        st.info(
            "Мұғалім тест дайындағаннан кейін қайта кіріңіз."
        )

    else:

        test_names = []

        for i, test in enumerate(tests):

            if isinstance(test, dict):

                name = (
                    test.get("title")
                    or test.get("name")
                    or test.get("topic")
                    or f"Тест {i + 1}"
                )

            else:
                name = f"Тест {i + 1}"

            test_names.append(name)

        selected_test_name = st.selectbox(
            "📚 Тестті таңдаңыз",
            test_names,
            key="student_test_select"
        )

        st.divider()

        if st.button(
            "🚀 ТЕСТТІ БАСТАУ",
            use_container_width=True
        ):

            if student_name.strip() == "":
                st.warning(
                    "⚠️ Аты-жөніңізді енгізіңіз."
                )

            elif student_class.strip() == "":
                st.warning(
                    "⚠️ Сыныбыңызды енгізіңіз."
                )

            else:

                selected_index = test_names.index(
                    selected_test_name
                )

                st.session_state.student_name = (
                    student_name.strip()
                )

                st.session_state.student_class = (
                    student_class.strip()
                )

                st.session_state.selected_test = (
                    tests[selected_index]
                )

                st.session_state.student_started = True
                st.session_state.finished = False

                st.rerun()


# =========================================================
# 2. ТЕСТ БӨЛІМІ
# =========================================================

if st.session_state.student_started:

    test = st.session_state.selected_test

    st.success(
        f"👋 Сәттілік, {st.session_state.student_name}!"
    )

    st.write(
        f"🏫 Сыныбы: *{st.session_state.student_class}*"
    )

    # -----------------------------------------------------
    # Тест атауы
    # -----------------------------------------------------

    if isinstance(test, dict):

        test_title = (
            test.get("title")
            or test.get("name")
            or test.get("topic")
            or "Тест"
        )

        questions = (
            test.get("questions")
            or test.get("items")
            or []
        )

    else:

        test_title = "Тест"
        questions = test

    st.divider()

    st.header(f"📝 {test_title}")

    # -----------------------------------------------------
    # Егер сұрақтар табылмаса
    # -----------------------------------------------------

    if not questions:

        st.error(
            "❌ Бұл тестте сұрақтар табылмады."
        )

    else:

        st.write(
            f"📌 Сұрақ саны: *{len(questions)}*"
        )

        st.divider()

        # -------------------------------------------------
        # СҰРАҚТАР
        # -------------------------------------------------

        for i, question in enumerate(questions):

            if not isinstance(question, dict):
                continue

            question_text = (
                question.get("question")
                or question.get("text")
                or f"{i + 1}-сұрақ"
            )

            options = (
                question.get("options")
                or question.get("answers")
                or []
            )

            st.subheader(
                f"{i + 1}. {question_text}"
            )

            if options:

                st.radio(
                    "Жауабыңызды таңдаңыз:",
                    options,
                    key=f"student_answer_{i}",
                    index=None
                )

            else:

                st.warning(
                    "Бұл сұрақтың жауап нұсқалары жоқ."
                )

        st.divider()

        # -------------------------------------------------
        # ТЕСТІ АЯҚТАУ
        # -------------------------------------------------

        if st.button(
            "✅ ТЕСТІ АЯҚТАУ",
            use_container_width=True
        ):

            score = 0
            unanswered = 0

            # ---------------------------------------------
            # ЖАУАПТАРДЫ ТЕКСЕРУ
            # ---------------------------------------------

            for i, question in enumerate(questions):

                if not isinstance(question, dict):
                    continue

                correct_answer = question.get(
                    "answer"
                )

                user_answer = st.session_state.get(
                    f"student_answer_{i}"
                )

                if user_answer is None:
                    unanswered += 1

                elif user_answer == correct_answer:
                    score += 1

            total = len(questions)

            st.session_state.score = score
            st.session_state.total = total
            st.session_state.finished = True

            st.rerun()


# =========================================================
# 3. НӘТИЖЕ
# =========================================================

if st.session_state.finished:

    st.divider()

    st.header("🏆 ТЕСТ НӘТИЖЕСІ")

    score = st.session_state.score
    total = st.session_state.total

    if total > 0:
        percentage = round(
            score / total * 100
        )
    else:
        percentage = 0

    st.success(
        f"👤 Оқушы: {st.session_state.student_name}"
    )

    st.info(
        f"🏫 Сыныбы: {st.session_state.student_class}"
    )

    st.write("")

    st.metric(
        "Жинаған ұпай",
        f"{score} / {total}"
    )

    st.metric(
        "Нәтиже",
        f"{percentage}%"
    )

    st.divider()

    # -----------------------------------------------------
    # БАҒАЛАУ
    # -----------------------------------------------------

    if percentage >= 90:

        st.balloons()

        st.success(
            "🌟 Өте жақсы! Жарайсың!"
        )

    elif percentage >= 70:

        st.success(
            "👍 Жақсы нәтиже!"
        )

    elif percentage >= 50:

        st.warning(
            "🙂 Жаман емес. Тақырыпты тағы бір қайталап көр."
        )

    else:

        st.error(
            "📚 Тақырыпты қайта қарап шыққан дұрыс."
        )

    st.divider()

    st.info(
        "ℹ️ Тест аяқталды. Нәтиже көрсетілді."
    )

    # -----------------------------------------------------
    # ҚАЙТА БАСТАУ
    # -----------------------------------------------------

    if st.button(
        "🔄 ЖАҢА ТЕСТ БАСТАУ",
        use_container_width=True
    ):

        # Тек оқушы сессиясын тазалаймыз
        for key in list(st.session_state.keys()):

            if key.startswith("student_answer_"):
                del st.session_state[key]

        st.session_state.student_started = False
        st.session_state.finished = False
        st.session_state.selected_test = None
        st.session_state.score = 0
        st.session_state.total = 0

        st.rerun()
