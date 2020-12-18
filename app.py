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
from nhlib.nhMachine import *

load_dotenv( )

machine = NhMachine(
        states = ["home", "help", "switch",
                  "popular", "newest", "search",
                  "next", "goto", "open",
                  "watch", "close"],
        transitions = [
            # home
            {
                "trigger" : "do",
                "source" : ["home", "popular", "newest", "search", "open"],
                "dest" : "home",
                "conditions" : "home",
            },
            # help
            {
                "trigger" : "do",
                "source" : ["home", "popular", "newest", "search", "open"],
                "dest" : "help",
                "conditions" : "help",
            },
            # switch
            {
                "trigger" : "do",
                "source" : ["home", "popular", "newest", "search", "open"],
                "dest" : "switch",
                "conditions" : "switch",
            },
            # help/switch done
            {
                "trigger" : "done",
                "source" : ["help", "switch"],
                "dest" : "home",
            },
            # popular
            {
                "trigger" : "do",
                "source" : ["home", "popular", "newest", "search", "open"],
                "dest" : "popular",
                "conditions" : "popular",
            },
            # newest
            {
                "trigger" : "do",
                "source" : ["home", "popular", "newest", "search", "open"],
                "dest" : "newest",
                "conditions" : "newest",
            },
            # search
            {
                "trigger" : "do",
                "source" : ["home", "popular", "newest", "search", "open"],
                "dest" : "search",
                "conditions" : "search",
            },
            # next
            {
                "trigger" : "do",
                "source" : ["home", "popular", "newest", "search", "open"],
                "dest" : "next",
                "conditions" : "next",
            },
            # goto
            {
                "trigger" : "do",
                "source" : ["home", "popular", "newest", "search", "open"],
                "dest" : "goto",
                "conditions" : "goto",
            },
            # open
            {
                "trigger" : "do",
                "source" : ["home", "popular", "newest", "search", "open"],
                "dest" : "open",
                "conditions" : "open",
            },
            # popular done
            {
                "trigger" : "popular_done",
                "source" : "open",
                "dest" : "popular",
            },
            # newest done
            {
                "trigger" : "newest_done",
                "source" : ["next", "goto", "close"],
                "dest" : "newest",
            },
            # search done
            {
                "trigger" : "search_done",
                "source" : ["next", "goto", "close"],
                "dest" : "saerch",
            },
            # watch
            {
                "trigger" : "do",
                "source" : ["home", "popular", "newest", "search", "open"],
                "dest" : "watch",
                "conditions" : "watch",
            },
            # watch done
            {
                "trigger" : "watch_done",
                "source" : "watch",
                "dest" : "open",
            },
            # close
            {
                "trigger" : "do",
                "source" : ["home", "popular", "newest", "search", "open"],
                "dest" : "close",
                "conditions" : "close",
            },
        ],
        initial = "home"
                  "",
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
            machine.reset_reply( )
            machine.do( tokens )
            img_url, reply = machine.get_reply( ).get_reply_message( machine.get_current_state( ) )
            
            # check if this has image url
            if img_url is not None :
                # send a image
                send_image_by_url( event.reply_token, img_url, NhRequest.get_warning( ), NhEyes.get_mode( ) )
            # reply user with message
            send_text_message( event.reply_token, event.source.user_id, reply )
        
        #
        #
        #
        # print( f"\nFSM STATE: {machine.state}" )
        # print( f"REQUEST BODY: \n{body}" )
        # response = machine.advance( event )
        # if response == False :
        #     send_text_message( event.reply_token, resp )
    
    return "OK"


@app.route( "/show-fsm", methods = ["GET"] )
def show_fsm ( ) :
    machine.get_graph( ).draw( "fsm.png", prog = "dot", format = "png" )
    return send_file( "fsm.png", mimetype = "image/png" )


if __name__ == "__main__" :
    port = os.environ.get( "PORT", 777 )
    app.run( host = "0.0.0.0", port = port, debug = True )