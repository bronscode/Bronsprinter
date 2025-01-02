from fpdf import FPDF
import cups

# def get_project_name_from_repo(repo):
#   if (repo == "")

issues = [
    {
        "assignees": ["StevenBrons"],
        "content": {
            "body": "",
            "number": 19,
            "repository": "bronscode/NxtGen",
            "title": "Initial ontology",
            "type": "Issue",
            "url": "https://github.com/bronscode/NxtGen/issues/19",
        },
        "id": "PVTI_lADOBw9x7c4AIwrvzgQrvVU",
        "labels": ["meta"],
        "repository": "https://github.com/bronscode/NxtGen",
        "status": "This Sprint",
        "title": "Initial ontology",
    },
    {
        "assignees": ["StevenBrons"],
        "content": {
            "body": "",
            "number": 19,
            "repository": "bronscode/NxtGen",
            "title": "Initial ontology",
            "type": "Issue",
            "url": "https://github.com/bronscode/NxtGen/issues/19",
        },
        "id": "PVTI_lADOBw9x7c4AIwrvzgQrvVU",
        "labels": ["meta"],
        "repository": "https://github.com/bronscode/NxtGen",
        "status": "This Sprint",
        "title": "Initial ontology",
    },
]


def get_project_name(repo: str):
    return repo.split("/")[1].capitalize()


def get_or_else(dic, key, default):
    return dic[key] if key in dic else default


def print_issues(issues):
    for issue in issues:
        pdf = FPDF(format=(80, 297))
        content = issue["content"]
        project_name = get_project_name(content["repository"])
        add_issue(
            pdf,
            project_name,
            content["number"],
            content["title"],
            content["body"],
            get_or_else(issue, "assignees", []),
            get_or_else(issue, "labels", []),
        )
        pdf.output("output.pdf")
        conn = cups.Connection()
        conn.printFile("Epson-TM-T88V", "output.pdf", "", {})


def add_item(pdf, key, value):
    pdf.set_font(style="b")
    pdf.write(text=f"{key}: ")
    pdf.set_font(size=12)
    pdf.write(text=f"{value}\n\n")


def add_issue(pdf, project_name, issue_number, title, description, assignees, labels):
    pdf.add_page()
    pdf.set_margin(4)
    pdf.image("logo.png", x=40, y=3, w=40)
    pdf.set_font("Helvetica", size=12, style="b")
    pdf.set_font(style="b")
    pdf.write(text=f"{project_name} #{issue_number}\n\n")

    add_item(pdf, "Title", title)

    if len(assignees) > 0:
        add_item(pdf, "Assignees", ", ".join(assignees))

    if len(labels) > 0:
        add_item(pdf, "Labels", ", ".join(labels))

    if description:
        add_item(pdf, "Description", description)
