import pandas as pd
import streamlit as st

# ========================================
# STEP 1: DATA LOAD KARNA
# ========================================

# Student performance dataset load karo
df = pd.read_csv("dataset/student_dataset.csv")

# ========================================
# STEP 2: DATA CLEANING
# ========================================

# Duplicates check karo
print("Duplicates before cleaning:", df.duplicated().sum())

# Duplicates remove karo aur df update karo
# Note: df = zaroori hai — warna original df update nahi hoga!
df = df.drop_duplicates()
print("Duplicates after cleaning:", df.duplicated().sum())

# Missing values check karo
print("\nMissing values per column:")
print(df.isnull().sum())

# Basic statistics dekho
print("\nBasic Statistics:")
print(df.describe())

# Unique Student IDs dekho
print("\nUnique Student IDs:", df["Student_ID"].unique())

# ========================================
# STEP 3: DONO DATASETS MERGE KARNA
# ========================================

# Student info dataset load karo (naam, branch, section)
df1 = pd.read_csv("dataset/student_info.csv")

# Student_ID ke basis pe dono datasets merge karo
final = pd.merge(df, df1, on="Student_ID")

# Available columns dekho
print("\nFinal Dataset Columns:", final.columns.tolist())

# Cleaned data save karo
final.to_csv("final_cleared.csv", index=False)
print("\nData successfully cleaned and saved!")

# ========================================
# STEP 4: RISK DETECTION SYSTEM
# ========================================

"""
Weighted Scoring Formula:
- Attendance       → 25% weight
- Internal Marks   → 25% weight  
- Assignments      → 20% weight
- Previous SGPA    → 30% weight (sabse strong predictor)

Zones:
- Green  (Safe)          → Score >= 70
- Yellow (Moderate Risk) → Score 45 to 70
- Red    (High Risk)     → Score < 45
"""

def classify(score):
    """Har student ka score dekhke zone assign karo"""
    if score >= 70:
        return "Green"
    elif score >= 45:
        return "Yellow"
    else:
        return "Red"


def weight():
    """
    Main function:
    1. User se columns select karwao
    2. Max marks input lo
    3. Normalize karo (0-100 scale)
    4. Weighted score calculate karo
    5. Risk zone assign karo
    6. Table dikhao
    """

    st.title("🎓 Student Risk Detection System")
    st.markdown("---")

    # ----------------------------------------
    # COLUMN SELECTION
    # ----------------------------------------
    st.subheader("📋 Step 1: Columns Select Karo")
    st.write("⚠️ Kripya **is order mein** select karo:")
    st.write("1️⃣ Attendance | 2️⃣ Internal Marks | 3️⃣ Assignments | 4️⃣ Previous SGPA")

    # User se exactly 4 columns select karwao
    column = st.multiselect(
        "Apne dataset ke columns yahan select karo:",
        final.columns,
        max_selections=4
    )

    st.markdown("---")

    # ----------------------------------------
    # MAX VALUES INPUT (Normalization ke liye)
    # ----------------------------------------
    st.subheader("📊 Step 2: Maximum Values Batao")
    st.write("Yeh values normalization ke liye zaroori hain (0-100 scale pe laane ke liye)")

    # Slider se max marks aur assignments lo
    # Note: Attendance aur Previous SGPA already % mein hain — inhe normalize nahi karna
    a = st.slider("Total Internal Marks (maximum):", min_value=1, max_value=100, value=30)
    b = st.slider("Total Assignments (maximum):", min_value=1, max_value=20, value=5)

    st.markdown("---")

    # ----------------------------------------
    # PROCESSING — sirf tab jab 4 columns select ho
    # ----------------------------------------
    if len(column) == 4:
        st.success("✅ Columns successfully selected!")
        st.write("Selected columns:", column)

        # NORMALIZATION — sabko 0-100 scale pe lao
        # Attendance already % mein hai — kuch nahi karna
        attendance = final[column[0]]

        # Internal marks normalize karo: (marks/total) * 100
        Internal = (final[column[1]] / a) * 100

        # Assignments normalize karo: (submitted/total) * 100
        Assignment = (final[column[2]] / b) * 100

        # Previous SGPA already % mein hai — kuch nahi karna
        Previous = final[column[3]]

        # WEIGHTED SCORE CALCULATE KARO
        # Formula: (Attendance*25%) + (Internal*25%) + (Assignment*20%) + (SGPA*30%)
        result = (
            (attendance * 0.25) +
            (Internal   * 0.25) +
            (Assignment * 0.20) +
            (Previous   * 0.30)
        )

        # Risk Score column add karo (2 decimal places)
        final['Risk_Score'] = result.round(2)

        # Har student pe classify() function chalao — .apply() loop ki jagah use hota hai
        # .apply() internally har row pe function chalata hai — fast aur clean!
        final['Risk_Zone'] = final['Risk_Score'].apply(classify)

        # Updated CSV save karo (Power BI mein import hoga)
        final.to_csv("final_with_risk.csv", index=False)

        # ----------------------------------------
        # RESULTS DIKHAO
        # ----------------------------------------
        st.markdown("---")
        st.subheader("📈 Step 3: Results")

        # Zone wise summary
        col1, col2, col3 = st.columns(3)
        with col1:
            green_count = len(final[final['Risk_Zone'] == 'Green'])
            st.metric("🟢 Green (Safe)", green_count)
        with col2:
            yellow_count = len(final[final['Risk_Zone'] == 'Yellow'])
            st.metric("🟡 Yellow (Moderate)", yellow_count)
        with col3:
            red_count = len(final[final['Risk_Zone'] == 'Red'])
            st.metric("🔴 Red (High Risk)", red_count)

        st.markdown("---")

        # Poora table dikhao
        st.subheader("📋 Student Risk Table")
        st.dataframe(
            final[['Student_ID', 'Name', 'Risk_Score', 'Risk_Zone']],
            use_container_width=True
        )

        # At-risk students alag dikhao
        st.subheader("⚠️ At-Risk Students (Red Zone)")
        red_students = final[final['Risk_Zone'] == 'Red']
        if len(red_students) > 0:
            st.error(f"{len(red_students)} students at high risk!")
            st.dataframe(
                red_students[['Student_ID', 'Name', 'Risk_Score']],
                use_container_width=True
            )
        else:
            st.success("Koi student high risk mein nahi hai! 🎉")

        st.success("✅ Data saved to 'final_with_risk.csv' — Power BI mein import kar sakte ho!")

    elif len(column) > 0:
        # Kuch select kiya but 4 nahi
        st.warning(f"⚠️ Abhi {len(column)} column select kiye — poore 4 select karo!")

    else:
        # Kuch bhi select nahi kiya
        st.info("👆 Upar se 4 columns select karo shuru karne ke liye")


# ========================================
# PROGRAM SHURU KARO
# ========================================
weight()