# Checking authorized roles for a user
from asyncio.log import logger
from typing import List
from fastapi import Depends, HTTPException, status
from . import Oauth2, models, schemas



class RoleChecker():
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles
        
    def __call__(self, user: models.Admin = Depends(Oauth2.get_current_user)):
        if user.role not in self.allowed_roles:
            logger.debug(f"User with role {user.role} is not in the allowed roles: {self.allowed_roles}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail="Operation not permitted, You are not authorized to perform this operation")