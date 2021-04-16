# Terminal TicTacToe

Text-based TicTacToe game that is playable in the terminal.

There are Server-Client applications that can be run to play your opponent online, via TCP sockets!

The arguments are as follows:
* tttServer \[PORT]
* tttClient \[IP] \[PORT]
  * 'localhost' can be inputted for \[IP] on local connection

There is also a local application, tttLocal, where 2 players can play within the same terminal window, taking turns inputting their moves each turn.

Currently, both the local application and the Server-Client applications are working as intended. I will be adding more to the latter to make the matches more user friendly.

Let me know if and how you break my code!

## Credits:
Initial idea originated from Engineer Man's Youtube channel. Particularly this [Project Review video](https://www.youtube.com/watch?v=BcYI-w_-rwg&t=12s)

He also uploaded the code onto [his Github](https://github.com/engineer-man/youtube/tree/master/043)

## To Be Implemented:
* IP address & Port as args when user launches client app -- **DONE**
* Make server output pretty -- **DONE**
* Play again option after game end
