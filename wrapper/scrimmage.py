
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout import FloatContainer, Float
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea, SearchToolbar, Dialog, Label, Button
from prompt_toolkit.eventloop import use_asyncio_event_loop
from prompt_toolkit.application import get_app
import requests
import asyncio
import os


## attempt to load credentials file
if False:
    pass
else:
    registered_team_name = None
    auth_token = None

kb = KeyBindings()

@kb.add('c-c')
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    event.app.exit()


buffer1 = Buffer()  # Editable buffer.

help_text = """Available Commands:
- announcements: Display announcements, updates automatically.
- leaderboard: Displays the leaderboard, updates automatically.
- register: Displays the registration form.

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


### Registration Dialog

def registration_submit_handler(buf):
    root_container.floats = []
    output_field.text = "Submitting registration..."
    loop = asyncio.get_event_loop()

    # verify auth file does not exist
    if not os.path.exists("byte-le-royale-auth.txt"):
        loop.create_task(register_team(registration_input_field.text))
    else:
        output_field.text = "You have already registered a team: \"{}\".\nOnly one " \
            "registration is allowed per team. Multiple registrations may result in disqualification." \
            .format(registered_team_name)


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
        registered_team_name = team_name

    else:
        output_field.text = "Registration failed for team \"{}\"\nReason:\n{}".format(team_name, response.raw)

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
    ])

layout = Layout(root_container, focused_element=input_field)


def input_parser(buff):
    global update_announcements_enabled
    loop = asyncio.get_event_loop()

    text = input_field.text
    text = text.strip()

    if text == "announcements":
        stop_screens()
        update_announcements_enabled = True
        loop.create_task(update_announcements())
        return
    elif text == "clear":
        stop_screens()
        output_field.text = help_text
    elif text == "registration":
        stop_screens()
        flt = Float(content=registration_dialog)
        layout.focus(registration_dialog)
        root_container.floats.append(flt)


def stop_screens():
    global update_announcements_enabled
    loop = asyncio.get_event_loop()

    if update_announcements_enabled:
        update_announcements_enabled= False




input_field.accept_handler = input_parser


host = os.getenv("BL_ROYALE_HOST",  "scrimmage.royale.ndacm.org")


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
    update_announcements_task = loop.create_task(update_announcements())





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
