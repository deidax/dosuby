from .search_response import SearchResponse

class SuccessResponse(SearchResponse):
    
    
    

    
    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return "{}: {}".format(msg.__class__.__name__, "{}".format(msg))
        return msg