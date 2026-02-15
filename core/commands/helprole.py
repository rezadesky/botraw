from highrise import BaseBot, User
from core.models import Role

async def help_role(bot: BaseBot, user: User, message: str):
    p = getattr(bot, 'prefix', '!')
    help_text = (
        f"👑 Role Management 👑\n"
        f"1. {p}role @user <role>\n"
        f"2. {p}unrole @user <role>\n"
        f"3. {p}role list - View assigned roles\n"
        f"\n"
        f"Available Roles:\n"
        f"👑 Host - Full Access\n"
        f"🛡 Admin - Staff (Tele, Emote, Tip @)\n"
        f"💎 VIP - Special User (Personal Tele)\n"
        f"🌍 Public - Basic (Help, Emote)"
    )
    from core.utils.chat import send_safe_chat
    await send_safe_chat(bot, help_text)

async def role_list_command(bot: BaseBot, user: User, message: str):
    roles = await Role.all()
    if not roles:
        await bot.highrise.chat("No roles assigned yet.")
        return
    
    # Sort roles for better display
    role_order = {"host": 0, "admin": 1, "vip": 2, "public": 3}
    sorted_roles = sorted(roles, key=lambda x: role_order.get(x.role_name, 99))
    
    lines = ["📋 Assigned Roles:"]
    for r in sorted_roles:
        display_name = r.username if r.username else r.user_id
        emoji = {"host": "👑", "admin": "🛡", "vip": "💎", "public": "🌍"}.get(r.role_name, "✨")
        lines.append(f"{emoji} {r.role_name.capitalize()}: @{display_name}")
    
    msg = "\n".join(lines)
    from core.utils.chat import send_safe_chat
    await send_safe_chat(bot, msg)

async def resolve_user_id(bot: BaseBot, username: str):
    username = username.replace("@", "").lower()
    
    # 1. Check Current Room
    try:
        room_users = await bot.highrise.get_room_users()
        if hasattr(room_users, 'content'):
            for u, _ in room_users.content:
                if u.username.lower() == username:
                    return u.id
    except:
        pass

    # 2. Check Bot Cache
    cached_id = getattr(bot, 'user_map', {}).get(username)
    if cached_id:
        return cached_id

    # 3. Use Web API (Like !mod)
    if hasattr(bot, 'webapi'):
        try:
            from highrise.webapi import GetPublicUserResponse
            endpoint = f"/users/{username}"
            response = await bot.webapi.send_request(endpoint, GetPublicUserResponse)
            if response and response.user:
                # Update cache while we are at it
                if hasattr(bot, 'user_map'):
                    bot.user_map[username] = response.user.user_id
                return response.user.user_id
        except:
            pass
            
    return None

async def role_command(bot: BaseBot, user: User, message: str):
    parts = message.strip().split()
    
    # Handle !role list
    if len(parts) >= 2 and parts[1].lower() == "list":
        await role_list_command(bot, user, message)
        return

    if len(parts) < 3 or not parts[1].startswith("@"):
        await bot.highrise.chat("Usage: !role @user <role> or !role list")
        return

    # Security Check
    from core.utils.permissions import get_user_role
    caller_role = await get_user_role(user.id, user.username)
    
    if caller_role != "host":
        await bot.highrise.chat("Only a Host can assign roles.")
        return

    target_username = parts[1].replace("@", "")
    new_role = parts[2].lower()
    
    if new_role not in ["host", "admin", "vip", "public"]:
        await bot.highrise.chat("Invalid role! Choose: host, admin, vip, public")
        return

    target_user_id = await resolve_user_id(bot, target_username)
    
    if not target_user_id:
        await bot.highrise.chat(f"User @{target_username} not found (even via API).")
        return

    # Update or Create
    await Role.update_or_create(
        user_id=target_user_id,
        role_name=new_role,
        defaults={'username': target_username}
    )
    
    role_emoji = {"host": "👑", "admin": "🛡", "vip": "💎", "public": "🌍"}.get(new_role, "✨")
    await bot.highrise.chat(f"{role_emoji} @{target_username} is now assigned as {new_role.capitalize()}!")

async def unrole_command(bot: BaseBot, user: User, message: str):
    parts = message.strip().split()
    if len(parts) < 3 or not parts[1].startswith("@"):
        await bot.highrise.chat("Usage: !unrole @user <role>")
        return

    from core.utils.permissions import get_user_role
    caller_role = await get_user_role(user.id, user.username)
    
    if caller_role != "host":
        await bot.highrise.chat("Only a Host can remove roles.")
        return

    target_username = parts[1].replace("@", "")
    role_to_remove = parts[2].lower()

    target_user_id = await resolve_user_id(bot, target_username)

    if not target_user_id:
         # Try removal from DB directly by username fallback
         role_obj = await Role.filter(username=target_username.lower(), role_name=role_to_remove).first()
         if role_obj:
             target_user_id = role_obj.user_id
         else:
             await bot.highrise.chat(f"User @{target_username} not found in room or database.")
             return

    deleted = await Role.filter(user_id=target_user_id, role_name=role_to_remove).delete()
    if deleted:
        await bot.highrise.chat(f"Removed {role_to_remove} role from @{target_username}.")
    else:
        await bot.highrise.chat(f"@{target_username} does not have the {role_to_remove} role.")
