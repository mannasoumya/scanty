import os
import sys
import ast
import inspect

print("\n\n\n\t scanty is here !!!\n\n\n")

def contains_explicit_return(f):
    return any(isinstance(node, ast.Return) for node in ast.walk(ast.parse(inspect.getsource(f))))

help_cmd = {
    "ls": "List all files and directories in current path",
    "lsdir": "List all directories in current path",
    "commands":"Get List of All Commands",
    "exit":"Exit Console",
    "cls":"Clear The Screen"
}

pwd = os.getcwd()
prompt_prefix=""
cmd_dct = {
    "ls": "os.listdir()",
    "commands": "sorted(list(cmd_dct.keys()))",
    "cd": "os.chdir('{arg}')",
    "lsdir": "list(filter(os.path.isdir, os.listdir()))",
    "help": "help_cmd.get('{arg}')",
    "cls": "os.system('cls') if os.name=='nt' else os.system('clear')",
    "exit": "sys.exit(1)",
    "setprompt" : "prompt_prefix='{arg} '",
    "pwd" : "os.getcwd()"
}

while True:
    sys.stdout.write(pwd+"> ")
    inp = input()
    inp = inp.strip()
    command_tokens = inp.split(" ")
    command = command_tokens[0]
    try:
        if command in cmd_dct and command.strip() != '':
            console_command = cmd_dct[command].format(arg="".join(command_tokens[1:]))
            if command == "cd":
                eval(console_command)
                pwd = prompt_prefix + os.getcwd()

            if command == "setprompt":
                exec(console_command)
                pwd = prompt_prefix + os.getcwd()

            elif isinstance(eval(cmd_dct[command]), list):
                for item in eval(cmd_dct[command]):
                    print(item)

            elif isinstance(eval(console_command), str) == True:
                print(eval(console_command))

            else:
                eval(console_command)

        elif command.strip() == '':
            pass
        else:
            print("Command Not Found !! Type 'commands' to get a list of commands ")
    except Exception as e:
        pass