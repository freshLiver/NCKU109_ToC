import os

from linebot import LineBotApi, WebhookParser
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
                            ImageMessage, )

channel_access_token = os.getenv( "LINE_CHANNEL_ACCESS_TOKEN", None )


def send_text_message ( reply_token, text ) :
    line_bot_api = LineBotApi( channel_access_token )
    line_bot_api.reply_message( reply_token, TextSendMessage( text = text ) )
    
    return "OK"


def send_image_by_url ( msg_target: str, origin: str, preview: str ) :
    # convert origin img and preview img into image message
    image_msg = ImageSendMessage( origin, preview )
    # push this image msg
    LineBotApi( channel_access_token ).push_message( msg_target, image_msg )


"""
def send_button_message(id, text, buttons):
    pass
"""