import unittest
from unittest.mock import Mock, patch
from external.exams import Exams
from external.users import Users
from notifications.NotificationManager import NotificationManager
from persistence.postgre import DB
from service.Course import CourseService
from exceptions.CourseException import *
from validator.CourseValidator import CourseValidator
from requests import HTTPError
FAKE_COURSE_ID = 96
FAKE_CREATOR = 69
FAKE_USER_ID = 1


class TestCourses(unittest.TestCase):
    def _getMock(self, classToMock, attributes=None):
        if attributes is None:
            attributes = {}
        mock = Mock(spec=classToMock)
        mock.configure_mock(**attributes)
        return mock

    def testAddCourseWorksCorrectly(self):
        attrsValidator = {'hasACourseWithTheSameName.return_value': False}
        mockValidator = self._getMock(CourseValidator, attrsValidator)
        mockDB = self._getMock(DB)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        courseInfo = {"name": "FakeCourse", "user_id": FAKE_CREATOR}
        service.addCourse(courseInfo)
        mockValidator.hasACourseWithTheSameName.assert_called_once()
        mockValidator.hasACourseWithTheSameName.assert_called_with(courseInfo["name"], courseInfo["user_id"])
        mockDB.addCourse.assert_called_once_with(courseInfo)

    def testAddCourseRaiseExceptionIfCourseNameIsRepeated(self):
        attrsValidator = {'hasACourseWithTheSameName.return_value': True}
        mockValidator = self._getMock(CourseValidator, attrsValidator)
        mockDB = self._getMock(DB)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        courseInfo = {"name": "FakeCourse", "user_id": FAKE_CREATOR}
        with self.assertRaises(CourseAlreadyExists):
            service.addCourse(courseInfo)
        mockValidator.hasACourseWithTheSameName.assert_called_once()
        mockValidator.hasACourseWithTheSameName.assert_called_with(courseInfo["name"], courseInfo["user_id"])
        mockDB.addCourse.assert_not_called()

    def testGetCourseRaiseExceptionIfCourseDoesNotExist(self):
        mockValidator = self._getMock(CourseValidator)
        attr = {'getCourse.return_value': None}
        mockDB = self._getMock(DB, attr)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        with self.assertRaises(CourseDoesNotExist):
            service.getCourse(FAKE_COURSE_ID, FAKE_CREATOR)
        mockValidator.canViewCourse.assert_not_called()
        mockDB.getCourse.assert_called_once_with(FAKE_COURSE_ID)

    @patch('service.Course.CourseService._getUsersData')
    def testGetCourseRaiseExceptionIfUserCanNotViewCourse(self, mockGetUsersData):
        mockGetUsersData.return_value = {FAKE_CREATOR: "FakeUserData"}
        attrValidator = {'canViewCourse.return_value': False}
        mockValidator = self._getMock(CourseValidator, attrValidator)
        attrDB = {'getCourse.return_value': {"creator_id": FAKE_CREATOR}}
        mockDB = self._getMock(DB, attrDB)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        with self.assertRaises(CourseDoesNotExist):
            service.getCourse(FAKE_COURSE_ID, FAKE_CREATOR)
        mockValidator.canViewCourse.assert_called_once_with({"creator_id": FAKE_CREATOR}, "FakeUserData")
        mockGetUsersData.assert_called_once_with([{"creator_id": FAKE_CREATOR}], FAKE_CREATOR)
        mockDB.getCourse.assert_called_once_with(FAKE_COURSE_ID)

    @patch('service.Course.CourseService._getUsersData')
    @patch('service.Course.CourseService._addExtraData')
    def testGetCourseWorksCorrectly(self, mockAddExtraData, mockGetUsersData):
        fakeCourseData = {"creator_id": FAKE_CREATOR, "id": FAKE_COURSE_ID}
        mockGetUsersData.return_value = {FAKE_CREATOR: "FakeUserData"}
        mockAddExtraData.return_value = None
        attrValidator = {'canViewCourse.return_value': True}
        mockValidator = self._getMock(CourseValidator, attrValidator)
        attrDB = {'getCourse.return_value': fakeCourseData}
        mockDB = self._getMock(DB, attrDB)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        self.assertEqual(service.getCourse(FAKE_COURSE_ID, FAKE_CREATOR), fakeCourseData)
        mockValidator.canViewCourse.assert_called_once_with(fakeCourseData, "FakeUserData")
        mockDB.getCourse.assert_called_once_with(FAKE_COURSE_ID)
        mockAddExtraData.assert_called_once()
        mockGetUsersData.assert_called_once_with([fakeCourseData], FAKE_CREATOR)

    @patch('service.Course.CourseService._filterCourses')
    def testGetCoursesWorksCorrectly(self, mockFilterCourses):
        fakeCourseData = [{"creator_id": FAKE_CREATOR, "id": FAKE_COURSE_ID}]
        mockFilterCourses.return_value = fakeCourseData
        attrDB = {'getCourses.return_value': fakeCourseData}
        mockDB = self._getMock(DB, attrDB)
        service = CourseService(mockDB, Mock(), Mock(), Mock(), Mock())
        self.assertEqual(service.getCourses(FAKE_USER_ID, {"fake": "filter"}), fakeCourseData)
        mockDB.getCourses.assert_called_once_with({"fake": "filter"})
        mockFilterCourses.assert_called_once_with(fakeCourseData, FAKE_USER_ID, {"fake": "filter"})

    def testCancelCourseRaiseExceptionIfCourseDoesNotExist(self):
        attrs = {'raiseExceptionIfCourseDoesNotExists.side_effect': CourseDoesNotExist()}
        mockValidator = self._getMock(CourseValidator, attrs)
        mockDB = self._getMock(DB)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        with self.assertRaises(CourseDoesNotExist):
            service.cancelCourse(FAKE_COURSE_ID, FAKE_CREATOR)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfIsNotTheCourseCreator.assert_not_called()
        mockDB.cancelCourse.assert_not_called()

    def testCancelCourseRaiseInvalidUserActionIfIsNotTheCourseCreator(self):
        attrs = {'raiseExceptionIfIsNotTheCourseCreator.side_effect': InvalidUserAction()}
        mockValidator = self._getMock(CourseValidator, attrs)
        mockDB = self._getMock(DB)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        with self.assertRaises(InvalidUserAction):
            service.cancelCourse(FAKE_COURSE_ID, FAKE_USER_ID)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfIsNotTheCourseCreator.assert_called_once_with(FAKE_COURSE_ID, FAKE_USER_ID)
        mockDB.cancelCourse.assert_not_called()

    def testCancelCourseWorksCorrectly(self):
        mockValidator = self._getMock(CourseValidator)
        mockDB = self._getMock(DB)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        service.cancelCourse(FAKE_COURSE_ID, FAKE_USER_ID)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfIsNotTheCourseCreator.assert_called_once_with(FAKE_COURSE_ID, FAKE_USER_ID)
        mockDB.cancelCourse.assert_called_once_with(FAKE_COURSE_ID)

    def testEditCourseRaiseExceptionIfCourseDoesNotExist(self):
        courseNewInfo = {
            "id": FAKE_COURSE_ID,
            "user_id": FAKE_USER_ID,
            "name": "FakeCourse"
        }
        attrs = {'raiseExceptionIfCourseDoesNotExists.side_effect': CourseDoesNotExist()}
        mockValidator = self._getMock(CourseValidator, attrs)
        mockDB = self._getMock(DB)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        with self.assertRaises(CourseDoesNotExist):
            service.editCourse(courseNewInfo)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfIsNotTheCourseCreator.assert_not_called()
        mockValidator.hasACourseWithTheSameName.assert_not_called()
        mockDB.editCourse.assert_not_called()

    def testEditCourseRaiseExceptionIfIsNotTheCourseCreator(self):
        courseNewInfo = {
            "id": FAKE_COURSE_ID,
            "user_id": FAKE_USER_ID,
            "name": "FakeCourse"
        }
        attrs = {'raiseExceptionIfIsNotTheCourseCreator.side_effect': InvalidUserAction()}
        mockValidator = self._getMock(CourseValidator, attrs)
        mockDB = self._getMock(DB)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        with self.assertRaises(InvalidUserAction):
            service.editCourse(courseNewInfo)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfIsNotTheCourseCreator.assert_called_once_with(FAKE_COURSE_ID, FAKE_USER_ID)
        mockValidator.hasACourseWithTheSameName.assert_not_called()
        mockDB.editCourse.assert_not_called()

    def testEditCourseRaiseExceptionIfTheCourseNameIsRepeated(self):
        courseNewInfo = {
            "id": FAKE_COURSE_ID,
            "user_id": FAKE_CREATOR,
            "name": "FakeCourse"
        }
        attrsValidator = {"hasACourseWithTheSameName.return_value": True}
        mockValidator = self._getMock(CourseValidator, attrsValidator)
        attrsDB = {"getCourse.return_value": {"name": "FakeCourse2"}}
        mockDB = self._getMock(DB, attrsDB)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        with self.assertRaises(CourseAlreadyExists):
            service.editCourse(courseNewInfo)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfIsNotTheCourseCreator.assert_called_once_with(FAKE_COURSE_ID, FAKE_CREATOR)
        mockValidator.hasACourseWithTheSameName.assert_called_once_with("FakeCourse", FAKE_CREATOR)
        mockDB.editCourse.assert_not_called()

    def testEditCourseWorksCorrectly(self):
        courseNewInfo = {
            "id": FAKE_COURSE_ID,
            "user_id": FAKE_CREATOR,
            "name": "FakeCourse"
        }
        mockValidator = self._getMock(CourseValidator)
        attrsDB = {"getCourse.return_value": {"name": "FakeCourse"}}
        mockDB = self._getMock(DB, attrsDB)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        service.editCourse(courseNewInfo)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfIsNotTheCourseCreator.assert_called_once_with(FAKE_COURSE_ID, FAKE_CREATOR)
        mockValidator.hasACourseWithTheSameName.assert_not_called()
        mockDB.editCourse.assert_called_once_with(courseNewInfo)

    def testAddCollaboratorRaiseExceptionIfCourseDoesNotExist(self):
        collaborator = {
            "id": FAKE_COURSE_ID,
            "user_id": FAKE_USER_ID,
        }
        attrs = {'raiseExceptionIfCourseDoesNotExists.side_effect': CourseDoesNotExist()}
        mockValidator = self._getMock(CourseValidator, attrs)
        mockDB = self._getMock(DB)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        with self.assertRaises(CourseDoesNotExist):
            service.addCollaborator(collaborator)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfCanNotCollaborate.assert_not_called()
        mockDB.addCollaborator.assert_not_called()

    def testAddCollaboratorRaiseExceptionIfUserCanNotCollaborate(self):
        collaborator = {
            "id": FAKE_COURSE_ID,
            "user_id": FAKE_USER_ID,
        }
        fakeUserData = {"name": "Rafael"}
        attrs = {'raiseExceptionIfCanNotCollaborate.side_effect': IsAlreadyACollaborator()}
        mockValidator = self._getMock(CourseValidator, attrs)
        mockDB = self._getMock(DB)
        attrsUser = {'getUser.return_value': fakeUserData}
        mockUsers = self._getMock(Users, attrsUser)
        service = CourseService(mockDB, mockValidator, mockUsers, Mock(), Mock())
        with self.assertRaises(IsAlreadyACollaborator):
            service.addCollaborator(collaborator)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfCanNotCollaborate.assert_called_once_with(FAKE_COURSE_ID, fakeUserData)
        mockDB.addCollaborator.assert_not_called()

    def testAddCollaboratorWorksCorrectly(self):
        collaborator = {
            "id": FAKE_COURSE_ID,
            "user_id": FAKE_USER_ID,
        }
        fakeUserData = {"name": "Rafael"}
        mockValidator = self._getMock(CourseValidator)
        mockDB = self._getMock(DB)
        attrsUser = {'getUser.return_value': fakeUserData}
        mockUsers = self._getMock(Users, attrsUser)
        service = CourseService(mockDB, mockValidator, mockUsers, Mock(), Mock())
        service.addCollaborator(collaborator)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfCanNotCollaborate.assert_called_once_with(FAKE_COURSE_ID, fakeUserData)
        mockDB.addCollaborator.assert_called_once_with(collaborator)

    def testBlockCourseRaiseExceptionIfCourseIsAlreadyBlocked(self):
        attrsValidator = {"isBlocked.return_value": True}
        mockValidator = self._getMock(CourseValidator, attrsValidator)
        mockDB = self._getMock(DB)
        mockUsers = self._getMock(Users)
        service = CourseService(mockDB, mockValidator, mockUsers, Mock(), Mock())
        with self.assertRaises(CourseIsAlreadyBlocked):
            service.blockCourse(FAKE_COURSE_ID, FAKE_CREATOR)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockUsers.getUser.asser_called_once_with(FAKE_USER_ID)
        mockValidator.raiseExceptionIfIsNotAdmin.assert_called_once()
        mockValidator.isBlocked.assert_called_once_with(FAKE_COURSE_ID)
        mockDB.blockCourse.assert_not_called()

    def testBlockCourseWorksCorrectly(self):
        attrsValidator = {"isBlocked.return_value": False}
        mockValidator = self._getMock(CourseValidator, attrsValidator)
        mockDB = self._getMock(DB)
        mockUsers = self._getMock(Users)
        service = CourseService(mockDB, mockValidator, mockUsers, Mock(), Mock())
        service.blockCourse(FAKE_COURSE_ID, FAKE_CREATOR)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockUsers.getUser.asser_called_once_with(FAKE_USER_ID)
        mockValidator.raiseExceptionIfIsNotAdmin.assert_called_once()
        mockValidator.isBlocked.assert_called_once_with(FAKE_COURSE_ID)
        mockDB.blockCourse.assert_called_once_with(FAKE_COURSE_ID)

    def testUnblockCourseRaiseExceptionIfCourseIsAlreadyBlocked(self):
        attrsValidator = {"isBlocked.return_value": False}
        mockValidator = self._getMock(CourseValidator, attrsValidator)
        mockDB = self._getMock(DB)
        mockUsers = self._getMock(Users)
        service = CourseService(mockDB, mockValidator, mockUsers, Mock(), Mock())
        with self.assertRaises(CourseIsNotBlocked):
            service.unblockCourse(FAKE_COURSE_ID, FAKE_CREATOR)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockUsers.getUser.asser_called_once_with(FAKE_USER_ID)
        mockValidator.raiseExceptionIfIsNotAdmin.assert_called_once()
        mockValidator.isBlocked.assert_called_once_with(FAKE_COURSE_ID)
        mockDB.unblockCourse.assert_not_called()

    def testUnblockCourseWorksCorrectly(self):
        attrsValidator = {"isBlocked.return_value": True}
        mockValidator = self._getMock(CourseValidator, attrsValidator)
        mockDB = self._getMock(DB)
        mockUsers = self._getMock(Users)
        service = CourseService(mockDB, mockValidator, mockUsers, Mock(), Mock())
        service.unblockCourse(FAKE_COURSE_ID, FAKE_CREATOR)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockUsers.getUser.asser_called_once_with(FAKE_USER_ID)
        mockValidator.raiseExceptionIfIsNotAdmin.assert_called_once()
        mockValidator.isBlocked.assert_called_once_with(FAKE_COURSE_ID)
        mockDB.unblockCourse.assert_called_once_with(FAKE_COURSE_ID)

    def testGetUsersRaiseExceptionIfIsNotTheCourseCreator(self):
        usersFilter = {"subscribers": True, "first_name": "Rafa", "last_name": "Nadal"}
        attrsValidator = {"isTheCourseCreator.return_value": False}
        mockValidator = self._getMock(CourseValidator, attrsValidator)
        mockDB = self._getMock(DB)
        attrsUsers = {"getUser.return_value": {"is_admin": False}}
        mockUsers = self._getMock(Users, attrsUsers)
        service = CourseService(mockDB, mockValidator, mockUsers, Mock(), Mock())
        with self.assertRaises(InvalidUserAction):
            service.getUsers(FAKE_COURSE_ID, FAKE_USER_ID, usersFilter)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockUsers.getUser.asser_called_once_with(FAKE_USER_ID)
        mockValidator.isTheCourseCreator.assert_called_once_with(FAKE_COURSE_ID, FAKE_USER_ID)
        mockDB.getUsers.assert_not_called()

    def testGetUsersWorksCorrectly(self):
        usersFilter = {"subscribers": True, "first_name": "Rafa", "last_name": "Nadal"}
        users = {"users": [{"first_name": "Rafa", "last_name": "Nadal"},
                 {"first_name": "Rafa", "last_name": "Quintero"},
                 {"first_name": "Pepe", "last_name": "Argento"},
                 {"first_name": "Roger", "last_name": "Federer"}]
        }
        attrsValidator = {"isTheCourseCreator.return_value": True}
        mockValidator = self._getMock(CourseValidator, attrsValidator)
        mockDB = self._getMock(DB)
        attrsUsers = {
            "getUser.return_value": {"is_admin": False},
            "getBatchUsers.return_value": users}
        mockUsers = self._getMock(Users, attrsUsers)
        service = CourseService(mockDB, mockValidator, mockUsers, Mock(), Mock())
        result = service.getUsers(FAKE_COURSE_ID, FAKE_USER_ID, usersFilter)
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0], {"first_name": "Rafa", "last_name": "Nadal"})
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockUsers.getUser.asser_called_once_with(FAKE_USER_ID)
        mockUsers.getBatchUsers.asser_called_once()
        mockValidator.isTheCourseCreator.assert_called_once_with(FAKE_COURSE_ID, FAKE_USER_ID)
        mockDB.getUsers.assert_called_once_with(FAKE_COURSE_ID, usersFilter)

    def testAddFavorite(self):
        mockValidator = self._getMock(CourseValidator)
        mockDB = self._getMock(DB)
        favCourse = {"id": FAKE_COURSE_ID, "user_id": FAKE_CREATOR}
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        service.addFavoriteCourse(favCourse)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfCourseIsAlreadyLiked.assert_called_once_with(FAKE_COURSE_ID, FAKE_CREATOR)
        mockDB.addFavoriteCourse.assert_called_once_with(FAKE_COURSE_ID, FAKE_CREATOR)

    @patch('service.Course.CourseService._filterCourses')
    def testGetFavoriteCourses(self, mockFilterCourses):
        favCourse = {"id": FAKE_COURSE_ID, "user_id": FAKE_CREATOR}
        mockFilterCourses.return_value = favCourse
        mockValidator = self._getMock(CourseValidator)
        attrsDB = {'getFavoriteCourses.return_value': favCourse}
        mockDB = self._getMock(DB, attrsDB)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        service.getFavoriteCourses(FAKE_USER_ID, {})
        mockDB.getFavoriteCourses.assert_called_once_with(FAKE_USER_ID, {})
        mockFilterCourses.assert_called_once_with(favCourse, FAKE_USER_ID, {})

    def testRemoveFavoriteCourse(self):
        mockValidator = self._getMock(CourseValidator)
        mockDB = self._getMock(DB)
        favCourse = {"id": FAKE_COURSE_ID, "user_id": FAKE_CREATOR}
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        service.removeFavoriteCourse(favCourse)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfCourseIsNotLiked.assert_called_once_with(FAKE_COURSE_ID, FAKE_CREATOR)
        mockDB.removeFavoriteCourse.assert_called_once_with(FAKE_COURSE_ID, FAKE_CREATOR)

    def testAddMultimedia(self):
        mockValidator = self._getMock(CourseValidator)
        mockDB = self._getMock(DB)
        multimedia = {"title": "Temazo", "url": "https://www.youtube.com/watch?v=ULTtWUZhD9c", "user_id": FAKE_USER_ID}
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        service.addMultimedia(FAKE_COURSE_ID, multimedia)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfIsNotTheCourseCreator.assert_called_once_with(FAKE_COURSE_ID, FAKE_USER_ID)
        mockDB.addMultimedia.assert_called_once_with(FAKE_COURSE_ID, multimedia)

    def testGetMultimedia(self):
        mockDB = self._getMock(DB)
        mockValidator = self._getMock(CourseValidator)
        service = CourseService(mockDB, mockValidator, Mock(), Mock(), Mock())
        service.getMultimedia(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockDB.getMultimedia.assert_called_once_with(FAKE_COURSE_ID)

    def testGetUserTokenRaiseExceptionIfSomethingFails(self):
        attrUsers = {"getUserToken.side_effect": HTTPError()}
        mockUsers = self._getMock(Users, attrUsers)
        service = CourseService(Mock(), Mock(), mockUsers, Mock(), Mock())
        with self.assertRaises(TokenNotFound):
            service.getUserToken(FAKE_USER_ID)

    def testGetUsersDataRaiseExceptionIfSomethingFails(self):
        attrUsers = {"getBatchUsers.side_effect": HTTPError()}
        mockUsers = self._getMock(Users, attrUsers)
        service = CourseService(Mock(), Mock(), mockUsers, Mock(), Mock())
        with self.assertRaises(UserNotFound):
            service.getUsersData([FAKE_USER_ID])

    def testGetPublishedExamsWorksCorrectly(self):
        exams = [{"status": "published", "id": 1}, {"status": "draft", "id": 2}, {"status": "published", "id": 3}]
        attrs = {"getExams.return_value": exams}
        mockExams = self._getMock(Exams, attrs)
        service = CourseService(Mock(), Mock(), Mock(), mockExams, Mock())
        result = service.getPublishedExams(FAKE_COURSE_ID, FAKE_USER_ID)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {"status": "published", "id": 1})
        self.assertEqual(result[1], {"status": "published", "id": 3})
        mockExams.getExams.assert_called_once_with(FAKE_COURSE_ID, FAKE_USER_ID)

    def testGetPublishedExamsRaiseExceptionIfSomethingFails(self):
        attrs = {"getExams.side_effect": HTTPError()}
        mockExams = self._getMock(Exams, attrs)
        service = CourseService(Mock(), Mock(), Mock(), mockExams, Mock())
        with self.assertRaises(ExamsNotFound):
            service.getPublishedExams(FAKE_COURSE_ID, FAKE_USER_ID)

    def testGetUserDataRaiseExceptionIfSomethingFails(self):
        attrUsers = {"getUser.side_effect": HTTPError()}
        mockUsers = self._getMock(Users, attrUsers)
        service = CourseService(Mock(), Mock(), mockUsers, Mock(), Mock())
        with self.assertRaises(UserNotFound):
            service.getUserData([FAKE_USER_ID])

    def testAddSubscriber(self):
        subscriberData = {"first_name": "Natalia", "last_name": "Natalia"}
        mockValidator = self._getMock(CourseValidator)
        mockDB = self._getMock(DB)
        attr = {"getUser.return_value": subscriberData}
        mockUsers = self._getMock(Users, attr)
        service = CourseService(mockDB, mockValidator, mockUsers, Mock(), Mock())
        service.addSubscriber(FAKE_COURSE_ID, FAKE_USER_ID)
        mockValidator.raiseExceptionIfCourseDoesNotExists.assert_called_once_with(FAKE_COURSE_ID)
        mockValidator.raiseExceptionIfCanNotSubscribe.assert_called_once_with(FAKE_COURSE_ID, subscriberData)
        mockDB.addSubscriber.assert_called_once_with(FAKE_COURSE_ID, FAKE_USER_ID)

    def testRemoveSubscriberRaiseExceptionIfUserIsNotSubscribed(self):
        attr = {"isSubscribed.return_value": False}
        mockValidator = self._getMock(CourseValidator, attr)
        service = CourseService(Mock(), mockValidator, Mock(), Mock(), Mock())
        with self.assertRaises(IsNotSubscribed):
            service.removeSubscriber(FAKE_COURSE_ID, FAKE_USER_ID)

    def testSendNotification(self):
        attr = {"getUserToken.return_value": {"token": 123}}
        mockUser = self._getMock(Users, attr)
        mockNotification = self._getMock(NotificationManager)
        service = CourseService(Mock(), Mock(), mockUser, Mock(), mockNotification)
        notification = {
            "title": "La champions liga",
            "body": "Hola que tal tu como estaaaaas? Dime si eres feliz",
            "user_id": FAKE_USER_ID
        }
        service.sendNotification(notification)
        mockNotification.sendNotification.assert_called_once_with(123, "La champions liga", "Hola que tal tu como estaaaaas? Dime si eres feliz")

    def testUpdateSubscriberStatusSendNotificationIfCourseIsFinished(self):
        attrsDB = {"getCourse.return_value": {"name": "Sarasa", "exams": 3}}
        subscriberGrades = {
            "course_id": FAKE_COURSE_ID,
            "user_id": FAKE_USER_ID,
            "grades": ["pass", "fail", "pass"]
        }
        mockDB = self._getMock(DB, attrsDB)
        attrsUsers = {"getUserToken.return_value": {"token": 123}}
        mockUsers = self._getMock(Users, attrsUsers)
        mockNotification = self._getMock(NotificationManager)
        service = CourseService(mockDB, Mock(), mockUsers, Mock(), mockNotification)
        service.updateSubscriberStatus(subscriberGrades)
        mockNotification.sendNotification.assert_not_called()
        mockDB.updateSubscriberStatus.assert_called_once_with(FAKE_COURSE_ID, "approved", FAKE_USER_ID)
        mockNotification.courseFinished.assert_called_once_with(123, "Sarasa", "approved")

    def testUpdateSubscriberStatusSendNotificationAboutExamIfCourseIsNotFinished(self):
        attrsDB = {"getCourse.return_value": {"name": "Sarasa", "exams": 4}}
        subscriberGrades = {
            "course_id": FAKE_COURSE_ID,
            "user_id": FAKE_USER_ID,
            "grades": ["pass", "fail", "pass"]
        }
        mockDB = self._getMock(DB, attrsDB)
        attrsUsers = {"getUserToken.return_value": {"token": 123}}
        mockUsers = self._getMock(Users, attrsUsers)
        mockNotification = self._getMock(NotificationManager)
        service = CourseService(mockDB, Mock(), mockUsers, Mock(), mockNotification)
        service.updateSubscriberStatus(subscriberGrades)
        mockNotification.sendNotification.assert_called_once_with(
            123,
            "Examen corregido",
            "Tu examen del curso 'Sarasa' fue corregido"
        )
        mockDB.updateSubscriberStatus.assert_not_called()
        mockNotification.courseFinished.assert_not_called()

    def testUpdateSubscriberStatusRaiseExceptionIfCourseDoesNotExist(self):
        attrsDB = {"getCourse.return_value": None}
        subscriberGrades = {
            "course_id": FAKE_COURSE_ID,
            "user_id": FAKE_USER_ID,
            "grades": ["pass", "fail", "pass"]
        }
        mockDB = self._getMock(DB, attrsDB)
        service = CourseService(mockDB, Mock(), Mock(), Mock(), Mock())
        with self.assertRaises(CourseDoesNotExist):
            service.updateSubscriberStatus(subscriberGrades)

