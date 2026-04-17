from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, match_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[match_id].append(websocket)

    def disconnect(self, match_id: int, websocket: WebSocket) -> None:
        connections = self.active_connections.get(match_id)
        if not connections:
            return

        if websocket in connections:
            connections.remove(websocket)

        if not connections:
            self.active_connections.pop(match_id, None)

    async def broadcast(self, match_id: int, message: dict[str, int | str]) -> None:
        connections = self.active_connections.get(match_id, [])
        disconnected: list[WebSocket] = []

        for connection in connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(match_id, connection)


connection_manager = ConnectionManager()
