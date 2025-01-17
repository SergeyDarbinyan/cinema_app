from django.db import models


# Create your models here.

class Rooms(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=100)

    def __str__(self):
        return self.room_name

class Movies(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=100)

    def __str__(self):
        return self.movie_name

class Events(models.Model):
    event_id = models.AutoField(primary_key=True)

    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)

    time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.movie_name} at {self.time}"

    def __repr__(self):
        return f"{self.movie.movie_name} at {self.time}"

class Seats(models.Model):
    seat_id = models.AutoField(primary_key=True)
    seat_row = models.IntegerField()
    seat_col = models.IntegerField()

    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)

    def __str__(self):
        return f"Row {self.seat_row}, Seat {self.seat_col}"

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name

class Reservations(models.Model):
    reservation_id = models.AutoField(primary_key=True)

    seat = models.ForeignKey(Seats, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation by {self.user.user_name} for {self.event}"
