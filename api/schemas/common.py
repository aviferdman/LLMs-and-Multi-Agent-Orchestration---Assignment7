"""Common API schemas."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    """Generic success response."""

    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Generic error response."""

    success: bool = False
    error: str
    detail: Optional[str] = None


class PaginationParams(BaseModel):
    """Pagination parameters."""

    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")


class PaginatedResponse(BaseModel):
    """Base paginated response."""

    total: int
    page: int
    page_size: int
    total_pages: int
