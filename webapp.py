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
    html = render_template("student_info.html", first_name=row['firstname'], last_name=row['lastname'], 
                                    github=row['github'], grades=grades)
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

if __name__ == "__main__":
    app.run(debug=True)