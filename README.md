# AI Relationship
AI relationship with an AI Girlfriend or an AI Boyfriend!

Customize some settings and have some fun!

This project isn't coded neatly (it's still under development), so bear with me! Star this repo for faster development.
- Feel free to open a PR cleaning up my code.

Eventually, when this is cleaned up and ready, I'll make it customizable without going into `main.py` and have releases.

### SCROLL DOWN FOR SETTINGS, SETUP, and details on SAVE FILES

# OpenAI API KEY
This project uses OpenAI's API.

Using ChatGPT 3.5 Turbo.

You can get an API key here: https://platform.openai.com/account/api-keys
!! API KEYS ARE PAID, AND WILL NOT WORK WITHOUT VALID BILLING !!

### Cost Estimates
coming soon...

# Settings
There are some things you can change in `main.py`, depending on what you want for your AI relationship!

### Normal Settings
These are located near the top of the file.
```python
username = ""
settings = {
    "girlfriend": False,
    "boyfriend": False,
    "anime": False, # Act like anime character?
    "gay": False # gay relationship? yes or no.
}
apikey = ""
typing = True
debug = False
```

username - The name you're using to talk to the AI. (EG. Your username is "John". The AI will talk to you as John.)
settings - Settings for your relationship
 - girlfriend - Is the AI your girlfriend? (Only one of girlfriend/boyfriend must be true)
 - boyfriend - Is the AI your boyfriend? (Only one of girlfriend/boyfriend must be true)
 - anime - Act like an anime character and have a Japanese name?
 - gay - Whether this relationship is gay or not. (EG. If gay = True and girlfriend = True, AI assumes you're a girl and the AI is your girlfriend. Or, if gay = True and boyfriend = True, AI assumes you're a boy and the AI is your boyfriend.)
apikey - Your OpenAI API Key. Obtainable at https://platform.openai.com/account/api-keys
typing - Whether or not to use a typing effect.
debug - Debug mode? This gets messy fast, and should not be used normally. (DEBUG messages are not saved in save files.)

### Setting a Custom AI Name
You can set a custom AI name for your relationship! Simply find the line commented with "# AI CUSTOM NAME"
```python
ai_name = None # AI CUSTOM NAME eg. "Amber"
```
Simply set `ai_name = "Name"` to set a custom name.
Set `ai_name = None` for a random name.

### Formatting Settings
These settings are located under the comment `# formatting settings`, around line 60
```python
resetall = f"{Fore.RESET}{Style.RESET_ALL}{Back.RESET}"
ai_format = f"{Style.BRIGHT}"
user_format = f"{Style.BRIGHT}"
system_format = f"{Style.BRIGHT}{Fore.BLUE}"
debug_format = f"{Style.BRIGHT}{Fore.YELLOW}[DEBUG]{resetall} {Style.DIM}{Fore.YELLOW}>>{resetall}{Style.BRIGHT} "
```
resetall - You shouldn't change this.
ai_format - Format for AI prefix. It is used like `{ai_format}AI's NAME{resetall} > {AI MESSAGE}`
user_format - Format for USER prefix. It is used like `{user_format}USERNAME{resetall} > {INPUTTED MESSAGE}`
system_format - Format for System command responses. It is used like `{system_format}>>>{resetall} SYSTEM MESSAGE/RESPONSE`
debug_format - Format for DEBUG messages. It is used like `{debug_format}DEBUG MESSAGE`

# Setup
1. Insert all relevant settings and customize them to your liking. (See: SETTINGS section)
2. Install the requirements with `pip install -r requirements.txt`
3. Run `run.bat` on Windows, or open a console and run it there.
4. Have fun chatting!

# Save files
Here is an explanation on save files.

The AI will load any save file named `save` (no file type suffix) in its current running directory.

If not found, a new converstion will start with the current settings used.

If found:
1. It will attempt to load the `save` file (if fails, a new conversation starts).
2. It will print every old message EXCLUDING DEBUG MESSAGES (`$toggle_debug`).
3. The conversation will continue where you left off.

### New Settings
New settings cannot be applied to old save files; save files will continue using your username and AI name used in your conversation. (of course though, you can manually edit the save file (no tutorial for this) and replace your names)

### Saving
When your conversation saves.
- The conversation auto-saves after the AI responds.
- The conversation saves when you run the `$save` command.
- The conversation saves when you run the `$end` command.