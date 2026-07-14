from saml2.config import Config
from saml2.metadata import create_metadata_string

from sp_config import CONFIG

metadata = create_metadata_string(
    None,
    config=Config().load(CONFIG),
)

with open("metadata/sp-metadata.xml", "wb") as f:
    f.write(metadata)

print("Metadata generated.")