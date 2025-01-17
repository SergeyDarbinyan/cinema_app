from django.urls import path

from . import views

urlpatterns = [
    path("manage/rooms", views.RoomManageView.as_view(), name="room-manage"),
    path("manage/movies", views.MovieManageView.as_view(), name="movie-manage"),
    path("manage/events", views.EventManageView.as_view(), name="event-manage"),
    path("manage/users", views.UserManageView.as_view(), name="user-manage"),
    path("manage/reservations", views.ReservationManageView.as_view(), name="reservation-manage")
]
