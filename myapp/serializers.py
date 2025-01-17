from rest_framework import serializers

from .models import Rooms, Movies, Events, Users, Reservations, Seats


class RoomSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField()

    class Meta:
        model = Rooms
        fields = ['room_id', 'room_name']


class SeatSerializer(serializers.ModelSerializer):
    seat_row = serializers.CharField()
    seat_col = serializers.CharField()

    class Meta:
        model = Movies
        fields = ['seat_row', 'seat_col']


class MovieSerializer(serializers.ModelSerializer):
    movie_name = serializers.CharField()

    class Meta:
        model = Movies
        fields = ['movie_id', 'movie_name']


class EventSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField()
    room_id = serializers.IntegerField()

    class Meta:
        model = Events
        fields = ['event_id', 'movie_id', 'room_id', 'time']

    def validate(self, data):
        try:
            Movies.objects.get(pk=data['movie_id'])
        except Movies.DoesNotExist:
            raise serializers.ValidationError({"movie_id": f"Movie with {data['movie_id']} ID does not exist."})

        try:
            Rooms.objects.get(pk=data['room_id'])
        except Rooms.DoesNotExist:
            raise serializers.ValidationError({"room_id": f"Room with {data['room_id']} ID does not exist."})

        return data


class UserSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField()

    class Meta:
        model = Users
        fields = ['user_id', 'user_name']


class ReadReservationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Reservations
        depth = 1


class ReservationSerializer(serializers.ModelSerializer):
    seat_id = serializers.IntegerField()
    event_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Reservations
        fields = ['reservation_id', 'seat_id', 'event_id', 'user_id']

    def validate_seat_id(self, seat_id):
        try:
            Seats.objects.get(pk=seat_id)
        except Seats.DoesNotExist:
            raise serializers.ValidationError({"seat_id": f"Seat with {seat_id} ID does not exist."})
        return seat_id

    def validate_event_id(self, event_id):
        try:
            Events.objects.get(pk=event_id)
        except Events.DoesNotExist:
            raise serializers.ValidationError({"event_id": f"Event with {event_id} ID does not exist."})
        return event_id

    def validate_user_id(self, user_id):
        try:
            Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            raise serializers.ValidationError({"user_id": f"User with {user_id} ID does not exist."})
        return user_id
