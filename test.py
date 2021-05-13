from get_cover_art import CoverFinder

finder = CoverFinder({'verbose': True})

# then you can run either of these:
finder.scan_folder(r"C:\Users\rahul\Desktop\Listen Together")
finder.scan_file(r"media\song_files\Alberto_Giurioli_-_Nightfall.mp3")
