from flask_jwt_extended import create_access_token

def access_token(identity, additional_claims, expires_delta):
    token = create_access_token(identity=identity, additional_claims=additional_claims, expires_delta=expires_delta)
    return token