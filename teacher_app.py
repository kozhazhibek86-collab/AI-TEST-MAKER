import streamlit as st
import json
import os
import requests
import pandas as pd


# ============================================================
# БЕТ БАПТАУ
# ============================================================

st.set_page_config(
    page_title="AI Test Maker - Мұғалім",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# GOOGLE APPS SCRIPT URL
# ============================================================

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwgJoktoyeeNtlmFrNKWD6kTwBeDVDnKbriNrEZ0Aa_1EdaCVq4OuXs2YcigxhpQikU/exec"


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
    font-size: 18px;
    color: #666;
    margin-bottom: 25px;
}

.info-card {
    background-color: #f5f7fa;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
}

.result-card {
    background-color: #f0f8ff;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TESTS.JSON ЖҮКТЕУ
# ============================================================

def load_tests():

    file_path = "tests.json"

    if not os.path.exists(file_path):

        st.error("❌ tests.json файлы табылмады!")

        return {}

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as e:

        st.error(
            f"❌ tests.json оқу кезінде қате: {e}"
        )

        return {}


tests_data = load_tests()


# ============================================================
# GOOGLE SHEETS-ТЕН НӘТИЖЕ ОҚУ
# ============================================================

def load_results():

    try:

        response = requests.get(
            GOOGLE_SCRIPT_URL,
            timeout=15
        )

        if response.status_code != 200:

            return []

        data = response.json()

        if isinstance(data, list):

            return data

        return []

    except Exception as e:

        st.error(
            f"❌ Нәтижелерді жүктеу кезінде қате: {e}"
        )

        return []


# ============================================================
# НӘТИЖЕЛЕРДІ ҚАЛЫПҚА КЕЛТІРУ
# ============================================================

def normalize_results(data):

    results = []

    for row in data:

        if not isinstance(row, dict):
            continue

        student = (
            row.get("Оқушы")
            or row.get("student")
            or row.get("student_name")
            or ""
        )

        grade = (
            row.get("Сынып")
            or row.get("grade")
            or ""
        )

        topic = (
            row.get("Тақырып")
            or row.get("topic")
            or ""
        )

        correct = (
            row.get("Дұрыс жауап")
            or row.get("correct")
            or 0
        )

        total = (
            row.get("Барлық сұрақ")
            or row.get("total")
            or 0
        )

        percent = (
            row.get("Нәтижелер %")
            or row.get("Нәтиже %")
            or row.get("percent")
            or 0
        )

        date = (
            row.get("Күні")
            or row.get("date")
            or ""
        )

        try:
            percent = float(
                str(percent)
                .replace("%", "")
                .strip()
            )
        except:
            percent = 0

        results.append({
            "student": str(student),
            "grade": str(grade),
            "topic": str(topic),
            "correct": correct,
            "total": total,
            "percent": percent,
            "date": str(date)
        })

    return results


# ============================================================
# БАСТЫ БЕТ
# ============================================================

st.markdown(
    '<div class="main-title">🎓 AI Test Maker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Мұғалімнің басқару панелі</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# ============================================================
# МӘЗІР
# ============================================================

menu = st.radio(
    "Бөлімді таңдаңыз:",
    [
        "👩‍🏫 Мұғалім",
        "👨‍🎓 Оқушы",
        "📊 Нәтижелер"
    ],
    horizontal=True
)

st.markdown("---")


# ============================================================
# МҰҒАЛІМ РЕЖИМІ
# ============================================================

if menu == "👩‍🏫 Мұғалім":

    st.header("👩‍🏫 Мұғалім режимі")

    if not tests_data:

        st.warning(
            "⚠️ Тесттер табылмады."
        )

    else:

        st.success(
            "✅ Тесттер жүйеге жүктелді."
        )

        st.markdown(
            """
            <div class="info-card">
                <h3>📚 Тесттерді басқару</h3>
                <p>
                Мұнда мұғалім сыныптар мен тақырыптарға
                арналған тесттерді басқара алады.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # СЫНЫПТАР
        # ----------------------------------------------------

        st.subheader("🎓 Сыныптар")

        grades = []

        for key, value in tests_data.items():

            if isinstance(value, dict):

                grade = value.get(
                    "grade",
                    key
                )

                if str(grade) not in grades:

                    grades.append(
                        str(grade)
                    )

        if grades:

            selected_grade = st.selectbox(
                "Сыныпты таңдаңыз:",
                grades
            )

            st.info(
                f"🎓 Таңдалған сынып: **{selected_grade}**"
            )

        else:

            st.warning(
                "Сыныптар табылмады."
            )


# ============================================================
# ОҚУШЫ РЕЖИМІ
# ============================================================

elif menu == "👨‍🎓 Оқушы":

    st.header("👨‍🎓 Оқушы режимі")

    st.info(
        "Оқушылар тестті арнайы оқушы сілтемесі арқылы тапсырады."
    )

    st.write(
        "Оқушы режимінде:"
    )

    st.write(
        "1️⃣ Сыныбын таңдайды"
    )

    st.write(
        "2️⃣ Тақырыбын таңдайды"
    )

    st.write(
        "3️⃣ Аты-жөнін енгізеді"
    )

    st.write(
        "4️⃣ Тест тапсырады"
    )

    st.write(
        "5️⃣ Нәтижесін көреді"
    )


# ============================================================
# НӘТИЖЕЛЕР
# ============================================================

elif menu == "📊 Нәтижелер":

    st.header("📊 Оқушылардың нәтижелері")

    st.write(
        "Оқушылардың тест нәтижелері осы жерде автоматты түрде көрінеді."
    )

    st.markdown("---")


    # ========================================================
    # ЖАҢАРТУ
    # ========================================================

    if st.button(
        "🔄 Нәтижелерді жаңарту",
        use_container_width=True
    ):

        st.rerun()


    # ========================================================
    # GOOGLE SHEETS-ТЕН АЛУ
    # ========================================================

    raw_results = load_results()

    results = normalize_results(
        raw_results
    )


    # ========================================================
    # НӘТИЖЕ ЖОҚ
    # ========================================================

    if not results:

        st.warning(
            "📭 Әзірге нәтижелер жоқ."
        )

        st.info(
            "Оқушы тест тапсырғаннан кейін "
            "нәтиже осы бөлімде пайда болады."
        )

    else:

        # ====================================================
        # СҮЗГІЛЕР
        # ====================================================

        grades = sorted(
            list(
                set(
                    r["grade"]
                    for r in results
                    if r["grade"]
                )
            )
        )

        topics = sorted(
            list(
                set(
                    r["topic"]
                    for r in results
                    if r["topic"]
                )
            )
        )


        col1, col2 = st.columns(2)


        with col1:

            grade_filter = st.selectbox(
                "🎓 Сынып:",
                ["Барлық сыныптар"] + grades
            )


        with col2:

            topic_filter = st.selectbox(
                "📚 Тақырып:",
                ["Барлық тақырыптар"] + topics
            )


        # ====================================================
        # СҮЗГІЛЕУ
        # ====================================================

        filtered = []

        for result in results:

            if (
                grade_filter !=
                "Барлық сыныптар"
                and
                result["grade"] !=
                grade_filter
            ):

                continue


            if (
                topic_filter !=
                "Барлық тақырыптар"
                and
                result["topic"] !=
                topic_filter
            ):

                continue


            filtered.append(
                result
            )


        st.markdown("---")


        # ====================================================
        # СТАТИСТИКА
        # ====================================================

        st.subheader("📈 Жалпы статистика")


        total_students = len(
            filtered
        )


        if total_students > 0:

            average = round(
                sum(
                    r["percent"]
                    for r in filtered
                )
                /
                total_students
            )

            excellent = sum(
                1
                for r in filtered
                if r["percent"] >= 90
            )

            good = sum(
                1
                for r in filtered
                if 70 <= r["percent"] < 90
            )

            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "👥 Оқушы",
                    total_students
                )


            with col2:

                st.metric(
                    "📊 Орташа",
                    f"{average}%"
                )


            with col3:

                st.metric(
                    "🏆 90%+",
                    excellent
                )


            with col4:

                st.metric(
                    "👍 70–89%",
                    good
                )


        st.markdown("---")


        # ====================================================
        # НӘТИЖЕЛЕР КЕСТЕСІ
        # ====================================================

        st.subheader(
            "📋 Нәтижелер"
        )


        table_data = []


        for result in filtered:

            table_data.append({

                "Күні":
                    result["date"],

                "Оқушы":
                    result["student"],

                "Сынып":
                    result["grade"],

                "Тақырып":
                    result["topic"],

                "Дұрыс жауап":
                    result["correct"],

                "Барлық сұрақ":
                    result["total"],

                "Нәтиже %":
                    f'{result["percent"]:.0f}%'

            })


        if table_data:

            df = pd.DataFrame(
                table_data
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


            # =================================================
            # ОҚУШЫЛАРДЫ ЖЕКЕ КӨРСЕТУ
            # =================================================

            st.markdown("---")

            st.subheader(
                "👤 Оқушылардың нәтижелері"
            )


            for result in filtered:

                percent = result[
                    "percent"
                ]


                if percent >= 90:

                    status = "🏆 Өте жақсы"

                elif percent >= 70:

                    status = "👍 Жақсы"

                elif percent >= 50:

                    status = "🙂 Қанағаттанарлық"

                else:

                    status = "📚 Қайта қарау қажет"


                with st.expander(
                    f'👤 {result["student"]} — {percent:.0f}%'
                ):

                    c1, c2, c3 = st.columns(3)


                    with c1:

                        st.write(
                            f'🎓 **Сынып:** '
                            f'{result["grade"]}'
                        )

                        st.write(
                            f'📚 **Тақырып:** '
                            f'{result["topic"]}'
                        )


                    with c2:

                        st.write(
                            f'✅ **Дұрыс:** '
                            f'{result["correct"]} / '
                            f'{result["total"]}'
                        )

                        st.write(
                            f'📊 **Нәтиже:** '
                            f'{percent:.0f}%'
                        )


                    with c3:

                        st.write(
                            f'📅 **Күні:** '
                            f'{result["date"]}'
                        )

                        st.write(
                            f'📌 **Баға:** '
                            f'{status}'
                        )


            # =================================================
            # CSV ЖҮКТЕУ
            # =================================================

            st.markdown("---")

            csv_data = df.to_csv(
                index=False
            ).encode(
                "utf-8-sig"
            )

            st.download_button(
                "📥 Нәтижелерді жүктеу",
                data=csv_data,
                file_name="test_results.csv",
                mime="text/csv",
                use_container_width=True
            )


        else:

            st.info(
                "🔍 Таңдалған сынып немесе тақырып бойынша нәтиже жоқ."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🎓 AI Test Maker | Мұғалім режимі"
)
