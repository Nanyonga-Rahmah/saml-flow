from saml2 import BINDING_HTTP_POST
from saml2 import BINDING_HTTP_REDIRECT

CONFIG = {

    "entityid": "http://localhost:9000/idp",

    "key_file": "certs/idp.key",

    "cert_file": "certs/idp.crt",

    "service": {

        "idp": {

            "endpoints": {

                "single_sign_on_service": [

                    (
                        "http://localhost:9000/sso",
                        BINDING_HTTP_REDIRECT,
                    ),

                    (
                        "http://localhost:9000/sso",
                        BINDING_HTTP_POST,
                    ),
                ],

            },

            "policy": {

                "default": {

                    "sign_response": True,

                    "sign_assertion": True,

                }

            },

        }

    },

   "metadata": {
    "local": [
        "metadata/sp-metadata.xml"
    ]
}

}