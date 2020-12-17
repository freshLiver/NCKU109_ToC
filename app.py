import os
import sys

from flask import Flask, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import *

from nhlib.nhCommand import *
from nhlib.nhUser import *
from nhlib.nhReply import *
from nhlib.nhRequest import *

load_dotenv( )

machine = TocMachine(
        states = ["user", "state1", "state2"],
        transitions = [
            {
                "trigger" : "advance",
                "source" : "user",
                "dest" : "state1",
                "conditions" : "is_going_to_state1",
            },
            {
                "trigger" : "advance",
                "source" : "user",
                "dest" : "state2",
                "conditions" : "is_going_to_state2",
            },
            { "trigger" : "go_back", "source" : ["state1", "state2"], "dest" : "user" },
        ],
        initial = "user",
        auto_transitions = False,
        show_conditions = True,
)

app = Flask( __name__, static_url_path = "" )

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv( "LINE_CHANNEL_SECRET", None )
channel_access_token = os.getenv( "LINE_CHANNEL_ACCESS_TOKEN", None )

if channel_secret is None :
    print( "Specify LINE_CHANNEL_SECRET as environment variable." )
    sys.exit( 1 )
if channel_access_token is None :
    print( "Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable." )
    sys.exit( 1 )

line_bot_api = LineBotApi( channel_access_token )
parser = WebhookParser( channel_secret )


@app.route( "/callback", methods = ["POST"] )
def callback ( ) :
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data( as_text = True )
    app.logger.info( "Request body: " + body )
    
    # parse webhook body
    try :
        events = parser.parse( body, signature )
    except InvalidSignatureError :
        abort( 400 )
    
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events :
        if not isinstance( event, MessageEvent ) :
            continue
        if not isinstance( event.message, TextMessage ) :
            continue
        
        line_bot_api.reply_message(
                event.reply_token, TextSendMessage( text = event.message.text )
        )
    
    return "OK"


@app.route( "/webhook", methods = ["POST"] )
def webhook_handler ( ) :
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data( as_text = True )
    app.logger.info( f"Request body: {body}" )
    
    # parse webhook body
    try :
        events = parser.parse( body, signature )
    except InvalidSignatureError :
        abort( 400 )
    
    # if event is MessageEvent and message is TextMessage
    for event in events :
        
        # should be message event
        if not isinstance( event, MessageEvent ) :
            continue
        # should also be text message
        if not isinstance( event.message, TextMessage ) :
            continue
        # should also be a string
        if not isinstance( event.message.text, str ) :
            continue
        
        # if this is a text message
        command = event.message.text
        
        legal, tokens = NhCommand.is_command( command )
        
        # if this is a command, do this command
        if legal == True :
            # call user.do_command and get NhReply
            img_url, reply = NhUser.do_command( tokens ).get_reply_message( )
            
            # check if this has image url
            if img_url is not None :
                # send a image
                send_image_by_url( event.reply_token, img_url, NhRequest.get_warning( ), NhEyes.get_mode( ) )
            # reply user with message
            send_text_message( event.reply_token, event.source.user_id, reply )
    
    # print( f"\nFSM STATE: {machine.state}" )
    # print( f"REQUEST BODY: \n{body}" )
    # response = machine.advance( event )
    # if response == False :
    # send_text_message( event.reply_token, resp )
    # send_image_by_url( event.reply_token, "https://i.imgur.com/Rk6HdeA.jpg", "https://i.imgur.com/pgJFHsN.jpg" )
    
    return "OK"


@app.route( "/show-fsm", methods = ["GET"] )
def show_fsm ( ) :
    machine.get_graph( ).draw( "fsm.png", prog = "dot", format = "png" )
    return send_file( "fsm.png", mimetype = "image/png" )


if __name__ == "__main__" :
    port = os.environ.get( "PORT", 777 )
    app.run( host = "0.0.0.0", port = port, debug = True )