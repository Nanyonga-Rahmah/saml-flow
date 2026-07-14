from saml2 import BINDING_HTTP_POST

CONFIG = {
    "entityid": "http://localhost:8000/metadata",

    "service": {
        "sp": {
            "endpoints": {
                "assertion_consumer_service": [
                    (
                        "http://localhost:8000/acs",
                        BINDING_HTTP_POST,
                    )
                ]
            },

            "allow_unsolicited": True,

            "want_assertions_signed": True,

            "authn_requests_signed": False,
        }
    },

    "key_file": "certs/sp.key",
    "cert_file": "certs/sp.crt",

    "metadata": {
    "local": [
        "metadata/idp-metadata.xml"
    ]
},

    "debug": 1,
}