from enum import Enum


class PlanType(str, Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class DatabaseType(str,Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    SQLSERVER = "sqlserver"
class UserRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class AgentType(str, Enum):
    SUPPORT = "support"
    SALES = "sales"
    ASSISTANT = "assistant"
    


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class FilterOperator(str,Enum):
    EQ = "eq"
    CONTAINS = "contains"
    LT = "lt"
    GT = "gt"
    LTE = "lte"
    GTE = "gte"