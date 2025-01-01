from django.urls import path

from cashviz.person.ajax import person_fee_details
from cashviz.person.views import PersonFeeNotLinkedView, PersonFeeView

urlpatterns = [
    path("person/fee/list/", PersonFeeView.as_view(), name="person_fee_table"),
    path(
        "person/fee/not_linked/list/",
        PersonFeeNotLinkedView.as_view(),
        name="person_fee_not_linked_table",
    ),
    path(
        "person/view_fee_details/<int:person_id>/",
        person_fee_details,
        name="view_person_fee_details",
    ),
]
