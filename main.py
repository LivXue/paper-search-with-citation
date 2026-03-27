"""
Academic Search API - FastAPI deployment of Semantic Scholar search functionality
"""
import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

from S2_search import AcademicCitationTool


# Pydantic models for request/response validation
class PaperSearchRequest(BaseModel):
    query: str = Field(..., description="Search keywords", example="attention")
    limit: int = Field(default=3, ge=1, le=20, description="Number of results to return (1-20)")
    include_bibtex: bool = Field(default=True, description="Whether to include BibTeX citations")


class Paper(BaseModel):
    index: Optional[str] = None  # Changed to Optional[str] to support paperId
    title: str
    authors: str
    year: Optional[int]
    venue: str
    doi: Optional[str]
    citation_count: int
    is_open_access: bool
    fields_of_study: List[str]
    abstract: Optional[str] = None  # Changed to Optional to handle None values
    url: str
    bibtex: Optional[str] = None


class ManagerStatsResponse(BaseModel):
    """Response model for API manager statistics"""
    total_configs: int
    healthy_configs: int
    rate_limited_configs: int
    proxied_configs: int
    current_index: int


class SearchResponse(BaseModel):
    success: bool
    query: str
    total_results: int
    papers: List[Paper]
    message: Optional[str] = None
    api_key_used: Optional[int] = None  # Added to track which API key was used


class BibtexRequest(BaseModel):
    doi: str = Field(..., description="DOI string", example="10.1007/s10579-019-09480-1")


class BibtexResponse(BaseModel):
    success: bool
    bibtex: Optional[str] = None
    message: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    api_key_configured: bool


# Global tool instance
citation_tool: Optional[AcademicCitationTool] = None


def get_citation_tool() -> AcademicCitationTool:
    """Get or create a new citation tool instance"""
    global citation_tool
    if citation_tool is None:
        # Load from config directory by default
        citation_tool = AcademicCitationTool()
    return citation_tool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the API"""
    # Startup - ensure tool is initialized
    get_citation_tool()
    yield
    # Shutdown
    global citation_tool
    citation_tool = None


# Create FastAPI app
app = FastAPI(
    title="Academic Search API",
    description="API for searching academic papers and generating BibTeX citations using Semantic Scholar",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - welcome message"""
    return {
        "message": "Academic Search API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"], response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "api_key_configured": True  # Now always True as we load from config files
    }


@app.get("/manager/stats", tags=["Manager"], response_model=ManagerStatsResponse)
async def get_manager_stats():
    """Get API manager statistics - shows which API keys are active, rate limited, etc."""
    tool = get_citation_tool()
    stats = tool.get_manager_stats()
    return stats


@app.post("/search", tags=["Search"], response_model=SearchResponse)
async def search_papers(request: PaperSearchRequest):
    """
    Search for academic papers using Semantic Scholar API

    Args:
        request: Search request containing query, limit, and include_bibtex flag

    Returns:
        Search results with paper information and optional BibTeX citations
    """
    tool = get_citation_tool()
    result = tool.search_and_get_citations(
        query=request.query,
        limit=request.limit,
        include_bibtex=request.include_bibtex
    )

    if not result["success"]:
        # Return 200 with success: false instead of 404
        return result

    return result


@app.get("/search", tags=["Search"], response_model=SearchResponse)
async def search_papers_get(
    query: str = Query(..., description="Search keywords", example="attention"),
    limit: int = Query(default=3, ge=1, le=20, description="Number of results to return (1-20)"),
    include_bibtex: bool = Query(default=True, description="Whether to include BibTeX citations")
):
    """
    Search for academic papers (GET method)

    Args:
        query: Search keywords
        limit: Number of results to return
        include_bibtex: Whether to include BibTeX citations

    Returns:
        Search results with paper information and optional BibTeX citations
    """
    tool = get_citation_tool()
    result = tool.search_and_get_citations(
        query=query,
        limit=limit,
        include_bibtex=include_bibtex
    )

    if not result["success"]:
        # Return 200 with success: false instead of 404
        return result

    return result


@app.post("/bibtex", tags=["BibTeX"], response_model=BibtexResponse)
async def get_bibtex(request: BibtexRequest):
    """
    Get BibTeX citation for a paper using its DOI

    Args:
        request: Request containing the DOI

    Returns:
        BibTeX citation
    """
    tool = get_citation_tool()
    bibtex_result = tool.get_single_paper_bibtex(request.doi)

    if "❌" in bibtex_result:
        return {
            "success": False,
            "message": bibtex_result.replace("❌ ", "")
        }

    # Extract the BibTeX from the markdown code block
    bibtex_text = bibtex_result.replace("```bibtex\n", "").replace("\n```", "")

    return {
        "success": True,
        "bibtex": bibtex_text
    }


@app.get("/bibtex/{doi:path}", tags=["BibTeX"], response_model=BibtexResponse)
async def get_bibtex_get(doi: str):
    """
    Get BibTeX citation for a paper using its DOI (GET method)

    Args:
        doi: DOI string (e.g., 10.1007/s10579-019-09480-1)

    Returns:
        BibTeX citation
    """
    tool = get_citation_tool()
    bibtex_result = tool.get_single_paper_bibtex(doi)

    if "❌" in bibtex_result:
        return {
            "success": False,
            "message": bibtex_result.replace("❌ ", "")
        }

    # Extract the BibTeX from the markdown code block
    bibtex_text = bibtex_result.replace("```bibtex\n", "").replace("\n```", "")

    return {
        "success": True,
        "bibtex": bibtex_text
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8111,
        reload=True
    )
