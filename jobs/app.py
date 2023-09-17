from flask import Flask, render_template, g
import sqlite3

PATH = "db/jobs.sqlite"

app = Flask(__name__)


def open_connection():
    connection = None
    connection = getattr(g, '_connection', None)
    if connection == None:
        connection
        g._connection = sqlite3.connect(PATH)
        connection = g._connection

    connection.row_factory = sqlite3.Row
    return connection


def execute_sql(sql, values: tuple = (), commit: bool = False, single: bool = False):
    connection: sqlite3.Connection = open_connection()
    cursor: sqlite3.Cursor = connection.execute(sql, values)

    if commit:
        results = connection.commit()
        return results
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results


@app.route("/")
@app.route("/jobs")
def jobs():
    jobs = execute_sql(
        sql='SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)


@app.route("/job/<job_id>")
def job(job_id):
    job = execute_sql(sql='SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?', values=[
                      job_id], single=True)
    return render_template('job.html', job_data=job)


@app.teardown_appcontext
def close_connection(exeption):
    connection: sqlite3.Connection | None = getattr(g, '_connection', None)
    if connection != None:
        connection.close()
