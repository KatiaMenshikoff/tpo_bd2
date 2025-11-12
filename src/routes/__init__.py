from .clients import router as clients_router
from .policies import router as policies_router
from .claims import router as claims_router
from .queries import router as queries_router

__all__ = ["clients_router", "policies_router", "claims_router", "queries_router"]
