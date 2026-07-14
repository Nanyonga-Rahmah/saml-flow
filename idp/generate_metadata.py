from saml2.config import IdPConfig
from saml2.metadata import create_metadata_string

from idp_config import CONFIG

metadata = create_metadata_string(
    None,
    config=IdPConfig().load(CONFIG),
)

with open("metadata/idp-metadata.xml", "wb") as f:
    f.write(metadata)