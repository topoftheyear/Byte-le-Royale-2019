
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout import FloatContainer, Float
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea, SearchToolbar, Dialog, Label, Button, RadioList
from prompt_toolkit.eventloop import use_asyncio_event_loop
from prompt_toolkit.application import get_app
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.key_binding.bindings.scroll import scroll_page_up, scroll_page_down, scroll_one_line_down, scroll_one_line_up

import requests
from requests.auth import HTTPBasicAuth
import asyncio
import os
import re
import time


## attempt to load credentials file
if os.path.exists("byte-le-royale-auth.txt"):
    with open("byte-le-royale-auth.txt", "r") as f:
        lines = f.readlines()
        registered_team_name = lines[0].strip()
        registered_auth_token = lines[1].strip()
else:
    registered_team_name = None
    auth_token = None


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

kb = KeyBindings()

@kb.add('c-c')
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    event.app.exit()

@kb.add('up')
def _(event):
    scroll_one_line_up(event)

@kb.add('down')
def _(event):
    scroll_one_line_down(event)

@kb.add('pageup')
def _(event):
    scroll_page_up(event)

@kb.add('pagedown')
def _(event):
    scroll_page_down(event)

bit = False
block_backtick = False
@kb.add('`')
def _(event):
    global bit

    if block_backtick:
        return

    bit = not bit
    if bit:
        layout.focus(input_field)
    else:
        layout.focus(output_field)

buffer1 = Buffer()  # Editable buffer.

help_text = """Available Commands:
- announcements: Display announcements, updates automatically.
- registration: Displays the registration form.
- leaderboard: Displays the leaderboard, updates automatically.
- submit: Submit a client to the scrimmage server.
- results: View results for submitted clients.
- help: Display this help page.

Note: Press the backtick key to toggle between the results panel and the input prompt. Use up, down, pageup, and pagedown to navigate the results panel.

Press Ctrl+C to exit"""
search_field = SearchToolbar()
output_field = TextArea(
    style='class:output-field',
    text=help_text,
    scrollbar=True,
    read_only=True)

input_field = TextArea(
    height=1, prompt='>>> ', style='class:input-field', multiline=False,
    wrap_lines=False, search_field=search_field)


########################
### Registration Dialog
########################

def registration_submit_handler(buf):
    clear_floats()
    output_field.text = "Submitting registration..."
    loop = asyncio.get_event_loop()

    # verify auth file does not exist
    if not os.path.exists("byte-le-royale-auth.txt"):
        loop.create_task(register_team(registration_input_field.text))
    else:
        output_field.text = "You have already registered a team: \"{}\".\nOnly one " \
            "registration is allowed per team. Multiple registrations may result in disqualification.\n" \
            "We applolgize for this inconvinience but it ensure that the scrimmage matches run as smoothly as possible \n" \
            "Instead of registering another team, please share the byte-le-royale-auth.txt file with your teammates to \n" \
            "allow them access to your team's accout. Do not share this with other teams." \
            .format(registered_team_name)
        layout.focus(input_field)


async def register_team(team_name):
    loop = asyncio.get_event_loop()

    request_data = {
        "team_name": team_name
    }
    response = await loop.run_in_executor(
            None,
            lambda: requests.post("http://" + host + "/register", json=request_data))


    if response.status_code == 200:
        with open("byte-le-royale-auth.txt", "w") as f:
            f.write("{}\n".format(team_name))
            f.write("{}\n".format(response.json()["auth_token"]))

        output_field.text = "Registration Successful for team \"{}\"".format(team_name)
        global registered_team_name
        global registered_auth_token
        registered_team_name = team_name
        registered_auth_token = response.json()["auth_token"]


    else:
        output_field.text = "Registration failed for team \"{}\"\nReason:\n{}".format(team_name, cleanhtml(response.text))

    global block_backtick
    block_backtick = False
    layout.focus(input_field)

registration_input_field = TextArea(
        height=1,
        style='class:input-field',
        multiline=False,
        wrap_lines=False,
        accept_handler=registration_submit_handler)


registration_dialog = Dialog(
        title="Registration",
        body=HSplit([
            Label("Team Name:"),
            registration_input_field,
        ]),
        buttons=[
            Button(text="Submit", handler=lambda :registration_submit_handler(None))
        ])

#############################
## Rusults Selection Dialog
#############################
results_select = RadioList([(None, None)])


def show_results_select_dialog():
    output_field.text = "Getting submission information..."

    loop = asyncio.get_event_loop()
    loop.create_task(async_show_results_select_dialog())

async def async_show_results_select_dialog():
    loop = asyncio.get_event_loop()

    auth = HTTPBasicAuth(registered_team_name, registered_auth_token)
    response = await loop.run_in_executor(
            None,
            lambda: requests.get("http://" + host + "/submissions/list", auth=auth))


    if response.status_code != 200:
        output_field.text = "Failed to fetch submissions information.\nReason:\n{}".format(cleanhtml(response.text))
        return

    data = response.json()

    results_select.values = [
            (s["submission_no"],
                "{} {}".format(
                s["name"],
                s["submission_state"])
                )
            for s in data]

    submission_options.values.append(("None", "None"))

    flt = Float(content=results_select_dialog)
    layout.focus(results_select_dialog)
    root_container.floats.append(flt)
    output_field.text = ""

def results_select_submit_handler(buf):
    global show_submission_info_enabled
    clear_floats()
    submission = results_select.current_value

    if submission == "None":
        layout.focus(input_field)
        return

    output_field.text = "Getting submission \"{}\" information...".format(submission)

    loop = asyncio.get_event_loop()
    show_submission_info_enabled = True
    loop.create_task(async_show_submission_info(submission))


show_submission_info_enabled = False
async def async_show_submission_info(submission):
    loop = asyncio.get_event_loop()

    if not show_submission_info_enabled:
        return

    auth = HTTPBasicAuth(registered_team_name, registered_auth_token)
    response = await loop.run_in_executor(
        None,
        lambda: requests.get(
            "http://" + host + "/report/submissions/{}".format(submission),
            auth=auth))

    if response.status_code != 200:
        output_field.text = "Failed to fetch submission \"{}\" information.\nReason:\n{}".format(submission, cleanhtml(response.text))
        return

    submission_data = response.json()

    output_field.text = """
Note: Press the backtick key to toggle between the results panel and the input prompt. Use up, down, pageup, and pagedown to navigate the results panel.
-----------------------
{}
Upload Date: {}
Submission State: {}

""".format(
            submission_data["name"],
            submission_data["upload_date"],
            submission_data["submission_state"])

    for run in submission_data["runs"][::-1]:
        output_field.text += ("-"*100) + "\n"
        output_field.text += "Match Number: {}\n".format(run["run_number"])
        output_field.text += "~~ | LOG | ~~\n"
        output_field.text += run["log"]
        output_field.text += ("-"*100) + "\n"

    global block_backtick
    block_backtick = False
    layout.focus(output_field)

    await asyncio.sleep(5)

    if not show_submission_info_enabled:
        return

    loop = asyncio.get_event_loop()
    loop.create_task(async_show_submission_info(submission))



results_select_dialog = Dialog(
        title="Submission Select",
        body=HSplit([
            Label("Select a submission to view:"),
            results_select,
            Label("Press tab and then enter to confirm."),
        ]),
        buttons=[
            Button(text="Submit", handler=lambda :results_select_submit_handler(None))
        ])


####################
## Submission Dialog
####################

def submission_submit_handler(buf):
    global block_backtick
    clear_floats()
    client_path = submission_options.current_value

    if client_path == "None":
        block_backtick = False
        layout.focus(input_field)
        return

    output_field.text = "Submitting client \"{}\"...".format(client_path)
    loop = asyncio.get_event_loop()

    if registered_team_name is None or registered_auth_token is None:
        output_field.text = "Submitting client failed.\n Reason:\n You have not registered a " \
                "team or you are missing credentails.\n If you have recently registered, or "\
                "copied a \"byte-le-royale-auth.txt\" file into the current directory. Call the"\
                "\"reload_auth\" command."

        block_backtick = False
        layout.focus(input_field)
    else:
        loop.create_task(submit_client(client_path))


async def submit_client(client_path):
    global show_submission_info_enabled
    loop = asyncio.get_event_loop()


    with open(client_path, "r") as f:
        file_data = f.read()

    request_data = {
        "file_data": file_data
    }
    auth = HTTPBasicAuth(registered_team_name, registered_auth_token)
    response = await loop.run_in_executor(
            None,
            lambda: requests.post("http://" + host + "/submissions", auth=auth, json=request_data))


    if response.status_code == 200:
        output_field.text = "Successfully submitted client."
    else:
        output_field.text = "Submission failed.\nReason:\n{}".format(cleanhtml(response.text))
        output_field.text += "\n " + registered_team_name + " " + registered_auth_token

    await asyncio.sleep(2)

    response_data = response.json()

    loop = asyncio.get_event_loop()
    show_submission_info_enabled = True
    loop.create_task(async_show_submission_info(response_data["submission_no"]))


submission_options = RadioList([(None, None)])

def show_submission_dialog():
    dir_path = os.getcwd()
    submission_options.values = [
            (obj, obj) for obj in os.listdir(dir_path)
            if os.path.isfile(obj) and obj[-3:] == ".py" ]
    submission_options.values.append(("None", "None"))

    flt = Float(content=submission_dialog)
    layout.focus(submission_dialog)
    root_container.floats.append(flt)

submission_dialog = Dialog(
        title="Submit a client",
        body=HSplit([
            Label("Please select a client to upload:"),
            submission_options,
            Label("Press tab and then enter to confirm."),
        ]),
        buttons=[
            Button(text="Submit", handler=lambda :submission_submit_handler(None))
        ])


update_leaderboard_enabled = False
async def update_leaderboard():
    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(
            None,
            lambda: requests.get(
                "http://" + host + "/leaderboard"))

    if response.status_code != 200:
        output_field.text = "Error:\n{}".format(cleanhtml(response.text))
        return

    data = response.json()

    if not update_leaderboard_enabled:
        return

    output_field.text = "Run Number: #{}\n\n".format(data["run_number"])
    output_field.text += "Leaderboard:\n\n"
    output_field.text += "    {1:<8} : {0:<20}\n".format(
            "Credits", "Team Name")

    for team in data["leaderboard"]:
        output_field.text += "    {1:<8} : {0:<20}\n".format(
            team["team_name"],
            team["credits"]
        )

    await asyncio.sleep(5)

    if not update_leaderboard_enabled:
        return
    loop.create_task(update_leaderboard())


# completions menu
completions_menu = Float(
        xcursor=True,
        ycursor=True,
        content=CompletionsMenu(
        max_height=16,
        scroll_offset=1))

# Style.
style = Style([
    ('output-field', 'bg:#000000 #ffffff'),
    ('input-field', 'bg:#000000 #ffffff'),
    ('line', '#004400 bg:#000000'),
])

root_container = FloatContainer(
    content=HSplit([
        output_field,
        Window(height=1, char="-", style="class:line"),
        input_field,
        search_field
    ]),
    floats=[
        completions_menu
    ],
    key_bindings=KeyBindings())

layout = Layout(root_container, focused_element=input_field)


def input_parser(buff):
    global update_announcements_enabled
    global update_leaderboard_enabled
    global block_backtick
    loop = asyncio.get_event_loop()

    text = input_field.text
    text = text.strip()

    if text == "announcements" or text == "a":
        stop_screens()
        update_announcements_enabled = True
        loop.create_task(update_announcements())
        return
    elif text == "clear" or text == "help" or text == "c":
        stop_screens()
        output_field.text = help_text
    elif text == "registration" or text == "register":
        stop_screens()
        block_backtick = True
        flt = Float(content=registration_dialog)
        layout.focus(registration_dialog)
        root_container.floats.append(flt)
    elif text == "submit" or text == "s":
        stop_screens()
        block_backtick = True
        show_submission_dialog()
        layout.focus(submission_options)
    elif text == "leaderboard" or text == "l":
        stop_screens()
        update_leaderboard_enabled = True
        loop.create_task(update_leaderboard())
    elif text == "results" or text == "r":
        stop_screens()
        block_backtick = True
        show_results_select_dialog()






def stop_screens():
    global update_announcements_enabled
    global update_leaderboard_enabled
    global show_submission_info_enabled

    if update_announcements_enabled:
        update_announcements_enabled= False

    if update_leaderboard_enabled:
        update_leaderboard_enabled= False

    if show_submission_info_enabled:
        show_submission_info_enabled = False

def clear_floats():
        root_container.floats.clear()
        root_container.floats.append(completions_menu)



input_field.accept_handler = input_parser


host = os.getenv("BL_ROYALE_HOST",  "scrimmage.royale.ndacm.org:5000")


update_announcements_enabled= False
async def update_announcements():
    loop = asyncio.get_event_loop()

    payload = await loop.run_in_executor(None, requests.get, "http://" + host + "/announcements")

    if not update_announcements_enabled:
        return

    output_field.text = "Announcements:\n\n"

    if payload.status_code != 200:
        output_field.text = "An error occurred: " + payload.raw

    data = payload.json()["announcements"]

    for announcement in sorted(data, key=lambda e: e["posted_date"], reverse=True):
        title = announcement["title"]
        message = announcement["message"]
        date = announcement["posted_date"]
        output_field.text += ("-"*50) + f"\n# {title}\nPosted at: {date}\n\n{message}\n" + ("-"*50) + "\n"

    if len(data) == 0:
        output_field.text += "\n No available announcements."

    await asyncio.sleep(5)

    if not update_announcements_enabled:
        return
    loop.create_task(update_announcements())





def run_scrimmage_ui():
    use_asyncio_event_loop()

    app = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=True,
        style=style,
        mouse_support=True,
        enable_page_navigation_bindings=True,)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        app.run_async().to_asyncio_future())
