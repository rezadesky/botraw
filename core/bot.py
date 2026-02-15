from highrise import BaseBot, User, Position, SessionMetadata, AnchorPosition
from tortoise import Tortoise
import os
import asyncio
from typing import Literal
from loguru import logger
from dotenv import load_dotenv

# Load dependencies for local testing (Docker will provide these via env_file)
# load_dotenv() is handled in main block or externally

class MyBot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        # Save bot ID
        self.my_id = session_metadata.user_id
        self.current_bot_emote = None
        
        # 1. Initialize Database FIRST
        try:
            if not getattr(self, '_db_connected', False):
                db_url = os.getenv("DATABASE_URL", "sqlite://database/bot.db")
                await Tortoise.init(
                    db_url=db_url,
                    modules={'models': ['core.models']}
                )
                await Tortoise.generate_schemas()
                
                # WAL Mode for better SQLite concurrency
                conn = Tortoise.get_connection("default")
                await conn.execute_script("PRAGMA journal_mode=WAL;")
                
                self._db_connected = True
                logger.success("Database connected (WAL mode) and schemas generated.")
        except Exception as e:
            if "already initialized" in str(e):
                self._db_connected = True
            else:
                logger.error(f"Failed to initialize database: {e}")

        # 2. Start Bot Emote Loop
        asyncio.create_task(self._bot_emote_loop())

        # 3. Load settings from DB
        from core.models import Setting
        pref_setting = await Setting.get_or_none(key="prefix")
        self.prefix = pref_setting.value if pref_setting else "!"

        self.loop_task = None
            
        logger.info("Bot is starting...")

        # 3. Handle Spawns and Loop
        try:
            from core.models import Teleport
            from highrise import Position
            bot_spawn = await Teleport.get_or_none(command="bot_spawn")
            if bot_spawn:
                pos = Position(bot_spawn.x, bot_spawn.y, bot_spawn.z, bot_spawn.facing)
                await asyncio.sleep(2)
                await self.highrise.teleport(self.my_id, pos)
                logger.info("Bot teleported to bot_spawn.")
            
            await self.update_loop_task()
        except Exception as e:
            logger.error(f"Error during startup teleport/loop: {e}")

        if hasattr(session_metadata, 'room_info') and hasattr(session_metadata.room_info, 'room_id'):
            logger.success(f"Bot connected to room: {session_metadata.room_info.room_id}")
        else:
             # Fallback for different SDK versions or mock
            logger.success(f"Bot connected to room (ID not directly available in metadata root)")

    async def update_loop_task(self):
        # Cancel existing task if any
        if self.loop_task:
            self.loop_task.cancel()
            self.loop_task = None

        from core.models import Setting
        l_on = await Setting.get_or_none(key="loop_on")
        if l_on and l_on.value == "true":
            self.loop_task = asyncio.create_task(self.run_loop_logic())
            logger.info("Loop task started.")

    async def run_loop_logic(self):
        try:
            while True:
                from core.models import Setting
                l_msg = await Setting.get_or_none(key="loop_msg")
                l_int = await Setting.get_or_none(key="loop_interval")
                
                msg = l_msg.value if l_msg else None
                interval = int(l_int.value) if l_int and l_int.value.isdigit() else 60
                
                if msg:
                    await self.highrise.chat(msg)
                
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            logger.info("Loop task cancelled.")
        except Exception as e:
            logger.error(f"Error in loop logic: {e}")

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        logger.info(f"User joined: {user.username} ({user.id})")

        async def handle_join():
            try:
                # User Auto Spawn (Optional logic check)
                from core.models import Teleport
                user_spawn = await Teleport.get_or_none(command="user_spawn")
                if user_spawn:
                    pos = Position(user_spawn.x, user_spawn.y, user_spawn.z, user_spawn.facing)
                    await self.highrise.teleport(user.id, pos)
                
                # Welcome Message
                from core.models import Setting
                welcome_setting = await Setting.get_or_none(key="welcome_message")
                if welcome_setting and welcome_setting.value:
                    await self.highrise.chat(welcome_setting.value.replace("@user", f"@{user.username}"))
                
                # Check for autorole
                autorole_setting = await Setting.get_or_none(key="autorole")
                if autorole_setting and autorole_setting.value:
                    from core.models import Role
                    await Role.update_or_create(
                        user_id=user.id,
                        defaults={"role_name": autorole_setting.value}
                    )
            except Exception as e:
                logger.error(f"Error in on_user_join task: {e}")
        
        asyncio.create_task(handle_join())
        
    async def on_tip(self, sender: User, receiver: User, tip: any) -> None:
        async def handle_tip():
            try:
                logger.info(f"Bot received tip {tip} from {sender.username}")
                # If bot is the receiver
                if receiver.id == getattr(self, 'my_id', None):
                    # Extract number from tip string (e.g., gold_bar_50 -> 50)
                    amount = tip.split("_")[-1].replace("k", "000")
                    await self.highrise.chat(f"Thank you for the {amount} Gold tip, @{sender.username}! 💖")
            except Exception as e:
                logger.error(f"Error in on_tip: {e}")
                
        asyncio.create_task(handle_tip())

    async def _bot_emote_loop(self) -> None:
        import random
        from core.commands.helpemote import ALL_EMOTES
        # Increase frequency as per standard bot loops (approx every 5-10s)
        while True:
            try:
                if self.current_bot_emote:
                    target_id = self.current_bot_emote
                    # If random shuffle is active, pick a random ID each iteration
                    if target_id == "random_shuffle":
                        _, target_id = random.choice(ALL_EMOTES)
                    
                    # Explicitly send to self as target
                    await self.highrise.send_emote(target_id, self.my_id)
            except Exception as e:
                # If unowned, we log it once but don't stop the loop
                if "not free or owned" in str(e).lower():
                    pass # Silently skip to avoid console spam
                else:
                    logger.error(f"Bot emote loop error: {e}")
            await asyncio.sleep(5) 

    async def queue_physical(self, channel: str, *args):
        """
        Generic queue for physical actions (emote, teleport) to prevent rate limits.
        """
        if not hasattr(self, '_phys_queue'):
            self._phys_queue = asyncio.Queue()
            asyncio.create_task(self._process_phys_queue())
        
        await self._phys_queue.put((channel, args))

    async def _process_phys_queue(self):
        while True:
            channel, args = await self._phys_queue.get()
            try:
                if channel == "emote":
                    await self.highrise.send_emote(*args)
                elif channel == "teleport":
                    await self.highrise.teleport(*args)
            except Exception as e:
                # Silent skip for ownership issues or cooldowns
                if "not free or owned" not in str(e).lower():
                    logger.error(f"Physical queue error ({channel}): {e}")
            
            # Small delay between any physical actions
            await asyncio.sleep(0.5) 
            self._phys_queue.task_done()

    async def on_chat(self, user: User, message: str) -> None:
        logger.info(f"[{user.username}]: {message}")
        
        msg = message.strip()
        if not msg:
            return

        # Ensure prefix is set (safeguard)
        prefix = getattr(self, 'prefix', '!')
        
        # Check command
        if msg.startswith(prefix):
            # Remove prefix
            content = msg[len(prefix):]
            parts = content.split()
            if not parts:
                return
                
            command = parts[0].lower()
            
            # Permission Check
            from core.utils.permissions import can_run_command
            if not await can_run_command(user.id, command, msg, user.username):
                await self.highrise.chat(f"Sorry @{user.username}, you don't have permission for that.")
                return

            # Dispatch to handlers
            from core.commands import COMMAND_HANDLERS
            
            if command in COMMAND_HANDLERS:
                handler = COMMAND_HANDLERS[command]
                # EXECUTION IMPROVEMENT: Wrap in task to prevent blocking the main event loop
                # This allows the bot to handle multiple users' commands simultaneously
                async def execute_cmd():
                    try:
                        await handler(self, user, message)
                    except Exception as e:
                        logger.error(f"Error executing command {command}: {e}")
                        await self.highrise.chat(f"Error in {command}: {str(e)[:50]}...")
                
                asyncio.create_task(execute_cmd())
                return # Command handoff complete
                
        # Check if message is a teleport trigger
        from core.utils.permissions import get_user_role
        user_role = await get_user_role(user.id, user.username)
        
        # Only VIP and above can use teleport triggers (saved names)
        if user_role in ["host", "admin", "vip"]:
            from core.commands.helptele import check_teleport_trigger
            try:
                 await check_teleport_trigger(self, user, msg)
            except Exception as e:
                 logger.error(f"Error checking teleport trigger: {e}")

        # Fallback: Check for non-command emote triggers (e.g. "maniac" or "maniac @user")
        from core.commands.helpemote import perform_emote_logic
        try:
            # Emote triggers are Public
            await perform_emote_logic(self, user, msg)
        except Exception as e:
            logger.error(f"Error checking emote logic: {e}")

    async def on_stop(self) -> None:
        logger.info("Bot is stopping...")
        await Tortoise.close_connections()

if __name__ == "__main__":
    # Load environment variables
    # If ENV_FILE is set (e.g. by run_bot_1.bat), load from there.
    env_file = os.getenv("ENV_FILE")
    if env_file:
        load_dotenv(env_file, override=True)
    else:
        load_dotenv(override=True)

    # This allows running the bot directly: python -m core.bot
    # Expects HIGHRISE_ROOM_ID and HIGHRISE_TOKEN in environment variables
    room_id = os.getenv("HIGHRISE_ROOM_ID")
    token = os.getenv("HIGHRISE_TOKEN")
    
    if not room_id or not token:
        logger.error("HIGHRISE_ROOM_ID or HIGHRISE_TOKEN not found in environment variables.")
        exit(1)

    logger.info(f"Starting bot for Room ID: {room_id}")
    
    # Debug: Verify loaded config
    logger.info(f"Loaded ENV_FILE: {env_file}")
    if token:
        logger.info(f"Token loaded: {token[:5]}...***** (Length: {len(token)})")
    else:
        logger.error("Token is EMPTY or None!")

    # Run the bot using runpy to simulate 'python -m highrise ...'
    # This avoids import errors with internal highrise functions
    import sys
    import runpy
    import time
    
    # Arguments: script_name, bot_path, room_id, token
    sys.argv = ["highrise", "core.bot:MyBot", room_id, token]
    
    while True:
        try:
            logger.info("Attempting to start bot session...")
            runpy.run_module("highrise", run_name="__main__")
        except SystemExit:
            logger.warning("Bot system exited. Retrying...")
        except Exception as e:
            logger.error(f"Bot session crashed with error: {e}")
            logger.exception(e)
        
        retry_delay = 5
        logger.info(f"Reconnecting in {retry_delay} seconds...")
        time.sleep(retry_delay)
