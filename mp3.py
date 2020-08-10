#!/usr/bin/env python
from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

# For saving the song name with there path
songs_with_path = {}

class Mp3_Player:
    

    # Initialize Pygame
    pygame.mixer.init()


    #---GLOBAL-----
    # This shows that if the song is stopped or not
    global stopped
    stopped = False


    # This shows that if the song is paused or not
    global paused
    paused = False


    # Adding One Song To Playlist.
    def add_song(self):
        # Get file Song Location.
        song_path = filedialog.askopenfilename(initialdir='audio', title='Choose A Song', filetypes=(("mp3 Files", "*.mp3" ), ("All", "*")))
        # Getting Song Name
        song = song_path.split('/')[-1]
        # Removing .mp3
        song = song.replace('.mp3', '')
        # Adding song name with song path
        songs_with_path[song] = song_path
        # Desplaying Song Name on the play_list
        playlist_box.insert(END, song)



    # Adding Many Songs To Playlist.
    def add_many_songs(self):        
        # Get file Song Location.
        songs = filedialog.askopenfilenames(initialdir='audio', title='Choose A Song', filetypes=(("mp3 Files", "*.mp3"), ("All", "*")))
        
        # Getting Each Name from the songs list.
        for song_path in songs:
            # Getting the songs name
            song = song_path.split('/')[-1]
            # Removing .mp3 in all songs
            song = song.replace('.mp3', '')
            # Adding song name with song path in dictonary
            songs_with_path[song] = song_path
            # Showing the name of the song in the playlist
            playlist_box.insert(END, song)



    # Removing Songs.
    def delete_song(self):
        # ANCHOR is the selected word in the playlist and deleting it.
        playlist_box.delete(ANCHOR)



    # Removing All Songs.
    def delete_all_songs(self):
        # Selecting 0 till end means all songs in the playlist and deleting them.
        playlist_box.delete(0, END)




    # Play Songs.
    def play(self):    
        global status_bar
        global song_slider
        global stopped
        
        # Clear the Status Bar
        status_bar.config(text='00:00  /00:00')

        # Set our slider to zero
        song_slider.config(value=0)
        
        
        # Song is Played
        stopped = False


        # Getting the selected song.
        songs  = str(playlist_box.get(ACTIVE))
        # Seeing the path of song in the dictonary with the song name.
        song = songs_with_path[songs]
        # Loading the song from the path which we got.
        pygame.mixer.music.load(song)
        # Playing the loaded song.
        pygame.mixer.music.play(loops=0)


        # Get Song Time
        self.play_time()


      

    # Stopping The Song    
    def stop(self):
        global status_bar
        global song_slider
        global stopped

        
        # Stop the playing song
        pygame.mixer.music.stop()
        # Clear Playlist select Bar
        playlist_box.selection_clear(ACTIVE)

        # Clear the Status Bar
        status_bar.config(text='00:00  /00:00')

        # Set our slider to zero
        song_slider.config(value=0)

        # Set Stop Veriable Stopped
        stopped = True




    # Pause The Song.
    def pause(self, is_paused):
        global paused
        paused = is_paused

        if paused:
            #Unpause
            pygame.mixer.music.unpause()
            # We have unpaused it so it is no longer in paused state
            paused = False
        
        else: 
            #Pause
            pygame.mixer.music.pause()
            # We have paused it so it is no longer in unpaused state
            paused = True



    # Play Next Song.
    def next_song(self):
        global status_bar
        global song_slider
        # Reset Status bar and slider.
        status_bar.config(text='00:00  /00:00')
        song_slider.config(value=0)


        # Return List with a number on it
        next_one = playlist_box.curselection()
        # Getting the number from the list and adding 1 with it
        next_one = next_one[0] + 1
        
        # Grab the song title from the song playlist
        song = playlist_box.get(next_one)
        # Getting song path
        song = songs_with_path[song]
        # Loading the song from the path which we got.
        pygame.mixer.music.load(song)
        # Playing the loaded song.
        pygame.mixer.music.play(loops=0)


        # Clear Active bar in playlist
        playlist_box.selection_clear(0, END)

        # Move Active bar to next song
        playlist_box.activate(next_one)

        # Set Active bar to the next song
        playlist_box.selection_set(next_one, last=None)



    # Play Previous Song.
    def previous_song(self):
        global status_bar
        global song_slider
        global playlist_box

        # Reseting slider bar.
        status_bar.config(text='00:00  /00:00')
        song_slider.config(value=0)

        # Return List with a number on it
        previous_one = playlist_box.curselection()
        # Getting the number from the list and adding 1 with it
        previous_one = previous_one[0] - 1
        
        # Grab the song title from the song playlist
        song = playlist_box.get(previous_one)
        # Getting song path
        song = songs_with_path[song]
        # Loading the song from the path which we got.
        pygame.mixer.music.load(song)
        # Playing the loaded song.
        pygame.mixer.music.play(loops=0)


        # Clear Active bar in playlist
        playlist_box.selection_clear(0, END)

        # Move Active bar to next song
        playlist_box.activate(previous_one)

        # Set Active bar to the next song
        playlist_box.selection_set(previous_one, last=None)



    # Get song timming
    def play_time(self):

        # Check If Song is stopped
        global stopped
        global playlist_box
        global song_slider
        global song_length
        global status_bar


        if stopped:
            return

        else:
            
            
            # Returning the Mili seconds dividing it with 1000 to get seconds
            current_time = pygame.mixer.music.get_pos() / 1000

            
            # Convert Song time to time format
            converted_time = time.strftime('%M:%S', time.gmtime(current_time))


            # Get Current Playing song path
            current_song = playlist_box.get(ACTIVE)
            song = songs_with_path[current_song]
            # Find Current Song Length
            song_mut = MP3(song)

            
            # Get Song Length in Seconds
            song_length = song_mut.info.length
            
            # Convert to time format
            converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

            # Check to see if song is over
            if int(song_slider.get()) == int(song_length):
                self.stop()
            
            elif paused:
                # Check to see if the song is paused
                pass

            else:
                

                # Move Slider as the song moves with 1 second at a time
                next_time = int(song_slider.get()) + 1

                # Output New time value and # Set Slider length to the length of the song
                song_slider.config(value=next_time, to=song_length )

                # Converting song slider position to time Formate
                converted_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

                # Outputing current time
                status_bar.config(text=f'{converted_time}  /{converted_song_length}')

            if current_time >= 0:
            
                # Add current time to status bar
                status_bar.config(text=f'{converted_time}  /{converted_song_length}')

            # Run this code every single second
            status_bar.after(1000, self.play_time)


    # Create Volumne Function.
    def volumne(self, x):
        global volume_slider

        # Setting the voulume of the song as the user selected
        pygame.mixer.music.set_volume(volume_slider.get())


    # Create a Song Slide Fuction
    def slide(self, x):
        global playlist_box
        global song_slider

        # Getting the selected song.
        songs  = str(playlist_box.get(ACTIVE))
        # Seeing the path of song in the dictonary with the song name.
        song = songs_with_path[songs]
        # Loading the song from the path which we got.
        pygame.mixer.music.load(song)
        # Playing the loaded song.
        pygame.mixer.music.play(loops=0, start=song_slider.get())


    def main(self):
        global playlist_box
        
        # Creating a window with tkinter
        tkinter_instance = Tk()
        # Giving the window a name
        tkinter_instance.title('MP3 Player')
        # Giving the size to the window
        tkinter_instance.geometry("500x400")


        # Creat Main Frame in which all thing is added like buttons, playlists box
        main_frame = Frame(tkinter_instance)
        # Giving a y padding
        main_frame.pack(pady=20)


        
        # Create a Playlist for songs to be displayed.
        playlist_box = Listbox(main_frame, bg='black', fg='white', width=50, selectbackground='green', selectforeground='black')
        # Adding the playlist_box to the screen.
        playlist_box.grid(row=0, column=0)

        # Adding Button Images.
        back_btn_img =  PhotoImage(file='images/back.png')
        forward_btn_img = PhotoImage(file='images/forward.png')
        play_btn_img = PhotoImage(file='images/play.png')
        stop_btn_img = PhotoImage(file='images/stop.png')
        pause_btn_img = PhotoImage(file='images/pause.png')


        # Create Button frame to hold all our buttons.
        button_controller = Frame(main_frame)
        # Adding the Frame to the main window.
        button_controller.grid(row=1, column=0, pady=20)

        # Create Buttons.
        # text=name or image=img.
        back_button = Button(button_controller, image=back_btn_img, borderwidth=0, command=self.previous_song)
        forward_button = Button(button_controller, image=forward_btn_img, borderwidth=0, command=self.next_song)
        stop_button = Button(button_controller, image=stop_btn_img, borderwidth=0, command=self.stop)
        pause_button = Button(button_controller, image=pause_btn_img, borderwidth=0, command=lambda: self.pause(paused))
        play_button = Button(button_controller, image=play_btn_img, borderwidth=0, command=self.play)


        # Putting Created Button on the screen using grid.
        back_button.grid(row=0, column=0, padx=5)
        play_button.grid(row=0, column=1, padx=5)
        forward_button.grid(row=0, column=2, padx=5)
        pause_button.grid(row=0, column=3, padx=5)
        stop_button.grid(row=0, column=4, padx=5)

        # Create Menu inside our main menu.
        my_menu = Menu(tkinter_instance)
        # Adding this menu to the main window
        tkinter_instance.config(menu=my_menu)


        # Song Menu Drop box.
        add_song_menu = Menu(my_menu, tearoff=1)
        # Adding a label of add songs on the main window
        my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
        # Creating a option to Add one song.
        add_song_menu.add_command(label='Add One Song', command=self.add_song)
        # Creating a option to Add many songs.
        add_song_menu.add_command(label='Add Many Songs', command=self.add_many_songs)


        # # Adding a label of Delete songs on the main window.
        remove_song = Menu(my_menu, tearoff=1)
        # Adding a label of remove songs inside a Delete song label.
        my_menu.add_cascade(label='Remove Songs', menu=remove_song)
        # Creating a option to Delete the selected songs.
        remove_song.add_command(label='Delete a Song From The Play List', command=self.delete_song)
        # Creating a option to Delete all songs in the playlist.
        remove_song.add_command(label='Delete All Songs From The Play List', command=self.delete_all_songs)

        # Making this global so that all fuctions can use it
        global status_bar

        # Creating a Status Bar to display time of the song.
        status_bar = Label(tkinter_instance, text='00:00  /00:00', bd=1, relief=GROOVE, anchor=E)
        # Adding the status bar with time at the bottom of the main window.
        status_bar.pack(fill=X, side=BOTTOM, pady=2)



        # Creating Volume Slider Frame.
        volume_frame = LabelFrame(main_frame, text='Volume')
        # Adding the frame in the main window.
        volume_frame.grid(row=0, column=1)

        # Making this global so that all fuctions can use it
        global volume_slider

        # Create Volume Slider to do low or high the volume inside the volume_frame.
        volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, length=120, value=0.5, command=self.volumne)
        # Adding volume slide in the volume frame inside the main window.
        volume_slider.pack(pady=20)

        # Making this global so that all fuctions can use it
        global song_slider

        # Create Song Slider to go forward and backward in time in song.
        song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=self.slide)
        # Adding it to the main window.
        song_slider.grid(row=2, column=0, pady=0)


        # This is too continue the loop so that our app don't get shutdown without clicking close.
        tkinter_instance.mainloop()



# Creating a mp3 instant
mp3 = Mp3_Player()    
# Running our main fuction to set up everyting
mp3.main()
