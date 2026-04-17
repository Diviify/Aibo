from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.match import Match
from app.models.user import User
from app.services.auth_service import verify_token
from app.services.chat_service import create_message
from app.services.connection_manager import connection_manager

router = APIRouter()


def _resolve_current_user(token: str, db) -> User | None:
    token_data = verify_token(token)
    statement = select(User).where(User.email == token_data["email"])
    return db.execute(statement).scalar_one_or_none()


def _resolve_match(match_id: int, db) -> Match | None:
    statement = select(Match).where(Match.id == match_id)
    return db.execute(statement).scalar_one_or_none()


@router.websocket("/ws/chat/{match_id}")
async def chat_websocket(websocket: WebSocket, match_id: int) -> None:
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Missing authentication token",
        )
        return

    db = SessionLocal()
    connected = False

    try:
        try:
            current_user = _resolve_current_user(token, db)
        except Exception:
            await websocket.close(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Invalid or expired token",
            )
            return

        if current_user is None:
            await websocket.close(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Authenticated user not found",
            )
            return

        match = _resolve_match(match_id, db)
        if match is None:
            await websocket.close(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Match not found",
            )
            return

        if current_user.id not in {match.user1_id, match.user2_id}:
            await websocket.close(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="User is not part of this match",
            )
            return

        await connection_manager.connect(match_id, websocket)
        connected = True

        while True:
            payload = await websocket.receive_json()
            message_text = str(payload.get("message", "")).strip()

            if not message_text:
                await websocket.send_json({"error": "Message cannot be empty"})
                continue

            saved_message = create_message(
                match_id=match_id,
                sender_id=current_user.id,
                message=message_text,
                db=db,
            )

            await connection_manager.broadcast(
                match_id,
                {
                    "sender_id": current_user.id,
                    "message": saved_message.message,
                    "created_at": saved_message.created_at.isoformat(),
                },
            )

    except WebSocketDisconnect:
        pass
    except Exception:
        if connected:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
    finally:
        if connected:
            connection_manager.disconnect(match_id, websocket)
        db.close()
