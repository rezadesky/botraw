from core.models import Role

async def get_user_role(user_id: str, username: str = ""):
    # Hardcoded bypass for owner
    if username.lower() == "rawrage":
        return "host"

    # Get highest role from DB
    roles = await Role.filter(user_id=user_id).values_list("role_name", flat=True)
    if not roles:
        return "public"
    
    # Priority: host > admin > vip > public
    if "host" in roles: return "host"
    if "admin" in roles: return "admin"
    if "vip" in roles: return "vip"
    return "public"

async def can_run_command(user_id: str, command: str, message: str = "", username: str = "") -> bool:
    role = await get_user_role(user_id, username)
    
    if role == "host":
        return True
    
    # Parts for argument-based checks
    parts = message.strip().split()
    cmd = parts[0].lower().replace("!", "") # assuming ! prefix but generic
    args = parts[1:] if len(parts) > 1 else []

    if role == "admin":
        # Admin can't do these:
        forbidden = ["prefix", "loop", "setspawn", "bot", "mod", "design", "outfit", "role", "unrole"]
        if cmd in forbidden:
            return False
        
        # Tip checks
        if cmd == "tip":
            if len(args) > 0:
                target = args[0].lower()
                if target == "all" or target.isdigit():
                    return False
        
        # Summon checks
        if cmd == "summon":
            if len(args) > 0 and args[0].lower() == "all":
                return False
                
        # Tele checks
        if cmd == "tele":
             # Only tele @user <name> is allowed for admin? 
             # User said: tele @user <name> (staff)
             # User said: tele @user <coords> (host only)
             if len(args) >= 2 and args[0].startswith("@"):
                 # Check if the rest is coords (3 floats)
                 try:
                     float(args[1]); float(args[2]); float(args[3])
                     return False # Coords is Host only
                 except:
                     pass # Not coords, name is ok
        
        return True

    if role == "vip":
        # VIP allowed: help, ping, emote, tele list, tele <name>, summon @user
        allowed = ["help", "ping", "helpemote", "helptele", "helptips", "helprole"]
        if cmd in allowed: return True
        
        if cmd == "emote": 
            return True # Can use !emote (targeting handled in command)
            
        if cmd == "summon":
            # Can summon @user but not 'all'
            if len(args) > 0 and args[0].startswith("@") and args[0].lower() != "@all":
                return True
            return False
        
        if cmd == "tele":
            if len(args) > 0:
                arg1 = args[0].lower()
                if arg1 == "list": return True
                # If it's a name (not coords, not @user)
                if not arg1.startswith("@") and len(args) == 1:
                    return True
        
        return False

    if role == "public":
        # Public allowed: help, ping, emote (basic)
        allowed = ["help", "ping", "helpemote", "helptele", "helptips", "helprole"]
        if cmd in allowed: return True
        if cmd == "emote":
            # Basic emote: only !emote <name> for self? 
            # If they provide @user, we might want to block it in the command or here.
            # For now, let's just allow the command and maybe restrict targeting in helpemote.py if needed.
            return True
        return False

    return False

def has_permission(user_role: str, required_role: str) -> bool:
    role_order = {"host": 0, "admin": 1, "vip": 2, "public": 3}
    user_val = role_order.get(user_role.lower(), 3)
    req_val = role_order.get(required_role.lower(), 3)
    return user_val <= req_val
