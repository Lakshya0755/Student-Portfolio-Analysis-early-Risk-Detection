import pandas as pd
df= pd.read_csv("student_dataset.csv")
#print(df.head(5))

print("your duplicate :",df.duplicated().sum())
df.drop_duplicates()
print(df.value_counts().sum())
print(df.info())
print(df.isnull().sum())
print(df.describe())

print(df["Student_ID"].unique())
df.to_csv("cleared.csv",index=False)

df1 = pd.read_csv("student_info.csv")

final= pd.merge(df,df1, on="Student_ID")

final1= final[["Student_ID","Name","Section","Branch","Attendance(%)", # ek sai jyda column kai liye[[]] double braket
"Internal_Marks","Assignments_Submitted","Previous_Sem_Result(%)"]]

print(final1)

final.to_csv("final_cleared.csv")
print("Data cleared")
