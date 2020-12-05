# Console app to work with TCP chat
Key features:
- reading chat messages
- register a new user
- user authentication
- sending chat messages

### Installing

1. just run "pip install -r requirements.txt" in you venv

###Usage

#####Chat reader
Default host is 'minechat.dvmn.org' and port is '5000'. Default
log file name is 'minechat.history'  

    >>> python3 chat_reader.py

#####Chat writer
Default host is 'minechat.dvmn.org' and port is '5050'. By default chat token
is got from os environment variable CHAT_TOKEN   

    >>> python3 chat_writer.py

###Help
Use --help arg to see available configuration args