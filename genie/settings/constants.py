########
# TIME #
########
SECONDS = 1
MINUTES = 60 * SECONDS
HOURS = 60 * MINUTES
DAYS = 24 * HOURS

############
# BACKENDS #
############
# AUTHORIZATION
STATIC_AUTHORIZATION_BACKEND = (
    'genie.contrib.auth.backends.static.StaticAuthenticationBackend'
)

SQLITE_DATABASE_BACKEND = (
    'genie.models.database.sqlite.backend.SqliteDatabaseBackend'
)

FAKE_SUCCESS_CATALOG_BACKEND = (
    'genie.extensions.fake.backends.catalog.FakeSuccessCatalogBackend'
)

FAKE_ERROR_CATALOG_BACKEND = (
    'genie.extensions.fake.backends.catalog.FakeErrorCatalogBackend'
)
