```json
{
    "action" : "%action", 
    "action_parameters" : { 
    }
}
```

# "action" contains one of the actions:
- attack
- defend
- take_all

# "action_parameters" contains the actions parameters like:
- cards being placed for attack/defend

# The server returns a json object string that looks like this:
```json
{
    "cards" : [],
    "turn" : "%turn"
}
```
# "turn" contains one of these:
- you
- notyou
