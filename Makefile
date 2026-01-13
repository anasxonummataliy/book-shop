init_alembic:
	alembic init migration

revision:
	alembic revision --autogenerate -m "Initial migration"
	
migrate:
	alembic upgrade head