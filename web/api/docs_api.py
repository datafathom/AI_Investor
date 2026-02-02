"""
API Documentation
Complete Swagger/OpenAPI documentation with interactive UI
"""

from flask import Blueprint, jsonify, send_from_directory, render_template_string
import os
from pathlib import Path

docs_bp = Blueprint('docs', __name__)

# OpenAPI/Swagger specification
OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "AI Investor API",
        "version": "1.0.0",
        "description": "Complete API documentation for the AI Investor platform",
        "contact": {
            "name": "API Support",
            "email": "support@ai-investor.com"
        },
        "license": {
            "name": "Proprietary"
        }
    },
    "servers": [
        {
            "url": os.getenv('API_BASE_URL', 'http://localhost:5050'),
            "description": "Production server"
        },
        {
            "url": "http://localhost:5050",
            "description": "Development server"
        }
    ],
    "tags": [
        {
            "name": "Authentication",
            "description": "User authentication and authorization"
        },
        {
            "name": "Portfolio",
            "description": "Portfolio management endpoints"
        },
        {
            "name": "Trading",
            "description": "Trading operations"
        },
        {
            "name": "Analytics",
            "description": "Analytics and insights"
        },
        {
            "name": "Legal",
            "description": "Legal documents and compliance"
        },
        {
            "name": "Onboarding",
            "description": "User onboarding flow"
        },
        {
            "name": "Health",
            "description": "Health check endpoints"
        },
        {
            "name": "Institutional",
            "description": "Institutional onboarding and analytics"
        },
        {
            "name": "Evolution",
            "description": "Genomic evolution and playback"
        },
        {
            "name": "Search",
            "description": "Systemic search and discovery"
        }
    ],
    "paths": {
        "/api/v1/health": {
            "get": {
                "tags": ["Health"],
                "summary": "Health check",
                "description": "Returns the health status of the API",
                "responses": {
                    "200": {
                        "description": "Healthy",
                        "content": {
                            "application/json": {
                                "example": {"status": "healthy", "version": "1.0.0"}
                            }
                        }
                    }
                }
            }
        },
        "/api/v1/legal/documents": {
            "get": {
                "tags": ["Legal"],
                "summary": "List legal documents",
                "description": "Get list of all available legal documents",
                "responses": {
                    "200": {
                        "description": "List of documents",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "name": {"type": "string"},
                                                    "version": {"type": "string"},
                                                    "effective_date": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/v1/legal/documents/{document_id}": {
            "get": {
                "tags": ["Legal"],
                "summary": "Get legal document",
                "description": "Get a specific legal document by ID",
                "parameters": [
                    {
                        "name": "document_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"},
                        "description": "Document identifier"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Document content",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "content": {"type": "string"},
                                                "version": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Document not found"
                    }
                }
            }
        },
        "/api/v1/onboarding/status": {
            "get": {
                "tags": ["Onboarding"],
                "summary": "Get onboarding status",
                "description": "Get user's onboarding completion status",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Onboarding status",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "completed": {"type": "boolean"},
                                        "current_step": {"type": "integer"},
                                        "total_steps": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/v1/onboarding/complete": {
            "post": {
                "tags": ["Onboarding"],
                "summary": "Complete onboarding",
                "description": "Mark onboarding as complete and save user preferences",
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "preferences": {
                                        "type": "object",
                                        "description": "User preferences from onboarding"
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Onboarding completed",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "message": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/v1/institutional/client/create": {
            "post": {
                "tags": ["Institutional"],
                "summary": "Create institutional client",
                "description": "Add a new institutional client to the roster",
                "responses": {
                    "201": {"description": "Client created"}
                }
            }
        },
        "/api/v1/evolution/playback": {
            "post": {
                "tags": ["Evolution"],
                "summary": "Genomic playback",
                "description": "Replay historical market data for a given genome",
                "responses": {
                    "200": {"description": "Playback results returned"}
                }
            }
        },
        "/api/v1/search/index": {
            "get": {
                "tags": ["Search"],
                "summary": "Refresh search index",
                "description": "Get latest searchable entities from Neo4j",
                "responses": {
                    "200": {"description": "Search index returned"}
                }
            }
        }
    },
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        },
        "schemas": {
            "Error": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "example": False},
                    "error": {"type": "string"},
                    "message": {"type": "string"}
                }
            },
            "Success": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "example": True},
                    "data": {"type": "object"}
                }
            }
        }
    }
}


@docs_bp.route('/api/docs', methods=['GET'])
def swagger_ui():
    """Serve Swagger UI."""
    swagger_ui_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Documentation - AI Investor</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui.css" />
        <style>
            html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
            *, *:before, *:after { box-sizing: inherit; }
            body { margin:0; background: #fafafa; }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: "/api/docs/openapi.json",
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout"
                });
            };
        </script>
    </body>
    </html>
    """
    return render_template_string(swagger_ui_html)


@docs_bp.route('/api/docs/openapi.json', methods=['GET'])
def openapi_spec():
    """Get OpenAPI specification."""
    return jsonify(OPENAPI_SPEC)


@docs_bp.route('/api/docs/redoc', methods=['GET'])
def redoc_ui():
    """Serve ReDoc UI."""
    redoc_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Documentation - AI Investor</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
            body { margin: 0; padding: 0; }
        </style>
    </head>
    <body>
        <redoc spec-url="/api/docs/openapi.json"></redoc>
        <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
    </body>
    </html>
    """
    return render_template_string(redoc_html)


@docs_bp.route('/api/docs/swagger.yaml', methods=['GET'])
def swagger_yaml():
    """Get Swagger YAML specification (converted from JSON)."""
    import yaml
    try:
        yaml_content = yaml.dump(OPENAPI_SPEC, default_flow_style=False, sort_keys=False)
        return yaml_content, 200, {'Content-Type': 'application/x-yaml'}
    except ImportError:
        return jsonify({"error": "PyYAML not installed"}), 500
