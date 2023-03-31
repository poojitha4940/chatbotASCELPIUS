import sys
import traceback
from datetime import datetime
from http import HTTPStatus

#This is git tutorial
 
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.ai.qna.dialogs import QnAMakerDialog
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    ConversationState,
    MemoryStorage,
    TurnContext,
    UserState,
)

from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes

from configuration import MainConfiguration
from SmartBot import Healthbot

CONFIGURATION = MainConfiguration()

SETTINGS = BotFrameworkAdapterSettings(CONFIGURATION.APP_ID, CONFIGURATION.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Handling errors in an event of a system failure 
async def on_error(context: TurnContext, error: Exception):

    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    await context.send_activity(
        "Please try again after some time"
    )

    if context.activity.channel_id == "emulator":   
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
       
        await context.send_activity(trace_activity)

ADAPTER.on_turn_error = on_error

# Creating memory object to store the conversation data and user data
BOTSTORAGE = MemoryStorage()
CONVERSATION_STATE = ConversationState(BOTSTORAGE)
USER_STATE = UserState(BOTSTORAGE)


BOTDIALOG = QnAMakerDialog(
    CONFIGURATION.QNA_KNOWLEDGEBASE_ID,
    CONFIGURATION.QNA_ENDPOINT_KEY,
    CONFIGURATION.QNA_ENDPOINT_HOST,
)

# Creating the healthbot object 
HEALTHBOT = Healthbot(CONVERSATION_STATE,USER_STATE,BOTDIALOG)

# Send and receiveing messages to the bot application
async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, HEALTHBOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=201)


APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

#driver code to start bot application
if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIGURATION.PORT)
    except Exception as error:
        raise error
