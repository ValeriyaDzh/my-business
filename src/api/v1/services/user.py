import logging
from typing import TYPE_CHECKING, Any

from src.models import User
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


if TYPE_CHECKING:
    from src.models import User

logger = logging.getLogger(__name__)


class UserService(BaseService):
    pass
