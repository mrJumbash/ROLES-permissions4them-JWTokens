ADMIN = 1
TENANT = 2
BUYER = 3

ROLE_CHOICES = ((ADMIN, "admin"), (TENANT, "tenant"), (BUYER, "buyer"))

AUTH_PROVIDERS = {
    "email": "email",
    "google": "google",
}
