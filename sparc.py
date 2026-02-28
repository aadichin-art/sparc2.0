from drafter import *
from dataclasses import dataclass
import random

"""
Sparc (Basic Prototype)
Home page: email login
Next page: group of 4, prompt, message box, skip + report
"""

@dataclass
class State:
    email: str
    group: list[str]
    prompt: str
    messages: list[str]
    report_note: str

NAMES = ["Ava", "Jay", "Mia", "Chris", "Noah", "Emma", "Zoe", "Ben"]
PROMPTS = [
    "What’s your go-to spot on campus?",
    "What class surprised you the most?",
    "What’s a hobby you wanna get into?",
    "What’s your current favorite song?",
]

@route
def index(state: State) -> Page:
    return Page(state, [
        "sparc",
        "Enter your university email:",
        TextBox("email", ""),
        Button("Enter", enter_email)
    ])

@route
def enter_email(state: State, email: str) -> Page:
    state.email = email.strip().lower()

    # Validate .edu email
    if not state.email.endswith(".edu") or "@" not in state.email:
        return Page(state, [
            "sparc",
            "Enter your university email:",
            TextBox("email", state.email),
            "Error: Please enter a valid .edu email address.",
            Button("Enter", enter_email)
        ])

    # Extract username
    username = state.email.split("@")[0]

    # Create group
    others = random.sample(NAMES, 3)
    state.group = [username] + others

    # Choose prompt
    state.prompt = random.choice(PROMPTS)

    state.messages = []
    state.report_note = ""

    return group_page(state)

@route
def group_page(state: State) -> Page:
    content = [
        "Your Group",
        "Members:",
        state.group[0],
        state.group[1],
        state.group[2],
        state.group[3],
        "Prompt:",
        state.prompt,
        "Messages:",
    ]

    if state.messages:
        content = content + state.messages
    else:
        content.append("(No messages yet)")

    content = content + [
        "Type a message:",
        TextBox("msg", ""),
        Button("Send", send_message),
        Button("Skip", skip_group),
        Button("Report", report_user),
    ]

    if state.report_note != "":
        content.append(state.report_note)

    return Page(state, content)

@route
def send_message(state: State, msg: str) -> Page:
    msg = msg.strip()
    if msg != "":
        sender = state.email.split("@")[0] if "@" in state.email else state.email
        state.messages.append(sender + ": " + msg)
    return group_page(state)

@route
def skip_group(state: State) -> Page:
    username = state.email.split("@")[0] if "@" in state.email else state.email
    others = random.sample(NAMES, 3)
    state.group = [username] + others
    state.messages = []
    state.report_note = ""
    return group_page(state)

@route
def report_user(state: State) -> Page:
    state.report_note = "Report submitted. This will be reviewed."
    return group_page(state)

start_server(State("", ["", "", "", ""], "", [], ""))