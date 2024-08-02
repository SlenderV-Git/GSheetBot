from app.models.sheets_entry import Client
import re

def validate_c_command(command):
    pattern = re.compile(r'^/c\s+-?\d+\s+\w+$')
    
    if pattern.match(command):
        return True
    else:
        return False
    
def validate_command(command):
    pattern_with_trips = re.compile(r'^/(a|r)\s+\w+\s+\w+-\w+\s+\d+/\d+\s+\d+$')
    pattern_without_trips = re.compile(r'^/(a|r)\s+\w+\s+\w+-\w+\s+\d+\s+\d+$')
    
    if pattern_with_trips.match(command):
        return True
    elif pattern_without_trips.match(command):
        return True
    else:
        return False

def clear_command_prefix(prefix : str, command : str):
    return command.replace(prefix, "", 1)

def convert_to_client(command: str):
    data = command.strip().split()
    from_client, where_client = data[1].split("-")
    
    if "/" in data[2]:
        hours, trips = data[2].split("/")
    else:
        hours, trips = data[2], ""
    
    return Client(
        name=data[0],
        from_client=from_client,
        where_client=where_client,
        hours=int(hours),
        trips=trips,
        summ=int(data[3])
    )