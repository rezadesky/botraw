from highrise import BaseBot, User

# Complete list of emotes: (Name, ID)
ALL_EMOTES = [
    ("Rest", "sit-idle-cute"),
    ("Zombie", "idle_zombie"),
    ("Relaxed", "idle_layingdown2"),
    ("Attentive", "idle_layingdown"),
    ("Sleepy", "idle-sleep"),
    ("PoutyFace", "idle-sad"),
    ("Posh", "idle-posh"),
    ("Sleepy", "idle-loop-tired"),
    ("TapLoop", "idle-loop-tapdance"),
    ("Sit", "idle-loop-sitfloor"),
    ("Shy", "idle-loop-shy"),
    ("Bummed", "idle-loop-sad"),
    ("Chillin", "idle-loop-happy"),
    ("Annoyed", "idle-loop-annoyed"),
    ("Aerobics", "idle-loop-aerobics"),
    ("Ponder", "idle-lookup"),
    ("HeroPose", "idle-hero"),
    ("Relaxing", "idle-floorsleeping2"),
    ("CozyNap", "idle-floorsleeping"),
    ("Enthused", "idle-enthusiastic"),
    ("BoogieSwing", "idle-dance-swinging"),
    ("FeelTheBeat", "idle-dance-headbobbing"),
    ("Irritated", "idle-angry"),
    ("Yes", "emote-yes"),
    ("IBelieveICanFly", "emote-wings"),
    ("TheWave", "emote-wave"),
    ("Tired", "emote-tired"),
    ("Think", "emote-think"),
    ("Theatrical", "emote-theatrical"),
    ("TapDance", "emote-tapdance"),
    ("SuperRun", "emote-superrun"),
    ("SuperPunch", "emote-superpunch"),
    ("SumoFight", "emote-sumo"),
    ("ThumbSuck", "emote-suckthumb"),
    ("SplitsDrop", "emote-splitsdrop"),
    ("SnowballFight", "emote-snowball"),
    ("SnowAngel", "emote-snowangel"),
    ("Shy", "emote-shy"),
    ("SecretHandshake", "emote-secrethandshake"),
    ("Sad", "emote-sad"),
    ("RopePull", "emote-ropepull"),
    ("Roll", "emote-roll"),
    ("ROFL", "emote-rofl"),
    ("Robot", "emote-robot"),
    ("Rainbow", "emote-rainbow"),
    ("Proposing", "emote-proposing"),
    ("Peekaboo", "emote-peekaboo"),
    ("Peace", "emote-peace"),
    ("Panic", "emote-panic"),
    ("No", "emote-no"),
    ("NinjaRun", "emote-ninjarun"),
    ("NightFever", "emote-nightfever"),
    ("MonsterFail", "emote-monster_fail"),
    ("Model", "emote-model"),
    ("FlirtyWave", "emote-lust"),
    ("LevelUp", "emote-levelup"),
    ("Amused", "emote-laughing2"),
    ("Laugh", "emote-laughing"),
    ("Kiss", "emote-kiss"),
    ("SuperKick", "emote-kicking"),
    ("Jump", "emote-jumpb"),
    ("JudoChop", "emote-judochop"),
    ("ImaginaryJetpack", "emote-jetpack"),
    ("HugYourself", "emote-hugyourself"),
    ("Sweating", "emote-hot"),
    ("HeroEntrance", "emote-hero"),
    ("Hello", "emote-hello"),
    ("Headball", "emote-headball"),
    ("HarlemShake", "emote-harlemshake"),
    ("Happy", "emote-happy"),
    ("Handstand", "emote-handstand"),
    ("GreedyEmote", "emote-greedy"),
    ("Graceful", "emote-graceful"),
    ("Moonwalk", "emote-gordonshuffle"),
    ("GhostFloat", "emote-ghost-idle"),
    ("GangnamStyle", "emote-gangnam"),
    ("Frolic", "emote-frollicking"),
    ("Faint", "emote-fainting"),
    ("Clumsy", "emote-fail2"),
    ("Fall", "emote-fail1"),
    ("FacePalm", "emote-exasperatedb"),
    ("Exasperated", "emote-exasperated"),
    ("ElbowBump", "emote-elbowbump"),
    ("Disco", "emote-disco"),
    ("BlastOff", "emote-disappear"),
    ("FaintDrop", "emote-deathdrop"),
    ("Collapse", "emote-death2"),
    ("Revival", "emote-death"),
    ("Dab", "emote-dab"),
    ("Curtsy", "emote-curtsy"),
    ("Confusion", "emote-confused"),
    ("Cold", "emote-cold"),
    ("Charging", "emote-charging"),
    ("BunnyHop", "emote-bunnyhop"),
    ("Bow", "emote-bow"),
    ("Boo", "emote-boo"),
    ("HomeRun", "emote-baseball"),
    ("FallingApart", "emote-apart"),
    ("ThumbsUp", "emoji-thumbsup"),
    ("Point", "emoji-there"),
    ("Sneeze", "emoji-sneeze"),
    ("Smirk", "emoji-smirking"),
    ("Sick", "emoji-sick"),
    ("Gasp", "emoji-scared"),
    ("Punch", "emoji-punch"),
    ("Pray", "emoji-pray"),
    ("Stinky", "emoji-poop"),
    ("Naughty", "emoji-naughty"),
    ("MindBlown", "emoji-mind-blown"),
    ("Lying", "emoji-lying"),
    ("Levitate", "emoji-halo"),
    ("FireballLunge", "emoji-hadoken"),
    ("GiveUp", "emoji-give-up"),
    ("TummyAche", "emoji-gagging"),
    ("Flex", "emoji-flex"),
    ("Stunned", "emoji-dizzy"),
    ("CursingEmote", "emoji-cursing"),
    ("Sob", "emoji-crying"),
    ("Clap", "emoji-clapping"),
    ("RaiseTheRoof", "emoji-celebrate"),
    ("Arrogance", "emoji-arrogance"),
    ("Angry", "emoji-angry"),
    ("VogueHands", "dance-voguehands"),
    ("SavageDance", "dance-tiktok8"),
    ("DontStartNow", "dance-tiktok2"),
    ("YogaFlow", "dance-spiritual"),
    ("Smoothwalk", "dance-smoothwalk"),
    ("RingonIt", "dance-singleladies"),
    ("LetsGoShopping", "dance-shoppingcart"),
    ("RussianDance", "dance-russian"),
    ("Robotic", "dance-robotic"),
    ("PennysDance", "dance-pennywise"),
    ("OrangeJuiceDance", "dance-orangejustice"),
    ("RockOut", "dance-metal"),
    ("Karate", "dance-martial-artist"),
    ("Macarena", "dance-macarena"),
    ("HandsintheAir", "dance-handsup"),
    ("Floss", "dance-floss"),
    ("DuckWalk", "dance-duckwalk"),
    ("Breakdance", "dance-breakdance"),
    ("KPopDance", "dance-blackpink"),
    ("PushUps", "dance-aerobics"),
    ("Hyped", "emote-hyped"),
    ("Jinglebell", "dance-jinglebell"),
    ("Nervous", "idle-nervous"),
    ("Toilet", "idle-toilet"),
    ("Attention", "emote-attention"),
    ("Astronaut", "emote-astronaut"),
    ("DanceZombie", "dance-zombie"),
    ("Ghost", "emoji-ghost"),
    ("HeartEyes", "emote-hearteyes"),
    ("Swordfight", "emote-swordfight"),
    ("TimeJump", "emote-timejump"),
    ("Snake", "emote-snake"),
    ("HeartFingers", "emote-heartfingers"),
    ("HeartShape", "emote-heartshape"),
    ("Hug", "emote-hug"),
    ("Laugh", "emote-lagughing"),
    ("Eyeroll", "emoji-eyeroll"),
    ("Embarrassed", "emote-embarrassed"),
    ("Float", "emote-float"),
    ("Telekinesis", "emote-telekinesis"),
    ("Sexydance", "dance-sexy"),
    ("Puppet", "emote-puppet"),
    ("Fighteridle", "idle-fighter"),
    ("Penguindance", "dance-pinguin"),
    ("Creepypuppet", "dance-creepypuppet"),
    ("Sleigh", "emote-sleigh"),
    ("Maniac", "emote-maniac"),
    ("EnergyBall", "emote-energyball"),
    ("Singing", "idle_singing"),
    ("Frog", "emote-frog"),
    ("Superpose", "emote-superpose"),
    ("Cute", "emote-cute"),
    ("TikTokDance9", "dance-tiktok9"),
    ("WeirdDance", "dance-weird"),
    ("TikTokDance10", "dance-tiktok10"),
    ("Pose7", "emote-pose7"),
    ("Pose8", "emote-pose8"),
    ("CasualDance", "idle-dance-casual"),
    ("Pose1", "emote-pose1"),
    ("Pose3", "emote-pose3"),
    ("Pose5", "emote-pose5"),
    ("Cutey", "emote-cutey"),
    ("PunkGuitar", "emote-punkguitar"),
    ("ZombieRun", "emote-zombierun"),
    ("Fashionista", "emote-fashionista"),
    ("Gravity", "emote-gravity"),
    ("IceCreamDance", "dance-icecream"),
    ("WrongDance", "dance-wrong"),
    ("UwU", "idle-uwu"),
    ("TikTokDance4", "idle-dance-tiktok4"),
    ("AdvancedShy", "emote-shy2"),
    ("AnimeDance", "dance-anime"),
    ("Kawaii", "dance-kawai"),
    ("Scritchy", "idle-wild"),
    ("IceSkating", "emote-iceskating"),
    ("SurpriseBig", "emote-pose6"),
    ("CelebrationStep", "emote-celebrationstep"),
    ("Creepycute", "emote-creepycute"),
    ("Frustrated", "emote-frustrated"),
    ("Pose10", "emote-pose10"),
    ("Relaxed", "sit-relaxed"),
    ("LaidBack", "sit-open"),
    ("Stargazing", "emote-stargaze"),
    ("Slap", "emote-slap"),
    ("Boxer", "emote-boxer"),
    ("HeadBlowup", "emote-headblowup"),
    ("KawaiiGoGo", "emote-kawaiigogo"),
    ("Repose", "emote-repose"),
    ("Tiktok7", "idle-dance-tiktok7"),
    ("Shrink", "emote-shrink"),
    ("DitzyPose", "emote-pose9"),
    ("Teleporting", "emote-teleporting"),
    ("Touch", "dance-touch"),
    ("AirGuitar", "idle-guitar"),
    ("ThisIsForYou", "emote-gift"),
    ("Pushit", "dance-employee"),
    ("SweetSmooch", "emote-kissing"),
    ("WopDance", "dance-tiktok11"),
    ("CuteSalute", "emote-cutesalute"),
    ("AtAttention", "emote-salute"),
]

import asyncio

async def help_emote(bot, user, message):
    """
    Displays the emote help menu.
    """
    p = getattr(bot, 'prefix', '!')
    help_text = (
        f"💃 Emote Help Menu 💃\n"
        f"Commands:\n"
        f"1. <emote_name> - Loop emote (e.g., 'maniac')\n"
        f"2. stop - Stop current emote loop\n"
        f"3. <emote_name> @user - Loop emote on user\n"
        f"4. {p}emoteall <emote_name> - Loop emote for everyone\n"
        f"5. {p}emote list - Send list via Whisper\n"
        f"6. random [@user] - Loop a random emote\n"
        f"7. {p}emote bot <name> - Bot loops emote"
    )
    from core.utils.chat import send_safe_chat
    await send_safe_chat(bot, help_text)

async def list_emotes(bot, user, message):
    """
    Lists all emotes (Names only) via whisper.
    """
    emote_names = [name for name, _ in ALL_EMOTES]
    await bot.highrise.whisper(user.id, "Available Emotes:")
    
    # Send names in chunks of 20, separated by newlines
    chunk_size = 30
    for i in range(0, len(emote_names), chunk_size):
        chunk = "\n".join(emote_names[i:i+chunk_size])
        await bot.highrise.whisper(user.id, chunk)

async def get_target_user(bot, username: str):
    room_users = await bot.highrise.get_room_users()
    if hasattr(room_users, 'content'):
        for r_user, _ in room_users.content:
            if r_user.username.lower() == username.lower():
                return r_user
    return None

async def stop_emote_task(bot, user_id: str):
    """
    Stops any active emote loop for the user.
    """
    if not hasattr(bot, 'emote_tasks'):
        bot.emote_tasks = {}
        
    if user_id in bot.emote_tasks:
        task = bot.emote_tasks[user_id]
        task.cancel()
        del bot.emote_tasks[user_id]

async def emote_loop(bot, user_id: str, emote_id: str):
    """
    Async loop to keep sending the emote.
    """
    from loguru import logger
    try:
        while True:
            try:
                # logger.debug(f"Sending emote {emote_id} to {user_id}")
                await bot.queue_physical("emote", emote_id, user_id)
            except Exception as e:
                # If error is about ownership, stop this loop as it will never work
                if "not free or owned" in str(e).lower():
                    if user_id == getattr(bot, 'my_id', None):
                         await bot.highrise.chat(f"I don't own this emote, please try a Free emote! ❌")
                         bot.current_bot_emote = None
                    logger.warning(f"Stopping emote loop for {user_id}: emote {emote_id} not owned.")
                    break
                logger.error(f"Failed to send emote {emote_id}: {e}")
            await asyncio.sleep(5) 
    except asyncio.CancelledError:
        pass

async def random_emote_loop(bot, user_id: str):
    """
    Async loop to keep sending random emotes.
    """
    import random
    from loguru import logger
    try:
        while True:
            try:
                _, emote_id = random.choice(ALL_EMOTES)
                # logger.debug(f"Sending random emote {emote_id} to {user_id}")
                await bot.queue_physical("emote", emote_id, user_id)
            except Exception as e:
                # Just skip if unowned in random mode, keep trying others
                if "not free or owned" in str(e).lower():
                    continue 
                logger.error(f"Failed to send random emote: {e}")
                break
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        pass

async def perform_emote_logic(bot, user, message, is_command=False):
    """
    Checks if message is an emote trigger (with or without prefix, or target).
    """
    msg = message.strip()
    parts = msg.split()
    if not parts:
        return False
        
    lower_msg = msg.lower()
    
    # Check for STOP command
    if lower_msg == "stop":
        await stop_emote_task(bot, user.id)
        # Clear bot's emote loop
        bot.current_bot_emote = None
        await bot.highrise.chat("Emote stopped.")
        return True

    # Check for EMOTE BOT command (can be "!emote bot name" or just "bot name")
    temp_msg = lower_msg
    is_explicit = False
    
    # If the prefix "!emote " is present, strip it for internal checking
    if temp_msg.startswith("emote "):
        temp_msg = temp_msg[len("emote "):].strip()
        is_explicit = True
    elif temp_msg.startswith("!emote "): # fallback for explicit
        temp_msg = temp_msg[len("!emote "):].strip()
        is_explicit = True

    if is_explicit and temp_msg.startswith("bot "):
        # Role check: Only Admin+ can make bot emote
        from core.utils.permissions import get_user_role, has_permission
        caller_role = await get_user_role(user.id, user.username)
        if not has_permission(caller_role, "admin"):
            await bot.highrise.chat(f"Sorry @{user.username}, only Admin and above can command the bot to emote.")
            return True

        target_input = temp_msg[len("bot "):].strip()
        
        # Handle "emote bot random"
        if target_input.lower() == "random":
            bot.current_bot_emote = "random_shuffle"
            await bot.highrise.chat(f"Bot will now start shuffling random emotes! 🤖🎲✨")
            return True

        match_id = None
        match_name = target_input # Default
        
        # 1. Try to find friendly name match
        for name, eid in ALL_EMOTES:
            if name.lower() == target_input.lower():
                match_id = eid
                match_name = name
                break
        
        # 2. Handle RAW ID or Ignore casual chat
        if not match_id:
            # If not explicit (just saying "bot ..."), don't guess raw IDs to avoid "bot lu knp"
            if not is_explicit:
                return False 
            # If explicit command ("!emote bot ..."), allow raw ID
            match_id = target_input
            
        # Set the ID for the on_start loop to pick up
        bot.current_bot_emote = match_id
        await bot.highrise.chat(f"Bot will now try to loop {match_name}! 🤖✨")
        return True

    # Check for RANDOM command
    if lower_msg.startswith("random"):
        # Role check: Only VIP+ can use random shuffle
        from core.utils.permissions import get_user_role, has_permission
        caller_role = await get_user_role(user.id, user.username)
        if not has_permission(caller_role, "vip"):
            await bot.highrise.chat(f"Sorry @{user.username}, only VIP and above can use random emotes.")
            return True

        parts = lower_msg.split()
        target_username = None
        if len(parts) > 1 and parts[1].startswith("@"):
            target_username = parts[1][1:].strip()

        target_user_id = user.id
        if target_username:
            # Check if user has permission to target others
            from core.utils.permissions import get_user_role
            role = await get_user_role(user.id, user.username)
            if role == "public":
                await bot.highrise.chat(f"Sorry @{user.username}, only VIP and above can target others with random emotes.")
                return True
                
            target_obj = await get_target_user(bot, target_username)
            if target_obj:
                target_user_id = target_obj.id
            else:
                await bot.highrise.chat(f"User @{target_username} not found.")
                return True

        await stop_emote_task(bot, target_user_id)
        # Use the new random cycle loop
        task = asyncio.create_task(random_emote_loop(bot, target_user_id))
        bot.emote_tasks[target_user_id] = task
        
        display_name = f"@{target_username}" if target_username else "you"
        await bot.highrise.chat(f"Looping random shuffle for {display_name}! 🎲✨")
        return True
    
    # Initialize tasks dict if needed
    if not hasattr(bot, 'emote_tasks'):
        bot.emote_tasks = {}

    # Sort ALL_EMOTES by length desc
    sorted_emotes = sorted(ALL_EMOTES, key=lambda x: len(x[0]), reverse=True)
    
    match_name = None
    match_id = None
    target_username = None
    
    for name, eid in sorted_emotes:
        if lower_msg.startswith(name.lower()):
            remaining = lower_msg[len(name):].strip()
            if not remaining or remaining.startswith("@"):
                match_name = name
                match_id = eid
                if remaining.startswith("@"):
                    target_username = remaining[1:].strip().split()[0]
                break
    
    if match_name and match_id:
        target_user_id = user.id
        if target_username:
            # Check if user has permission to target others
            from core.utils.permissions import get_user_role
            role = await get_user_role(user.id, user.username)
            if role == "public":
                await bot.highrise.chat(f"Sorry @{user.username}, only VIP and above can target others with emotes.")
                return True
                
            target_obj = await get_target_user(bot, target_username)
            if target_obj:
                target_user_id = target_obj.id
            else:
                await bot.highrise.chat(f"User @{target_username} not found.")
                return True
        
        await stop_emote_task(bot, target_user_id)
        task = asyncio.create_task(emote_loop(bot, target_user_id, match_id))
        bot.emote_tasks[target_user_id] = task
        await bot.highrise.chat(f"Looping {match_name}...")
        return True
        
    return False

async def handle_emote_action(bot, user, message):
    clean_msg = message[len("!emote"):].strip()
    if not clean_msg:
         await help_emote(bot, user, message)
         return
    
    if clean_msg.lower() == "list":
         await list_emotes(bot, user, message)
         return

    processed = await perform_emote_logic(bot, user, clean_msg)
    if not processed:
        await bot.highrise.chat("Emote not found.")

async def emote_all_command(bot, user, message):
    # Role check: Only Admin+
    from core.utils.permissions import get_user_role, has_permission
    caller_role = await get_user_role(user.id, user.username)
    if not has_permission(caller_role, "admin"):
        await bot.highrise.chat(f"Sorry @{user.username}, only Admin and above can use !emoteall.")
        return

    parts = message.strip().split()
    if len(parts) < 2:
        await bot.highrise.chat("Usage: !emoteall <emote_name>")
        return
    
    arg = " ".join(parts[1:]).lower()
    target_id = None
    for name, eid in ALL_EMOTES:
        if name.lower() == arg:
            target_id = eid
            break
            
    if not target_id:
        await bot.highrise.chat("Emote not found.")
        return
        
    room_users = await bot.highrise.get_room_users()
    if hasattr(room_users, 'content'):
        for r_user, _ in room_users.content:
            try:
                await bot.highrise.send_emote(target_id, r_user.id)
            except:
                pass
