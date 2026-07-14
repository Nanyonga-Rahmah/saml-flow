# Mock SAML Authentication Flow

## Overview

This project demonstrates a complete **SAML 2.0 authentication flow** by implementing both a **Service Provider (SP)** and an **Identity Provider (IdP)** using **PySAML2** and **Flask**.

The objective is to understand how SAML authentication works internally before introducing an identity broker such as **SATOSA**.



---

# Architecture

```text
                    Browser
                       │
                       │
               GET /login
                       │
                       ▼
              Service Provider (SP)
                       │
        Generate AuthnRequest
                       │
             HTTP Redirect
                       ▼
            Identity Provider (IdP)
                       │
            Parse AuthnRequest
                       │
          Present Login Page
                       │
        User enters credentials
                       │
      Authenticate against users
                       │
        Create SAML Response
                       │
      HTTP POST (Auto-submit Form)
                       ▼
        Assertion Consumer Service
               (SP /acs)
                       │
        Validate SAML Response
                       │
       Extract User Attributes
                       │
                  User Logged In
```

---

# Technologies Used

- Python 3
- Flask
- PySAML2
- XML Security
- SAML 2.0

---

# Components

## Service Provider (SP)

The Service Provider is the application requesting authentication.

### Responsibilities

- Generate SAML Authentication Requests
- Redirect users to the Identity Provider
- Receive SAML Responses
- Validate SAML Assertions
- Extract authenticated user attributes

### Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Home page |
| `/login` | Generates an AuthnRequest and redirects the browser to the IdP |
| `/acs` | Assertion Consumer Service. Receives and validates the SAML Response |


---

## Identity Provider (IdP)

The Identity Provider authenticates users and issues SAML Responses.

### Responsibilities

- Receive Authentication Requests
- Authenticate users
- Generate signed SAML Responses
- Return SAML Responses to the Service Provider

### Endpoints

| Endpoint | Description |
|----------|-------------|
| `/metadata` | Returns IdP metadata |
| `/sso` | Receives the AuthnRequest and displays the login page |
| `/login` | Authenticates the user and generates the SAML Response |

---

# Authentication Flow

## Step 1 - User accesses the Service Provider

The user visits:

```http
GET /login
```

The Service Provider generates a **SAML AuthnRequest**.

---

## Step 2 - Browser is redirected to the Identity Provider

```http
GET /sso?SAMLRequest=...&RelayState=...
```

The Identity Provider:

- Parses the AuthnRequest
- Determines which Service Provider initiated the request
- Stores request information in the session
- Displays the login page

---

## Step 3 - User authenticates

The user enters credentials.

Example:

```text
Username: rahmah
Password: password123
```

The browser submits:

```http
POST /login
```

---

## Step 4 - Identity Provider authenticates the user

Authentication is performed against an in-memory user store.

Example:

```python
USERS = {
    "rahmah": {
        "password": "password123",
        "givenName": "Rahmah",
        "sn": "Nanyonga",
        "mail": "rahmah@example.com",
    }
}
```

If authentication fails:

- No SAML Response is created.
- The login page is redisplayed with an error.

If authentication succeeds:

- User attributes are loaded from the user store.

---

## Step 5 - Generate the SAML Response

The Identity Provider creates a signed SAML Response containing:

- Given Name
- Surname
- Email
- NameID
- Authentication Statement

The response is wrapped inside an HTML form using the **HTTP POST Binding**.

The browser automatically submits the form to the Service Provider.

---

## Step 6 - Service Provider validates the response

The browser sends:

```http
POST /acs
```

The Service Provider:

- Validates the SAML Response
- Verifies signatures
- Confirms the request ID
- Extracts user attributes
- Authenticates the user

---

# Understanding the AuthnRequest

The Service Provider sends an Authentication Request containing information such as:

- Request ID
- Service Provider Entity ID
- Assertion Consumer Service (ACS) URL
- Identity Provider SSO URL
- Protocol Binding
- NameID Policy
- RelayState

The AuthnRequest **does not contain user credentials**.

Its purpose is simply to request authentication from the Identity Provider.

---

# Understanding the SAML Response

After successful authentication, the Identity Provider generates a SAML Response containing:

- Authentication status
- NameID
- User attributes
- Digital signatures
- `InResponseTo` reference to the original AuthnRequest

The Service Provider validates this response before granting access.

---



### Successful authentication

```text
Username exists
Password matches
```

### Failed authentication

```text
Unknown user
```

or

```text
Incorrect password
```

In both failure cases, **no SAML Response is generated**.

---

# Browser Flow

One important lesson from this project is that the browser drives the communication between the SP and IdP.

```text
User
 │
 ▼
GET /login
 │
 ▼
SP creates AuthnRequest
 │
 ▼
302 Redirect
 │
 ▼
GET /sso
 │
 ▼
IdP Login Page
 │
 ▼
POST /login
 │
 ▼
IdP creates SAML Response
 │
 ▼
Auto-submitting HTML Form
 │
 ▼
POST /acs
 │
 ▼
SP validates response
 │
 ▼
User authenticated
```

Neither the SP nor the IdP directly calls each other's functions. Instead, the browser follows redirects, displays pages, submits forms, and carries the SAML messages between the two systems.

---

# Project Structure

```text
project/

├── sp/
│   ├── app.py
│   ├── sp_config.py
│   ├── metadata/
│   ├── certificates/
│  
│
├── idp/
│   ├── app.py
│   ├── idp_config.py
│   ├── metadata/
│   ├── certificates/
│   └── templates/
│
└── README.md
```

---

# Lessons Learned

This project provided hands-on experience with:

- SAML 2.0 authentication
- Service Providers (SP)
- Identity Providers (IdP)
- Metadata generation
- AuthnRequest creation
- SAML Response generation
- Assertion Consumer Service (ACS)
- HTTP Redirect Binding
- HTTP POST Binding
- RelayState
- NameID
- User attributes
- XML signatures
- Certificates
- Browser-mediated authentication


---

# Current Status

-  Implemented a custom Service Provider
-  Implemented a custom Identity Provider
-  Generated SP and IdP metadata
-  Generated certificates
-  Implemented SP-initiated authentication
-  Implemented a mock user authentication mechanism
-  Generated signed SAML Responses
-  Implemented the Assertion Consumer Service (ACS)
-  Successfully completed an end-to-end SAML authentication flow using Flask and PySAML2

---

# Next Steps

The next phase is to introduce **SATOSA** into the authentication flow.

Current architecture:

```text
SP
 │
 ▼
IdP
```

Target architecture:

```text
SP
 │
 ▼
SATOSA
 │
 ▼
IdP
```

SATOSA will act as an identity broker, receiving authentication requests from the Service Provider, forwarding them to the backend Identity Provider, optionally transforming user attributes, and issuing a new SAML Response back to the Service Provider.