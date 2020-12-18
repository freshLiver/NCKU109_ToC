from nhlib.nhEyes import *
from nhlib.nhHand import *
from nhlib.nhCommand import *
from nhlib.nhGallery import *
from nhlib.nhReply import *


class NhUser( ) :
    __Hand = NhHand( )
    __Eyes = NhEyes( )
    __Reply = NhReply( )
    
    
    @classmethod
    def do_command ( cls, tokens: list ) -> NhReply :
        cls.__Reply.reset( )
        current_state = cls.__Eyes.get_current_state( )
        
        if tokens[0] == NhCommand.HOME :
            cls.home( )
        
        elif tokens[0] == NhCommand.HELP :
            cls.help( )
        
        elif tokens[0] == NhCommand.SWITCH :
            cls.switch( )
        
        elif tokens[0] == NhCommand.POPULAR :
            cls.popular( current_state )
        
        elif tokens[0] == NhCommand.NEWEST :
            cls.newest( current_state )
        
        elif tokens[0] == NhCommand.SEARCH :
            cls.search( current_state )
        
        elif tokens[0] == NhCommand.NEXT :
            cls.next( current_state )
        
        elif tokens[0] == NhCommand.GOTO :
            cls.goto( current_state )
        
        elif tokens[0] == NhCommand.OPEN :
            cls.open( current_state )
        
        elif tokens[0] == NhCommand.WATCH :
            cls.watch( current_state )
        
        elif tokens[0] == NhCommand.CLOSE :
            cls.close( current_state )
        
        else :
            raise Exception( "This Message is Not a Command !" )
        
        # add current state
        cls.__Reply.add_message( "目前位於 {0}".format( cls.__Eyes.get_current_state( ) ) )
        
        # return reply message to user
        return cls.__Reply
    
    
    # #############################################################
    # ##################### back to home page #####################
    # #############################################################
    @classmethod
    def home ( cls ) :
        # reset status and page
        cls.__Eyes.clear_state( )
        cls.__Eyes.clear_galleries( )
        cls.__Eyes.clear_reading( )
        cls.__Hand.reset_link_and_page( )
        
        # reply available commands
        cls.__Reply.add_message( "$home 成功, 可用的指令有 $popular, $newest, $search, $home" )
    
    
    # ##############################################################
    # ################ show help info (state graph) ################
    # ##############################################################
    @classmethod
    def help ( cls ) :
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
        cls.__Reply.add_message( help_msg )
    
    
    # ###############################################################
    # ################ send picture with R18 warning ################
    # ###############################################################
    @classmethod
    def switch ( cls ) :
        healthy_mode = cls.__Eyes.toggle_mode( )
        if healthy_mode == True :
            cls.__Reply.add_message( "開啟健康模式" )
        else :
            cls.__Reply.add_message( "開啟老司機模式" )
    
    
    # ###############################################################
    # #################### get popular galleries ####################
    # ###############################################################
    @classmethod
    def popular ( cls, current_state: NhCommand ) :
        # only available while current state is home
        if current_state == NhCommand.HOME :
            # get popular galleries and convert to reply form
            populars = cls.__Hand.get_popular_result( )
            found, reply = NhEyes.galleries_to_reply_form( populars )
            
            # check if any galleries found
            if found == True :
                # clear and add result galleries
                cls.__Eyes.clear_galleries( )
                cls.__Eyes.add_galleries( populars )
                
                # push into newest state
                cls.__Eyes.push_state( NhCommand.POPULAR )
                
                cls.__Reply.add_message( reply )
                cls.__Reply.add_message( "$popular 成功, 可用的指令有 $open, $home" )
            else :
                cls.__Reply.add_message( "$popular 失敗, 找不到 $popular" )
        else :
            cls.__Reply.add_message( "$popular 失敗, 必須位在 $home" )
    
    
    # ##############################################################
    # #################### get newest galleries ####################
    # ##############################################################
    @classmethod
    def newest ( cls, current_state: NhCommand ) :
        # only available while current state is home
        if current_state == NhCommand.HOME :
            # get newest galleries and convert to reply form
            newest = cls.__Hand.get_newest_result( 1 )
            found, reply = NhEyes.galleries_to_reply_form( newest )
            
            # check if any galleries found
            if found == True :
                # clear and add result galleries
                cls.__Eyes.clear_galleries( )
                cls.__Eyes.add_galleries( newest )
                
                # push into newest state
                cls.__Eyes.push_state( NhCommand.NEWEST )
                
                cls.__Reply.add_message( reply )
                cls.__Reply.add_message( "$newest 成功, 可用的指令有 $open, $next, $goto, $home" )
            
            else :
                cls.__Reply.add_message( "$newest 失敗, 找不到 $newest" )
        
        else :
            cls.__Reply.add_message( "$newest 失敗, 必須位在 $home" )
    
    
    # ##############################################################
    # ###################### search galleries ######################
    # ##############################################################
    @classmethod
    def search ( cls, current_state: NhCommand ) :
        # only available while current state is home
        if current_state == NhCommand.HOME :
            # use remain tokens as keywords to search
            keywords = tokens[1 :]
            
            # check if search without keywords
            if keywords != [] :
                # get search galleries and convert to reply form
                search_result = cls.__Hand.get_search_result( keywords, 1 )
                found, reply = NhEyes.galleries_to_reply_form( search_result )
                
                # check if any galleries found
                if found == True :
                    # clear and add result galleries
                    cls.__Eyes.clear_galleries( )
                    cls.__Eyes.add_galleries( search_result )
                    
                    # push into search state
                    cls.__Eyes.push_state( NhCommand.SEARCH )
                    
                    cls.__Reply.add_message( reply )
                    cls.__Reply.add_message( "$search 成功, 可用的指令有 $open, $next, $goto, $home" )
                
                else :
                    cls.__Reply.add_message( "$search 失敗, 此關鍵字無搜尋結果" )
            else :
                cls.__Reply.add_message( "$search 失敗, 搜尋帶關鍵字很難嗎？" )
        else :
            cls.__Reply.add_message( "$search 失敗, 必須位在 $home" )
    
    
    # ##############################################################
    # ####################### goto next page #######################
    # ##############################################################
    @classmethod
    def next ( cls, current_state: NhCommand ) :
        # only available while search or newest
        if current_state in [NhCommand.SEARCH, NhCommand.NEWEST] :
            # get next page galleries and convert to replay form
            next_page_result = cls.__Hand.get_next_page_result( )
            found, reply = NhEyes.galleries_to_reply_form( next_page_result )
            
            # check if any galleries found
            if found == True :
                # clear and add next page's galleries
                cls.__Eyes.clear_galleries( )
                cls.__Eyes.add_galleries( next_page_result )
                
                cls.__Reply.add_message( reply )
                cls.__Reply.add_message( "$next 成功, 可用的指令有 $open, $next, $goto, $home" )
            else :
                cls.__Reply.add_message( "$next 失敗, 找不到下一頁" )
        else :
            cls.__Reply.add_message( "$next 失敗, 必須位在 $search or $newest" )
    
    
    # #############################################################
    # ######################## goto page N ########################
    # #############################################################
    @classmethod
    def goto ( cls, current_state: NhCommand ) :
        # only available while search or newest
        if current_state in [NhCommand.SEARCH, NhCommand.NEWEST] :
            try :
                # try to use tokens[1] as page, if not int -> ValueError
                target_page = int( tokens[1] )
                
                if target_page == 0 :
                    target_page = 1
                    cls.__Reply.add_message( ">>> $goto 要從 1 開始，自動導向到 $goto 1 <<<\n\n" )
                
                # get target page result
                target_galleries = cls.__Hand.get_result_of_this_page( target_page )
                found, reply = NhEyes.galleries_to_reply_form( target_galleries )
                # check if any galleries found
                if found == True :
                    # clear and add target galleries
                    cls.__Eyes.clear_galleries( )
                    cls.__Eyes.add_galleries( target_galleries )
                    cls.__Reply.add_message( reply )
                    cls.__Reply.add_message( "$goto 成功, 可用的指令有 $open, $next, $goto, $home" )
                
                else :
                    cls.__Reply.add_message( "$goto 失敗, 指定的頁數不存在" )
            
            except IndexError :
                cls.__Reply.add_message( "$goto 失敗, 不輸入頁數是要我通靈？" )
            except ValueError :
                cls.__Reply.add_message( "$goto 失敗, 輸入一個頁「數」很難嗎？" )
        else :
            cls.__Reply.add_message( "$goto 失敗, 必須位在 $search or $newest" )
    
    
    # ###############################################################
    # ###################### open this gallery ######################
    # ###############################################################
    @classmethod
    def open ( cls, current_state: NhCommand ) :
        # only available while popular, search, newest
        if current_state in [NhCommand.POPULAR, NhCommand.SEARCH, NhCommand.NEWEST] :
            # use tokens[1] to select target gallery, if not int -> ValueError
            try :
                gallery_index = int( tokens[1] )
                
                gallery: NhGallery
                found, gallery = cls.__Eyes.get_gallery_by_index( gallery_index )
                
                # check if this index out of range
                if found == True :
                    # open gallery and set it new book
                    cls.__Eyes.open_this_gallery( gallery_index )
                    cls.__Eyes.push_state( NhCommand.OPEN )
                    
                    # get opened gallery info
                    reply = cls.__Eyes.get_reading_gallery_info( )
                    
                    cls.__Reply.add_message( reply )
                    cls.__Reply.add_message( "$open 成功, 可用的指令有 $watch, $close, $home" )
                
                # gallery index out of range
                else :
                    cls.__Reply.add_message( "$open 失敗, 輸入範圍內的編號很難嗎" )
            except IndexError :
                cls.__Reply.add_message( "$open 失敗, 不指定哪本是要我通靈？" )
            except ValueError :
                cls.__Reply.add_message( "$open 失敗, 輸入一個正確的「編號」很難嗎？" )
        else :
            cls.__Reply.add_message( "$open 失敗, 必須位在 $popular, $search, $newest" )
    
    
    # ###############################################################
    # #################### close reading gallery ####################
    # ###############################################################
    @classmethod
    def close ( cls, current_state: NhCommand ) :
        # only available while open
        if current_state == NhCommand.OPEN :
            # close and clear current reading
            cls.__Eyes.clear_reading( )
            # pop current state (go back to last state)
            cls.__Eyes.pop_state( )
            
            # check if new state is popular
            if cls.__Eyes.get_current_state( ) == NhCommand.POPULAR :
                cls.__Reply.add_message( "$close 成功, 可用的指令有 $open, $home" )
            else :
                cls.__Reply.add_message( "$close 成功, 可用的指令有 $open, $next, $goto, $home" )
        else :
            cls.__Reply.add_message( "$close 失敗, 沒先 $open 是要 $close 什麼？" )
    
    
    # ###############################################################
    # ####################### watch this page #######################
    # ###############################################################
    @classmethod
    def watch ( cls, current_state: NhCommand ) :
        # only available while open
        if current_state == NhCommand.OPEN :
            # check if tokens[1] exist
            try :
                # get token[1] as page number(start from 0), if not int -> ValueError
                page = int( tokens[1] )
                
                # try to get target page from current reading book
                found, url = cls.__Eyes.get_reading_page_link( page )
                if found == True :
                    cls.__Reply.set_url( url )
                    cls.__Reply.add_message( "$watch 成功, 可用的指令有 $watch, $close, $home" )
                
                else :
                    cls.__Reply.add_message( "$watch 失敗, 指定頁數超出範圍（從 0 開始）" )
            except IndexError :
                cls.__Reply.add_message( "$watch 失敗, 不輸入頁數是要我通靈？" )
            except ValueError :
                cls.__Reply.add_message( "$watch 失敗, 輸入正確的頁「數」很難嗎？" )
        else :
            cls.__Reply.add_message( "$watch 失敗, 沒先 $open 是要 $watch 什麼？" )


if __name__ == '__main__' :
    # msg = NhUser.do_command( ["$home"] )
    # msg = NhUser.do_command( ["$popular"] )
    msg = NhUser.do_command( ["$home"] )
    msg = NhUser.do_command( ["$newest"] )
    # msg = NhUser.do_command( ["$search", "ichiri", "isekai"] )
    # msg = NhUser.do_command( ["$open", "0"] )
    # msg = NhUser.do_command( ["$watch", "0"] )
    pass