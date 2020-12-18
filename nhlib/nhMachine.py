from transitions.extensions import GraphMachine

from nhlib.nhEyes import *
from nhlib.nhHand import *
from nhlib.nhCommand import *
from nhlib.nhGallery import *
from nhlib.nhReply import *


class NhMachine( GraphMachine ) :
    def __init__ ( self, **machine_configs ) :
        self.machine = GraphMachine( model = self, **machine_configs )
        
        self.__Hand = NhHand( )
        self.__Eyes = NhEyes( )
        self.__Reply = NhReply( )
    
    
    def get_reply ( self ) -> NhReply :
        return self.__Reply
    
    
    def reset_reply ( self ) -> None :
        self.__Reply.reset( )
    
    
    # #############################################################
    # ##################### back to home page #####################
    # #############################################################
    def home ( self, tokens: list ) -> bool :
        if tokens[0] == NhCommand.HOME :
            
            # reset status and page
            self.__Eyes.clear_state( )
            self.__Eyes.clear_galleries( )
            self.__Eyes.clear_reading( )
            self.__Hand.reset_link_and_page( )
            
            # reply available commands
            self.__Reply.add_message( "$home 成功, 可用的指令有 $popular, $newest, $search, $home" )
            return True
        
        return False
    
    
    def on_enter_home ( self, tokens = None ) :
        print( "at home" )
    
    
    def on_exit_home ( self, tokens = None ) :
        print( "exit home" )
    
    
    # ##############################################################
    # ################ show help info (state graph) ################
    # ##############################################################
    def help ( self, tokens: list ) -> bool :
        if tokens[0] == NhCommand.HELP :
            help_msg = ""
            help_msg += """\n┌─ {0} (預設, 可在任何狀態使用)""".format( NhCommand.HOME )
            help_msg += """\n├─ {0} (可在任何狀態使用)""".format( NhCommand.HELP )
            help_msg += """\n├─ {0} (可在任何狀態使用)""".format( NhCommand.SWITCH )
            help_msg += """\n│"""
            help_msg += """\n├─── {0} (不可使用 {1}, {2})""".format( NhCommand.POPULAR, NhCommand.GOTO, NhCommand.NEWEST )
            help_msg += """\n├─── {0}""".format( NhCommand.NEWEST )
            help_msg += """\n├─── {0}""".format( NhCommand.SEARCH )
            help_msg += """\n│"""
            help_msg += """\n├───── {0} (不會進入下一層)""".format( NhCommand.NEXT )
            help_msg += """\n├───── {0} (不會進入下一層)""".format( NhCommand.GOTO )
            help_msg += """\n├───── {0}""".format( NhCommand.OPEN )
            help_msg += """\n│"""
            help_msg += """\n├─────── {0}""".format( NhCommand.WATCH )
            help_msg += """\n└─────── {0} (會回到原本狀態)""".format( NhCommand.CLOSE )
            self.__Reply.add_message( help_msg )
            return True
        
        return False
    
    
    def on_enter_help ( self, tokens = None ) :
        print( "at help" )
        self.done( )
    
    
    def on_exit_help ( self, tokens = None ) :
        print( "exit help" )
    
    
    # ###############################################################
    # ################ send picture with R18 warning ################
    # ###############################################################
    def switch ( self, tokens: list ) -> bool :
        if tokens[0] == NhCommand.SWITCH :
            healthy_mode = self.__Eyes.toggle_mode( )
            if healthy_mode == True :
                self.__Reply.add_message( "開啟健康模式" )
            else :
                self.__Reply.add_message( "開啟老司機模式" )
            return True
        
        return False
    
    
    def on_enter_switch ( self, tokens = None ) :
        print( "at switch" )
        self.done( )
    
    
    def on_exit_switch ( self, tokens = None ) :
        print( "exit switch" )
    
    
    # ###############################################################
    # #################### get popular galleries ####################
    # ###############################################################
    def popular ( self, tokens: list ) -> bool :
        if tokens[0] == NhCommand.POPULAR :
            # only available while current state is home
            if self.get_current_state( ) == NhCommand.HOME :
                # get popular galleries and convert to reply form
                populars = self.__Hand.get_popular_result( )
                found, reply = NhEyes.galleries_to_reply_form( populars )
                
                # check if any galleries found
                if found == True :
                    # clear and add result galleries
                    self.__Eyes.clear_galleries( )
                    self.__Eyes.add_galleries( populars )
                    
                    # push into newest state
                    self.__Eyes.push_state( NhCommand.POPULAR )
                    
                    self.__Reply.add_message( reply )
                    self.__Reply.add_message( "$popular 成功, 可用的指令有 $open, $home" )
                    return True
                
                else :
                    self.__Reply.add_message( "$popular 失敗, 找不到 $popular" )
            else :
                self.__Reply.add_message( "$popular 失敗, 必須位在 $home" )
        return False
    
    
    def on_enter_popular ( self, tokens = None ) :
        print( "at popular" )
    
    
    def on_exit_popular ( self, tokens = None ) :
        print( "exit popular" )
    
    
    # ##############################################################
    # #################### get newest galleries ####################
    # ##############################################################
    def newest ( self, tokens: list ) -> bool :
        if tokens[0] == NhCommand.NEWEST :
            # only available while current state is home
            if self.get_current_state( ) == NhCommand.HOME :
                # get newest galleries and convert to reply form
                newest = self.__Hand.get_newest_result( 1 )
                found, reply = NhEyes.galleries_to_reply_form( newest )
                
                # check if any galleries found
                if found == True :
                    # clear and add result galleries
                    self.__Eyes.clear_galleries( )
                    self.__Eyes.add_galleries( newest )
                    
                    # push into newest state
                    self.__Eyes.push_state( NhCommand.NEWEST )
                    
                    self.__Reply.add_message( reply )
                    self.__Reply.add_message( "$newest 成功, 可用的指令有 $open, $next, $goto, $home" )
                    return True
                
                else :
                    self.__Reply.add_message( "$newest 失敗, 找不到 $newest" )
            else :
                self.__Reply.add_message( "$newest 失敗, 必須位在 $home" )
        return False
    
    
    def on_enter_newest ( self, tokens = None ) :
        print( "at newest" )
    
    
    def on_exit_newest ( self, tokens = None ) :
        print( "exit newest" )
    
    
    # ##############################################################
    # ###################### search galleries ######################
    # ##############################################################
    def search ( self, tokens: list ) -> bool :
        if tokens[0] == NhCommand.SEARCH :
            # only available while current state is home
            if self.get_current_state( ) == NhCommand.HOME :
                # use remain tokens as keywords to search
                keywords = tokens[1 :]
                
                # check if search without keywords
                if keywords != [] :
                    # get search galleries and convert to reply form
                    search_result = self.__Hand.get_search_result( keywords, 1 )
                    found, reply = NhEyes.galleries_to_reply_form( search_result )
                    
                    # check if any galleries found
                    if found == True :
                        # clear and add result galleries
                        self.__Eyes.clear_galleries( )
                        self.__Eyes.add_galleries( search_result )
                        
                        # push into search state
                        self.__Eyes.push_state( NhCommand.SEARCH )
                        
                        self.__Reply.add_message( reply )
                        self.__Reply.add_message( "$search 成功, 可用的指令有 $open, $next, $goto, $home" )
                        return True
                    
                    else :
                        self.__Reply.add_message( "$search 失敗, 此關鍵字無搜尋結果" )
                else :
                    self.__Reply.add_message( "$search 失敗, 搜尋帶關鍵字很難嗎？" )
            else :
                self.__Reply.add_message( "$search 失敗, 必須位在 $home" )
        return False
    
    
    def on_enter_search ( self, tokens = None ) :
        print( "at search" )
    
    
    def on_exit_search ( self, tokens = None ) :
        print( "exit search" )
    
    
    # ##############################################################
    # ####################### goto next page #######################
    # ##############################################################
    def next ( self, tokens: list ) -> bool :
        if tokens[0] == NhCommand.NEXT :
            
            # only available while search or newest
            if self.get_current_state( ) in [NhCommand.SEARCH, NhCommand.NEWEST] :
                # get next page galleries and convert to replay form
                next_page_result = self.__Hand.get_next_page_result( )
                found, reply = NhEyes.galleries_to_reply_form( next_page_result )
                
                # check if any galleries found
                if found == True :
                    # clear and add next page's galleries
                    self.__Eyes.clear_galleries( )
                    self.__Eyes.add_galleries( next_page_result )
                    
                    self.__Reply.add_message( reply )
                    self.__Reply.add_message( "$next 成功, 可用的指令有 $open, $next, $goto, $home" )
                    return True
                
                else :
                    self.__Reply.add_message( "$next 失敗, 找不到下一頁" )
            else :
                self.__Reply.add_message( "$next 失敗, 必須位在 $search or $newest" )
        return False
    
    
    def on_enter_next ( self, tokens = None ) :
        print( "at next" )
        if self.get_current_state( ) == NhCommand.NEWEST :
            self.newest_done( )
        else :
            self.search_done( )
    
    
    def on_exit_next ( self, tokens = None ) :
        print( "exit next" )
    
    
    # #############################################################
    # ######################## goto page N ########################
    # #############################################################
    def goto ( self, tokens: list ) -> bool :
        if tokens[0] == NhCommand.GOTO :
            # only available while search or newest
            if self.get_current_state( ) in [NhCommand.SEARCH, NhCommand.NEWEST] :
                try :
                    # try to use tokens[1] as page, if not int -> ValueError
                    target_page = int( tokens[1] )
                    
                    if target_page == 0 :
                        target_page = 1
                        self.__Reply.add_message( ">>> $goto 要從 1 開始，自動導向到 $goto 1 <<<\n\n" )
                    
                    # get target page result
                    target_galleries = self.__Hand.get_result_of_this_page( target_page )
                    found, reply = NhEyes.galleries_to_reply_form( target_galleries )
                    # check if any galleries found
                    if found == True :
                        # clear and add target galleries
                        self.__Eyes.clear_galleries( )
                        self.__Eyes.add_galleries( target_galleries )
                        self.__Reply.add_message( reply )
                        self.__Reply.add_message( "$goto 成功, 可用的指令有 $open, $next, $goto, $home" )
                        return True
                    
                    else :
                        self.__Reply.add_message( "$goto 失敗, 指定的頁數不存在" )
                except IndexError :
                    self.__Reply.add_message( "$goto 失敗, 不輸入頁數是要我通靈？" )
                except ValueError :
                    self.__Reply.add_message( "$goto 失敗, 輸入一個頁「數」很難嗎？" )
            else :
                self.__Reply.add_message( "$goto 失敗, 必須位在 $search or $newest" )
        return False
    
    
    def on_enter_goto ( self, tokens = None ) :
        print( "at goto" )
        if self.get_current_state( ) == NhCommand.NEWEST :
            self.newest_done( )
        else :
            self.search_done( )
    
    
    def on_exit_goto ( self, tokens = None ) :
        print( "exit goto" )
    
    
    # ###############################################################
    # ###################### open this gallery ######################
    # ###############################################################
    def open ( self, tokens: list ) -> bool :
        if tokens[0] == NhCommand.OPEN :
            # only available while popular, search, newest
            if self.get_current_state( ) in [NhCommand.POPULAR, NhCommand.SEARCH, NhCommand.NEWEST] :
                # use tokens[1] to select target gallery, if not int -> ValueError
                try :
                    gallery_index = int( tokens[1] )
                    
                    gallery: NhGallery
                    found, gallery = self.__Eyes.get_gallery_by_index( gallery_index )
                    
                    # check if this index out of range
                    if found == True :
                        # open gallery and set it new book
                        self.__Eyes.open_this_gallery( gallery_index )
                        self.__Eyes.push_state( NhCommand.OPEN )
                        
                        # get opened gallery info
                        reply = self.__Eyes.get_reading_gallery_info( )
                        
                        self.__Reply.add_message( reply )
                        self.__Reply.add_message( "$open 成功, 可用的指令有 $watch, $close, $home" )
                        return True
                    
                    # gallery index out of range
                    else :
                        self.__Reply.add_message( "$open 失敗, 輸入範圍內的編號很難嗎" )
                except IndexError :
                    self.__Reply.add_message( "$open 失敗, 不指定哪本是要我通靈？" )
                except ValueError :
                    self.__Reply.add_message( "$open 失敗, 輸入一個正確的「編號」很難嗎？" )
            else :
                self.__Reply.add_message( "$open 失敗, 必須位在 $popular, $search, $newest" )
        return False
    
    
    def on_enter_open ( self, tokens = None ) :
        print( "at open" )
    
    
    def on_exit_open ( self, tokens = None ) :
        print( "exit open" )
    
    
    def get_current_state ( self ) -> NhCommand :
        return self.__Eyes.get_current_state( )
    
    
    # ###############################################################
    # ####################### watch this page #######################
    # ###############################################################
    def watch ( self, tokens: list ) -> bool :
        if tokens[0] == NhCommand.WATCH :
            # only available while open
            if self.get_current_state( ) == NhCommand.OPEN :
                # check if tokens[1] exist
                try :
                    # get token[1] as page number(start from 0), if not int -> ValueError
                    page = int( tokens[1] )
                    
                    # try to get target page from current reading book
                    found, url = self.__Eyes.get_reading_page_link( page )
                    if found == True :
                        self.__Reply.set_url( url )
                        self.__Reply.add_message( "$watch 成功, 可用的指令有 $watch, $close, $home" )
                        return True
                    
                    else :
                        self.__Reply.add_message( "$watch 失敗, 指定頁數超出範圍（從 0 開始）" )
                except IndexError :
                    self.__Reply.add_message( "$watch 失敗, 不輸入頁數是要我通靈？" )
                except ValueError :
                    self.__Reply.add_message( "$watch 失敗, 輸入正確的頁「數」很難嗎？" )
            else :
                self.__Reply.add_message( "$watch 失敗, 沒先 $open 是要 $watch 什麼？" )
        return False
    
    
    def on_enter_watch ( self, tokens = None ) :
        print( "at watch" )
        self.watch_done( )
    
    
    def on_exit_watch ( self, tokens = None ) :
        print( "exit watch" )
    
    
    # ###############################################################
    # #################### close reading gallery ####################
    # ###############################################################
    def close ( self, tokens: list ) -> bool :
        if tokens[0] == NhCommand.CLOSE :
            # only available while open
            if self.get_current_state( ) == NhCommand.OPEN :
                # close and clear current reading
                self.__Eyes.clear_reading( )
                # pop current state (go back to last state)
                self.__Eyes.pop_state( )
                
                # check if new state is popular
                if self.get_current_state( ) == NhCommand.POPULAR :
                    self.__Reply.add_message( "$close 成功, 可用的指令有 $open, $home" )
                    return True
                else :
                    self.__Reply.add_message( "$close 成功, 可用的指令有 $open, $next, $goto, $home" )
                    return True
            
            else :
                self.__Reply.add_message( "$close 失敗, 沒先 $open 是要 $close 什麼？" )
        return False
    
    
    def on_enter_close ( self, tokens = None ) :
        print( "at close" )
        now = self.get_current_state( )
        if now == NhCommand.POPULAR :
            self.popular_done( )
        elif now == NhCommand.NEWEST :
            self.newest_done( )
        elif now == NhCommand.SEARCH :
            self.search_done( )
    
    
    def on_exit_close ( self, tokens = None ) :
        print( "exit close" )