from typing import List

from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    ConversationState,
    UserState,
    CardFactory,
    MessageFactory,
)

from botbuilder.dialogs import Dialog

from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    ThumbnailCard,
    ThumbnailUrl,
    CardImage,
    CardAction,
    ActionTypes,
    ActivityTypes,
    Activity,
)

from UserDialog.userdialoghelper import Userdialoghelper
# new change
# Implementation of Ascelpius chat bot with QnA maker 
class Healthbot(ActivityHandler):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog
    
    # for every turn of the conversation storing the conversation data and context of the conversation
    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)
    # for every member added in the conversation in different channels starting the chatbot script 
    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await self.Initialcard(turn_context)

                await turn_context.send_activity(MessageFactory.text("how are you feeling today ?"))
    
    # for every message received from the user chat would respond based on intent of the user 

    async def on_message_activity(self, turn_context: TurnContext):
        
        #Teaching the chatbot some of the basic intents to help user guide through different conversation            
        text = turn_context.activity.text.lower()
        #displaying interactive cards to enhance user experience
        if text in ("hello", "hi","hi how are you","how are you doing","how you doing"):
            await self.send_typing_information(turn_context)
            await self.Hello_card(turn_context)
        #dsiplaying help card if the user seems to be lost
        elif text in ("intro","help"):
            await self.send_typing_information(turn_context)
            await self.help_intro_card(turn_context)
        #partially end the covesration by asking the user if it served the purpose
        elif text in ("thank you","thank you for your help","thanks","really thank you for your help","really thank you","thanks for help"):
            await self.thank_you_card(turn_context)
            await self.send_typing_information(turn_context)
            await turn_context.send_activity(MessageFactory.text("I Hope i have answered your questions. Is there anything i can help you with ?"))
        #Taking the feedback from the user based on user response and ending the conversation
        elif text in ("no","no thank you"):
            await self.send_typing_information(turn_context)
            await turn_context.send_activity(MessageFactory.text("Thank you for your time today. Please leave us some feedback it would be helpful in improving our product"))
        #Taking the user to feel good dialogue
        elif text in ("i am feeling happy","i am feeling good","i am feeling great","good","great","happy"):
            await self.send_typing_information(turn_context)
            await self.FeelGood_card(turn_context)
        #Taking the user query to the knowledge base to check if it can provide the answer to the user or else directing the user to the right dialogue
        else:
            await Userdialoghelper.user_help_dialog(
                self.dialog,
                turn_context,
                self.conversation_state.create_property("DialogState"),
                )

    # Send typing notification to the user to acknowledge if it has received the message
    async def send_typing_information(self, turn_context: TurnContext):

        return await turn_context.send_activities([
            Activity(
                type=ActivityTypes.typing
            ),
            Activity(
                type="delay",
                value=2000
            )
        ])
    # Making Hero card object to send user welcome message   
    async def Initialcard(self,turn_context: TurnContext):
        intialcard = HeroCard(
            title="Acelpius: your buddy for Mental Health support!",
            text="Welcome my name is ascelpius; I am a smart chatbot which can give you some info on mental health"
            " I am here to support you while you wait for sometime to get help from the licensed practioner who can help you with your Mental Health problems"
            " You can ask me any question regarding mental health so that I can give some resources with respect to mental health alternatively you can choose"
            " from the below options which will give right information in the case of an Emergency.",
            images=[CardImage(url="https://images.idgesg.net/images/article/2018/10/chatbot_ai_machine-learning_emerging-tech-100778305-large.jpg?auto=webp&quality=85,70")],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="Get help from NHS", 
                    text="Please find below to get help from NHS in case of emergency",
                    display_text="NHS help for mental Health survey",
                    value="https://www.nhs.uk/mental-health/nhs-voluntary-charity-services/charity-and-voluntary-services/get-help-from-mental-health-helplines/"
                ),

                CardAction(
                    type=ActionTypes.open_url,
                    title="Nearest GP",
                    text="Please find contact details of GP near you",
                    display_text="Information about your nearest GP",
                    value="https://www.nhs.uk/service-search/find-a-gp"
                ),

                CardAction(
                    type=ActionTypes.open_url,
                    title="WHO information on mental Health",
                    text="Please find more information about mental health from WHO",
                    display_text="Information about mental health from WHO",
                    value="https://www.who.int/health-topics/mental-health#tab=tab_1"
                ),
            ], 
        )

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(intialcard))
        )

    #Creating a greeting card based on intial intents of the user
    async def Hello_card(self,turn_context: TurnContext):
        firstcard = HeroCard(
            title="Hello ! How are you doing today ?",
            text="I am a mental health informative chatbot to provide you with the information related to Mental Health."
                 " Please let me know if you need any help with your mental health"
                 " I maybe able to help you with any mental health information.",
            images=[CardImage(url="https://www.verywellmind.com/thmb/DbIdrx4Cb21om8EfHlefhn4kXzY=/960x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/mental-health-tracker-banner-03-db4c074daa7f4b719dfec6b4b4279c2d.png"),CardImage(url="https://44b3rr19j5k32jgxng3vkk48-wpengine.netdna-ssl.com/wp-content/uploads/2021/04/May-Is-Mental-Health-Month-1024x536.jpg")],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="Get Mental Health tips", 
                    text="Please find below to get some tips for Mental wellbeing",
                    display_text="Information on Mental wellbeing tips",
                    value="https://www.nhs.uk/mental-health/nhs-voluntary-charity-services/charity-and-voluntary-services/get-help-from-mental-health-helplines/"
                )
            ],
        )

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(firstcard))
        )

    #Creating a feelgood card based on intents from the user 
    async def FeelGood_card(self,turn_context: TurnContext):
        feelgoodcard = HeroCard(
            title="It's good to hear from you that you are feeling great",
            text="Here are some of the tips to keep mental well being in different scenarios",
            images=[CardImage(url="https://cabamentalwellbeing.org.uk/wp-content/uploads/2021/02/CABA_Mind-Matters_HOME.png")],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="Be Mentally fit",
                    text="please fin below to keep mentally well",
                    display_text="Information on mental wellbeing",
                    value="https://www.mind.org.uk/information-support/your-stories/what-is-mental-health-and-mental-wellbeing/"
                )
            ],
        )

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(feelgoodcard))
        )

    #Creating a HelpCard if the user seems to be lost in between the conversation
    async def help_intro_card(self,turn_context: TurnContext):
        helpintrocard = HeroCard(
            title="I am here to help you. You can ask me anything information about",
            text="These are the services provided by me",
            images=[CardImage(url="https://cdn6.f-cdn.com/contestentries/1476201/32214673/5c7f869653351_thumb900.jpg")],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="you can get help about mental health",
                    text="please check below resources",
                    display_text="Help desk",
                    value="https://www.nhs.uk/mental-health/advice-for-life-situations-and-events/where-to-get-urgent-help-for-mental-health/"
                ),

                CardAction(
                     type=ActionTypes.im_back,
                     title="List of services provided by me",
                     text="help provided by me",
                     display_text="Help desk",
                     value="Please help me with my mental health"                     
                ),
       
            ],
        )
        
        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(helpintrocard))
        )

    # Creating thank you card when user is satisfied with the information 
    async def thank_you_card(self,turn_context: TurnContext):
        thankyoucard = ThumbnailCard(
            images=[ThumbnailUrl(url="https://thumbs.dreamstime.com/z/handwritten-lettering-you-welcome-vector-illustration-template-banner-invitation-party-postcard-poster-print-sticker-173199867.jpg")],
            title="Glad i could be of your help",
        )

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.thumbnail_card(thankyoucard))
        )




        








        