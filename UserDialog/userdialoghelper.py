from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus


# Fetching the data from the QnA maker API to start multi turn conversation with the chatbot
class Userdialoghelper:
    @staticmethod
    async def user_help_dialog (dialog: Dialog, turn_context: TurnContext, accessor: StatePropertyAccessor
    ):
        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)
        
        #retrieving the answer from the chatbot 
        dialog_context = await dialog_set.create_context(turn_context)
        results = await dialog_context.continue_dialog()
        if results.status == DialogTurnStatus.Empty:
            await dialog_context.begin_dialog(dialog.id)