from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyQuery
from titiler.core.factory import TilerFactory

from ..auth import init_aws_session

init_aws_session()


api_key_query = APIKeyQuery(name="access_token", auto_error=False)


def token_validation(access_token: str = Security(api_key_query)):
    """Token validation."""
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing `access_token`")

    if not access_token == "token":
        raise HTTPException(status_code=401, detail="Invalid `access_token`")

    return True


private_router = APIRouter(dependencies=[Depends(token_validation)])
private_cog = TilerFactory(router_prefix="private/cog", router=private_router)

router = private_cog.router
