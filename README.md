# UOBLearn
  It should include: 
1) A brief description of the system and its purpose (max 200 words);
2) step-by-step instructions on how to run the project;
3) list of programming languages, frameworks, or tools used;
4) a summary of implemented functionalities; and 5) describe the contribution percentage to the project and describe the specific work done.


### How to Run the Project

---

#### 1. **Prerequisites**

Ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)
- A database system (e.g., SQLite, MySQL, or PostgreSQL)
- Git (optional, for cloning the repository)

---

#### 2. **Optional: Clone the Repository**

In case any files are missing or you prefer working with Git:

```bash
git clone https://github.com/yourusername/your-project.git
cd your-project
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

Create a .env file in the project root and add the following:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db  # Example for SQLite
```

Adjust DATABASE_URL if using MySQL/PostgreSQL:
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

