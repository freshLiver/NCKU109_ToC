import os

from linebot import LineBotApi, WebhookParser
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, )

channel_access_token = os.getenv( "LINE_CHANNEL_ACCESS_TOKEN", None )


def send_text_message ( reply_token: str, to: str, text: str ) :
    line_bot_api = LineBotApi( channel_access_token )
    
    # check if text message over 5000 words
    if len( text ) >= 5000 :
        # split message with "\n\n"
        parts = text.split( "\n\n" )
        for part in parts :
            line_bot_api.push_message( to, TextSendMessage( text = part ) )
    else :
        line_bot_api.reply_message( reply_token, TextSendMessage( text = text ) )
    
    return "OK"


def send_image_by_url ( reply_token: str, origin: str, preview: str ) :
    # get bot api
    bot = LineBotApi( channel_access_token )
    # convert origin img and preview img into image message
    image_msg = ImageSendMessage( origin, preview )
    # push this image msg
    bot.reply_message( reply_token, image_msg )
    
    return "OK"


"""
def send_button_message(id, text, buttons):
    pass
"""