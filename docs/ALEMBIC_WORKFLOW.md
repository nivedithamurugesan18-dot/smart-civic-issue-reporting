# Alembic Database Migration Workflow

## Purpose

Alembic is the project's explicit database schema migration mechanism. Database schema creation and changes are not performed automatically by FastAPI application startup.

Migration commands are deployment/release operations and must be run deliberately against an explicitly selected PostgreSQL database.

## Current baseline

The repository baseline is:

- Revision: `1b1e22234583`
- Description: `Initial schema baseline`
- Alembic version: `1.16.4`

The baseline represents these application tables:

- `users`
- `issues`
- `issue_updates`
- `issue_images`
- `departments`
- `assignments`
- `notifications`

## Existing database adoption

The existing `smart_civic` database was compared with the baseline using read-only PostgreSQL schema inspection. The comparison verified the application tables, columns, data types, nullability, primary keys, unique constraints, indexes, sequences, defaults, foreign keys, and foreign-key actions.

A PostgreSQL backup was created before adoption. With `ALEMBIC_DATABASE_URL` explicitly set to the intended database, the database was then stamped at revision `1b1e22234583`:

```text
python -m alembic -c alembic.ini stamp 1b1e22234583
```

Stamping recorded the existing schema revision in `alembic_version`; it did not execute the baseline table-creation statements. Application data and application schema objects were verified unchanged afterward.

The live database retains the approved `issues_reported_by_fkey` constraint:

```text
issues.reported_by -> users.id
```

## Normal future development workflow

For an intentional future schema change:

1. Modify the SQLAlchemy models intentionally.
2. Review the expected schema change before generating a revision.
3. Create a migration from the `backend` directory:

   ```powershell
   python -m alembic -c alembic.ini revision --autogenerate -m "describe change"
   ```

4. Inspect the generated migration manually.
5. Never blindly accept Alembic autogenerate output.
6. Check especially for unexpected drops, constraint changes, or foreign-key removals. Pay particular attention to `issues_reported_by_fkey`.
7. Test the migration against a disposable PostgreSQL database.
8. Run the migration against the disposable database:

   ```powershell
   python -m alembic -c alembic.ini upgrade head
   ```

9. Verify the disposable database schema and data.
10. Review the migration and verification evidence.
11. Only after approval, apply the migration to the intended deployment database:

    ```powershell
    python -m alembic -c alembic.ini upgrade head
    ```

12. Start or restart the application.

FastAPI startup does not run Alembic migrations. FastAPI also does not execute SQLAlchemy `create_all()`. Explicit deployment/release commands own schema changes.

## Target safety rule

Never run Alembic commands against the real or production database accidentally.

The Alembic environment requires `ALEMBIC_DATABASE_URL` explicitly. Supply that variable for each migration command and verify the target before executing a write operation. Do not rely on the application's ordinary `DATABASE_URL` implicitly for migrations.

Do not put passwords or complete real connection strings in source control or documentation. Use placeholders in examples.

## Windows PowerShell command reference

From the `backend` directory:

```powershell
$env:ALEMBIC_DATABASE_URL = "<explicit PostgreSQL URL>"
$env:PYTHONPATH = "."
python -m alembic -c alembic.ini current
python -m alembic -c alembic.ini heads
```

For a disposable PostgreSQL database:

```powershell
$env:ALEMBIC_DATABASE_URL = "<disposable PostgreSQL URL>"
$env:PYTHONPATH = "."
python -m alembic -c alembic.ini upgrade head
```

To create a migration after an intentional model change:

```powershell
python -m alembic -c alembic.ini revision --autogenerate -m "describe change"
```

Always inspect the generated revision before applying it.

## Rollback guidance

A downgrade is not an automatic safety net. Before using a downgrade, review the migration, understand its data-loss implications, verify whether the downgrade is actually reversible, and take an appropriate backup.

Do not assume that every migration can safely restore deleted or transformed data. Prefer a forward corrective migration when that is safer and more explicit.

## Baseline preservation policy

The baseline preserves the existing database contract, including:

- the legacy `assignments` table
- `issues_reported_by_fkey`
- existing indexes, including redundant primary-key indexes
- existing PostgreSQL sequences
- existing server defaults
- existing foreign-key actions
- the active assignment source of truth, `issues.assigned_to`

Do not add or remove constraints merely to make an automated comparison appear clean without a separate schema-policy decision.

## Known Alembic check warning

The current SQLAlchemy model does not declare the live `issues_reported_by_fkey` foreign key. Therefore:

```powershell
python -m alembic -c alembic.ini check
```

may report:

```text
remove_fk for issues_reported_by_fkey
```

This is an expected and approved model/database discrepancy. Do not apply that operation automatically. Do not remove the live foreign key and do not modify the `Issue` model solely to silence this warning.

Any additional autogenerate or check difference must be reviewed separately and must not be applied blindly.

## Migration safety policy

Before applying any future autogenerated migration:

1. Inspect the generated migration.
2. Check for `DROP` operations.
3. Check for unexpected foreign-key removals.
4. Check specifically for `issues_reported_by_fkey`.
5. Test the migration against a disposable PostgreSQL database.
6. Verify the resulting schema.
7. Verify that existing data is preserved.
8. Only then apply the migration to the intended database.

## CI boundary

CI validates Alembic imports, migration-file compilation, and baseline revision discovery without connecting to PostgreSQL. CI must not use the real `smart_civic` database and must not contain real database credentials.

A disposable PostgreSQL integration test can be added later if its service and isolation are explicitly designed and reviewed.
