import random

# Sample question banks (You can expand these)
physics_questions = [
    "A body is dropped from a height. What is its velocity after 3 seconds? (Assume g = 9.8 m/s²)",
    "Describe the principle of conservation of momentum with an example.",
    "Derive the equation for centripetal force in circular motion.",
    "Explain the working of a Carnot engine.",
    "What are the dimensions of Planck’s constant?"
]

chemistry_questions = [
    "What is the IUPAC name of CH3-CH2-OH?",
    "Explain the concept of hybridization with an example.",
    "Differentiate between ionic and covalent bonds.",
    "Describe the extraction of aluminium from bauxite.",
    "What is the pH of a 0.001 M HCl solution?"
]

biology_questions = [
    "Explain the structure of a nephron with a labeled diagram.",
    "What is the function of the placenta during pregnancy?",
    "Describe the process of photosynthesis and write the balanced equation.",
    "Differentiate between mitosis and meiosis.",
    "What is the role of tRNA in protein synthesis?"
]

# Function to generate the paper
def generate_neet_paper(num_questions=5):
    paper = []

    paper.append("NEET Practice Question Paper\n")
    paper.append("Section A: Physics")
    for q in random.sample(physics_questions, min(num_questions, len(physics_questions))):
        paper.append(f" - {q}")

    paper.append("\nSection B: Chemistry")
    for q in random.sample(chemistry_questions, min(num_questions, len(chemistry_questions))):
        paper.append(f" - {q}")

    paper.append("\nSection C: Biology")
    for q in random.sample(biology_questions, min(num_questions, len(biology_questions))):
        paper.append(f" - {q}")

    return '\n'.join(paper)

# Output the question paper
print(generate_neet_paper())
