grades = {
    "Greg": 75,
    "Rowley": 85,
    "Rodrick": 60,
    "Chirag": 95,
    "Fregley": 78
}

sorted_students = sorted(grades.items(), key=lambda x: x[1], reverse=True)

print("📚 School Rank List:")
for i, (student, grade) in enumerate(sorted_students, 1):
    print(f"{i}. {student} - {grade}%")
