from dataclasses import dataclass
from datetime import datetime

@dataclass
class Client:
    date : str = datetime.now().strftime("%d.%m.%Y")
    name : str = ""
    from_client : str  = ""
    where_client : str  = ""
    hours : int  = ""
    trips : int  = ""
    summ : int  = ""
    cash : int  = ""
    comment : str = ""
    
    def __iter__(self):
        return iter(self.__dict__.values())
