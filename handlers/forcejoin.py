import logging
from pyrogram import Client
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChannelInvalid, PeerIdInvalid
from config import FORCE_JOIN_CHANNELS, FORCE_JOIN

logger = logging.getLogger(__name__)


async def check_force_join(client: Client, user_id: int) -> bool:
    """
    Returns True if:
      - FORCE_JOIN is False (disabled globally), OR
      - User has joined ALL channels in FORCE_JOIN_CHANNELS

    Supports both:
      - Public  → "id": "@username"
      - Private → "id": -100xxxxxxxxxx  (numeric int)
    """

    # ── Force join globally disabled ────────────────────────
    if not FORCE_JOIN:
        return True

    for ch in FORCE_JOIN_CHANNELS:
        chat_id = ch.get("id")

        # Skip if misconfigured
        if not chat_id:
            logger.warning(f"Force join channel missing 'id': {ch}")
            continue

        try:
            member = await client.get_chat_member(chat_id, user_id)

            # Banned or left = not a valid member
            if member.status.name in ("BANNED", "LEFT", "KICKED"):
                logger.info(f"User {user_id} not member of {chat_id} (status: {member.status.name})")
                return False

        except UserNotParticipant:
            logger.info(f"User {user_id} not in {chat_id}")
            return False

        except (ChatAdminRequired, ChannelInvalid, PeerIdInvalid) as e:
            # Bot is not admin in private channel OR wrong ID
            logger.warning(
                f"Cannot check membership for {chat_id}: {e}\n"
                f"Fix: Make sure bot is ADMIN in this channel/group."
            )
            # Don't block user if bot itself can't check — skip this channel
            continue

        except Exception as e:
            logger.error(f"Unexpected error checking {chat_id}: {e}")
            return False

    return True
