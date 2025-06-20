#!/usr/bin/env bash
python - <<'PYCODE'
from sqlmodel import SQLModel, Session, create_engine, select
from app.models import User
from app.auth import get_password_hash
engine = create_engine('sqlite:///users.db')
SQLModel.metadata.create_all(engine)
with Session(engine) as session:
    if not session.exec(select(User).where(User.username=='admin')).first():
        u = User(username='admin', hashed_password=get_password_hash('admin123'))
        session.add(u)
        session.commit()
PYCODE
mc alias set local http://minio:9000 admin secret123
mc mb --ignore-existing local/cctv
mc cp /videos/*.mp4 local/cctv/
