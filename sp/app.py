import base64
import urllib.parse
import zlib

from flask import Flask, jsonify, redirect,request,render_template
from saml2 import BINDING_HTTP_POST
from saml2.client import Saml2Client
from saml2.config import Config

from sp_config import CONFIG

app = Flask(__name__)

# Create the SAML Service Provider client
sp_client = Saml2Client(config=Config().load(CONFIG))

# Keep track of authentication requests
outstanding_queries = {}


@app.route("/")
def home():
     
  return render_template("home.html")
    


@app.route("/login")
def login():

    # This must match the entityID of your IdP
    idp_entityid = "http://localhost:9000/idp"

    request_id, binding, http_info = (
        sp_client.prepare_for_negotiated_authenticate(
            entity_id=idp_entityid,
            relay_state="hello123",
        )
    )

    outstanding_queries[request_id] = "/"

    headers = dict(http_info["headers"])

   
  
    return redirect(headers["Location"])

   







@app.route("/acs", methods=["POST"])
def acs():
    """
    Assertion Consumer Service (ACS)

    Receives the SAML Response from the IdP,
    validates it,
    extracts the authenticated user's attributes.
    """

    # Get the SAMLResponse from the HTML form
    saml_response = request.form.get("SAMLResponse")


    if saml_response is None:
        return "No SAMLResponse received.", 400

    # RelayState is optional but usually present
    relay_state = request.form.get("RelayState")

    try:
        # Validate and parse the response
        authn_response = sp_client.parse_authn_request_response(
            saml_response,
            BINDING_HTTP_POST,
            outstanding_queries,
        )

    except Exception as e:
        return f"""
        <h2>SAML Validation Failed</h2>

        <pre>{e}</pre>
        """, 400

    # Extract user attributes
    attributes = authn_response.ava

    # NameID (unique identifier for the user)
    name_id = None
    if authn_response.name_id:
        name_id = authn_response.name_id.text

    # Remove the outstanding request
    in_response_to = authn_response.in_response_to

    if in_response_to in outstanding_queries:
        del outstanding_queries[in_response_to]

    return jsonify(
        {
            "status": "Authentication successful",
            "relay_state": relay_state,
            "name_id": name_id,
            "attributes": attributes,
        }
    )


@app.route("/metadata")
def metadata():

    with open("metadata/sp-metadata.xml") as f:
        xml = f.read()

    return xml, 200, {"Content-Type": "application/xml"}


if __name__ == "__main__":
    app.run(debug=True, port=8000)
