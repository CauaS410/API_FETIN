from fastapi import APIRouter, Query, Depends
from app.services.notificacao_service import NotificacaoService
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/notificacoes", tags=["Notificações"])


@router.get("", summary="Listar notificações do usuário logado")
def list_notificacoes(limit: int = Query(default=20, ge=1, le=100), current_user: dict = Depends(get_current_user)):
    return NotificacaoService.listar_do_usuario(current_user["email"], limit)


@router.patch("/{notificacao_id}/ler", summary="Marcar notificação como lida")
def marcar_como_lida(notificacao_id: str, current_user: dict = Depends(get_current_user)):
    return NotificacaoService.marcar_como_lida(notificacao_id, current_user["email"])