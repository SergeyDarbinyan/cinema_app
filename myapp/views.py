import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from .enums import SeatingConfig
from .models import Events, Movies, Rooms, Seats, Users, Reservations
from .serializers import EventSerializer, RoomSerializer, MovieSerializer, UserSerializer, ReservationSerializer, \
    ReadReservationSerializer


@method_decorator(csrf_exempt, name='dispatch')
class RoomManageView(View):
    def get(self, request):
        room_id = request.GET.get('room_id')

        if room_id:
            try:
                room = Rooms.objects.get(pk=room_id)
                serializer = RoomSerializer(room)
                return JsonResponse(serializer.data, safe=False)
            except Rooms.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Room not found.'}, status=404)
        else:
            rooms = Rooms.objects.all()
            serializer = RoomSerializer(rooms, many=True)
            return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})

        serializer = RoomSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse({'status': "error", 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        existing_room = Rooms.objects.filter(
            room_name=data["room_name"],
        ).exists()
        if existing_room:
            return JsonResponse(
                {'status': 'error', 'message': 'Room already exists for the selected name.'},
                status=status.HTTP_409_CONFLICT)

        room = Rooms.objects.create(
            room_name=data["room_name"],
        )
        rows = SeatingConfig.ROWS.value
        cols = SeatingConfig.COLUMNS.value
        for row in range(1, rows + 1):
            for col in range(1, cols + 1):
                Seats.objects.create(
                    room=room,
                    seat_row=row,
                    seat_col=col
                )
        return JsonResponse({'status': "success", 'event_id': room.room_id}, status=status.HTTP_201_CREATED)

    def put(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})

        room_id = data.get('room_id')
        room_name = data.get('room_name')

        if not room_id or not room_name:
            return JsonResponse({'status': 'error', 'message': 'Room ID and name are required.'},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Rooms.objects.get(room_id=room_id)
        except Rooms.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'Room with {room_id} ID not found.'},
                                status=status.HTTP_404_NOT_FOUND)

        if Rooms.objects.filter(room_name=room_name).exclude(room_id=room_id).exists():
            return JsonResponse({'status': 'error', 'message': 'Room name already exists.'},
                                status=status.HTTP_409_CONFLICT)

        room.room_name = room_name
        room.save()

        return JsonResponse({'status': 'success', 'message': 'Room updated successfully.'},
                            status=status.HTTP_200_OK)

    def delete(self, request):
        room_id = request.GET.get('room_id')

        if not room_id:
            return JsonResponse({'status': 'error', 'message': 'Room ID is required to delete a room.'},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Rooms.objects.get(room_id=room_id)

            Events.objects.filter(room=room).delete()
            Seats.objects.filter(room=room).delete()
            room.delete()

            return JsonResponse({'status': 'success', 'message': f'Room with {room_id} ID has been deleted.'},
                                status=status.HTTP_204_NO_CONTENT)
        except Rooms.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'Room with {room_id} ID not found.'},
                                status=status.HTTP_404_NOT_FOUND)


@method_decorator(csrf_exempt, name='dispatch')
class MovieManageView(View):
    def get(self, request):
        movie_id = request.GET.get('movie_id')

        if movie_id:
            try:
                movie = Movies.objects.get(pk=movie_id)
                serializer = MovieSerializer(movie)
                return JsonResponse(serializer.data, safe=False)
            except Movies.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Movie not found.'}, status=404)
        else:
            movies = Movies.objects.all()
            serializer = MovieSerializer(movies, many=True)
            return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})

        serializer = MovieSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse({'status': "error", 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        existing_movie = Movies.objects.filter(
            movie_name=data["movie_name"],
        ).exists()
        if existing_movie:
            return JsonResponse(
                {'status': 'error', 'message': 'Movie already exists for the selected name.'},
                status=status.HTTP_409_CONFLICT)

        movie = Movies.objects.create(
            movie_name=data["movie_name"],
        )
        return JsonResponse({'status': "success", 'event_id': movie.movie_id}, status=status.HTTP_201_CREATED)

    def put(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})

        movie_id = data.get('movie_id')
        movie_name = data.get('movie_name')

        if not movie_id or not movie_name:
            return JsonResponse({'status': 'error', 'message': 'Movie ID and name are required.'},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movies.objects.get(movie_id=movie_id)
        except Movies.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'Movie with {movie_id} ID not found.'},
                                status=status.HTTP_404_NOT_FOUND)

        if Movies.objects.filter(movie_name=movie_name).exclude(movie_id=movie_id).exists():
            return JsonResponse({'status': 'error', 'message': 'Movie name already exists.'},
                                status=status.HTTP_409_CONFLICT)

        movie.movie_name = movie_name
        movie.save()

        return JsonResponse({'status': 'success', 'message': 'Movie updated successfully.'},
                            status=status.HTTP_200_OK)

    def delete(self, request):
        movie_id = request.GET.get('movie_id')

        if not movie_id:
            return JsonResponse({'status': 'error', 'message': 'Movie ID is required to delete a movie.'},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movies.objects.get(movie_id=movie_id)

            Events.objects.filter(movie=movie).delete()

            movie.delete()
            return JsonResponse({'status': 'success', 'message': f'Movie with {movie_id} ID has been deleted.'},
                                status=status.HTTP_204_NO_CONTENT)
        except Movies.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'Movie with {movie_id} ID not found.'},
                                status=status.HTTP_404_NOT_FOUND)


@method_decorator(csrf_exempt, name='dispatch')
class EventManageView(View):
    def get(self, request):
        event_id = request.GET.get('event_id')
        room_id = request.GET.get('room_id')
        movie_id = request.GET.get('movie_id')

        events = Events.objects
        if event_id:
            events = events.filter(
                event_id=event_id
            )
        if movie_id:
            events = events.filter(
                movie_id=movie_id
            )
        if room_id:
            events = events.filter(
                room_id=room_id
            )
        events = events.all()
        serializer = EventSerializer(events, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})

        serializer = EventSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse({'status': "error", 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        movie = Movies.objects.get(movie_id=data["movie_id"])
        room = Rooms.objects.get(room_id=data["room_id"])

        existing_event = Events.objects.filter(
            movie=movie,
            room=room,
            time=data["time"]
        ).exists()
        if existing_event:
            return JsonResponse(
                {'status': 'error', 'message': 'Event already exists for the selected movie, room, and time.'},
                status=status.HTTP_409_CONFLICT)

        event = Events.objects.create(
            movie=movie,
            room=room,
            time=data["time"]
        )
        return JsonResponse({'status': "success", 'event_id': event.event_id}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        event_id = request.GET.get('event_id')

        if not event_id:
            return JsonResponse({'status': 'error', 'message': 'Event ID is required to delete an event.'},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Events.objects.get(event_id=event_id)
            event.delete()
            return JsonResponse({'status': 'success', 'message': f'Event with {event_id} ID has been deleted.'},
                                status=status.HTTP_204_NO_CONTENT)
        except Events.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'Event with {event_id} ID not found.'},
                                status=status.HTTP_404_NOT_FOUND)


@method_decorator(csrf_exempt, name='dispatch')
class UserManageView(View):
    def get(self, request):
        user_id = request.GET.get('user_id')

        if user_id:
            try:
                user = Users.objects.get(pk=user_id)
                serializer = UserSerializer(user)
                return JsonResponse(serializer.data, safe=False)
            except Users.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)
        else:
            users = Users.objects.all()
            serializer = UserSerializer(users, many=True)
            return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})

        serializer = UserSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse({'status': "error", 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = Users.objects.create(
            user_name=data["user_name"],
        )
        return JsonResponse({'status': "success", 'event_id': user.user_id}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        user_id = request.GET.get('user_id')

        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'User ID is required to delete a user.'},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Users.objects.get(user_id=user_id)

            # delete a reservation
            user.delete()
            return JsonResponse({'status': 'success', 'message': f'User with {user_id} ID has been deleted.'},
                                status=status.HTTP_204_NO_CONTENT)
        except Users.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'User with {user_id} ID not found.'},
                                status=status.HTTP_404_NOT_FOUND)


@method_decorator(csrf_exempt, name='dispatch')
class ReservationManageView(View):
    def get(self, request):
        reservation_id = request.GET.get('reservation_id')
        room_id = request.GET.get('room_id')
        event_id = request.GET.get('event_id')
        seat_id = request.GET.get('seat_id')
        reservations = Reservations.objects
        if reservation_id:
            reservations = reservations.filter(
                reservation_id=reservation_id
            )
        if room_id:
            reservations = reservations.filter(
                event_id__room_id=room_id
            )
        if event_id:
            reservations = reservations.filter(
                event_id=event_id
            )
        if seat_id:
            reservations = reservations.filter(
                seat_id=seat_id
            )
        reservations = reservations.all()
        serializer = ReadReservationSerializer(reservations, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})

        serializer = ReservationSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse({'status': "error", 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        seat = Seats.objects.get(seat_id=data["seat_id"])
        event = Events.objects.get(event_id=data["event_id"])
        user = Users.objects.get(user_id=data["user_id"])
        if seat.room_id != event.room_id:
            return JsonResponse(
                {'status': 'error',
                 'message': 'Incorrect seat specified. Event is in another room.'},
                status=status.HTTP_409_CONFLICT)
        existing_reservation = Reservations.objects.filter(
            seat=seat,
            event=event
        ).exists()
        if existing_reservation:
            return JsonResponse(
                {'status': 'error',
                 'message': 'Reservation already exists for the selected seat, event, and user.'},
                status=status.HTTP_409_CONFLICT)
        reservation = Reservations.objects.create(
            seat=seat,
            event=event,
            user=user
        )
        return JsonResponse({'status': "success", 'reservation_id': reservation.reservation_id},
                            status=status.HTTP_201_CREATED)

    def delete(self, request):
        reservation_id = request.GET.get('reservation_id')

        if not reservation_id:
            return JsonResponse({'status': 'error', 'message': 'Reservation ID is required to delete an event.'},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            reservation = Reservations.objects.get(reservation_id=reservation_id)
            reservation.delete()
            return JsonResponse(
                {'status': 'success', 'message': f'Reservation with {reservation_id} ID has been deleted.'},
                status=status.HTTP_204_NO_CONTENT)
        except Reservations.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'Reservation with {reservation_id} ID not found.'},
                                status=status.HTTP_404_NOT_FOUND)
