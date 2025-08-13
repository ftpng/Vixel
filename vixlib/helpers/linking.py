from vixlib import ensure_cursor, Cursor

class Linking:
    def __init__(self, discord_id: int) -> None:
        self.discord_id = discord_id

    @ensure_cursor
    def get_linked_player_uuid(self, *, cursor: Cursor=None) -> str | None:
        cursor.execute(
            "SELECT * FROM linked WHERE discord_id=%s", (self.discord_id,)
        )
        linked_data = cursor.fetchone()

        if linked_data and linked_data[1]:
            return linked_data[1]
        return None        

    @ensure_cursor
    def set_linked_player(self, uuid: str, *, cursor: Cursor=None) -> None:
        cursor.execute(
            "SELECT * FROM linked WHERE discord_id=%s", (self.discord_id,)
        )
        linked_data = cursor.fetchone()

        if not linked_data:
            cursor.execute(
                "INSERT INTO linked (discord_id, uuid) VALUES (%s, %s)", (self.discord_id, uuid,)
            )
        
        else:
            cursor.execute(
                "UPDATE linked SET uuid=%s WHERE discord_id=%s", (uuid, self.discord_id,)
            )

    @ensure_cursor
    def unlink_player(self, *, cursor: Cursor = None) -> bool:
        cursor.execute(
            "SELECT * FROM linked WHERE discord_id=%s", (self.discord_id,)
        )
        current_data = cursor.fetchone()

        if current_data:
            cursor.execute(
                "DELETE FROM linked WHERE discord_id=%s", (self.discord_id,)
            )
            return True
        else:
            return False

    @ensure_cursor
    def link_player(
        self, 
        discord_tag: str,
        hypixel_data: dict,
        uuid: str,
        *, cursor: Cursor=None
    ) -> int:
        
        if discord_tag.endswith('#0'):
            discord_tag = discord_tag[:-2]

        if not hypixel_data.get('player'):
            return -1
        
        hypixel_discord_tag: str = (hypixel_data.get('player') or {}).get('socialMedia', {}).get('links', {}).get('DISCORD', None)
        
        if hypixel_discord_tag:
            if discord_tag == hypixel_discord_tag:
                self.set_linked_player(uuid, cursor=cursor)
                return 1
            return 0
        return -1