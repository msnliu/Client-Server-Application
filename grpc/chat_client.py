class ChatClient:
    client_id: str
    online: bool = True

    def __init__(self, client_id, online=True):
        self.client_id = client_id
        self.online = online

    def is_online(self) -> bool:
        return self.online

    def set_online(self, online) -> None:
        self.online = online
