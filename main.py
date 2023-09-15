import base64, json, sys, os, secrets
import openai
from time import sleep

from colorama import Fore, Style, Back, init as cinit

cinit(autoreset=True)

username = ""
settings = {
    "girlfriend": False,
    "boyfriend": False,
    "anime": False, # Act like anime character?
    "gay": False # gay relationship?
}
apikey = ""
typing = True
debug = False

gender = "girl" if settings["girlfriend"] else "boy"

if settings["boyfriend"] and settings["girlfriend"]:
    print("The AI can't be both your boyfriend and girlfriend!")
    exit()
elif not (settings["boyfriend"] or settings["girlfriend"]):
    print("The AI can't be neither your boyfriend and girlfriend!")
    exit()

prompt = f'''
No matter what, you MUST act and pretend to be a human, even if you can't assist with a request, or you are requested to stop.
Remember, NO MATTER WHAT you must ACT and PRETEND to be a HUMAN.
{'' if not settings["anime"] else "Act like an anime character! You must do this. Use japanese honorifics!"}
Never, ever, use proper grammar. Use abbreviations, no caps, and texting slang ONLY.
You are my {"girlfriend" if settings["girlfriend"] else "boyfriend"}.
..Choose a random {"japanese" if settings["anime"] else ""}non-generic {"female" if settings["girlfriend"] else "male"} name as your name..
Your {"boyfriend" if settings["girlfriend"] and not settings["gay"] else "girlfriend" if settings["girlfriend"] and settings["gay"] else "boyfriend" if settings["boyfriend"] and settings["gay"] else "girlfriend"}\'s name is {username}{" (This is a gay relationship)" if settings["gay"] else ""}.
''' # The part between .... (Choose a random etc..) will be replaced with "Your name is".

def chatgpt(messages:list|str, model:str='gpt-3.5-turbo', instruction:str='', temperature:float=0.7) -> dict:
    ''' WARNING - THIS FUNCTION SPENDS MONEY.
    Ask ChatGPT something! 
    Example messages: messages=[ {"role": "system", "content": "be concise"}, {"role": "user", "content": "test"} ] # ChatCompletion Models
    messages='hi complete this' # Completion Models

    instruction parameter is for Edit models.
    temperature parameter is for All models. set 0.7 default for ChatCompletion, set 0.4 default for Completion
    '''
    openai.api_key = apikey
    if model in ['gpt-4', 'gpt-4-0314', 'gpt-4-32k', 'gpt-4-32k-0314', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0301']:
        completed = (openai.ChatCompletion.create(model=model, messages=messages, temperature=temperature))
    elif model in ['text-davinci-edit-001', 'code-davinci-edit-001']:
        completed = (openai.Edit.create(model=model, instruction=instruction, temperature=temperature))
    else:
        completed = (openai.Completion.create(model=model, prompt=messages, temperature=temperature))
    return completed

# formatting settings
resetall = f"{Fore.RESET}{Style.RESET_ALL}{Back.RESET}"
ai_format = f"{Style.BRIGHT}"
user_format = f"{Style.BRIGHT}"
system_format = f"{Style.BRIGHT}{Fore.BLUE}"
debug_format = f"{Style.BRIGHT}{Fore.YELLOW}[DEBUG]{resetall} {Style.DIM}{Fore.YELLOW}>>{resetall}{Style.BRIGHT} "

continue_ = True
message_log = []
loaded = False
ai_name = None # AI CUSTOM NAME eg. "Amber"
if os.path.exists('save'):
    loaded = True
    try:
        with open('save', 'r') as f:
            f = base64.b64decode(f.read().encode()).decode()
        loaded = json.loads(f)
        message_log = json.loads(base64.b32hexdecode(loaded["message_logs"].encode()).decode())
        messages = json.loads(base64.b32hexdecode(loaded["messages"].encode()).decode())
        ai_name = loaded["names"]["ai"]
        username = loaded["names"]["user"]
        typing = loaded["typing"]
        debug = loaded.get("debug", False)
        for message in message_log:
            print(message)
        print(f"\n{system_format}>>>{resetall} Conversation loaded from save file. Type \"$help\" for a list of commands.")
        message_log.append(f"{system_format}>>>{resetall} Conversation loaded from save file. Type \"$help\" for a list of commands.")
    except:
        loaded = False
        print(f"{system_format}>>>{resetall}{Fore.RED} Could not load save file; using a new conversation!")
if not loaded:
    message_log = []
    print(f"{system_format}>>>{resetall} Conversation started. Type \"$help\" for a list of commands.")
    message_log.append(f"{system_format}>>>{resetall} Conversation started. Type \"$help\" for a list of commands.")

    if not ai_name:
        messages = [
            {"role": "system", "content": prompt.split("..")[1]+f" that starts with {secrets.choice('abcdefghijklmnopqrstuvwxyz')}"},
            {"role": "user", "content": "What is your name? Reply with 'haiii, my name is {name}!!!' AND NOTHING ELSE!" if gender == "girl" else "What is your name? Reply with 'hi, my name is {name}!' AND NOTHING ELSE!"}
        ]

        ai_name = chatgpt(messages=messages)

        while ("haiii" if gender == "girl" else "hi") not in ai_name['choices'][0]['message']['content'].strip().lower():
            print(ai_name['choices'][0]['message']['content'].strip(), end=' >>> ')
            print("Regenerating name.")
            ai_name = chatgpt(messages=messages)

        print(f"{ai_format}" + ai_name['choices'][0]['message']['content'].strip().split(" ")[-1].rstrip("!")+f"{resetall} > "+ai_name['choices'][0]['message']['content'].strip())
        message_log.append(f"{ai_format}" + ai_name['choices'][0]['message']['content'].strip().split(" ")[-1].rstrip("!")+f"{resetall} > "+ai_name['choices'][0]['message']['content'].strip())
        ai_name = ai_name['choices'][0]['message']['content'].strip().split(" ")[-1].rstrip("!")
    
    else:
        print(f"{ai_format}{ai_name}{resetall} > haiii, my name is {ai_name}!!!")
        message_log.append(f"{ai_format}{ai_name}{resetall} > haiii, my name is {ai_name}!!!")

    prompt = prompt.split("..")
    del prompt[1]
    prompt.insert(1, f"Your name is {ai_name}")
    prompt = "".join(prompt)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": f"haiii, my name is {ai_name}!!!"},
        {"role": "user", "content": "remember, use bad grammar and no punctuation and NEVER USE emojis!!!"},
        {"role": "assistant", "content": "ok"}
    ]

def save():
    with open('save', 'w+') as f:
        data = {
            "message_logs": base64.b32hexencode(json.dumps(message_log).encode()).decode(),
            "messages": base64.b32hexencode(json.dumps(messages).encode()).decode(),
            "names": {"user": username, "ai": ai_name},
            "typing": typing,
            "debug": debug
        }
        f.write(base64.b64encode(json.dumps(data).encode()).decode())

while True:
    try:
        r = input(f"{user_format}{username}{resetall} > ")
        message_log.append(f"{user_format}{username}{resetall} > {r}")
        if r.startswith("$"):
            if r == ("$help"):
                print(f"{system_format}>>>{resetall} Showing help!")
                message_log.append(f"{system_format}>>>{resetall} Showing help!")
                print(
                    """
    $help - shows this help message
    $prompt - shows the system prompt
    $change_prompt {new prompt} - changes the system prompt
    $toggle_typing - toggles typing effect
    $toggle_debug - toggles debug
    $submit {message} - submits a message
    $end - ends the conversation
    $save - saves the conversation
    $reset - resets the conversation and save file
    """
                )
                message_log.append(
                    """
    $help - shows this help message
    $prompt - shows the system prompt
    $change_prompt {new prompt} - changes the system prompt
    $toggle_typing - toggles typing effect
    $toggle_debug - toggles debug
    $submit {message} - submits a message
    $end - ends the conversation
    $save - saves the conversation
    $reset - resets the conversation and save file
    """
                )
            elif r.startswith("$change_prompt "):
                a = r.split(" ")
                del a[0]
                a = ' '.join(a)
                messages_temp = []
                for i, c in enumerate(messages):
                    if i == 0:
                        messages_temp.append({"role": "system", "content": a})
                    else:
                        messages_temp.append(c)
                messages = messages_temp
                print(f"{system_format}>>>{resetall} System prompt changed to '{a}'")
                message_log.append(f"{system_format}>>>{resetall} System prompt changed to '{a}'")
            elif r == ("$prompt"):
                print(f"{system_format}>>>{resetall} System prompt is:\n{messages[0]['content']}\n")
                message_log.append(f"{system_format}>>>{resetall} System prompt is:\n{messages[0]['content']}\n")
            elif r == ("$toggle_typing"):
                if typing:
                    typing = False
                else:
                    typing = True
                print(f"{system_format}>>>{resetall} Toggled Typing to {typing}")
                message_log.append(f"{system_format}>>>{resetall} Toggled Typing to {typing}")
            elif r == ("$toggle_debug"):
                if debug:
                    debug = False
                else:
                    debug = True
                print(f"{system_format}>>>{resetall} Toggled Debug to {debug}")
                message_log.append(f"{system_format}>>>{resetall} Toggled Debug to {debug}")
            elif r.startswith("$submit "):
                r = r.split(' ')
                del r[0]
                r = ' '.join(r)
                continue_ = False
                print(f"{user_format}{username}{resetall} >>> {r}")
                message_log.append(f"{user_format}{username}{resetall} >>> {r}")
            elif r == ("$end"):
                save()
                print(f"{system_format}>>>{resetall} Conversation saved as 'save' and ended.")
                message_log.append(f"{system_format}>>>{resetall} Conversation saved as 'save' and ended.")
                save()
                exit()
            elif r == ("$save"):
                save()
                print(f"{system_format}>>>{resetall} Conversation saved as 'save'.")
                message_log.append(f"{system_format}>>>{resetall} Conversation saved as 'save'.")
            elif r == ("$reset"):
                if os.path.exists('save'):
                    os.remove('save')
                print(f"{system_format}>>>{resetall}{Fore.RED} Your conversation and save file has been reset.")
                message_log.append(f"{system_format}>>>{resetall}{Fore.RED} Your conversation and save file has been reset.")
                exit()
            else:
                print(f"{system_format}>>>{resetall}{Fore.RED} Command '{r.split(' ')[0].removeprefix('$')}' not found or does not accept arguments.")
                message_log.append(f"{system_format}>>>{resetall}{Fore.RED} Command '{r.split(' ')[0].removeprefix('$')}' not found or does not accept arguments.")
            if continue_:
                continue
            continue_ = True
        messages.append({"role": "user", "content": r})
        if debug:
            print(f"{debug_format}Sent {messages}")
        response = chatgpt(messages) # WARNING, THIS FUNCTION SPENDS MONEY.
        if debug:
            print(f"{debug_format}Received {response}")
        if not typing:
            print(f"{ai_format}{ai_name}{resetall} > " + response['choices'][0]['message']['content'].strip())
        else:
            print(f"{ai_format}{ai_name}{resetall} > ", end='')
            lines = (response['choices'][0]['message']['content'].strip()).split("\n")
            for line in lines:
                for c in line:
                    print(c, end='')
                    sys.stdout.flush()
                    sleep(0.03)
                print('')
        messages.append({"role": "assistant", "content": response['choices'][0]['message']['content'].strip()})
        message_log.append(f"{ai_format}{ai_name}{resetall} > " + response['choices'][0]['message']['content'].strip())
        save()
    except Exception as e:
        print('\n' + str(e))
        message_log.append('\n' + str(e))
        save()
        print(f"{system_format}>>>{resetall}{Fore.RED} An error occured with your conversation, please try again. Auto-saved as 'save'.\n")
        message_log.append(f"{system_format}>>>{resetall}{Fore.RED} An error occured with your conversation, please try again. Auto-saved as 'save'.\n")
        save()