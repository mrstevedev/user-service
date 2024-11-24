from flask_jwt_extended import create_refresh_token as refresh_token

def refresh(identity, additional_claims, expires_delta):
    refresh_token_value = refresh_token(identity=identity, additional_claims=additional_claims, expires_delta=expires_delta)
    return refresh_token_value