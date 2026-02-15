from loguru import logger

async def send_safe_chat(bot, message: str):
    """
    Sends a chat message, automatically splitting it into multiple messages
     if it exceeds the Highrise character limit (approx 256 chars).
    """
    if not message:
        return

    # Highrise limit is around 256, let's use 200 for safety and better readability
    limit = 200
    
    if len(message) <= limit:
        await bot.highrise.chat(message)
        return

    # Split by lines first to avoid cutting words/sentences
    lines = message.split('\n')
    current_chunk = ""
    
    for line in lines:
        # If a single line is already too long (rare for help text), split it by 200
        if len(line) > limit:
            # Send whatever was in current_chunk first
            if current_chunk:
                await bot.highrise.chat(current_chunk.strip())
                current_chunk = ""
            
            # Split the long line
            for i in range(0, len(line), limit):
                await bot.highrise.chat(line[i:i+limit])
            continue

        # If adding this line exceeds the limit, send current_chunk
        if len(current_chunk) + len(line) + 1 > limit:
            await bot.highrise.chat(current_chunk.strip())
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"

    # Send remaining
    if current_chunk:
        await bot.highrise.chat(current_chunk.strip())
