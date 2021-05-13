from django.db import models

# Create your models here.


class Songs(models.Model):
    song_file = models.FileField(upload_to='song_files/', unique=True)


class Songs_Metadata(models.Model):
    song_id = models.OneToOneField(Songs, on_delete=models.CASCADE, unique=True)
    album_name = models.CharField(max_length=80)
    album_img = models.ImageField(upload_to='album_images/')
    artist_name = models.CharField(max_length=50)
    genre_name = models.CharField(max_length=50, default="miscellaneous")
