from core.commands.general import help_command
from core.commands.helpemote import help_emote, handle_emote_action, emote_all_command
from core.commands.helpsettings import help_settings, set_prefix_command, mod_command, designer_command, outfit_command, welcome_command, loop_command, status_command
from core.commands.helptele import help_tele, create_command, delete_command, tele_command, summon_command, bot_command, setspawn_command
from core.commands.helptips import help_tips, tip_command, wallet_command
from core.commands.helprole import help_role, role_command, unrole_command

# Define commands as async functions that take (bot, user, message) as args.
# Or any structure you prefer.
# We will use simple mapping here.
async def handle_ping_command(bot, user, message):
    await bot.highrise.chat(f"Pong! {user.username}")

# Keys are command names WITHOUT prefix
COMMAND_HANDLERS = {
    "help": help_command,
    "emote": handle_emote_action,
    "helpemote": help_emote,
    "emoteall": emote_all_command,
    "helpsettings": help_settings,
    "prefix": set_prefix_command,
    "mod": mod_command,
    "design": designer_command,
    "outfit": outfit_command,
    "ping": handle_ping_command,
    "tele": tele_command,
    "helptele": help_tele,
    "create": create_command,
    "delete": delete_command,
    "summon": summon_command,
    "bot": bot_command,
    "setspawn": setspawn_command,
    "welcome": welcome_command,
    "loop": loop_command,
    "status": status_command,
    "helptips": help_tips,
    "tip": tip_command,
    "wallet": wallet_command,
    "helprole": help_role,
    "role": role_command,
    "unrole": unrole_command,
}
