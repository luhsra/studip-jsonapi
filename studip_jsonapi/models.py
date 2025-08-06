from datetime import datetime, timezone, timedelta

"""
Models according to Stud.IP JSON:API
"""


class ModelInterface:
    @staticmethod
    def createFromResponse(json):
        pass


class User(ModelInterface):
    """
    Stud.IP User Model
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/users#schema
    """

    def __init__(self, id, username, formattedName, familyName, givenName, email):
        self.id = id
        self.username = username
        self.formattedName = formattedName
        self.familyName = familyName
        self.givenName = givenName
        self.email = email

    @staticmethod
    def createFromResponse(json):
        assert "type" in json
        assert "users" == json["type"]

        assert "id" in json
        id = json["id"]

        assert "attributes" in json

        assert "username" in json["attributes"]
        username = json["attributes"]["username"]

        assert "formatted-name" in json["attributes"]
        formattedName = json["attributes"]["formatted-name"]

        assert "family-name" in json["attributes"]
        familyName = json["attributes"]["family-name"]

        assert "given-name" in json["attributes"]
        givenName = json["attributes"]["given-name"]

        assert "email" in json["attributes"]
        email = json["attributes"]["email"]

        return User(
            id=id,
            username=username,
            formattedName=formattedName,
            familyName=familyName,
            givenName=givenName,
            email=email,
        )


class Semester(ModelInterface):
    """
    Stud.IP Semester Model
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/semesters#schema-semesters
    """

    def __init__(self, id, title, start, end):
        self.id = id
        self.title = title
        self.start = start
        self.end = end

    @staticmethod
    def createFromResponse(json):
        assert "type" in json
        assert "semesters" == json["type"]

        assert "id" in json
        id = json["id"]

        assert "attributes" in json

        assert "title" in json["attributes"]
        title = json["attributes"]["title"]

        # assert 'description' in json['attributes']
        # description = json['attributes']['description']

        assert "start" in json["attributes"]
        start = json["attributes"]["start"]
        start = datetime.fromisoformat(start)

        assert "end" in json["attributes"]
        end = json["attributes"]["end"]
        end = datetime.fromisoformat(end)

        return Semester(
            id=id,
            title=title,
            start=start,
            end=end,
        )


class Course(ModelInterface):
    """
    Stud.IP Course Model
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/courses#schema-courses
    """

    def __init__(self, id, title, subtitle, description, start_semester):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.start_semester = start_semester

    @staticmethod
    def createFromResponse(json):
        assert "type" in json
        assert "courses" == json["type"]

        assert "id" in json
        id = json["id"]

        assert "attributes" in json

        assert "title" in json["attributes"]
        title = json["attributes"]["title"]

        assert "subtitle" in json["attributes"]
        subtitle = json["attributes"]["subtitle"]

        assert "description" in json["attributes"]
        description = json["attributes"]["description"]

        assert "relationships" in json

        assert "start-semester" in json["relationships"]
        assert "data" in json["relationships"]["start-semester"]
        assert "id" in json["relationships"]["start-semester"]["data"]
        start_semester = json["relationships"]["start-semester"]["data"]["id"]

        return Course(
            id=id,
            title=title,
            subtitle=subtitle,
            description=description,
            start_semester=start_semester,
        )


class CourseMembership(ModelInterface):
    """
    Stud.IP Course Membership
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/courses#schema-course-memberships
    """

    def __init__(self, id, courseId, userId, permission):
        self.id = id
        self.courseId = courseId
        self.userId = userId
        self.permission = permission

    @staticmethod
    def createFromResponse(json):
        assert "type" in json
        assert "course-memberships" == json["type"]

        assert "id" in json
        id = json["id"]

        assert "attributes" in json
        assert "permission" in json["attributes"]
        permission = json["attributes"]["permission"]

        assert "relationships" in json

        assert "course" in json["relationships"]
        assert "data" in json["relationships"]["course"]
        assert "id" in json["relationships"]["course"]["data"]
        courseId = json["relationships"]["course"]["data"]["id"]

        assert "user" in json["relationships"]
        assert "data" in json["relationships"]["user"]
        assert "id" in json["relationships"]["user"]["data"]
        userId = json["relationships"]["user"]["data"]["id"]

        return CourseMembership(
            id=id, courseId=courseId, userId=userId, permission=permission
        )


class FileRef(ModelInterface):
    """
    Stud.IP File-Ref Model
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/files#schema-file-refs
    """

    def __init__(self, id, name, parent):
        self.id = id
        self.name = name
        self.parent = parent

    @staticmethod
    def createFromResponse(json):
        assert "type" in json
        assert "file-refs" == json["type"]

        assert "id" in json
        id = json["id"]

        assert "attributes" in json

        assert "name" in json["attributes"]
        name = json["attributes"]["name"]

        assert "relationships" in json
        assert "parent" in json["relationships"]
        assert "data" in json["relationships"]["parent"]
        assert "type" in json["relationships"]["parent"]["data"]
        assert "folders" == json["relationships"]["parent"]["data"]["type"]
        assert "id" in json["relationships"]["parent"]["data"]
        parent = json["relationships"]["parent"]["data"]["id"]

        return FileRef(
            id=id,
            name=name,
            parent=parent,
        )


class Folder(ModelInterface):
    """
    Stud.IP Folder Model
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/files#type-folders
    """

    def __init__(self, id, name, type, parent):
        self.id = id
        self.name = name
        self.type = type
        self.parent = parent

    @staticmethod
    def createFromResponse(json):
        assert "type" in json
        assert "folders" == json["type"]

        assert "id" in json
        id = json["id"]

        assert "attributes" in json

        assert "name" in json["attributes"]
        name = json["attributes"]["name"]

        assert "folder-type" in json["attributes"]
        type = json["attributes"]["folder-type"]

        assert "relationships" in json

        # For the root folder, there is no parent in the response
        parent = None
        if "parent" in json["relationships"]:
            assert "parent" in json["relationships"]
            assert "data" in json["relationships"]["parent"]
            assert "type" in json["relationships"]["parent"]["data"]
            assert "folders" == json["relationships"]["parent"]["data"]["type"]
            assert "id" in json["relationships"]["parent"]["data"]
            parent = json["relationships"]["parent"]["data"]["id"]

        return Folder(
            id=id,
            name=name,
            type=type,
            parent=parent,
        )


class StatusGroup(ModelInterface):
    """
    Stud.IP StatusGroup
    This is currently not documented and based on reverse engineering of the source code!
    """

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def createFromResponse(json):
        assert "type" in json
        assert "status-groups" == json["type"]

        assert "id" in json
        id = json["id"]

        assert "attributes" in json

        assert "name" in json["attributes"]
        name = json["attributes"]["name"]

        return StatusGroup(
            id=id,
            name=name,
        )


class CreateAnnouncement:
    """
    Model used for creating announcements
    """

    def __init__(
        self,
        title,
        content,
        publicationStart=None,
        publicationEnd=None,
        commentsAllowed=False,
    ):
        self.title = title
        self.content = content
        self.publicationStart = publicationStart or datetime.now(timezone.utc)
        self.publicationEnd = publicationEnd or self.publicationStart + timedelta(
            days=7
        )
        self.commentsAllowed = commentsAllowed

    def toJSON(self):
        return {
            "type": "news",
            "attributes": {
                "title": self.title,
                "content": self.content,
                "publication-start": self.publicationStart.isoformat(),
                "publication-end": self.publicationEnd.isoformat(),
                "comments-allowed": self.commentsAllowed,
            },
        }


class CreateFile:
    """
    Model used for creating a new empty file and fileRef
    """

    def __init__(self, name, description, license):
        self.name = name
        self.description = description
        self.license = license

    def toJSON(self):
        return {
            "type": "file-refs",
            "attributes": {
                "name": self.name,
                "description": self.description,
            },
            "relationships": {
                "terms-of-use": {
                    "data": {
                        "type": "terms-of-use",
                        "id": self.license,
                    }
                }
            },
        }


class CreateMessage:
    """
    Model used for creating a new message
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/messages#eine-nachricht-senden
    """

    def __init__(self, subject, body, recipients):
        self.subject = subject
        self.body = body
        self.recipients = recipients

    def toJSON(self):
        return {
            "type": "messages",
            "attributes": {
                "subject": self.subject,
                "message": self.body,
                "priority": "normal",
            },
            "relationships": {
                "recipients": {
                    "data": [
                        {
                            "type": "users",
                            "id": recipient,
                        }
                    ]
                    for recipient in self.recipients
                }
            },
        }
