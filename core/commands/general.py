from highrise import BaseBot, User

async def help_command(bot: BaseBot, user: User, message: str):
    """
    Displays the help menu with sub-categories.
    Usage: !help [category]
    Categories: emote, tele, settings, tips
    """
    parts = message.strip().split()
    # parts[0] is "!help", parts[1] is the category if present
    
    p = getattr(bot, 'prefix', '!')
    
    if len(parts) == 1:
        # Main Help Menu
        help_text = (
            f"🤖 Bot Help Menu 🤖\n"
            f"Usage: {p}help <category>\n"
            f"Categories:\n"
            f"1. {p}help emote - Emote commands\n"
            f"2. {p}help tele - Teleport commands\n"
            f"3. {p}help settings - Bot settings\n"
            f"4. {p}help tips - Tipping commands\n"
            f"5. {p}help role - Role management\n"
            "\n"
            "General:\n"
            f"{p}ping - Check bot latency"
        )
        from core.utils.chat import send_safe_chat
        await send_safe_chat(bot, help_text)
        return

    category = parts[1].lower()

    if category == "emote":
        # Import dynamically or at top (dynamic to avoid circular if helpemote imports general)
        from core.commands.helpemote import help_emote as show_emote_help
        await show_emote_help(bot, user, message)

    elif category == "tele":
        from core.commands.helptele import help_tele as show_tele_help
        await show_tele_help(bot, user, message)

    elif category == "settings":
        from core.commands.helpsettings import help_settings as show_settings_help
        await show_settings_help(bot, user, message)

    elif category == "tips":
        from core.commands.helptips import help_tips as show_tips_help
        await show_tips_help(bot, user, message)

    elif category == "role":
        from core.commands.helprole import help_role as show_role_help
        await show_role_help(bot, user, message)

    else:
        await bot.highrise.chat(f"Unknown category: {category}. Try !help")

