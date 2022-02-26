#!/usr/bin/env python3
import os

# configuration class to connect to the Qna KB of Bot  
# Adding QnA maker knowledge base id
# Adding end point key 
# Adding end point hostname

class MainConfiguration:
    

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    QNA_KNOWLEDGEBASE_ID = os.environ.get("QnAKnowledgebaseId", "743f670a-f78b-4c47-aff2-86999a86d848")
    QNA_ENDPOINT_KEY = os.environ.get("QnAEndpointKey", "8df75876-6b7b-491b-93ad-781185aebd85")
    QNA_ENDPOINT_HOST = os.environ.get("QnAEndpointHostName", "https://mentalhealth-8fbc.azurewebsites.net/qnamaker")