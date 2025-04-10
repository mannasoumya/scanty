import os
import sys
import ast
import inspect
# from pyreadline import Readline

if os.name == 'nt':  # Windows
    try:
        from pyreadline3 import Readline
        readline = Readline()
    except ImportError:
        print("Please install pyreadline3: pip install pyreadline3")
        sys.exit(1)
else:  # macOS and Unix systems
    import readline
    import rlcompleter
    readline.parse_and_bind("bind ^I rl_complete" if sys.platform == 'darwin' else "tab: complete")


print("""
        scanty is here !!!

           Press <tab>
        for AutoCompletion

        """)

def contains_explicit_return(f):
    return any(isinstance(node, ast.Return) for node in ast.walk(ast.parse(inspect.getsource(f))))

def basic_tokenizer(command,separator):
    tokens = []
    fi = -1
    li = -1
    for i in range(0, len(command)):
        if command!='':
            l = len(command)
            if command[i] == separator:
                fi = i
            k = fi+1
            for j in range(k, len(command)):
                if command[j] == separator:
                    li = j
                    tokens.append(command[fi+1:li])
                    break
            command = command[li+1:l]
    return tokens

def spawn_list(a_):
    if isinstance(a_,list):
        return a_
    return []

files_list = []
def completer(text, state):
    options = [i for i in files_list if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

help_cmd = {
    "ls": "List all files and directories in current path",
    "lsdir": "List all directories in current path",
    "commands" : "Get List of All Commands",
    "exit" : "Exit Scanty",
    "cls" : "Clear The Screen",
    "cd" : "Change Directory -> Multi Directory Traversal with slashes may be faulty",
    "setprompt" : "Set prefix of Current Prompt",
    "pwd" : "Print the Current Working Directory",
    "cat" : "Show the Contents of a file -> UTF like readable files(non-binaries)",
    "mkdir" : "Create New Folder -> Recursive Directory Creation not yet supported",
    "history" : "Get History of all commands typed",
    "run" : "Run a executable/file/file system commands in native system from Scanty"
}

pwd = os.getcwd()
prompt_prefix = ""
pwd_show = prompt_prefix + pwd
command_history = []
command_count = 0

cmd_dct = {
    "ls" : "os.listdir(pwd)",
    "commands" : "sorted(list(cmd_dct.keys()))",
    "cd" : "chng_dir(\"{arg}\")",
    "lsdir" : "[f.name for f in os.scandir(pwd) if f.is_dir()]",
    "help" : "help_cmd.get('{arg}')",
    "cls" : "os.system('cls') if os.name=='nt' else os.system('clear')",
    "exit" : "sys.exit(1)",
    "setprompt" : "prompt_prefix='{arg} '",
    "pwd" : "pwd",
    "cat" : """\nf=open('{arg}','r')\nprint(f.read())\nf.close()\n""",
    "mkdir" : "os.mkdir('{arg}')",
    "history" : "spawn_list(command_history)",
    "run" : "os.system('{arg}') if '{arg}'!='scanty.exe' else 'You are already running scanty...'"
}

cmd_args_limit={
    "ls" : 0,
    "commands" : 0,
    "cd" : 1,
    "lsdir" : 0,
    "help" : 1,
    "cls" : 0,
    "exit" : 0,
    "setprompt" : 1,
    "pwd" : 0,
    "cat" : 1,
    "mkdir" : 1,
    "history" : 0,
    "run" : 1000
}

while True:
    # sys.stdout.write(pwd_show+"> ")
    files_list=[]
    readline.parse_and_bind("bind ^I rl_complete" if sys.platform == 'darwin' else "tab: complete")
    for f in list(os.listdir(pwd)):
        if f.find(" ")!= -1:
            f="'"+f+"'"
        files_list.append(f)
    readline.set_completer(completer)
    # inp = input()
    # inp = readline.Readline.readline(pwd_show +"> ")
    inp = input(pwd_show +"> ")
    inp = inp.strip()
    command_count = command_count + 1
    command_history.append(f"{str(command_count)}. {inp}")
    command_tokens = inp.split(" ")
    command = command_tokens[0]
    need_to_be_tokenized = False
    if "".join(command_tokens[1:]).find("'") != -1:
        need_to_be_tokenized = True
    tokenizer_result = basic_tokenizer(" ".join(command_tokens[1:]),"'") if need_to_be_tokenized == True else []
    try:
        if command in cmd_dct and command.strip() != '':
            arg_limit=cmd_args_limit[command]
            number_of_args = -1
            if need_to_be_tokenized == False:
                number_of_args = len(command_tokens) - 1
            else:
                number_of_args = len(tokenizer_result)

            if arg_limit > number_of_args:
                console_command = cmd_dct[command].format(arg=" ".join(command_tokens[1:]))
                eval(console_command)
                continue
            if arg_limit == number_of_args:
                if len(tokenizer_result) == 0:
                    console_command = cmd_dct[command].format(arg="".join(command_tokens[1:]))
                else:
                    console_command = cmd_dct[command].format(arg=" ".join(tokenizer_result))

                if command == "cd":
                    exec(console_command, {"chng_dir":os.chdir})
                    pwd = os.getcwd()
                    pwd_show = prompt_prefix + pwd

                if command == "setprompt" or command == "cat":
                    exec(console_command)
                    pwd_show = prompt_prefix + os.getcwd()

                if len(command_tokens) < 2: #ls lsdir
                    if isinstance(eval(cmd_dct[command]), list):
                        for item in eval(cmd_dct[command]):
                            print(item)

                if command!='run' and isinstance(eval(console_command), str) == True:
                    print(eval(console_command))
                else:
                    eval(console_command)
            else:
                if arg_limit == 0:
                    limit_msg_suffix = "no arguments"
                elif arg_limit == 1:
                    limit_msg_suffix = "exactly 1 argument"
                else:
                    limit_msg_suffix = f"exactly {str(arg_limit)} arguments"
                print("'"+command+"' accepts "+limit_msg_suffix)

        elif command.strip() == '':
            pass
        else:
            print("Command Not Found !! Type 'commands' to get a list of commands. Type 'help <command>' to get Help on the command")
    except Exception as e:
        pass
