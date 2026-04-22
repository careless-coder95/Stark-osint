import logging
from pyrogram import Client
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChannelInvalid
from config import FORCE_JOIN_CHANNELS

logger = logging.getLogger(__name__)


async def check_force_join(client: Client, user_id: int) -> bool:
    """
    Returns True if the user has joined ALL required channels.
    Returns False if any channel membership check fails.
    """
    for channel in FORCE_JOIN_CHANNELS:
        username = channel.get("username", "").lstrip("@")
        try:
            member = await client.get_chat_member(username, user_id)
            # Banned or kicked users are treated as non-members
            if member.status.name in ("BANNED", "LEFT"):
                logger.info(f"User {user_id} has left/banned from {username}")
                return False
        except UserNotParticipant:
            logger.info(f"User {user_id} not in {username}")
            return False
        except (ChatAdminRequired, ChannelInvalid) as e:
            # Bot is not admin or channel invalid → skip this channel gracefully
            logger.warning(f"Cannot check {username}: {e}. Skipping.")
            continue
        except Exception as e:
            logger.error(f"Force join check error for {username}: {e}")
            return False
    return True
