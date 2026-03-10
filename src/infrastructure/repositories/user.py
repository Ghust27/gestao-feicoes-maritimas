from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.infrastructure.database.models.user import UserModel
from src.infrastructure.database.models.oil_feature import OilFeatureModel
from src.domain.entities.user import User
from src.schemas.user import UserDTO, Role


def _to_role(value) -> Role:
    if isinstance(value, Role):
        return value
    if isinstance(value, str):
        return Role(value.strip().lower())
    raise ValueError("Invalid role value")


def _to_db_role(value) -> str:
    role = _to_role(value)
    return role.value.upper()


def _model_to_user(model: UserModel) -> User:
    dto = UserDTO(
        name=model.name,
        email=model.email,
        hashed_password=model.password,
        role=_to_role(model.role),
    )
    return User(
        data=dto,
        active=model.active,
        created_at=model.created_at,
        id=model.id,
    )


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        return _model_to_user(model) if model else None

    def get_user_by_id(self, user_id: UUID) -> User | None:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return _model_to_user(model) if model else None

    def create_user(self, user: User) -> User:
        model = UserModel(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.hashed_password,
            role=_to_db_role(user.role),
            active=user.active,
            created_at=user.created_at,
        )
        self.db.add(model)
        try:
            self.db.commit()
            self.db.refresh(model)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Email already registered.")
        return _model_to_user(model)

    def get_all(self) -> list:
        models = self.db.query(UserModel).all()
        return [_model_to_user(m) for m in models]

    def is_user_active(self, user_id: UUID) -> bool:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return model.active if model else False

    def update_user(self, user_id: UUID, data: dict) -> User | None:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not model:
            return None
        update_dict = dict(data)
        if "hashed_password" in update_dict:
            update_dict["password"] = update_dict.pop("hashed_password")
        for key, value in update_dict.items():
            if hasattr(model, key):
                if key == "role" and value is not None:
                    setattr(
                        model,
                        key,
                        _to_db_role(value),
                    )
                else:
                    setattr(model, key, value)
        self.db.commit()
        self.db.refresh(model)
        return _model_to_user(model)

    def confirmed_features_count(self, user_id: UUID) -> int:
        return self.db.query(OilFeatureModel).filter(
            OilFeatureModel.confirmed_by == user_id
        ).count()

    def delete_user(self, user_id: UUID) -> bool:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False