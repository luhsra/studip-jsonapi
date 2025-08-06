from datetime import datetime, timezone
from urllib.parse import urlencode
from .models import (
    User,
    Course,
    CourseMembership,
    Semester,
    FileRef,
    Folder,
    StatusGroup,
    CreateAnnouncement,
    CreateFile,
    CreateMessage,
)

class Client:
    """
    Stud.IP JSON:API client

    session: You must provide an instance of 'requests.Session'.
    This session must already be authenticated against the JSON:API.

    apiBaseUrl: URL to JSON:API endpoint, including version and without trailing slash.
    e.g., `https://studip.example.com/jsonapi.php/v1`
    """

    def __init__(self, session, apiBaseUrl):
        self.apiBaseUrl = apiBaseUrl
        self.session = session

    #
    # Stage 0: Plain HTTP requests
    #

    def _get(self, url):
        r = self.session.get(url)
        r.raise_for_status()
        return r

    def _post(self, url, headers, json):
        r = self.session.post(url, headers=headers, json=json)
        r.raise_for_status()
        return r.json()

    def _postFile(self, url, filename, content):
        files = {
            "file": content
        }  # Use a generic name and overwrite it using the 'Slug' header
        headers = {"Slug": filename}
        r = self.session.post(url, files=files, headers=headers)
        r.raise_for_status()

    #
    # Stage 1: Plain API requests, returning models. No caching.
    #

    def _apiGetSingle(self, url, obj):
        json = self._get("{base}/{path}".format(base=self.apiBaseUrl, path=url)).json()
        assert "data" in json
        return obj.createFromResponse(json["data"])

    def _apiGetCollection(self, url, obj, limit=10000, params={}):
        params.update({"page[limit]": limit})

        json = self._get(
            "{base}/{path}?{params}".format(
                base=self.apiBaseUrl, path=url, params=urlencode(params)
            )
        ).json()
        assert "data" in json
        return [obj.createFromResponse(item) for item in json["data"]]

    def _apiPost(self, url, data, respObj=None):
        """Post to a JSON:API compatible URL. Provided payload data must be JSON-encodable."""
        json = self._post(
            "{base}/{path}".format(base=self.apiBaseUrl, path=url),
            json={"data": data.toJSON()},
            headers={"Content-Type": "application/vnd.api+json"},
        )
        if respObj:
            assert "data" in json
            return respObj.createFromResponse(json["data"])

    #
    # Stage 2: Convenience API wrappers, returning models. No caching.
    #

    ## Users
    def getUsers(self):
        """
        Returns all users of the Stud.IP system that the user is permitted to see.
        Warning: This may be many, use with caution!
        """
        return self._apiGetCollection("users", User)

    def getUserById(self, userId):
        return self._apiGetSingle("users/{}".format(userId), User)

    def getUserCourses(self, userId, semesterId=None):
        """
        Returns the courses of a given user (by id) while optionally filtering
        for a given semester (by id).
        """
        return self._apiGetCollection(
            "users/{}/courses".format(userId),
            Course,
            params={"filter[semester]": semesterId} if semesterId else {},
        )

    ## Semesters
    def getSemesters(self):
        """Returns all semesters the user is permitted to see."""
        return self._apiGetCollection("semesters", Semester)

    def getSemesterById(self, semesterId):
        return self._apiGetSingle("semesters/{}".format(semesterId), Semester)

    ## Courses
    def getCourses(self):
        """Returns all courses the cuser is permitted to see."""
        return self._apiGetCollection("courses", Course)

    def getCourseById(self, cid):
        return self._apiGetSingle("courses/{}".format(cid), Course)

    def getCourseMemberships(self, cid, permission=None):
        """
        Returns memberships of a given course.
        Optionally filter by a given permission (e.g. 'tutor', 'dozent').
        """
        return self._apiGetCollection(
            "courses/{}/memberships".format(cid),
            CourseMembership,
            params={"filter[permission]": permission} if permission else {}
        )

    def hasUserPermissionInCourse(self, uid, cid, permission):
        """
        Returns true if the given user has a given permission in a given course.
        """
        for membership in self.getCourseMemberships(cid, permission):
            if membership.userId == uid:
                return True

        return False

    ## Status groups ("Teilnehmergruppen")
    def getCourseStatusGroups(self, cid):
        return self._apiGetCollection(
            "courses/{}/status-groups".format(cid), StatusGroup
        )

    ## Announcements
    def postCourseAnnouncement(self, cid, topic, body):
        """Post an announcement in a given course."""
        self._apiPost(
            "courses/{}/news".format(cid), data=CreateAnnouncement(topic, body)
        )

    ## Messages
    def postMessage(self, subject, body, recipients):
        self._apiPost("messages", data=CreateMessage(subject, body, recipients))

    ## Files & Folders
    def getUserFiles(self, uid):
        """Returns all FileRefs associated with the given user."""
        return self._apiGetCollection("users/{}/file-refs".format(uid), FileRef)

    def getCourseFiles(self, cid):
        """Retrieves all FileRefs of a course, regardless of directory structure."""
        return self._apiGetCollection("courses/{}/file-refs".format(cid), FileRef)

    def getCourseFolders(self, cid):
        """Returns all Folders in a course."""
        return self._apiGetCollection("courses/{}/folders".format(cid), Folder)

    def getFolderFiles(self, fid):
        """Returns all FileRefs in a folder (does not search in sub-directories)."""
        return self._apiGetCollection("folders/{}/file-refs".format(fid), FileRef)

    #
    # Stage 3: Methods working solely with models.
    #

    def testAuthentication(self):
        try:
            self.getOwnUser()
            return True
        except:
            return False

    def getOwnUser(self):
        return self.getUserById("me")  # Use magical 'me' user-id

    def getOwnCourses(self):
        # Since magical 'me' does not work, we have to get the real user id first
        return self.getUserCourses(self.getOwnUser().id)

    def getOwnCoursesBySemester(self, semester):
        """Returns the current user's courses in the given semester."""
        return self.getUserCourses(self.getOwnUser().id, semesterId=semester.id)

    def getOwnCourseByTitle(self, courseTitle, semester=None):
        """Find an own course by its title (exact match), while optionally filtering by semester."""
        courses = (
            self.getOwnCoursesBySemester(semester)
            if semester is not None
            else self.getOwnCourses()
        )
        for course in courses:
            if course.title == courseTitle:
                return course

        return None

    def getOwnFiles(self):
        return self.getUserFiles(self.getOwnUser().id)

    def getCurrentSemester(self):
        """Find the current semester. May return None if no semester found."""
        now = datetime.now(timezone.utc)
        for semester in self.getSemesters():
            if semester.start <= now and semester.end > now:
                return semester

        return None

    def getCourseRootFolder(self, cid):
        """Find the first folder in a course that has the 'RootFolder' type. May return None if no such folder exists."""
        for folder in self.getCourseFolders(cid):
            if folder.type == "RootFolder":
                return folder

        return None

    def findFolderInCourseByName(self, folderName, cid):
        """Find a folder in a course by name (exact match). May return None if no such folder exists."""
        for folder in self.getCourseFolders(cid):
            if folder.name == folderName:
                return folder

        return None

    def findFolderInCourseById(self, folderId, cid):
        """Find a folder in a course by id. May return None if no such folder exists."""
        for folder in self.getCourseFolders(cid):
            if folder.id == folderId:
                return folder

        return None

    def findFileInCourse(self, filename, cid):
        """Find a file by name (exact match) in a whole course. May return None if no such folder exists."""
        fileRefs = self.getCourseFiles(cid)
        for fileRef in fileRefs:
            if fileRef.name == filename:
                return fileRef

        return None

    def findFileInFolder(self, filename, folderId):
        """Find a file by name (exact match) in a given folder. May return None if no such folder exists."""
        fileRefs = self.getFolderFiles(folderId)
        for fileRef in fileRefs:
            if fileRef.name == filename:
                return fileRef

        return None

    def createFileInFolder(self, folderId, filename, description, license):
        """Create a file in a given folder. Returns a FileRef to the new file. If a file with the same name already exists, Stud.IP may generate a name with a numeric suffix."""
        return self._apiPost(
            "folders/{}/file-refs".format(folderId),
            data=CreateFile(name=filename, description=description, license=license),
            respObj=FileRef,
        )

    def updateFileContent(self, fileRef, content):
        """Updates the file referenced by fileRef with the provided binary content"""
        self._postFile(
            "{base}/file-refs/{fileId}/content".format(
                base=self.apiBaseUrl, fileId=fileRef.id
            ),
            fileRef.name,
            content,
        )

    def uploadFile(
        self,
        fileName,
        content,
        parentFolder,
        description="",
        license="FREE_LICENSE",
    ):
        # Attempt to find the target file ...
        fileRef = self.findFileInFolder(fileName, parentFolder.id)

        # ... if it does not exist yet, create it (empty)
        if not fileRef:
            fileRef = self.createFileInFolder(
                parentFolder.id, fileName, description, license
            )

        # Update content of (new or old) file
        self.updateFileContent(fileRef, content)
