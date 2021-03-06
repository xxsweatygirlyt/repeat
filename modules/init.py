
import os, json, time, sys
from modules import package

try:
    from colorama import Fore
except ImportError as e:
    package.install_module(module=e.name)
    print(f"Installed missing module {e.name}, restarting..")
    package.restart()

def init():
    
    from modules.util import clear, log, console, check_token, get_config, get_token, error
    import modules.util_detect_token as utd
    clear()
    if not os.path.exists("./config.json"):
        clear()
        log("Welcome to the initial setup process for the Nuked selfbot.")
        log("If you're updating, you can move your current config.json here and use that configuration.\n")
        choice = console.input("Enter '1' if you would like to log in using your Discord credentials [bold](will not work with 2FA!)[/bold]\nEnter '2' if you would like to log in using your Discord token.\nEnter '3' if you would like Nuked to automatically detect Discord accounts [bold](Experimental)[/bold].\n>")
        match choice:
            case '1':
                with open("./config.json", "w") as fp:
                    clear()
                    setup_email = console.input("Enter your [bold]Discord email[/bold]: ")
                    setup_password = console.input("Enter your [bold]Discord password[/bold]: ")
                    token = get_token(setup_email, setup_password)
                    if token != None:
                        setup_data = {
                            "Auto Update": True,
                            "Discord Token": token,
                            "Discord Password": setup_password,
                            "Discord Rich Presence": True,
                            "Default Prefix": ".",
                            "Enable Mention Logger": True,
                            "Enable Mention Blocker": False,
                            "Enable Light Mode": False,
                            "Disable Eval Command": False,
                            "Enable Slotbot Sniper": True,
                            "Enable Nitro Sniper": True,
                            "Automatically Check for Updates": True,
                            "Random Splash Color": False,
                            "Theme": "Default",
                            "Disable Cog Load Message": True,
                            "Logging": {
                                "Nitro Logger": ""
                            }
                        }
                        json.dump(setup_data, fp, indent=4)
                        log("[bold]Additional settings can be tweaked in config.json![/bold]")
                        time.sleep(2)
                        check_token(setup_data["Discord Token"])
                    else:
                        error("The username and password combination was incorrect. Restarting..")
                        os.remove("config.json")
                        time.sleep(1)
                        package.restart()
            case '2':
                with open("./config.json", "w") as fp:
                    clear()
                    setup_token = console.input("Enter your [bold]Discord token[/bold]: ")
                    setup_password = console.input(
                        "Enter your [bold]Discord password[/bold] (enter [bold]None[/bold] or press the [bold]Enter[/bold] key if you don't want to): ")
                    if setup_password == "":
                        setup_password = "None"
                    setup_data = {
                        "Discord Token": setup_token,
                        "Discord Password": setup_password,
                        "Discord Rich Presence": True,
                        "Default Prefix": ".",
                        "Enable Mention Logger": True,
                        "Enable Mention Blocker": False,
                        "Enable Light Mode": False,
                        "Disable Eval Command": False,
                        "Enable Slotbot Sniper": True,
                        "Enable Nitro Sniper": True,
                        "Automatically Check for Updates": True,
                        "Random Splash Color": False,
                        "Theme": "Default",
                        "Disable Cog Load Message": True,
                        "Logging": {
                            "Nitro Logger": ""
                        }
                    }
                    json.dump(setup_data, fp, indent=4)
                    log("[bold]Additional settings can be tweaked in config.json![/bold]")
                    time.sleep(2)
                    check_token(setup_data["Discord Token"])
            case '3':
                accounts = utd.detect_tokens()
                print(f'\nItems found: {len(accounts)}')
                print('Accounts:')
                for item in accounts:
                    print(f'{utd.get_username(item)} -- {item[:24]}..')
                num = console.input(f'\nOut of the {len(accounts)} tokens, which one would you like to log into?\n\n>')
                slice = int(num)
                if slice == 1:
                    slice = 0
                with open("./config.json", "w") as fp:
                    clear()
                    setup_data = {
                        "Discord Token": accounts[slice],
                        "Discord Password": None,
                        "Discord Rich Presence": True,
                        "Default Prefix": ".",
                        "Enable Mention Logger": True,
                        "Enable Mention Blocker": False,
                        "Enable Light Mode": False,
                        "Disable Eval Command": False,
                        "Enable Slotbot Sniper": True,
                        "Enable Nitro Sniper": True,
                        "Automatically Check for Updates": True,
                        "Random Splash Color": False,
                        "Theme": "Default",
                        "Disable Cog Load Message": True,
                        "Logging": {
                            "Nitro Logger": ""
                        }
                    }
                    json.dump(setup_data, fp, indent=4)
                    log("[bold]Additional settings can be tweaked in config.json![/bold]")
                    time.sleep(2)
                    check_token(setup_data["Discord Token"])
            case _:
                package.restart()
        # clear()
    else:
        if os.path.getsize(f"{os.getcwd()}/config.json") == 0:
            os.remove(f"{os.getcwd()}/config.json")
            package.restart()
        else:
            check_token(get_config()["Discord Token"])