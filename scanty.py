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
    "commands" : "Get List of All Commands",
    "exit" : "Exit Scanty",
    "cls" : "Clear The Screen",
    "cd" : "Change Directory -> Multi Directory Traversal with slashes may be faulty",
    "setprompt" : "Set prefix of Current Prompt",
    "pwd" : "Print the Current Working Directory",
    "cat" : "Show the Contents of a file -> UTF like readable files(non-binaries)",
    "mkdir" : "Create New Folder -> Recursive Directory Creation not yet supported"
}

pwd = os.getcwd()
prompt_prefix = ""
cmd_dct = {
    "ls" : "os.listdir()",
    "commands" : "sorted(list(cmd_dct.keys()))",
    "cd" : "os.chdir('{arg}')",
    "lsdir" : "list(filter(os.path.isdir, os.listdir()))",
    "help" : "help_cmd.get('{arg}')",
    "cls" : "os.system('cls') if os.name=='nt' else os.system('clear')",
    "exit" : "sys.exit(1)",
    "setprompt" : "prompt_prefix='{arg} '",
    "pwd" : "os.getcwd()",
    "cat" : """\nf=open('{arg}','r')\nprint(f.read())\nf.close()\n""",
    "mkdir" : "os.mkdir('{arg}')"
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
    "mkdir" : 1
}

while True:
    sys.stdout.write(pwd+"> ")
    inp = input()
    inp = inp.strip()
    command_tokens = inp.split(" ")
    command = command_tokens[0]
    try:
        if command in cmd_dct and command.strip() != '':
            arg_limit=cmd_args_limit[command]
            if arg_limit == len(command_tokens) - 1:
                console_command = cmd_dct[command].format(arg="".join(command_tokens[1:]))
                if command == "cd":
                    eval(console_command)
                    pwd = prompt_prefix + os.getcwd()

                if command == "setprompt" or command == "cat":
                    exec(console_command)
                    pwd = prompt_prefix + os.getcwd()

                if len(command_tokens) < 2: #ls lsdir
                    if isinstance(eval(cmd_dct[command]), list):
                        for item in eval(cmd_dct[command]):
                            print(item)
                    
                if isinstance(eval(console_command), str) == True:
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