from datetime import datetime, timezone, timedelta
from dataclasses import dataclass

"""
Models according to Stud.IP JSON:API
"""


class ModelInterface:
    @staticmethod
    def createFromResponse(json):
        pass


@dataclass
class User(ModelInterface):
    """
    Stud.IP User Model
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/users#schema
    """
    id:str
    username: str
    formattedName: str
    familyName: str
    givenName: str
    email: str

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


@dataclass
class Semester(ModelInterface):
    """
    Stud.IP Semester Model
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/semesters#schema-semesters
    """

    id: str
    title: str
    start: str
    end: str

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


@dataclass
class Course(ModelInterface):
    """
    Stud.IP Course Model
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/courses#schema-courses
    """

    id: str
    title: str
    subtitle: str
    description: str
    start_semester: str

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


@dataclass
class CourseMembership(ModelInterface):
    """
    Stud.IP Course Membership
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/courses#schema-course-memberships
    """

    id: str
    courseId: str
    userId: str
    permission: str

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


@dataclass
class FileRef(ModelInterface):
    """
    Stud.IP File-Ref Model
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/files#schema-file-refs
    """

    id: str
    name: str
    parent: str

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


@dataclass
class Folder(ModelInterface):
    """
    Stud.IP Folder Model
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/files#type-folders
    """

    id: str
    name: str
    type: str
    parent: str

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


@dataclass
class StatusGroup(ModelInterface):
    """
    Stud.IP StatusGroup
    This is currently not documented and based on reverse engineering of the source code!
    """

    id : str
    name : str

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


@dataclass
class CreateAnnouncement:
    """
    Model used for creating announcements
    """
    title: str
    content: str
    publicationStart: datetime
    publicationEnd: datetime
    commentsAllowed: bool = False

    def __post_init__(self):
        if not self.publicationStart:
            self.publicationStart = datetime.now(timezone.utc)
        if not self.publicationEnd:
            self.publicationEnd = self.publicationStart + timedelta(days=7) # 7 days is the default in the web interface

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


@dataclass
class CreateFile:
    """
    Model used for creating a new empty file and fileRef
    """


    name: str
    description: str
    license: str

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


@dataclass
class CreateMessage:
    """
    Model used for creating a new message
    @see https://docs.gitlab.studip.de/entwicklung/docs/jsonapi/messages#eine-nachricht-senden
    """

    subject: str
    body: str
    recipients: str

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
