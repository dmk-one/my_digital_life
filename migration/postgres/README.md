Generic single-database configuration.

To autogenerate migration file type:
# alembic -c migration/postgres/alembic.ini revision --autogenerate -m 'Your comment about it migration'

If your changes in models were not included in migration file
look at migration/env.py _IGNORE_TABLES

To apply existing migration files type:
# alembic -c migration/postgres/alembic.ini upgrade head

(You may need to create postgis extension in your db)
