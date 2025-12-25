def analyze_subjects(marks):
    strong, weak = [], []
    heatmap = {}

    for subject, score in marks.items():
        score = int(score)

        if score >= 75:
            strong.append(subject)
            heatmap[subject] = "green"
        elif score >= 40:
            heatmap[subject] = "yellow"
        else:
            weak.append(subject)
            heatmap[subject] = "red"

    return strong, weak, heatmap


def drift_status(attendance, weak_count):
    attendance = int(attendance)

    if attendance < 70 or weak_count >= 2:
        return "At Risk"
    elif attendance < 80 or weak_count == 1:
        return "Watch List"
    return "Stable"


def risk_score(attendance, weak_count):
    attendance = int(attendance)
    score = 0

    if attendance < 70:
        score += 2
    elif attendance < 80:
        score += 1

    score += weak_count
    return score


def risk_reasons(attendance, weak_subjects):
    attendance = int(attendance)
    reasons = []

    if attendance < 70:
        reasons.append("Attendance below 70%")

    if weak_subjects:
        reasons.append(
            "Weak performance in subjects: " + ", ".join(weak_subjects)
        )

    if not reasons:
        reasons.append("No major academic risks detected")

    return reasons


def rescue_plan(attendance, weak_subjects):
    attendance = int(attendance)
    plans = []

    if attendance < 75:
        plans.append("Improve attendance through regular class participation")

    for subject in weak_subjects:
        plans.append(f"Attend remedial classes for {subject}")

    if not plans:
        plans.append("Maintain current academic performance")

    return plans
