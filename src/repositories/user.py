from src.models import User
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):

    model = User

    async def get_by_email(self, email: str) -> User | None:
        return await self.get_by_field("email", email)
