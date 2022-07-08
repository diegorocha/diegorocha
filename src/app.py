from os import path

from click import option
from flask import render_template, Flask

from db import get_curriculum


app = Flask(__name__)


@app.template_filter()
def education_status(status):
    if not status:
        return ""
    status_map = {
        "E": "Em Curso",
        "C": "Concluido",
        "T": "Trancado",
    }
    return status_map.get(status, "")


@app.template_filter()
def job_date(date):
    if not date:
        return "Presente data"
    months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    month_name = months[date.month - 1]
    year = date.year
    return f"{month_name} {year}"


@app.route("/")
def index():
    curriculum = get_curriculum()
    return render_template("home.html", curriculum=curriculum)


@app.route("/404")
def not_found():
    return render_template("not-found.html")


@app.cli.command("generate_static_html")
@option("--directory")
def generate_static_html(directory):
    with app.app_context(), app.test_request_context():
        client = app.test_client()
        for rule in app.url_map.iter_rules():
            output_file = path.join(directory, f"{rule.endpoint}.html")
            print(f"Generating {output_file}")
            response = client.get(rule.rule)
            with open(output_file, "w") as f:
                f.write(response.text)


if __name__ == "__main__":
    app.run()
