from pydantic import BaseModel

class BaseEmailDTO(BaseModel):
    user_id: int

class EmailResetPasswordDTO(BaseEmailDTO):
    reset_password_url: str

class EmailWelcomeDTO(BaseEmailDTO):
    email: str