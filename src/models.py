from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import select

db = SQLAlchemy()

# ------------------ USER ------------------
class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    tareas: Mapped[list["Tarea"]] = relationship(
        "Tarea", back_populates="user", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "tareas": [t.serialize() for t in self.tareas]
        }

    # ------------------ CRUD ------------------
    @classmethod
    def create(cls, email):
        user = cls(email=email)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_all(cls):
        stmt = select(cls)
        return db.session.scalars(stmt).all()

    @classmethod
    def get_by_id(cls, user_id):
        return db.session.get(cls, user_id)

    @classmethod
    def update_email(cls, user_id, new_email):
        user = db.session.get(cls, user_id)
        if user:
            user.email = new_email
            db.session.commit()
            return user
        return None

    @classmethod
    def delete(cls, user_id):
        user = db.session.get(cls, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False


# ------------------ TAREA ------------------
class Tarea(db.Model):
    __tablename__ = "tareas"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped[User] = relationship("User", back_populates="tareas")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "user_id": self.user_id
        }

    # ------------------ CRUD ------------------
    @classmethod
    def create(cls, title, user_id, completed=False):
        tarea = cls(title=title, user_id=user_id, completed=completed)
        db.session.add(tarea)
        db.session.commit()
        return tarea

    @classmethod
    def get_all(cls):
        stmt = select(cls)
        return db.session.scalars(stmt).all()

    @classmethod
    def get_by_id(cls, tarea_id):
        return db.session.get(cls, tarea_id)

    @classmethod
    def update(cls, tarea_id, title=None, completed=None):
        tarea = db.session.get(cls, tarea_id)
        if tarea:
            if title is not None:
                tarea.title = title
            if completed is not None:
                tarea.completed = completed
            db.session.commit()
            return tarea
        return None

    @classmethod
    def delete(cls, tarea_id):
        tarea = db.session.get(cls, tarea_id)
        if tarea:
            db.session.delete(tarea)
            db.session.commit()
            return True
        return False
