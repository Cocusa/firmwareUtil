from typing import Tuple

from models.technical_control_model import (
    Status,
    StatusError,
)


def get_failed_info(error_text: str, hint: str = "") -> Tuple[Status, StatusError]:
    return Status.Failed, StatusError(error_text, hint)
