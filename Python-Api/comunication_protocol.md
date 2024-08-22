

# Used commands 
## `set` 
set led colors 
    
throws:
`GENERAL LED ERROR` 

request:
`command data\n`

request example:
`set 00ff00 ff00ff 00ff00 ff0056\n`

response:
`errors\n`

correct response example:
`ok\n`

error response example:
`GENERAL LED ERROR\n`


## `get` 
reads current board state
throws:
`GENERAL BUTTON MATRIX ERROR`

request:
`command\n`

request example:
`get\n`

response:
`errors data change_id\n`

change id is used to distinguish two board states  

correct response example:
`ok 0 1 0 0 4\n`

error response example:
`GENERAL BUTTON MATRIX ERROR\n`


## `avt`
waits for board state to change than returns new board state
can be interrupted with new set/get command // todo
throws:
`GENERAL BUTTON MATRIX ERROR`

request:
`command\n`

request example:
`get\n`

response:
`errors data change_id\n`

change id is used to distinguish two board states  

correct response example:
`ok 0 1 0 0 4\n`

error response example:
`GENERAL BUTTON MATRIX ERROR\n`

