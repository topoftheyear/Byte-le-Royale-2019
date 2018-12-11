
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea, SearchToolbar
from prompt_toolkit.eventloop import use_asyncio_event_loop
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.markup import MarkdownLexer
from prompt_toolkit.application import get_app
import requests
import asyncio
import os

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

help_text = "Press Ctrl+C to exit"
search_field = SearchToolbar()
output_field = TextArea(
    style='class:output-field',
    text=help_text,
    scrollbar=True,
    read_only=True,
    lexer=PygmentsLexer(MarkdownLexer))

input_field = TextArea(
    height=1, prompt='>>> ', style='class:input-field', multiline=False,
    wrap_lines=False, search_field=search_field)

def accept_input(buff):
    # Evaluate "calculator" expression.
    try:
        output = '\n\nIn:  {}\nOut: {}'.format(
            input_field.text,
            eval(input_field.text))  # Don't do 'eval' in real code!
    except BaseException as e:
        output = '\n\n{}'.format(e)
    new_text = output_field.text + output

    # Add text to output buffer.
    output_field.buffer.document = Document(
        text=new_text, cursor_position=len(new_text))


input_field.accept_handler = accept_input


# Style.
style = Style([
    ('output-field', 'bg:#000000 #ffffff'),
    ('input-field', 'bg:#000000 #ffffff'),
    ('line', '#004400 bg:#000000'),
])

root_container = HSplit([
    output_field,
    Window(height=1, char="-", style="class:line"),
    input_field,
    search_field
])

layout = Layout(root_container, focused_element=input_field)


def input_parser():
    pass



host = os.getenv("BL_ROYALE_HOST",  "scrimmage.royale.ndacm.org")

async def update_announcements():
    loop = asyncio.get_event_loop()


    payload = await loop.run_in_executor(None, requests.get, "http://" + host + "/announcements")

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
    loop.create_task(update_announcements())
    loop.run_until_complete(
        app.run_async().to_asyncio_future())
