from django.urls import path
from poll.views import *

app_name = "poll"

urlpatterns = [
    path('poll-list/',Poll_list.as_view(),name="poll-list"),
    path('add-poll',Add_poll.as_view(),name=("add")),
    path('poll-details/<int:poll_id>/',Poll_Details.as_view(),name="poll-details"),
    path('end-poll/<int:poll_id>/',End_Poll.as_view(),name="end-poll"),
    path('poll-edit/<int:poll_id>',Poll_Edit.as_view(),name="poll-edit"),
    path('poll-delete/<int:poll_id>/',Poll_delete.as_view(),name="poll-delete"),
    path('poll-result/<int:poll_id>/',Poll_result.as_view(),name='poll-result'),
    path('choice-edit/<int:choice_id>/',Choice_edit.as_view(),name="choice-edit"),
]