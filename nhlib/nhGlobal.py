from queue import Queue
from nhlib.nhBook import *


class NhGlobal :
    # requests relatives
    HEADERS = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, '
                       'like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    
    # nhentai relative
    HOME = "https://nhentai.net"
    
    # system relative
    ILLEGAL_SYMBOLS = {
        '/' : '／'
        , '\\' : '＼'
        , '|' : '｜'
        , '<' : '＜'
        , '>' : '＞'
        , '?' : '？'
        , ':' : '：'
        , '"' : '＂'
        , '*' : '＊'
    }


class NhState :
    # current state info
    State = Queue( )
    
    # visible galleries
    Visible = []
    
    # current hold book
    Checking = None
    
    