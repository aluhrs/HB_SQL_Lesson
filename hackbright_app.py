import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def get_project_by_title(title):
    query = """SELECT id, title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Title: %s
Description: %s
Grade: %s""" % (row[1], row[2], row[3]) 

def get_grade_by_project(project):
    query = """SELECT first_name, last_name, grade FROM Grades JOIN Students 
                ON github = student_github WHERE project_title = ?"""
    DB.execute(query, (project,))
    row = DB.fetchone()
    print """\
Student Name: %s %s
Project: %s
Grade: %d""" % (row[0], row[1], project, row[2])

def show_all_grades(first_name, last_name):
    #github_query = """SELECT github From Students
                #WHERE first_name = ? and last_name = ?"""
    # print "First Name: '%s', Last Name: '%s'" % (first_name, last_name)
    #DB.execute(github_query, (first_name, last_name))
    #github = DB.fetchone()
    # print github[0]
    query = """SELECT project_title, grade FROM Grades 
                JOIN Students
                ON github = student_github
                WHERE first_name = ? AND last_name = ?"""
    DB.execute(query, (first_name, last_name))
    row = DB.fetchone()
    print """\
Student Name: %s %s
Project: %s
Grade: %d""" % (first_name, last_name, row[0], row[1])


def make_new_project(title, description, max_grade):
    query = """INSERT INTO Projects (title, description, max_grade) Values (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s" % (title)

def make_new_grade(student_github, project_title, grade):
    query = """INSERT INTO Grades VALUES (?, ?, ?)"""
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    print "Successfully added grade: %s" % (grade)

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(None, 1)
        command = tokens[0]
        arguments = tokens[1]
        arguments1 = arguments.split(",")
        args = [ x.strip() for x in arguments1 ]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "title":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "grades":
            get_grade_by_project(*args)
        elif command == "add_grade":
            make_new_grade(*args)
        elif command == "show_grades":
            show_all_grades(*args)    

    CONN.close()

if __name__ == "__main__":
    main()
