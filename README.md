# UOBLearn
  It should include: 
1) A brief description of the system and its purpose (max 200 words);
2) step-by-step instructions on how to run the project;
3) list of programming languages, frameworks, or tools used;
4) a summary of implemented functionalities; 
5) describe the contribution percentage to the project and describe the specific work done.

### What is UOBLearn and its purpose
UOBLearn is a support platform specifically designed  for Computer Science students at the University of Birmingham. Its primary purpose is to help students who are struggling with a certain aspect of their course or module by offering quick access to high-quality, free online resources and one-to-one academic support from mentors. 

By centralising academic resources and personalised mentorship in a singular platform, UOBLearn aims to encourage students to take greater ownership of their learning.

While platforms like Canvas offer core course materials, they don’t offer a space for students to access tailored content or request one-to-one academic mentorship. UOBLearn fills this gap in the university’s existing systems by combining curated resources with a mentoring system that directly connects students to university professors for extra support.

We implemented three key features in this prototype: 
- users can securely log in
- search for available topics and save useful resources
- request academic support from registered mentors and schedule one-to-one sessions based on availability and shared interests.
  
This prototype demonstrates the fundamental functionality of the UOBLearn platform that would be essential in the full-scale implementation showcasing the core architecture and operation of the UOBLearn platform.


### How to Run the Project

---

#### 1. **Prerequisites**

Ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)
- A database system (e.g., SQLite, MySQL, or PostgreSQL)
- Git (optional, for cloning the repository)



#### 2. **Optional: Clone the Repository**

If any files are missing or if you prefer working with Git, you can clone the repository as follows:

```bash
git clone https://github.com/Esports-Medusa/UOBLearn.git
cd UOBLearn
```

#### 3. **Set Up a Virtual Environment**

Create and activate the virtual environment:

```bash
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows
```

#### 4. **Install Dependencies**

```bash
pip install -r requirements.txt
```

#### 5. **Configure Environment Variables**

The current prototype uses a `.flaskenv` file for local development with the following content:

```env
FLASK_APP=run.py
FLASK_ENV=development
```

A separate .env file is not required unless you wish to override the default settings defined in config.py.

For reference, the system is preconfigured as follows:

```python
# config.py
SECRET_KEY = os.environ.get('SECRET_KEY') or b'WR#&f&+%78er0we=%799eww+#7^90-;s'
SQLALCHEMY_DATABASE_URI = 'sqlite:///app/data/data.sqlite'
```

If you plan to use MySQL or PostgreSQL, you can override the database URL:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

#### 6. **Initialize the Database**

```bash
flask db init      # Only needed if migrations folder is missing
flask db migrate   # Generate migration scripts
flask db upgrade   # Apply migrations
```

#### 7. **Run the Application**

```bash
flask run
```
The app will be accessible at: http://localhost:5000

#### 8. **Verify the Setup**

1. Open `http://localhost:5000/register` in a browser.

2. Test registration:
   - **Student**: Fill in student fields (e.g., interests)
   - **Mentor**: Fill in mentor fields (e.g., expertise, available hours)

3. Log in with the created account to ensure basic functionality works.

#### 9. Sample Accounts

You may use the following pre-defined accounts for testing login:

**🧑‍🎓 Students**

| Email               | Password   |
|---------------------|------------|
| student1@uob.edu    | password1  |
| student2@uob.edu    | password2  |
| student3@uob.edu    | password3  |
| student4@uob.edu    | password4  |
| student5@uob.edu    | password5  |
| student6@uob.edu    | password6  |
| student7@uob.edu    | password7  |
| student8@uob.edu    | password8  |
| student9@uob.edu    | password9  |
| student10@uob.edu   | password10 |

**👨‍🏫 Mentors**

| Email               | Password   |
|---------------------|------------|
| mentor1@uob.edu     | password1  |
| mentor2@uob.edu     | password2  |
| mentor3@uob.edu     | password3  |
| mentor4@uob.edu     | password4  |
| mentor5@uob.edu     | password5  |
| mentor6@uob.edu     | password6  |
| mentor7@uob.edu     | password7  |
| mentor8@uob.edu     | password8  |
| mentor9@uob.edu     | password9  |
| mentor10@uob.edu    | password10 |

**🛠 Admins**

| Email               | Password   |
|---------------------|------------|
| admin1@uob.edu      | password1  |
| admin2@uob.edu      | password2  |

## Summary of Implemented Functionalities

### Core Functionalities

- **User Authentication (Login System)**  
  Users can log in with predefined credentials that are hardcoded into a database. The system handles both valid and invalid login attempts, providing appropriate feedback.

- **Saved/Favourite Courses**  
  Users can save or favourite a course by clicking a button, which stores it under their profile for easy access later. Only valid courses can be saved.

- **Mentor Request System**  
  Students can request academic support from mentors registered on the platform. They can select a topic, choose a mentor, and send a message to schedule a session. The system validates requests and displays an error if any required field is left empty.

### Technical Implementations

- **Notification System (Publish/Subscribe Pattern)**  
  When a new course is added, all users are automatically notified without querying the system. In this setup, a newly added course acts as the *publisher*, while all registered users function as *subscribers*. This simulates a real-time content update system.

- **Role-Based Structure (Student & Mentor)**  
  The application uses inheritance to distinguish between different user types: Student and Mentor. This allows tailored interactions and features for each role. Mentor-student interaction is modeled using association, as students initiate mentoring requests to specific mentors.

- **Student–Course Relationship**  
  A many-to-many aggregation relationship exists between Students and Courses. Courses can be saved by many students, and each student can save multiple courses. Students are modeled as independent entities, existing outside the context of their courses.

- **User–Appointment Relationship**  
  Users (both students and mentors) have a one-to-many aggregation relationship with appointments. Each appointment must be associated with at least one user, but a user can have multiple appointments. Users exist independently of this relationship.



### Testing Approach

All test cases were written in Python, focusing on visible functionality and expected outcomes. Each team member was assigned specific tests to develop and validate.

Each core feature was tested with both positive and negative test cases to ensure robust functionality and proper error handling:

#### Login Authentication
- **Positive test:** Verified that valid user credentials allowed access to the system.
- **Negative test:** Ensured appropriate error handling for invalid or non-existent user credentials.

#### Mentor Request Form
- **Positive test:** Confirmed that a meeting is successfully created when a student completes and submits the mentor request form correctly.
- **Negative test:** Ensured proper error messaging when the form was submitted with missing or invalid data.

#### Saving Courses
- **Positive test:** Verified that authenticated users can successfully save courses to their account.
- **Negative test:** Ensured that unauthorized users (not logged in) were unable to save a course and received appropriate error feedback.




### Contribution

Team members participated in collaborative discussions, feature reviews, and testing to ensure quality and consistency throughout the development process.

---


| Student Name     | ID      | Contribution (%) | Key Contributions / Tasks Completed                                                                                                | Comments (if any)               | Signature |
| ---------------- | ------- | ---------------- |------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|-----------|
| Jiaqi Yuan       | 2869046 | 20%              | Led development of core features; implemented backend logic for user authentication, course functions, and mentor interactions.    | Username: QiQi / Esports-Medusa | JY        |
| Shadie Abdulkawi | 2878514 | 20%              | Developed the saved courses feature and implemented a corresponding test case. Contributed to frontend and co-directed demo video. |                                 |           |
| Nusrat Begum     | 2246349 | 20%              | Developed test cases for secure login functionality (positive & negative). Co-authored the README documentation.                   |                                 | NB        |
| Nadiya Miah      | 2889339 | 20%              | Developed test cases for mentor request feature (positive & negative). Co-directed the demo video of the system.                   |                                 |           |
| Alisha Thapa     | 2167059 | 20%              | Designed the mentor request form interface. Created a negative test case for saved courses. Co-authored the README Documentation.  |                                 | AT        |

#### Additional comments

---

**Jiaqi Yuan**

> **🗓 Work Log**

| Date       | Description                                                                                                                               |
|------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| 2025-04-29 | Completed the main page and navigation bar for the starter code.                                                                          |
| 2025-04-30 | Completed the login and profile pages for the starter code, and finished initializing the database.                                       |
| 2025-05-01 | Resolved merge conflict errors caused by an incorrect merge into the main branch, within the fix-broken-main branch.                      |
| 2025-05-02 | Reviewed Alisha Thapa’s merge request, made minor adjustments, and completed the merge.                                                   |
| 2025-05-04 | Improved the UI of the login page. Completed the register page and the new course notification feature.                                   |
| 2025-05-05 | Completed the Mentor Appointment feature and the Save/Favourite Course feature.                                                           |
| 2025-05-06 | Fixed a bug in the register page where students and mentors couldn’t register due to validation checking fields intended for other roles. |

> **🛠️ Implemented Features**
- **User registration/login functionality**  
- **Notify all students when a new course is added**  
- **Save/favourite course feature**  
- **Student–mentor appointment scheduling feature**

> **📄 Documentation & Coordination**
- Wrote the 'How to Run the Project' section in the `README.md` file.
- Coordinated version control structure and Git clean-up

---

**Shadie Abdulkawi**


---

**Nusrat Begum**


---

**Nadiya Miah**


---

**Alisha Thapa**
