# Stud.IP JSON:API Client for Python

## Authentication

Authentication against your Stud.IP server is out of scope for this client, it is your task to provide an authenticated instance of `requests.Session`. See the following examples.

The Stud.IP JSON:API currently supports three kinds of authentication:
 - HTTP Basic Auth
 - Session Cookie and
 - OAuth2 Access Token

See https://docs.gitlab.studip.de/entwicklung/docs/jsonapi

### Example: Session Cookie

```python
from requests import Session
session = Session()
session.cookies.set("Studip_Session", "12399c380813a65084a45c6b06f29692")

from studip_jsonapi.client import Client
client = Client(session=session, apiBaseUrl="https://example.com/jsonapi.php/v1")
print(client.getOwnUser().formattedName)
# Testaccount Dozent
```

### Example: HTTP Basic Auth

```python
from requests import Session
import base64
session = Session()

token = base64.b64encode(
    "{username}:{password}".format(
        username="test_dozent", password="testing"
    ).encode("utf-8")
).decode("ascii")
session.headers.update({"Authorization": "Basic {token}".format(token=token)})

from studip_jsonapi.client import Client
client = Client(session=session, apiBaseUrl="https://example.com/jsonapi.php/v1")
print(client.getOwnUser().formattedName)
# Testaccount Dozent
```
