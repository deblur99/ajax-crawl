import json
from messages import MessageManager


def lambda_handler(event, context):
    return {
        'message': MessageManager().getSingleMessage()
    }
