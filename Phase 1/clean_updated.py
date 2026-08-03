import pandas as pd
import streamlit as st 
import os

# Purana test code — abhi zaroorat nahi, isliye comment mein rakha hai
"""dp= pd.DataFrame({
    "name":["aa","bb","cc"],
    "age":[12,23,45],
    "no":[11,22,33]
}
)
print(dp)"""

# ----------------------------------------
# STEP 1: DATA LOAD KARNA
# ----------------------------------------
df = pd.read_csv("dataset\student_dataset.csv")

# ----------------------------------------
# STEP 2: DATA CLEANING
# ----------------------------------------

# Duplicates check karo
print("your duplicate :", df.duplicated().sum())

# df = zaroori hai warna original df update nahi hoga!
df = df.drop_duplicates()

print(df.value_counts().sum())
print(df.info())
print(df.isnull().sum())
print(df.describe())
print(df["Student_ID"].unique())

# ----------------------------------------
# STEP 3: DONO DATASETS MERGE KARNA
# ----------------------------------------
df1 = pd.read_csv("dataset\student_info.csv")

# Student_ID ke basis pe dono datasets merge karo
final1 = pd.merge(df, df1, on="Student_ID")

# Sirf zaroori columns rakho
final1 = final1[["Student_ID", "Name", "Section", "Branch", 
                  "Attendance(%)", "Internal_Marks", 
                  "Assignments_Submitted", "Previous_Sem_Result(%)"]]

# index=False — extra index column CSV mein nahi aayega
final1.to_csv("final_cleared.csv", index=False)
print("Data cleared")

# ----------------------------------------
# STEP 4: WEIGHTAGE
# Attendance     → 25%
# Internal Marks → 25%
# Assignments    → 20%
# Previous SGPA  → 30%
# ----------------------------------------

# ----------------------------------------
# STEP 5: ZONE CLASSIFY KARNA
# .apply() use karo — har student pe alag function chalata hai
# ----------------------------------------
def classify(score):
    if score >= 70:
        return "Green"
    elif score >= 45:
        return "Yellow"
    else:
        return "Red"

# ----------------------------------------
# STEP 6: STREAMLIT DASHBOARD
# ----------------------------------------
def dash():
    if st.button("📊 Dashboard visual"):
        os.startfile(r"C:\Users\Asus\OneDrive\Desktop\Project & internship\college project\college demo.pbix")

        st.info("""
          Power BI khul raha hai...
          Khulne ke baad:
        👉 Home → Refresh button dabao
        👉 For Latest Report!
        """)


def weight():
    global final1  # bahar wala final1 use karo

    st.write("Kripya is order mein select karo:")
    st.write("1️⃣ Attendance | 2️⃣ Internal Marks | 3️⃣ Assignments | 4️⃣ Previous SGPA")

    # User se exactly 4 columns select karwao
    column = st.multiselect("", final1.columns, max_selections=4)

    # Slider — number_input pe empty crash hota tha
    a = st.slider("Total Internal Marks:", min_value=1, max_value=100, value=30)
    b = st.slider("Total Assignments:", min_value=1, max_value=20, value=5)

    # Sirf tab aage badho jab poore 4 columns select ho
    if len(column) == 4:
        st.success("Columns has been selected")
        st.write("columns selected :", column)

        # NORMALIZATION — sabko 0-100 scale pe lao
        # Attendance already % mein hai
        attendance = final1[column[0]]

        # Internal marks normalize karo: (marks/total) * 100
        Internal = (final1[column[1]] / a) * 100

        # Assignments normalize karo: (submitted/total) * 100
        Assignment = (final1[column[2]] / b) * 100

        # Previous SGPA already % mein hai
        Previous = final1[column[3]]

        # WEIGHTED SCORE CALCULATE KARO
        result = ((attendance * 0.25) + (Internal  * 0.25) +
                  (Assignment * 0.20) + (Previous  * 0.30))

        # Risk Score column add karo — agar nahi hai toh add ho jaayega
        final1['Risk_Score'] = result.round(2)

        # .apply() har student ke score pe classify() chalata hai
        final1['Risk_Zone'] = final1['Risk_Score'].apply(classify)

        # Updated CSV save karo — Power BI mein import hoga
        final1.to_csv("updated_finalset.csv", index=False)

        # Result table dikhao
        #st.dataframe(final1[['Student_ID', 'Name', 'Risk_Score', 'Risk_Zone']])
        dash()

    else:
        st.error("Select your columns please")


weight()

