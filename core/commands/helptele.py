from highrise import BaseBot, User, Position
from core.models import Teleport

async def help_tele(bot: BaseBot, user: User, message: str):
    p = getattr(bot, 'prefix', '!')
    help_text = (
        f"🌌 Teleport Help 🌌\n"
        f"1. {p}tele list\n"
        f"2. {p}create tele <name>\n"
        f"3. {p}delete tele <name>\n"
        f"4. {p}tele <name> <role> - Set required role\n"
        f"5. {p}tele @user <x|name>\n"
        f"6. {p}summon <@user|all>\n"
        f"7. {p}bot - Bot follows & sets spawn\n"
        f"8. {p}setspawn - Set user spawn point\n"
        f"Tip: {p}tele name public - Back to public"
    )
    from core.utils.chat import send_safe_chat
    await send_safe_chat(bot, help_text)

async def bot_command(bot: BaseBot, user: User, message: str):
    # Get user position
    room_users = await bot.highrise.get_room_users()
    user_pos = None
    if hasattr(room_users, 'content'):
        for u, pos in room_users.content:
            if u.id == user.id:
                if isinstance(pos, Position):
                    user_pos = pos
                break
    
    if not user_pos:
        await bot.highrise.chat("Could not determine your position.")
        return

    # Teleport bot to user (use cached ID)
    bot_id = getattr(bot, 'my_id', None)
    if bot_id:
        await bot.queue_physical("teleport", bot_id, user_pos)
    
    # Save as bot_spawn
    from core.models import Teleport
    await Teleport.update_or_create(
        command="bot_spawn",
        defaults={
            'x': user_pos.x, 
            'y': user_pos.y, 
            'z': user_pos.z, 
            'facing': user_pos.facing
        }
    )
    await bot.highrise.chat("Bot spawn point set to current location.")

async def setspawn_command(bot: BaseBot, user: User, message: str):
    # Get user position
    room_users = await bot.highrise.get_room_users()
    user_pos = None
    if hasattr(room_users, 'content'):
        for u, pos in room_users.content:
            if u.id == user.id:
                if isinstance(pos, Position):
                    user_pos = pos
                break
    
    if not user_pos:
        await bot.highrise.chat("Could not determine your position.")
        return

    # Save as user_spawn
    from core.models import Teleport
    await Teleport.update_or_create(
        command="user_spawn",
        defaults={
            'x': user_pos.x, 
            'y': user_pos.y, 
            'z': user_pos.z, 
            'facing': user_pos.facing
        }
    )
    await bot.highrise.chat("User spawn point set to current location.")

async def create_command(bot: BaseBot, user: User, message: str):
    parts = message.strip().split()
    # Expect: !create tele <name>
    if len(parts) < 3 or parts[1].lower() != "tele":
        await bot.highrise.chat("Usage: !create tele <name>")
        return

    name = parts[2].lower()
    
    # Get user position
    room_users = await bot.highrise.get_room_users()
    user_pos = None
    if hasattr(room_users, 'content'):
        for u, pos in room_users.content:
            if u.id == user.id:
                if isinstance(pos, Position):
                    user_pos = pos
                break
    
    if not user_pos:
        await bot.highrise.chat("Could not determine your position.")
        return

    # Save to DB (update if exists)
    # Default role is public
    await Teleport.update_or_create(
        command=name,
        defaults={
            'x': user_pos.x, 
            'y': user_pos.y, 
            'z': user_pos.z, 
            'facing': user_pos.facing,
            'role': 'public'
        }
    )
    await bot.highrise.chat(f"Teleport '{name}' created for Public.")

async def delete_command(bot: BaseBot, user: User, message: str):
    parts = message.strip().split()
    # Expect: !delete tele <name>
    if len(parts) < 3 or parts[1].lower() != "tele":
        await bot.highrise.chat("Usage: !delete tele <name>")
        return

    name = parts[2].lower()
    deleted_count = await Teleport.filter(command=name).delete()
    
    if deleted_count:
        await bot.highrise.chat(f"Teleport '{name}' deleted.")
    else:
        await bot.highrise.chat(f"Teleport '{name}' not found.")

async def tele_command(bot: BaseBot, user: User, message: str):
    parts = message.strip().split()
    if len(parts) < 2:
        await bot.highrise.chat("Usage: !tele <args>")
        return

    arg1 = parts[1].lower()

    # 1. Handle !tele list
    if arg1 == "list":
        # Sort and filter manually to avoid ORM filter errors
        all_t = await Teleport.all()
        teleports = [t for t in all_t if t.command not in ["user_spawn", "bot_spawn"]]
        
        if not teleports:
            await bot.highrise.chat("No saved teleports.")
        else:
            lines = [f"- {t.command} ({t.role})" for t in teleports]
            msg = f"🌌 Saved Teleports 🌌\n" + "\n".join(lines)
            from core.utils.chat import send_safe_chat
            await send_safe_chat(bot, msg)
        return

    # 2. Handle !tele <name> <role> (Change Role)
    # Only if len(parts) == 3 and parts[2] is a role keyword
    role_keywords = ["host", "admin", "vip", "public"]
    if len(parts) == 3 and parts[1].lower() in [t.command for t in await Teleport.all()] and parts[2].lower() in role_keywords:
        target_tele_name = parts[1].lower()
        new_role = parts[2].lower()
        
        # Permission check: Only Host/Admin can change teleport roles
        from core.utils.permissions import get_user_role
        u_role = await get_user_role(user.id, user.username)
        if u_role not in ["host", "admin"]:
            await bot.highrise.chat("You don't have permission to change teleport roles.")
            return

        updated = await Teleport.filter(command=target_tele_name).update(role=new_role)
        if updated:
            await bot.highrise.chat(f"Teleport '{target_tele_name}' is now restricted to {new_role.capitalize()}.")
        return

    # 3. Handle Teleportation Logic
    target_user_id = None
    target_username = None
    start_idx = 1
    
    if arg1.startswith("@"):
        target_username = arg1.replace("@", "")
        # Resolve ID from room
        room_users = await bot.highrise.get_room_users()
        if hasattr(room_users, 'content'):
            for u, _ in room_users.content:
                if u.username.lower() == target_username.lower():
                    target_user_id = u.id
                    break
        if not target_user_id:
             await bot.highrise.chat(f"User {target_username} not found in room.")
             return
        start_idx = 2 

    tele_target_id = target_user_id if target_user_id else user.id

    if len(parts) <= start_idx:
        await bot.highrise.chat("Missing coordinates or teleport name.")
        return

    # Try Coordinates
    try:
        if len(parts) >= start_idx + 3:
            x = float(parts[start_idx])
            y = float(parts[start_idx+1])
            z = float(parts[start_idx+2])
            pos = Position(x, y, z, "FrontRight")
            await bot.queue_physical("teleport", tele_target_id, pos)
            return
    except ValueError:
        pass

    # Try Named Teleport
    tele_name = parts[start_idx].lower()
    tele_obj = await Teleport.get_or_none(command=tele_name)
    
    if tele_obj:
        # Check Permissions
        from core.utils.permissions import get_user_role, has_permission
        caller_role = await get_user_role(user.id, user.username)
        
        if not has_permission(caller_role, tele_obj.role):
            await bot.highrise.chat(f"Sorry @{user.username}, teleport '{tele_name}' requires {tele_obj.role.capitalize()} role.")
            return

        pos = Position(tele_obj.x, tele_obj.y, tele_obj.z, tele_obj.facing)
        await bot.queue_physical("teleport", tele_target_id, pos)
    else:
        await bot.highrise.chat(f"Invalid coord or teleport '{tele_name}' not found.")

async def summon_command(bot: BaseBot, user: User, message: str):
    parts = message.strip().split()
    if len(parts) < 2:
        await bot.highrise.chat("Usage: !summon <@user|all>")
        return

    arg = parts[1].lower()
    room_users = await bot.highrise.get_room_users()
    caller_pos = None
    users_list = []
    
    if hasattr(room_users, 'content'):
        users_list = room_users.content
        for u, pos in users_list:
            if u.id == user.id:
                if isinstance(pos, Position):
                    caller_pos = pos
                break
    
    if not caller_pos:
        await bot.highrise.chat("Could not determine your position.")
        return

    bot_id = getattr(bot, 'my_id', None)

    if arg == "all":
        count = 0
        for u, _ in users_list:
            if u.id != user.id and u.id != bot_id:
                await bot.queue_physical("teleport", u.id, caller_pos)
                count += 1
        await bot.highrise.chat(f"Summoned {count} users.")
    elif arg.startswith("@"):
        target_name = arg.replace("@", "")
        target_id = None
        for u, _ in users_list:
            if u.username.lower() == target_name.lower():
                target_id = u.id
                break
        if target_id:
            await bot.queue_physical("teleport", target_id, caller_pos)
            await bot.highrise.chat(f"Summoned @{target_name}.")
        else:
            await bot.highrise.chat(f"User @{target_name} not found.")

async def check_teleport_trigger(bot: BaseBot, user: User, message: str):
    msg = message.strip().lower()
    tele_obj = await Teleport.get_or_none(command=msg)
    
    if tele_obj:
        # Check Permissions
        from core.utils.permissions import get_user_role, has_permission
        caller_role = await get_user_role(user.id, user.username)
        
        if not has_permission(caller_role, tele_obj.role):
            # Maybe don't spam chat for triggers, or just let it fail silently? 
            # User might type the word by accident. 
            # But let's warn so they know why it didn't work.
            await bot.highrise.chat(f"@{user.username}, '{msg}' is a {tele_obj.role.capitalize()} teleport.")
            return

        pos = Position(tele_obj.x, tele_obj.y, tele_obj.z, tele_obj.facing)
        try:
            await bot.queue_physical("teleport", user.id, pos)
        except Exception as e:
            print(f"Teleport trigger failed: {e}")
