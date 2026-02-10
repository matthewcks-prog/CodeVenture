# Django MCP Server Setup

This document explains how to use the Django MCP (Model Context Protocol) server for debugging your CodeVenture application.

## What is Django MCP?

The Django MCP server provides debugging and inspection tools that let you:
- List and inspect Django models
- Query the database using Django ORM
- Run management commands
- Check migration status
- Inspect URL patterns and settings
- Execute read-only SQL queries

## Setup

The Django MCP server is already configured in `.cursor/mcp.json`. Cursor will automatically load it when you open the project.

### Configuration

Location: `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "django-debug": {
      "command": "python",
      "args": ["django_mcp_server.py"],
      "cwd": "${workspaceFolder}",
      "env": {
        "DJANGO_SETTINGS_MODULE": "CodeVenture.settings",
        "PYTHONPATH": "${workspaceFolder}"
      },
      "description": "Django debugging and inspection tools"
    }
  }
}
```

## Testing the Server

Test that the server works correctly:

```bash
# List available tools
python django_mcp_server.py list-tools

# Run comprehensive test
python django_mcp_server.py test
```

## Available Tools

### 1. django_models_list
List all Django models in the project.

**Example:**
```json
{
  "app_label": "auth"  // Optional: filter by app
}
```

### 2. django_model_inspect
Inspect a specific model's fields and structure.

**Example:**
```json
{
  "app_label": "auth",
  "model_name": "User"
}
```

### 3. django_query
Query a model using Django ORM.

**Example:**
```json
{
  "app_label": "auth",
  "model_name": "User",
  "filter": {"is_superuser": true},
  "limit": 10
}
```

### 4. django_sql_query
Execute raw SQL queries (SELECT only).

**Example:**
```json
{
  "sql": "SELECT * FROM auth_user LIMIT 5"
}
```

### 5. django_management_command
Run Django management commands.

**Example:**
```json
{
  "command": "showmigrations",
  "args": [],
  "options": {}
}
```

### 6. django_settings_inspect
Inspect Django settings (sensitive values are redacted).

**Example:**
```json
{
  "setting_name": "DEBUG"  // Optional: specific setting
}
```

### 7. django_urls_list
List all URL patterns in the project.

### 8. django_migrations_status
Check migration status for all apps.

**Example:**
```json
{
  "app_label": "auth"  // Optional: filter by app
}
```

## Usage in Cursor

Once configured, you can use natural language to interact with Django through Cursor:

**Examples:**
- "List all Django models"
- "Show me the User model structure"
- "Query the database for all superusers"
- "Check the migration status"
- "Show me all URL patterns"
- "What is the DEBUG setting value?"

Cursor will automatically call the appropriate MCP tools to answer your questions.

## Fixing Migration Issues

If you encounter migration inconsistencies, use the fix script:

```bash
python fix_migrations.py
```

This script will:
1. Detect migration order issues
2. Offer to fix them automatically
3. Show the current migration status

## Security Notes

- SQL queries are restricted to SELECT statements only
- Sensitive settings (SECRET_KEY, passwords, etc.) are automatically redacted
- The MCP server runs locally and doesn't expose any network endpoints
- All operations use your local Django configuration

## Troubleshooting

### Server Won't Start

1. Make sure you're in the project directory
2. Check that Django is properly installed: `pip install Django`
3. Verify the settings module: `python manage.py check`

### Can't Connect to Database

1. Check your `.env` file has the correct DATABASE_URL
2. For local development, ensure PostgreSQL/SQLite is running
3. Run: `python manage.py check --database default`

### Migration Errors

Use the fix script:
```bash
python fix_migrations.py
```

Or manually fix:
```bash
python manage.py migrate sites --fake-initial
python manage.py migrate
```

## Local Development vs Production

The Django MCP server works with your local `.env` configuration. 

**Local (SQLite):**
- Uses `db.sqlite3` file
- Configured via `.env` or defaults

**Production (Render):**
- Uses PostgreSQL via DATABASE_URL environment variable
- The MCP server queries your local database, not production

To inspect production database, you'll need to:
1. Download a database backup from Render
2. Import it locally
3. Use the MCP server to inspect it

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Cursor MCP Guide](https://docs.cursor.com/advanced/mcp)

## Support

If you encounter issues:
1. Check the logs in Cursor's output panel
2. Test the server manually: `python django_mcp_server.py test`
3. Verify Django setup: `python manage.py check`
