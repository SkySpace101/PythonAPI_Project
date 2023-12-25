# A file to store all our utility function and codes and logics.
# such as hashing logics

from passlib.context import CryptContext

# creating a hashing context object and selecting a hashing algorithm which in this case is bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# a hash function
def hash(password):
    return pwd_context.hash(password)