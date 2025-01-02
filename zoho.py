import requests
import json
import dotenv
import datetime
import pickle as pkl
import cups
from fpdf import FPDF

dotenv.load_dotenv()

env = dotenv.dotenv_values()


def get_auth_token():
    url = "https://accounts.zoho.eu/oauth/v2/token"
    params = {
        "refresh_token": env["ZOHO_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
        "client_id": env["ZOHO_CLIENT_ID"],
        "client_secret": env["ZOHO_CLIENT_SECRET"],
    }

    res = requests.post(url, params=params)

    obj = res.json()

    return obj["access_token"]


auth_token = get_auth_token()


def get_tickets():
    url = "https://desk.zoho.eu/api/v1/tickets"
    headers = {
        "Authorization": f"Zoho-oauthtoken {auth_token}",
        "orgId": env["ZOHODESK_ORG_ID"],
    }
    res = requests.get(url, headers=headers)

    return res.json()["data"]


def get_new_tickets():
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(
        days=1
    )  # so we dont print tickets older than 1 day

    # Query Zoho for updated tickets
    tickets = get_tickets()

    try:
        # Get cached tickets
        with open("tickets_cache.pkl", "rb") as f:
            cached_tickets = pkl.load(f)
    except:
        cached_tickets = []

    # Update cache
    with open("tickets_cache.pkl", "wb") as f:
        pkl.dump(tickets, f)


    new_tickets = []
    for ticket in tickets:
        # sanity check: if the ticket is older than 1 day, skip it
        created = datetime.datetime.fromisoformat(ticket["createdTime"].rstrip("Z") + "000")
        if created < yesterday:
            continue
        found = False
        for t2 in cached_tickets:
            if t2["ticketNumber"] == ticket["ticketNumber"]:
                found = True
        if not found:
            new_tickets.append(ticket)

    return new_tickets[:1]


def get_or_else(dic, key, default):
    return dic[key] if key in dic else default


def print_tickets(tickets):
    for ticket in tickets:
        pdf = FPDF(format=(80, 297))
        add_ticket(
            pdf,
            ticket["ticketNumber"],
            ticket["subject"],
            ticket["email"],
            get_or_else(ticket, "labels", []),
        )
        pdf.output("output.pdf")
        conn = cups.Connection()
        conn.printFile("Epson-TM-Thermal", "output.pdf", "", {})


def add_item(pdf, key, value):
    pdf.set_font("Helvetica", size=12, style="b")
    pdf.write(12, txt=f"{key}: ")
    pdf.set_font("Helvetica", size=12, style="b")
    pdf.write(12, txt=f"{value}\n\n")


def add_ticket(pdf, number, title, email, labels):
    pdf.add_page()
    pdf.set_margins(top=4, right=4, left=4)
    # pdf.image("logo.png", x=40, y=3, w=40)
    pdf.set_font("Helvetica", size=12, style="b")
    pdf.write(12, txt=f"#{number}\n\n")

    add_item(pdf, "Title", title)
    add_item(pdf, "From", email)

    if len(labels) > 0:
        add_item(pdf, "Labels", ", ".join(labels))


if __name__ == "__main__":
    tickets = get_new_tickets()
    print_tickets(tickets)
