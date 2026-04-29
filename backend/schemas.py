from pydantic import BaseModel, Field
from typing import List, Optional

# --- DATABASE SCHEMAS ---
class ColumnSchema(BaseModel):
    name: str = Field(description="The name of the database column")
    type: str = Field(description="The data type, e.g., uuid, string, integer")
    primary_key: Optional[bool] = Field(default=False)
    relation: Optional[str] = Field(description="Foreign key relation, if any")

class TableSchema(BaseModel):
    name: str = Field(description="The name of the table")
    columns: List[ColumnSchema]

class DatabaseSchema(BaseModel):
    tables: List[TableSchema]

# --- API SCHEMAS ---
class EndpointSchema(BaseModel):
    path: str = Field(description="API endpoint path, e.g., /api/users")
    method: str = Field(description="HTTP method: GET, POST, PUT, DELETE")
    requires_auth: bool = Field(default=True)
    allowed_roles: List[str] = Field(description="Roles allowed to access this endpoint")

class APISchema(BaseModel):
    endpoints: List[EndpointSchema]

# --- UI SCHEMAS ---
class PageSchema(BaseModel):
    route: str = Field(description="The URL route, e.g., /dashboard")
    layout: str = Field(description="The layout wrapper, e.g., AdminLayout")
    components: List[str] = Field(description="List of UI components on this page")

class UISchema(BaseModel):
    pages: List[PageSchema]

# --- AUTH SCHEMAS ---
class RolePermission(BaseModel):
    role: str = Field(description="The role name, e.g., admin")
    allowed_actions: List[str] = Field(description="List of granted permissions")

class AuthSchema(BaseModel):
    roles: List[str] = Field(description="List of user roles, e.g., admin, user")
    permissions: List[RolePermission] = Field(description="Mapping of roles to permissions")

# --- THE MASTER SCHEMA ---
class AppConfiguration(BaseModel):
    app_name: str
    database: DatabaseSchema
    api: APISchema
    ui: UISchema
    auth: AuthSchema