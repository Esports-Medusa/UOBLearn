from app import db, app
from models import Course

courses = [
    Course(
        title="AI For Everyone",
        platform="Coursera",
        description="A non-technical course that explains how AI can be used in business.",
        keywords="ai, business, non-coding",
        url="https://www.coursera.org/learn/ai-for-everyone"
    ),
    Course(
        title="Machine Learning",
        platform="Coursera",
        description="Andrew Ng's foundational course in machine learning using Octave/Matlab.",
        keywords="machine learning, ml, beginner",
        url="https://www.coursera.org/learn/machine-learning"
    ),
    Course(
        title="Deep Learning Specialization",
        platform="Coursera",
        description="A 5-course series covering deep learning fundamentals and practice.",
        keywords="deep learning, neural networks, ai",
        url="https://www.coursera.org/specializations/deep-learning"
    ),
    Course(
        title="Python for Everybody",
        platform="Coursera",
        description="Learn Python from scratch — no prior programming experience needed.",
        keywords="python, beginner, programming",
        url="https://www.coursera.org/specializations/python"
    ),
    Course(
        title="Algorithms Part I",
        platform="Coursera",
        description="Introduction to algorithms and data structures in Java from Princeton.",
        keywords="algorithms, data structures, java",
        url="https://www.coursera.org/learn/algorithms-part1"
    )
]

# ✅ 正确的上下文方式
with app.app_context():
    db.create_all()
    db.session.bulk_save_objects(courses)
    db.session.commit()
    print("✅ Sample Coursera courses inserted.")
