from .colors import ColorMappings

class DisplayName:
    def __init__(self, hypixel_data: dict) -> None:
        self.hypixel_data: dict = hypixel_data

    def _get_default_rank(self) -> str:
        if self.hypixel_data.get('rank'):
            return self.hypixel_data['rank']

        if self.hypixel_data.get("monthlyPackageRank") == "SUPERSTAR":
            return "MVP_PLUS_PLUS"

        if self.hypixel_data.get("packageRank") or self.hypixel_data.get("newPackageRank"):
            rank_hierarchy = ["MVP_PLUS", "MVP", "VIP_PLUS", "VIP", "NONE"]

            old_package_rank = self.hypixel_data.get("packageRank", "NONE")
            new_package_rank = self.hypixel_data.get("newPackageRank", "NONE")

            return rank_hierarchy[min([
                rank_hierarchy.index(old_package_rank),
                rank_hierarchy.index(new_package_rank)
            ])]

        return "NONE"

    def get_rank_info(self) -> dict:
        player_uuid = self.hypixel_data.get('uuid')
        plus_color = self.hypixel_data.get("rankPlusColor", "gold").lower()
        rank = self._get_default_rank()

        base_rank_color = self.hypixel_data.get("rankColor") or self.hypixel_data.get("newPackageRankColor") or None
        if not base_rank_color:
            base_rank_color = "gold" if rank == "MVP_PLUS_PLUS" else "gray"

        rank_configs = {
            "STAFF": {"prefix": "&c[ADMIN] ", "color": "&c"},
            "GAME_MASTER": {"prefix": "&2[GM] ", "color": "&2"},
            "YOUTUBER": {"prefix": "&c[&fYOUTUBE&c] ", "color": "&c"},
            "MVP_PLUS_PLUS": {"prefix": f"&6[MVP{{plus_color}}++&6] ", "color": "&6"},
            "MVP_PLUS": {"prefix": f"&b[MVP{{plus_color}}+&b] ", "color": "&b"},
            "MVP": {"prefix": "&b[MVP] ", "color": "&b"},
            "VIP_PLUS": {"prefix": "&a[VIP&6+&a] ", "color": "&a"},
            "VIP": {"prefix": "&a[VIP] ", "color": "&a"},
            "NONE": {"prefix": "&7", "color": "&7"},
        }

        custom_configs = {
            "f7c77d999f154a66a87dc4a51ef30d19": {"prefix": "&c[OWNER] ", "color": "&c"},
            "9b2a30ecf8b34dfebf499c5c367383f8": {"prefix": "&c[OWNER] ", "color": "&c"},
            "b876ec32e396476ba1158438d83c67d4": {"prefix": "&d[PIG&b+++&d] ", "color": "&d"},
            "e80e8194323e414298515e1bcb8a3508": {"prefix": "&d[INNIT] ", "color": "&d"},
        }

        info = custom_configs.get(player_uuid)

        if not info:
            info = rank_configs.get(rank, {"prefix": "&7", "color": "&7"})

        prefix = info.get("prefix") or ""
        color = info.get("color") or "&7"

        if "{plus_color}" in prefix:
            plus_code = ColorMappings.str_to_color_code.get(plus_color, "&6")
            prefix = prefix.replace("{plus_color}", plus_code)

        return {
            "uuid": player_uuid,
            "rank": rank,
            "prefix": prefix,
            "color": color,
            "plus_color": plus_color,
        }

    def convert_color_codes(self, text: str | None) -> str:
        if not text:
            return ""
        for code, actual in ColorMappings.str_to_color_code.items():
            text = text.replace(code, actual)
        return text

    def get_displayname(self) -> str:
        username = self.hypixel_data.get('displayname') or self.hypixel_data.get('playername', 'Unknown')

        rank_info = self.get_rank_info()

        prefix = rank_info["prefix"]
        color = rank_info["color"]

        colored_prefix = self.convert_color_codes(prefix)
        username_color = self.convert_color_codes(color)

        return f"{colored_prefix}{username_color}{username}"
    
    def get_guild_tag(self) -> str:
        guild: dict = self.hypixel_data.get("guild")
        if not guild or not isinstance(guild, dict):
            return ""
        if not guild.get("tag"):
            return ""

        tag = guild.get("tag")
        tag_color = guild.get("tagColor", "gray").lower()

        color_code = ColorMappings.str_to_color_code.get(tag_color, "&7")
        colored_tag = f"{color_code}[{tag}]"
        return self.convert_color_codes(colored_tag)

    def get_displayname_guild(self) -> str:
        displayname = self.get_displayname()
        guild_tag = self.get_guild_tag()

        if guild_tag:
            full_name = f"{displayname} {guild_tag}"
        else:
            full_name = displayname

        return self.convert_color_codes(full_name)