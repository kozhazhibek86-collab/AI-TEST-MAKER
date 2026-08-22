import streamlit as st
import json
import os


# ============================================================
# БЕТ ПАРАМЕТРЛЕРІ
# ============================================================

st.set_page_config(
    page_title="AI Test Maker",
    page_icon="📝",
    layout="centered"
)


# ============================================================
# ТЕСТТЕРДІ ЖҮКТЕУ
# ============================================================

def load_tests():
    file_path = "tests.json"

    if not os.path.exists(file_path):
        st.error("❌ tests.json файлы табылмады!")
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    except json.JSONDecodeError as e:
        st.error("❌ tests.json файлының JSON форматы қате.")
        st.code(str(e))
        return {}

    except Exception as e:
        st.error("❌ Файлды оқу кезінде қате пайда болды.")
        st.code(str(e))
        return {}


# ============================================================
# ДЕРЕКТЕРДІ ТЕСТ ФОРМАТЫНА КЕЛТІРУ
# ============================================================

def prepare_tests(data):

    tests = []

    if not isinstance(data, dict):
        return tests

    # Егер JSON ішінде "tests" деген кілт болса
    if "tests" in data:

        test_data = data["tests"]

        if isinstance(test_data, list):
            for index, test in enumerate(test_data):

                if isinstance(test, dict):
                    test = dict(test)

                    if "title" not in test:
                        test["title"] = f"Тест {index + 1}"

                    tests.append(test)

        elif isinstance(test_data, dict):

            for title, test in test_data.items():

                if isinstance(test, dict):
                    test = dict(test)
                    test.setdefault("title", title)
                    tests.append(test)

        return tests

    # --------------------------------------------------------
    # Сіздің қазіргі tests.json форматыңыз
    #
    # {
    #   "Ақпаратты шифрлау": {
    #       "subject": "Информатика",
    #       "grade": "5",
    #       "questions": [...]
    #   }
    # }
    # --------------------------------------------------------

    for title, test in data.items():

        if isinstance(test, dict):

            prepared_test = dict(test)

            prepared_test.setdefault("title", title)

            tests.append(prepared_test)

    return tests


# ============================================================
# БАСТАПҚЫ ДЕРЕКТЕР
# ============================================================

data = load_tests()

tests = prepare_tests(data)


# ============================================================
# ТАҚЫРЫП
# ============================================================

st.title("📝 AI Test Maker")

st.write(
    "Информатика пәні бойынша тест тапсырмаларын орындаңыз."
)


# ============================================================
# ТЕСТ БАР МА?
# ============================================================

if not tests:

    st.warning("⚠️ Қазіргі уақытта тесттер табылмады.")

    st.write("Тексеріңіз:")

    st.write("1. tests.json файлы GitHub-та бар ма?")

    st.write("2. student_app.py және tests.json бір папкада ма?")

    st.write("3. tests.json дұрыс JSON форматында ма?")

    st.stop()


# ============================================================
# ТЕСТ ТАҢДАУ
# ============================================================

test_titles = []

for test in tests:

    title = test.get("title", "Атаусыз тест")

    test_titles.append(title)


selected_title = st.selectbox(
    "📚 Тестті таңдаңыз:",
    test_titles
)


# ============================================================
# ТАҢДАЛҒАН ТЕСТ
# ============================================================

selected_test = None

for test in tests:

    if test.get("title", "Атаусыз тест") == selected_title:
        selected_test = test
        break


if selected_test is None:
    st.error("❌ Тест табылмады.")
    st.stop()


# ============================================================
# ТЕСТ АҚПАРАТЫ
# ============================================================

subject = selected_test.get(
    "subject",
    "Информатика"
)

grade = selected_test.get(
    "grade",
    ""
)

st.divider()

st.subheader(f"📖 {selected_title}")

st.write(f"*Пәні:* {subject}")

if grade:
    st.write(f"*Сыныбы:* {grade}")


# ============================================================
# СҰРАҚТАР
# ============================================================

questions = selected_test.get(
    "questions",
    []
)


if not questions:

    st.warning(
        "⚠️ Бұл тесттің ішінде сұрақтар жоқ."
    )

    st.stop()


st.write(
    f"*Сұрақ саны: {len(questions)}*"
)

st.divider()


# ============================================================
# SESSION STATE
# ============================================================

if "submitted" not in st.session_state:

    st.session_state.submitted = False


# ============================================================
# ЖАУАПТАРДЫ ЖИНАУ
# ============================================================

answers = {}


for i, question in enumerate(questions):

    if not isinstance(question, dict):
        continue

    question_text = question.get(
        "question",
        f"{i + 1}-сұрақ"
    )

    st.markdown(
        f"### {i + 1}. {question_text}"
    )

    options = question.get(
        "options",
        {}
    )

    # Егер options dictionary болса
    if isinstance(options, dict):

        option_keys = list(options.keys())

        option_texts = []

        for key in option_keys:

            option_texts.append(
                f"{key}) {options[key]}"
            )

        selected_answer = st.radio(
            "Жауабыңызды таңдаңыз:",
            option_texts,
            key=f"question_{i}"
        )

        # Таңдалған A/B/C/D әрпін алу
        if selected_answer:

            answers[i] = selected_answer.split(")")[0]

    # Егер options list болса
    elif isinstance(options, list):

        selected_answer = st.radio(
            "Жауабыңызды таңдаңыз:",
            options,
            key=f"question_{i}"
        )

        answers[i] = selected_answer


    st.write("")


# ============================================================
# ТЕСТТІ АЯҚТАУ
# ============================================================

st.divider()

if st.button(
    "✅ Тестті аяқтау",
    type="primary",
    use_container_width=True
):

    score = 0
    total = len(questions)

    results = []

    for i, question in enumerate(questions):

        if not isinstance(question, dict):
            continue

        correct_answer = question.get(
            "answer",
            ""
        )

        user_answer = answers.get(
            i,
            ""
        )

        # Кіші/үлкен әріп айырмашылығын жою
        correct_answer = str(
            correct_answer
        ).strip().upper()

        user_answer = str(
            user_answer
        ).strip().upper()

        is_correct = (
            user_answer == correct_answer
        )

        if is_correct:
            score += 1

        results.append(
            {
                "question": question.get(
                    "question",
                    ""
                ),
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct
            }
        )

    st.session_state.score = score
    st.session_state.total = total
    st.session_state.results = results
    st.session_state.submitted = True


# ============================================================
# НӘТИЖЕ
# ============================================================

if st.session_state.get(
    "submitted",
    False
):

    score = st.session_state.score
    total = st.session_state.total

    if total > 0:

        percent = round(
            score / total * 100
        )

    else:

        percent = 0


    st.divider()

    st.header("🎉 Тест нәтижесі")

    st.metric(
        "Нәтиже",
        f"{score} / {total}"
    )

    st.metric(
        "Пайыз",
        f"{percent}%"
    )


    # Баға
    if percent >= 90:

        st.success(
            "🌟 Өте жақсы! Біліміңіз жоғары деңгейде."
        )

    elif percent >= 70:

        st.success(
            "👍 Жақсы нәтиже!"
        )

    elif percent >= 50:

        st.warning(
            "🙂 Қанағаттанарлық. Тағы да қайталап көріңіз."
        )

    else:

        st.error(
            "📚 Тақырыпты қайта қарап шығу керек."
        )


    # ========================================================
    # ӘР СҰРАҚТЫ ТЕКСЕРУ
    # ========================================================

    st.subheader(
        "📋 Жауаптарды тексеру"
    )


    for i, result in enumerate(
        st.session_state.results
    ):

        st.write(
            f"*{i + 1}. {result['question']}*"
        )

        if result["is_correct"]:

            st.success(
                f"✅ Дұрыс жауап: {result['correct_answer']}"
            )

        else:

            st.error(
                f"❌ Сіздің жауабыңыз: "
                f"{result['user_answer'] or 'Жауап берілмеді'}"
            )

            st.info(
                f"Дұрыс жауап: "
                f"{result['correct_answer']}"
            )


    st.divider()

    if st.button(
        "🔄 Тестті қайта бастау",
        use_container_width=True
    ):

        st.session_state.submitted = False

        st.rerun()


# ============================================================
# ТӨМЕНГІ АҚПАРАТ
# ============================================================

st.divider()

st.caption(
    "AI Test Maker • Информатика пәні"
)
