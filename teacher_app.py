
import streamlit as st
import json
import os
from datetime import datetime

# ============================================================
# БЕТ БАПТАУ
# ============================================================

st.set_page_config(
    page_title="AI Test Maker - Мұғалім",
    page_icon="🎓",
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
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    font-size: 20px;
    color: #666;
    margin-bottom: 30px;
}

.card {
    background-color: #f7f9fc;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
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
# ФАЙЛДЫ ЖҮКТЕУ
# ============================================================

def load_tests():

    file_path = "tests.json"

    if not os.path.exists(file_path):
        st.error("❌ tests.json файлы табылмады!")
        return {}

    try:

        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as e:

        st.error(f"❌ tests.json оқу кезінде қате: {e}")
        return {}


def load_results():

    file_path = "results.json"

    if not os.path.exists(file_path):
        return []

    try:

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except Exception:
        return []


# ============================================================
# ДЕРЕКТЕР
# ============================================================

tests_data = load_tests()
results_data = load_results()


# ============================================================
# ТАҚЫРЫПТАР МЕН СЫНЫПТАР
# ============================================================

all_grades = []
all_topics = []

for grade_key, grade_data in tests_data.items():

    # grade_key мысалы: "5"

    if isinstance(grade_data, dict):

        grade_value = str(
            grade_data.get("grade", grade_key)
        )

        if grade_value not in all_grades:
            all_grades.append(grade_value)

        for topic_name, topic_data in grade_data.items():

            if topic_name in [
                "grade",
                "subject"
            ]:
                continue

            if isinstance(topic_data, dict):

                if topic_name not in all_topics:
                    all_topics.append(topic_name)


# Егер tests.json ескі форматта болса
if not all_grades:

    for topic_name, topic_data in tests_data.items():

        if isinstance(topic_data, dict):

            grade = str(
                topic_data.get("grade", "")
            )

            if grade and grade not in all_grades:
                all_grades.append(grade)

            if topic_name not in all_topics:
                all_topics.append(topic_name)


# ============================================================
# БАСТЫ ТАҚЫРЫП
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
# БАСҚАРУ БӨЛІМДЕРІ
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

    # --------------------------------------------------------
    # ЖАЛПЫ СТАТИСТИКА
    # --------------------------------------------------------

    total_tests = len(all_topics)
    total_grades = len(all_grades)
    total_results = len(results_data)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📚 Барлық тақырып",
            total_tests
        )

    with col2:

        st.metric(
            "🎓 Сынып саны",
            total_grades
        )

    with col3:

        st.metric(
            "📊 Нәтиже саны",
            total_results
        )

    st.markdown("---")

    # --------------------------------------------------------
    # СЫНЫПТАР
    # --------------------------------------------------------

    st.subheader("🎓 Сыныптар")

    if all_grades:

        grade_options = [
            "Барлық сыныптар"
        ] + sorted(
            all_grades,
            key=lambda x: int(x) if x.isdigit() else 999
        )

        selected_grade = st.selectbox(
            "Сыныпты таңдаңыз:",
            grade_options
        )

    else:

        st.warning(
            "⚠️ tests.json ішінде сыныптар табылмады."
        )

        selected_grade = "Барлық сыныптар"

    # --------------------------------------------------------
    # ТАҚЫРЫПТАР
    # --------------------------------------------------------

    st.subheader("📚 Тақырыптар")

    visible_topics = []

    for grade_key, grade_data in tests_data.items():

        if not isinstance(grade_data, dict):
            continue

        grade_value = str(
            grade_data.get("grade", grade_key)
        )

        if (
            selected_grade != "Барлық сыныптар"
            and grade_value != selected_grade
        ):
            continue

        for topic_name, topic_data in grade_data.items():

            if topic_name in [
                "grade",
                "subject"
            ]:
                continue

            if isinstance(topic_data, dict):

                if topic_name not in visible_topics:
                    visible_topics.append(topic_name)

    # Ескі форматты қолдау
    if not visible_topics:

        for topic_name, topic_data in tests_data.items():

            if not isinstance(topic_data, dict):
                continue

            grade_value = str(
                topic_data.get("grade", "")
            )

            if (
                selected_grade == "Барлық сыныптар"
                or grade_value == selected_grade
            ):

                if topic_name not in visible_topics:
                    visible_topics.append(topic_name)

    if visible_topics:

        for topic in visible_topics:

            st.markdown(
                f"""
                <div class="card">
                    📘 <b>{topic}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "Бұл сыныпқа арналған тақырыптар жоқ."
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
# НӘТИЖЕЛЕР РЕЖИМІ
# ============================================================

elif menu == "📊 Нәтижелер":

    st.header("📊 Оқушылардың нәтижелері")

    # --------------------------------------------------------
    # НӘТИЖЕ ЖОҚ БОЛСА
    # --------------------------------------------------------

    if not results_data:

        st.info(
            "📭 Әзірге оқушылардың нәтижелері жоқ."
        )

        st.write(
            "Оқушылар тест тапсырып болғаннан кейін "
            "нәтижелер осы жерде көрсетіледі."
        )

    else:

        # ----------------------------------------------------
        # СҮЗГІЛЕР
        # ----------------------------------------------------

        result_grades = []

        result_topics = []

        for result in results_data:

            grade = str(
                result.get("grade", "")
            )

            topic = str(
                result.get("topic", "")
            )

            if grade and grade not in result_grades:
                result_grades.append(grade)

            if topic and topic not in result_topics:
                result_topics.append(topic)

        col1, col2 = st.columns(2)

        with col1:

            grade_filter = st.selectbox(
                "🎓 Сынып:",
                ["Барлық сыныптар"] + sorted(
                    result_grades,
                    key=lambda x: int(x)
                    if x.isdigit() else 999
                )
            )

        with col2:

            topic_filter = st.selectbox(
                "📚 Тақырып:",
                ["Барлық тақырыптар"] + sorted(
                    result_topics
                )
            )

        # ----------------------------------------------------
        # СҮЗГІЛЕНГЕН НӘТИЖЕЛЕР
        # ----------------------------------------------------

        filtered_results = []

        for result in results_data:

            result_grade = str(
                result.get("grade", "")
            )

            result_topic = str(
                result.get("topic", "")
            )

            grade_ok = (
                grade_filter == "Барлық сыныптар"
                or result_grade == grade_filter
            )

            topic_ok = (
                topic_filter == "Барлық тақырыптар"
                or result_topic == topic_filter
            )

            if grade_ok and topic_ok:

                filtered_results.append(result)

        st.markdown("---")

        # ----------------------------------------------------
        # СТАТИСТИКА
        # ----------------------------------------------------

        st.subheader("📈 Статистика")

        total_students = len(filtered_results)

        if total_students > 0:

            total_percent = 0

            for result in filtered_results:

                total_percent += float(
                    result.get("percentage", 0)
                )

            average = round(
                total_percent / total_students
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "👥 Оқушы саны",
                    total_students
                )

            with c2:

                st.metric(
                    "📊 Орташа нәтиже",
                    f"{average}%"
                )

            with c3:

                excellent = 0

                for result in filtered_results:

                    if float(
                        result.get(
                            "percentage",
                            0
                        )
                    ) >= 90:

                        excellent += 1

                st.metric(
                    "🏆 90%+",
                    excellent
                )

        else:

            st.info(
                "Таңдалған сүзгі бойынша нәтиже жоқ."
            )

        st.markdown("---")

        # ----------------------------------------------------
        # ОҚУШЫ НӘТИЖЕЛЕРІ
        # ----------------------------------------------------

        st.subheader("📋 Оқушылар тізімі")

        for index, result in enumerate(
            filtered_results
        ):

            student_name = result.get(
                "student_name",
                "Белгісіз оқушы"
            )

            grade = result.get(
                "grade",
                ""
            )

            topic = result.get(
                "topic",
                ""
            )

            score = result.get(
                "score",
                0
            )

            total = result.get(
                "total",
                0
            )

            percentage = result.get(
                "percentage",
                0
            )

            date = result.get(
                "date",
                ""
            )

            if float(percentage) >= 90:

                status = "🏆 Өте жақсы"
                message_type = "success"

            elif float(percentage) >= 70:

                status = "👍 Жақсы"
                message_type = "info"

            elif float(percentage) >= 50:

                status = "🙂 Қанағаттанарлық"
                message_type = "warning"

            else:

                status = "📚 Қайта оқу қажет"
                message_type = "error"

            with st.expander(
                f"👤 {student_name} — {percentage}%"
            ):

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"🎓 *Сынып:* {grade}"
                    )

                    st.write(
                        f"📚 *Тақырып:* {topic}"
                    )

                with col2:

                    st.write(
                        f"✅ *Дұрыс:* {score} / {total}"
                    )

                    st.write(
                        f"📊 *Нәтиже:* {percentage}%"
                    )

                with col3:

                    st.write(
                        f"📅 *Күні:* {date}"
                    )

                    st.write(
                        f"📌 *Баға:* {status}"
                    )

        # ----------------------------------------------------
        # CSV КӨРІНІСІ
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader("📥 Нәтижелерді жүктеу")

        import pandas as pd

        export_data = []

        for result in filtered_results:

            export_data.append({
                "Оқушы": result.get(
                    "student_name",
                    ""
                ),
                "Сынып": result.get(
                    "grade",
                    ""
                ),
                "Тақырып": result.get(
                    "topic",
                    ""
                ),
                "Дұрыс жауап": result.get(
                    "score",
                    0
                ),
                "Барлық сұрақ": result.get(
                    "total",
                    0
                ),
                "Нәтиже %": result.get(
                    "percentage",
                    0
                ),
                "Күні": result.get(
                    "date",
                    ""
                )
            })

        if export_data:

            df = pd.DataFrame(
                export_data
            )

            csv = df.to_csv(
                index=False
            ).encode(
                "utf-8-sig"
            )

            st.download_button(
                "📥 Excel/CSV форматында жүктеу",
                csv,
                "test_results.csv",
                "text/csv",
                use_container_width=True
            )


# ============================================================
# ТӨМЕНГІ АҚПАРАТ
# ============================================================

st.markdown("---")

st.caption(
    "🎓 AI Test Maker | Мұғалімнің басқару панелі"
)
