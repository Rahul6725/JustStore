from django.shortcuts import render, redirect
from .models import Songs, Songs_Metadata
from mutagen.id3 import ID3
from io import BytesIO
from PIL import Image
import numpy as np
import os
# Create your views here.


# File Management Methods starts

def coverArtWrite(tags, song_file):
    pict = tags.get("APIC:").data
    temp = str(song_file)
    temp = temp.replace(" ", "_")
    if "song_files/" in temp:
        temp = temp.lstrip("media/song_files/")
    coverart = "media/album_images/" + str(temp)
    coverart = coverart.rstrip(".mp3")
    coverart = coverart + ".jpeg"
    destination = open(coverart, "wb+")
    destination.write(pict)
    destination.close()
    return(coverart)

def songFileWrite(song_file):
    temp = str(song_file)
    temp = temp.replace(" ", "_")
    with open('media/song_files/' + str(temp), 'wb+') as destination:
        for chunk in song_file.chunks():
            destination.write(chunk)
    return('media/song_files/' + str(temp))

def songFileDelete():
    for x in os.listdir("media/song_files"):
        x = "song_files/" + x
        p = Songs.objects.all().filter(song_file=x)
        x = "media/" + x
        if not p:
            os.remove(x)
        

def coverArtDelete():
    for x in os.listdir("media/album_images"):
        x = "media/album_images/" + x
        p = Songs_Metadata.objects.all().filter(album_img=x)
        if not p:
            os.remove(x)
    
# File Management Methods ends
    
    

def readSongsMetaData():
    j = ""
    res = ""
    song = Songs.objects.all()
    for i in song:
        p = Songs_Metadata.objects.all().filter(song_id_id=i.id)
        if not p:
            j = str(i.song_file)
            j = "media/" + j
            tags = ID3(j)
            coverart = coverArtWrite(tags, j)
            pict = tags.get("APIC:").data
            j = j.strip("media/song_files/")
            genre = tags.get("TCON")
            if str(genre) == "None":
                genre = "miscellaneous"
            metadata = Songs_Metadata(
                song_id=Songs.objects.get(id=i.id),
                album_name=tags.get("TALB"),
                album_img=coverart,
                artist_name=tags.get("TPE1"),
                genre_name=genre
            )
            metadata.save()
            return(coverart)


def welcome(request):
    songFileDelete()
    coverArtDelete()
    dict = {}
    t = readSongsMetaData()
    song = Songs_Metadata.objects.all()
    main_song = Songs.objects.all()
    for i in range(0,len(song)):
        dict[i] = {}
        dict[i]['song'] = "media/" + str(main_song[i].song_file)
        dict[i]['album_name'] = song[i].album_name
        dict[i]['album_img'] = song[i].album_img
        dict[i]['artist'] = song[i].artist_name
        dict[i]['genre'] = song[i].genre_name
    return render(request, "welcome.html", {"main_dict":dict})

def upload(request):
    return render(request, "upload.html")

def uploadingsongs(request):
    if request.method == 'POST':
        meta = {}
        song_file = request.FILES.get("songfile", None)
        song_path = songFileWrite(song_file)
        meta['pict'] = readSongsMetaData()
        tags = ID3(song_path)
        meta['pict'] = coverArtWrite(tags, song_file)
        print(meta['pict'])
        meta['pict'] = "/" + str(meta['pict'])
        meta["album_name"]=tags.get("TALB")
        meta["artist_name"]=tags.get("TPE1")
        meta['genre'] = tags.get("TCON")
        if str(meta['genre']) == "None":
            meta['genre'] = 'miscellaneous'
        return render(request, "upload.html", meta)
        

def uploaded(request):
    for x in os.listdir("media/song_files"):
        x = "song_files/" + x
        p = Songs.objects.all().filter(song_file=x)
        if not p:
            p = Songs(song_file=x)
            p.save()
    return redirect("welcome")
        