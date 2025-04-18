from typing import TYPE_CHECKING, Optional

from ..core.db.connection import allow_writer
from . import ExportEvents
from .models import ExportEvent

if TYPE_CHECKING:
    from ..account.models import User
    from ..app.models import App
    from .models import ExportFile


@allow_writer()
def export_started_event(
    *,
    export_file: "ExportFile",
    user: Optional["User"] = None,
    app: Optional["App"] = None,
) -> None:
    ExportEvent.objects.create(
        export_file=export_file, user=user, app=app, type=ExportEvents.EXPORT_PENDING
    )


@allow_writer()
def export_success_event(
    *,
    export_file: "ExportFile",
    user: Optional["User"] = None,
    app: Optional["App"] = None,
) -> None:
    ExportEvent.objects.create(
        export_file=export_file, user=user, app=app, type=ExportEvents.EXPORT_SUCCESS
    )


@allow_writer()
def export_failed_event(
    *,
    export_file: "ExportFile",
    user: Optional["User"] = None,
    app: Optional["App"] = None,
    message: str,
    error_type: str,
) -> None:
    ExportEvent.objects.create(
        export_file=export_file,
        user=user,
        app=app,
        type=ExportEvents.EXPORT_FAILED,
        parameters={"message": message, "error_type": error_type},
    )


@allow_writer()
def export_deleted_event(
    *,
    export_file: "ExportFile",
    user: Optional["User"] = None,
    app: Optional["App"] = None,
) -> None:
    ExportEvent.objects.create(
        export_file=export_file, user=user, app=app, type=ExportEvents.EXPORT_DELETED
    )


@allow_writer()
def export_file_sent_event(*, export_file_id: int, user_id: int) -> None:
    ExportEvent.objects.create(
        export_file_id=export_file_id,
        user_id=user_id,
        type=ExportEvents.EXPORTED_FILE_SENT,
    )


@allow_writer()
def export_failed_info_sent_event(*, export_file_id: int, user_id: int) -> None:
    ExportEvent.objects.create(
        export_file_id=export_file_id,
        user_id=user_id,
        type=ExportEvents.EXPORT_FAILED_INFO_SENT,
    )
