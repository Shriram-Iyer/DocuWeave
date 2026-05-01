"""
DocuWeave FastAPI application factory.
"""
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from docuweave.config import settings
from docuweave.infrastructure.template_db_factory import close_template_db, init_template_db
from docuweave.adapters.http.routers.health import router as health_router
from docuweave.adapters.http.routers.transformations import router as transformations_router
from docuweave.adapters.http.routers.templates import router as templates_router
from docuweave.adapters.http.routers.data_sources import router as data_sources_router
from docuweave.adapters.http.routers.selectors import router as selectors_router
from docuweave.adapters.http.routers.documents import router as documents_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_template_db()
    yield
    await close_template_db()


def create_app() -> FastAPI:
    app = FastAPI(
        title="DocuWeave API",
        description="Backend-driven document generation platform",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(transformations_router)
    app.include_router(templates_router)
    app.include_router(data_sources_router)
    app.include_router(selectors_router)
    app.include_router(documents_router)

    return app


app = create_app()
