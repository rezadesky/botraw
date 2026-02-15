from highrise import BaseBot, User
from core.models import Setting, Teleport

async def help_settings(bot: BaseBot, user: User, message: str):
    """
    Displays the settings help menu.
    """
    p = getattr(bot, 'prefix', '!')
    help_text = (
        f"⚙️ Settings Help Menu ⚙️\n"
        f"1. {p}prefix - Change bot command prefix\n"
        f"2. {p}welcome - Set and toggle join message\n"
        f"3. {p}loop - Set and toggle timed messages\n"
        f"4. {p}status - View all current bot status\n"
        f"5. {p}mod @user / {p}design @user - Set roles\n"
        f"6. {p}outfit - Change bot appearance (1-10)"
    )
    from core.utils.chat import send_safe_chat
    await send_safe_chat(bot, help_text)

async def welcome_command(bot: BaseBot, user: User, message: str):
    parts = message.strip().split()
    if len(parts) < 2:
        await bot.highrise.chat("Usage: !welcome <message|on|off>")
        return
    
    arg = parts[1].lower()
    if arg == "on":
        await Setting.update_or_create(key="welcome_on", defaults={"value": "true"})
        await bot.highrise.chat("Welcome message enabled.")
    elif arg == "off":
        await Setting.update_or_create(key="welcome_on", defaults={"value": "false"})
        await bot.highrise.chat("Welcome message disabled.")
    else:
        # It's a message
        msg_text = " ".join(parts[1:])
        await Setting.update_or_create(key="welcome_msg", defaults={"value": msg_text})
        await bot.highrise.chat(f"Welcome message set to: {msg_text}")

async def loop_command(bot: BaseBot, user: User, message: str):
    parts = message.strip().split()
    if len(parts) < 2:
        await bot.highrise.chat("Usage: !loop <message|seconds|on|off>")
        return
    
    arg = parts[1].lower()
    if arg == "on":
        await Setting.update_or_create(key="loop_on", defaults={"value": "true"})
        await bot.highrise.chat("Loop message enabled.")
        # Trigger bot to re-check and start loop
        if hasattr(bot, 'update_loop_task'):
            await bot.update_loop_task()
    elif arg == "off":
        await Setting.update_or_create(key="loop_on", defaults={"value": "false"})
        await bot.highrise.chat("Loop message disabled.")
        if hasattr(bot, 'update_loop_task'):
            await bot.update_loop_task()
    elif arg.isdigit():
        interval = int(arg)
        if interval < 5:
             await bot.highrise.chat("Interval too short. Min 5s.")
             return
        await Setting.update_or_create(key="loop_interval", defaults={"value": str(interval)})
        await bot.highrise.chat(f"Loop interval set to {interval} seconds.")
        if hasattr(bot, 'update_loop_task'):
            await bot.update_loop_task()
    else:
        msg_text = " ".join(parts[1:])
        await Setting.update_or_create(key="loop_msg", defaults={"value": msg_text})
        await bot.highrise.chat(f"Loop message set to: {msg_text}")
        if hasattr(bot, 'update_loop_task'):
            await bot.update_loop_task()

async def status_command(bot: BaseBot, user: User, message: str):
    # Prefix
    prefix = getattr(bot, 'prefix', '!')

    # Welcome
    w_on = await Setting.get_or_none(key="welcome_on")
    w_msg = await Setting.get_or_none(key="welcome_msg")
    w_status = "ON" if w_on and w_on.value == "true" else "OFF"
    w_txt = w_msg.value if w_msg else "None"

    # Loop
    l_on = await Setting.get_or_none(key="loop_on")
    l_msg = await Setting.get_or_none(key="loop_msg")
    l_int = await Setting.get_or_none(key="loop_interval")
    l_status = "ON" if l_on and l_on.value == "true" else "OFF"
    l_txt = l_msg.value if l_msg else "None"
    l_sec = l_int.value if l_int else "60"

    # Spawns
    bot_spawn = await Teleport.get_or_none(command="bot_spawn")
    user_spawn = await Teleport.get_or_none(command="user_spawn")
    
    b_pos = f"{bot_spawn.x:.1f}, {bot_spawn.y:.1f}, {bot_spawn.z:.1f}" if bot_spawn else "Not set"
    u_pos = f"{user_spawn.x:.1f}, {user_spawn.y:.1f}, {user_spawn.z:.1f}" if user_spawn else "Not set"

    status_msg = (
        f"📊 Bot Status 📊\n"
        f"Prefix: {prefix}\n"
        f"Welcome: [{w_status}] {w_txt}\n"
        f"Loop: [{l_status}] ({l_sec}s) {l_txt}\n"
        f"Bot Spawn: {b_pos}\n"
        f"User Spawn: {u_pos}"
    )
    from core.utils.chat import send_safe_chat
    await send_safe_chat(bot, status_msg)

async def set_prefix_command(bot: BaseBot, user: User, message: str):
    # ... rest of file (set_prefix, mod, designer, outfit) ...
    """
    Changes the bot's command prefix.
    """
    parts = message.strip().split()
    if len(parts) < 2:
        p = getattr(bot, 'prefix', '!')
        await bot.highrise.chat(f"Usage: {p}prefix <new_prefix>")
        return
    
    new_prefix = parts[1]
    if len(new_prefix) > 3:
        await bot.highrise.chat("Prefix too long. Max 3 characters.")
        return
        
    bot.prefix = new_prefix
    await Setting.update_or_create(key="prefix", defaults={"value": new_prefix})
    await bot.highrise.chat(f"Prefix changed to: {new_prefix}")

async def mod_command(bot: BaseBot, user: User, message: str):
    """
    Promotes a user to Moderator.
    Usage: !mod @user
    """
    parts = message.strip().split()
    if len(parts) < 2:
        await bot.highrise.chat("Usage: !mod @user")
        return
    
    target_username = parts[1].replace("@", "")
    target_user_id = None
    
    # 1. Resolve user ID from Room (Standard, reliable)
    try:
        room_users = await bot.highrise.get_room_users()
        if hasattr(room_users, 'content'):
            for r_user, _ in room_users.content:
                if r_user.username.lower() == target_username.lower():
                    target_user_id = r_user.id
                    break
    except Exception:
        pass
            
    # 2. Resolve user ID from Web API if not in room
    if not target_user_id:
        if not hasattr(bot, 'webapi'):
             await bot.highrise.chat("Error: Web API is not active.")
        else:
            try:
                from highrise.webapi import GetPublicUserResponse
                endpoint = f"/users/{target_username}"
                response = await bot.webapi.send_request(endpoint, GetPublicUserResponse)
                
                if response and response.user:
                    target_user_id = response.user.user_id
                else:
                     await bot.highrise.chat(f"User {target_username} not found via API.")
            except Exception as e:
                # Handle 404 or other errors
                if "404" in str(e):
                    await bot.highrise.chat(f"User {target_username} not found (API 404).")
                else:
                    await bot.highrise.chat(f"API Error: {e}")
            
    if target_user_id:
        try:
             from highrise.models import RoomPermissions
             
             # Check current privileges to toggle
             priv_response = await bot.highrise.get_room_privilege(target_user_id)
             
             # Handle response unwrapping if needed
             if hasattr(priv_response, 'content'):
                 current_permissions = priv_response.content
             else:
                 current_permissions = priv_response
             
             if current_permissions.moderator:
                 # Remove moderator
                 new_permissions = RoomPermissions(moderator=False)
                 await bot.highrise.change_room_privilege(target_user_id, new_permissions)
                 await bot.highrise.chat(f"@{target_username} is no longer a Moderator.")
             else:
                 # Add moderator
                 new_permissions = RoomPermissions(moderator=True)
                 await bot.highrise.change_room_privilege(target_user_id, new_permissions)
                 await bot.highrise.chat(f"@{target_username} is now a Moderator!")
                 
        except Exception as e:
             await bot.highrise.chat(f"Failed to change privilege: {e}")
    else:
        # Pass silently here since API block handles feedback if it ran
        pass

async def designer_command(bot: BaseBot, user: User, message: str):
    """
    Promotes or demotes a user to/from Designer (Toggle).
    Usage: !design @user
    """
    parts = message.strip().split()
    if len(parts) < 2:
        await bot.highrise.chat("Usage: !design @user")
        return
    
    target_username = parts[1].replace("@", "")
    target_user_id = None
    
    # 1. Resolve user ID from Room
    try:
        room_users = await bot.highrise.get_room_users()
        if hasattr(room_users, 'content'):
            for r_user, _ in room_users.content:
                if r_user.username.lower() == target_username.lower():
                    target_user_id = r_user.id
                    break
    except Exception:
        pass

    # 2. Resolve user ID from Web API if not in room
    if not target_user_id:
        if not hasattr(bot, 'webapi'):
             await bot.highrise.chat("Error: Web API is not active.")
        else:
            try:
                from highrise.webapi import GetPublicUserResponse
                endpoint = f"/users/{target_username}"
                response = await bot.webapi.send_request(endpoint, GetPublicUserResponse)
                
                if response and response.user:
                    target_user_id = response.user.user_id
                else:
                     await bot.highrise.chat(f"User {target_username} not found via API.")
            except Exception as e:
                if "404" in str(e):
                    await bot.highrise.chat(f"User {target_username} not found (API 404).")
                else:
                    await bot.highrise.chat(f"API Error: {e}")
            
    if target_user_id:
        try:
             from highrise.models import RoomPermissions
             
             # Check current privileges to toggle
             priv_response = await bot.highrise.get_room_privilege(target_user_id)
             
             # Handle response unwrapping if needed
             if hasattr(priv_response, 'content'):
                 current_permissions = priv_response.content
             else:
                 current_permissions = priv_response
             
             if current_permissions.designer:
                 # Remove designer
                 new_permissions = RoomPermissions(designer=False)
                 await bot.highrise.change_room_privilege(target_user_id, new_permissions)
                 await bot.highrise.chat(f"@{target_username} is no longer a Designer.")
             else:
                 # Add designer
                 new_permissions = RoomPermissions(designer=True)
                 await bot.highrise.change_room_privilege(target_user_id, new_permissions)
                 await bot.highrise.chat(f"@{target_username} is now a Designer!")

        except Exception as e:
             await bot.highrise.chat(f"Failed to change privilege: {e}")
    else:
        pass

async def outfit_command(bot: BaseBot, user: User, message: str):
    """
    Changes the bot's outfit based on index (1-10).
    Usage: !outfit <index>
    """
    parts = message.strip().split()
    if len(parts) < 2:
        await bot.highrise.chat("Usage: !outfit <1-10>")
        return

    index = parts[1]
    
    try:
        from core.data.outfits import get_outfit
        from highrise.models import Item
        
        outfit_data = get_outfit(index)
        if not outfit_data:
            await bot.highrise.chat(f"Outfit {index} not found. Available: 1-10")
            return
            
        # Convert dict items to Item objects
        new_outfit = []
        for item_dict in outfit_data['outfit']:
            new_outfit.append(Item(
                id=item_dict['id'],
                type=item_dict['type'],
                amount=item_dict['amount'],
                active_palette=item_dict.get('active_palette')
            ))
            
        await bot.highrise.set_outfit(new_outfit)
        await bot.highrise.chat(f"Changed outfit to: {outfit_data['name']}")
        
    except Exception as e:
        await bot.highrise.chat(f"Failed to set outfit: {e}")
