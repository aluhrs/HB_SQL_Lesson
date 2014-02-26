from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    # row[0] = first name, row[1] = last name
    grades = hackbright_app.show_all_grades(row['firstname'], row['lastname'])
    html = render_template("student_info.html", first_name=row['firstname'], 
                                last_name=row['lastname'], github=row['github'], grades=grades)
    return html

@app.route("/project")
def get_grade():
    hackbright_app.connect_to_db()
    student_project = request.args.get("project")
    row = hackbright_app.get_grade_by_project(student_project)
    html = render_template("get_grades.html", project=student_project, grades=row)
    return html

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/studentrecord")
def make_new_student():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")
    row = hackbright_app.make_new_student(first_name, last_name, github)
    html = render_template("studentrecord.html", first_name = first_name, last_name = last_name,
                             github = github)
    return html

@app.route("/projectrecord")
def make_new_project():
    hackbright_app.connect_to_db()
    title = request.args.get("title")
    description = request.args.get("description")
    max_grade = request.args.get("max_grade")
    row = hackbright_app.make_new_project(title, description, max_grade)
    html = render_template("projectrecord.html", title=title, description=description, 
                                max_grade=max_grade)
    return html

@app.route("/new_grade")
def make_new_grade():
    hackbright_app.connect_to_db()
    student_github = request.args.get("student_github")
    project_title = request.args.get("project_title")
    grade = request.args.get("grade")
    row = hackbright_app.make_new_grade(student_github, project_title, grade)
    html = render_template("new_grade.html", student_github=student_github, project_title=project_title, grade=grade)
    return html

if __name__ == "__main__":
    app.run(debug=True)