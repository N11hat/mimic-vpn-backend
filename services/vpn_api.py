import uuid

class MarzbanAPI:
    @staticmethod
    async def create_user_config(tg_id: int) -> str:
        # Имитация работы API, пока нет реального сервера
        fake_uuid = str(uuid.uuid4())
        return f"vless://{fake_uuid}@192.168.1.1:443?type=tcp&security=reality#VPN_{tg_id}"