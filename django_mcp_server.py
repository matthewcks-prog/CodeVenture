#!/usr/bin/env python
"""
Django MCP Server for Debugging
Provides tools to inspect and debug Django applications through MCP
"""
import os
import sys
import json
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodeVenture.settings')
django.setup()

from django.core.management import call_command
from django.apps import apps
from django.db import connection
from io import StringIO


class DjangoMCPServer:
    """MCP Server for Django debugging and inspection"""
    
    def __init__(self):
        self.name = "django-debug"
        self.version = "1.0.0"
    
    def list_tools(self):
        """List available MCP tools"""
        return [
            {
                "name": "django_models_list",
                "description": "List all Django models in the project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "app_label": {
                            "type": "string",
                            "description": "Optional: Filter by app label"
                        }
                    }
                }
            },
            {
                "name": "django_model_inspect",
                "description": "Inspect a specific Django model (fields, methods, etc.)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "app_label": {
                            "type": "string",
                            "description": "App label (e.g., 'auth')"
                        },
                        "model_name": {
                            "type": "string",
                            "description": "Model name (e.g., 'User')"
                        }
                    },
                    "required": ["app_label", "model_name"]
                }
            },
            {
                "name": "django_query",
                "description": "Query a Django model using ORM",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "app_label": {
                            "type": "string",
                            "description": "App label"
                        },
                        "model_name": {
                            "type": "string",
                            "description": "Model name"
                        },
                        "filter": {
                            "type": "object",
                            "description": "Filter parameters (e.g., {'username': 'admin'})"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Limit number of results",
                            "default": 10
                        }
                    },
                    "required": ["app_label", "model_name"]
                }
            },
            {
                "name": "django_sql_query",
                "description": "Execute a raw SQL query (read-only)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "SQL query to execute"
                        }
                    },
                    "required": ["sql"]
                }
            },
            {
                "name": "django_management_command",
                "description": "Run a Django management command",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Command name (e.g., 'showmigrations')"
                        },
                        "args": {
                            "type": "array",
                            "description": "Command arguments",
                            "items": {"type": "string"}
                        },
                        "options": {
                            "type": "object",
                            "description": "Command options"
                        }
                    },
                    "required": ["command"]
                }
            },
            {
                "name": "django_settings_inspect",
                "description": "Inspect Django settings (sanitized)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "setting_name": {
                            "type": "string",
                            "description": "Optional: specific setting to inspect"
                        }
                    }
                }
            },
            {
                "name": "django_urls_list",
                "description": "List all URL patterns in the project",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "django_migrations_status",
                "description": "Check migration status for all apps",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "app_label": {
                            "type": "string",
                            "description": "Optional: Filter by app label"
                        }
                    }
                }
            }
        ]
    
    def handle_tool_call(self, tool_name, arguments):
        """Handle tool calls"""
        try:
            if tool_name == "django_models_list":
                return self.list_models(arguments.get("app_label"))
            elif tool_name == "django_model_inspect":
                return self.inspect_model(arguments["app_label"], arguments["model_name"])
            elif tool_name == "django_query":
                return self.query_model(
                    arguments["app_label"],
                    arguments["model_name"],
                    arguments.get("filter", {}),
                    arguments.get("limit", 10)
                )
            elif tool_name == "django_sql_query":
                return self.execute_sql(arguments["sql"])
            elif tool_name == "django_management_command":
                return self.run_management_command(
                    arguments["command"],
                    arguments.get("args", []),
                    arguments.get("options", {})
                )
            elif tool_name == "django_settings_inspect":
                return self.inspect_settings(arguments.get("setting_name"))
            elif tool_name == "django_urls_list":
                return self.list_urls()
            elif tool_name == "django_migrations_status":
                return self.check_migrations(arguments.get("app_label"))
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"error": str(e), "type": type(e).__name__}
    
    def list_models(self, app_label=None):
        """List all Django models"""
        models = []
        for model in apps.get_models():
            if app_label and model._meta.app_label != app_label:
                continue
            models.append({
                "app_label": model._meta.app_label,
                "model_name": model.__name__,
                "table_name": model._meta.db_table,
                "verbose_name": str(model._meta.verbose_name),
            })
        return {"models": models, "count": len(models)}
    
    def inspect_model(self, app_label, model_name):
        """Inspect a specific model"""
        model = apps.get_model(app_label, model_name)
        
        fields = []
        for field in model._meta.get_fields():
            field_info = {
                "name": field.name,
                "type": field.__class__.__name__,
            }
            if hasattr(field, "max_length"):
                field_info["max_length"] = field.max_length
            if hasattr(field, "null"):
                field_info["null"] = field.null
            if hasattr(field, "blank"):
                field_info["blank"] = field.blank
            if hasattr(field, "related_model") and field.related_model:
                field_info["related_model"] = field.related_model.__name__
            fields.append(field_info)
        
        return {
            "app_label": model._meta.app_label,
            "model_name": model.__name__,
            "table_name": model._meta.db_table,
            "verbose_name": str(model._meta.verbose_name),
            "fields": fields,
            "object_count": model.objects.count()
        }
    
    def query_model(self, app_label, model_name, filter_params, limit):
        """Query a model"""
        model = apps.get_model(app_label, model_name)
        queryset = model.objects.all()
        
        if filter_params:
            queryset = queryset.filter(**filter_params)
        
        queryset = queryset[:limit]
        
        results = []
        for obj in queryset:
            obj_dict = {}
            for field in model._meta.get_fields():
                if hasattr(field, "get_attname"):
                    try:
                        value = getattr(obj, field.name)
                        # Convert to serializable format
                        if hasattr(value, "isoformat"):
                            value = value.isoformat()
                        elif hasattr(value, "__str__"):
                            value = str(value)
                        obj_dict[field.name] = value
                    except:
                        pass
            results.append(obj_dict)
        
        return {
            "results": results,
            "count": len(results),
            "total": model.objects.count()
        }
    
    def execute_sql(self, sql):
        """Execute raw SQL query"""
        # Safety check - only allow SELECT queries
        if not sql.strip().upper().startswith("SELECT"):
            return {"error": "Only SELECT queries are allowed"}
        
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
        
        return {
            "results": results,
            "count": len(results),
            "columns": columns
        }
    
    def run_management_command(self, command, args, options):
        """Run a Django management command"""
        output = StringIO()
        try:
            call_command(command, *args, stdout=output, stderr=output, **options)
            return {
                "success": True,
                "output": output.getvalue()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": output.getvalue()
            }
    
    def inspect_settings(self, setting_name=None):
        """Inspect Django settings (sanitized)"""
        from django.conf import settings
        
        # List of settings to sanitize
        sensitive_settings = [
            "SECRET_KEY", "PASSWORD", "API_KEY", "TOKEN", 
            "AWS_SECRET", "DATABASE_URL"
        ]
        
        if setting_name:
            if hasattr(settings, setting_name):
                value = getattr(settings, setting_name)
                # Sanitize sensitive values
                if any(s in setting_name.upper() for s in sensitive_settings):
                    value = "***REDACTED***"
                return {setting_name: value}
            else:
                return {"error": f"Setting '{setting_name}' not found"}
        
        # Return common settings
        common_settings = [
            "DEBUG", "ALLOWED_HOSTS", "INSTALLED_APPS", "MIDDLEWARE",
            "DATABASES", "STATIC_URL", "STATIC_ROOT", "MEDIA_URL",
            "LANGUAGE_CODE", "TIME_ZONE", "USE_TZ"
        ]
        
        result = {}
        for setting in common_settings:
            if hasattr(settings, setting):
                value = getattr(settings, setting)
                # Sanitize database URLs
                if setting == "DATABASES" and isinstance(value, dict):
                    value = {k: {**v, "PASSWORD": "***"} if "PASSWORD" in v else v 
                            for k, v in value.items()}
                result[setting] = value
        
        return result
    
    def list_urls(self):
        """List all URL patterns"""
        from django.urls import get_resolver
        
        def extract_urls(urlpatterns, prefix=""):
            urls = []
            for pattern in urlpatterns:
                pattern_str = str(pattern.pattern)
                full_path = prefix + pattern_str
                
                if hasattr(pattern, "url_patterns"):
                    # It's an included URLconf
                    urls.extend(extract_urls(pattern.url_patterns, full_path))
                else:
                    # It's a URL pattern
                    urls.append({
                        "path": full_path,
                        "name": getattr(pattern, "name", None),
                        "view": str(pattern.callback) if hasattr(pattern, "callback") else None
                    })
            return urls
        
        resolver = get_resolver()
        urls = extract_urls(resolver.url_patterns)
        return {"urls": urls, "count": len(urls)}
    
    def check_migrations(self, app_label=None):
        """Check migration status"""
        output = StringIO()
        args = [app_label] if app_label else []
        call_command("showmigrations", *args, stdout=output, verbosity=2)
        
        return {
            "output": output.getvalue(),
            "app_label": app_label
        }


def main():
    """Main entry point for the MCP server"""
    server = DjangoMCPServer()
    
    # Simple CLI for testing
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "list-tools":
            print(json.dumps(server.list_tools(), indent=2))
        elif command == "test":
            # Test the server
            print("Testing Django MCP Server...")
            print("\n1. Listing models:")
            result = server.handle_tool_call("django_models_list", {})
            print(json.dumps(result, indent=2))
            
            print("\n2. Checking migrations:")
            result = server.handle_tool_call("django_migrations_status", {})
            print(result["output"])
            
            print("\n3. Listing URLs:")
            result = server.handle_tool_call("django_urls_list", {})
            print(f"Found {result['count']} URLs")
            
            print("\n[SUCCESS] Django MCP Server is working!")
    else:
        print("Django MCP Server")
        print("Usage:")
        print("  python django_mcp_server.py list-tools  - List available tools")
        print("  python django_mcp_server.py test        - Test the server")


if __name__ == "__main__":
    main()
