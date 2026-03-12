from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

def init_db():

    conn = sqlite3.connect("reports.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_date TEXT,
        task TEXT,
        learned TEXT,
        tomorrow TEXT
    )
    """)

    conn.commit()
    conn.close()


@app.route("/", methods=["GET","POST"])
def home():

    if request.method == "POST":

        task = request.form["task"]
        learned = request.form["learned"]
        tomorrow = request.form["tomorrow"]

        conn = sqlite3.connect("reports.db")
        c = conn.cursor()

        c.execute(
        "INSERT INTO reports (report_date, task, learned, tomorrow) VALUES (?,?,?,?)",
        (str(date.today()), task, learned, tomorrow)
        )

        conn.commit()
        conn.close()

        return redirect("/reports")

    return render_template("index.html")


@app.route("/reports")
def reports():

    conn = sqlite3.connect("reports.db")
    c = conn.cursor()

    c.execute("SELECT * FROM reports ORDER BY id DESC")

    data = c.fetchall()

    conn.close()

    return render_template("reports.html", reports=data)


@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("reports.db")
    c = conn.cursor()

    c.execute("DELETE FROM reports WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/reports")


@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):

    conn = sqlite3.connect("reports.db")
    c = conn.cursor()

    if request.method == "POST":

        task = request.form["task"]
        learned = request.form["learned"]
        tomorrow = request.form["tomorrow"]

        c.execute("""
        UPDATE reports
        SET task=?, learned=?, tomorrow=?
        WHERE id=?
        """,(task, learned, tomorrow, id))

        conn.commit()
        conn.close()

        return redirect("/reports")

    c.execute("SELECT * FROM reports WHERE id=?", (id,))
    report = c.fetchone()

    conn.close()

    return render_template("edit.html", report=report)


@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("reports.db")
    c = conn.cursor()

    c.execute("SELECT report_date, LENGTH(task)*5 FROM reports")

    rows = c.fetchall()

    conn.close()

    labels = []
    values = []

    for r in rows:
        labels.append(r[0])
        values.append(r[1])

    return render_template(
        "dashboard.html",
        labels=labels,
        values=values
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)