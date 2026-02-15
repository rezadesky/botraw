from highrise import BaseBot, User, Position
from typing import Literal
import random

async def help_tips(bot: BaseBot, user: User, message: str):
    p = getattr(bot, 'prefix', '!')
    help_text = (
        f"💰 Tip Help Menu 💰\n"
        f"1. {p}tip all <amount> - Tip everyone\n"
        f"2. {p}tip @user <amount> - Tip a person\n"
        f"3. {p}tip <num> <amount> - Tip random users\n"
        f"4. {p}wallet - Check bot balance\n"
        "Amounts: 1, 5, 10, 50, 100, 500, 1k, 5k, 10k"
    )
    from core.utils.chat import send_safe_chat
    await send_safe_chat(bot, help_text)

def get_tip_literal(amount: str):
    mapping = {
        "1": "gold_bar_1",
        "5": "gold_bar_5",
        "10": "gold_bar_10",
        "50": "gold_bar_50",
        "100": "gold_bar_100",
        "500": "gold_bar_500",
        "1000": "gold_bar_1k",
        "1k": "gold_bar_1k",
        "5000": "gold_bar_5000",
        "5k": "gold_bar_5000",
        "10000": "gold_bar_10k",
        "10k": "gold_bar_10k"
    }
    return mapping.get(str(amount).lower())

async def get_bot_gold(bot: BaseBot):
    try:
        balance = await bot.highrise.get_wallet()
        if hasattr(balance, 'content'):
            for item in balance.content:
                if item.type == 'gold':
                    return item.amount
    except Exception:
        pass
    return 0

async def wallet_command(bot: BaseBot, user: User, message: str):
    gold = await get_bot_gold(bot)
    await bot.highrise.chat(f"👛 Bot Wallet: {gold} Gold")

async def tip_command(bot: BaseBot, user: User, message: str):
    parts = message.strip().split()
    if len(parts) < 3:
        await bot.highrise.chat("Usage: !tip <@user|all|num> <amount>")
        return

    target = parts[1].lower()
    amount_str = parts[2].lower()
    tip_bar = get_tip_literal(amount_str)

    if not tip_bar:
        await bot.highrise.chat("Invalid amount! Use: 1, 5, 10, 50, 100, 500, 1k, 5k, 10k.")
        return

    room_users = await bot.highrise.get_room_users()
    users_list = []
    if hasattr(room_users, 'content'):
        users_list = room_users.content

    if target == "all":
        candidates = [u for u, _ in users_list if u.id != bot.my_id]
        if not candidates:
            await bot.highrise.chat("No users in room.")
            return

        for u in candidates:
            res = await bot.highrise.tip_user(u.id, tip_bar)
            if res == "success":
                await bot.highrise.chat(f"Tipped @{u.username} {amount_str} Gold! 💰")
            elif res == "insufficient_funds":
                gold = await get_bot_gold(bot)
                await bot.highrise.chat(f"Insufficent Gold! Current balance: {gold} Gold.")
                break # Stop if out of money
            else:
                await bot.highrise.chat(f"Error tipping @{u.username}: {res}")

    elif target.startswith("@"):
        username = target.replace("@", "")
        target_id = None
        for u, _ in users_list:
            if u.username.lower() == username:
                target_id = u.id
                break
        
        if target_id:
            res = await bot.highrise.tip_user(target_id, tip_bar)
            if res == "success":
                await bot.highrise.chat(f"Tipped @{username} {amount_str} Gold! 💰")
            elif res == "insufficient_funds":
                gold = await get_bot_gold(bot)
                await bot.highrise.chat(f"Insufficent Gold! Current balance: {gold} Gold.")
            else:
                await bot.highrise.chat(f"Error: {res}")
        else:
            await bot.highrise.chat(f"User {target} not found.")

    elif target.isdigit():
        num_targets = int(target)
        candidates = [u for u, _ in users_list if u.id != bot.my_id]
        if not candidates:
            await bot.highrise.chat("No users in room.")
            return
            
        random_targets = random.sample(candidates, min(num_targets, len(candidates)))
        for u in random_targets:
            res = await bot.highrise.tip_user(u.id, tip_bar)
            if res == "success":
                await bot.highrise.chat(f"Tipped @{u.username} {amount_str} Gold! 💰")
            elif res == "insufficient_funds":
                gold = await get_bot_gold(bot)
                await bot.highrise.chat(f"Insufficent Gold! Current balance: {gold} Gold.")
                break
            else:
                await bot.highrise.chat(f"Error: {res}")
