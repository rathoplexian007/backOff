import imp
from django.urls import path
from .views import *

urlpatterns = [
    path('main/', main),
    path('register/',RegisterUser.as_view()),
    path('login/',LoginUser.as_view()),
    path('showuser/',UserDataView.as_view()),
    path('showofficials/',OfficalsView.as_view()),
    path('uploadDocs/',UploadDocuments.as_view()),
    path('getUnappointed/',UnappointedView.as_view()),
    path('requestMeeting/',RequestMeeting.as_view()),
    path('showmeetings/',MeetingView.as_view()),
    path('updateofficials/<int:pk>',UpdateOfficial.as_view()),
    path('deletemeetings/<int:pk>/delete',DeleteMeetings.as_view()),
    path('getmeetings/',ShowMeetings.as_view()),
    path('approvemeeting/',ApproveMeeting.as_view()),
    path('deletemeeting/',DeleteMeeting.as_view()),
    path('getallmeetings/',ShowAllMeetingsForAdmin.as_view()),
    path('approverequest/',ApproveKYC.as_view()),
    path('rejectrequest/',RejectKYC.as_view()),
    path('status/',Status.as_view()),

    # path('concall/', VideoConferenceView.as_view())
]