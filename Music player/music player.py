from tkinter import *
from tkinter import filedialog,ttk
import tkinter as tk    
import os 
from pygame import mixer
from mutagen.mp3 import MP3
import time


canvas= tk.Tk()
canvas.title("Music player")
canvas.geometry("680x600")
canvas.config(bg="#eeeeee")
mixer.init()
def time_info():
    #current song elapse time 
    current_time=mixer.music.get_pos() / 1000
    #slider_lable.config(text=f'slider:{int(my_slider.get())} and Song pos{int(current_time)}')
    #insert the time elapsed time to the status_bar 
    converted_time= time.strftime('%M:%S',time.gmtime(current_time))
    playing_song=box.curselection()
    
    playing_song_name=box.get(playing_song) #the error is cause the curselection fuction get the name of the song instead of numberical value therefore the error
    mut_song=MP3(playing_song_name)
    #song length 
    global song_length
    song_length=mut_song.info.length
    converted_song_time= time.strftime('%M:%S',time.gmtime(song_length))
    current_time +=1
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time elapsed: {converted_song_time} of {converted_song_time}'  )
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        #slider hasnt moved 
        slider_position=int(song_length)
    
        my_slider.config(to=slider_position,value=int(current_time))
    else:
        slider_position=int(song_length)
    
        my_slider.config(to=slider_position,value=int(my_slider.get()))
        converted_time= time.strftime('%M:%S',time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'Time elapsed: {converted_time} of {converted_song_time}'  )

        next_time=int(my_slider.get()) + 1
        my_slider.config(value=next_time)
        







        status_bar.config(text=f'Time elapsed: {converted_time} of {converted_song_time}'  )
    





    #my_slider.config(value=int(current_time))
    #status_bar.config(text=converted_time)
   

    #update every 1000ms 
    status_bar.after(1000,time_info)

    

def open_folder():
    
     #funtion use for locating the folder to be used 
    
    path=filedialog.askdirectory()
    if path:
        os.chdir(path)
        #check if the folder/dir have MP3 files or not 
        mp3_files = [file for file in os.listdir(path) if file.endswith(".mp3")]
        
        if len(mp3_files) == 0:
            lable.config(text="No MP3 files in this folder")
        songs=os.listdir(path)
       
        #for loop for adding the files/items with ending of MP3
        for song in songs: 
            
            if song.endswith('.mp3'):
               
                box.insert(END,song)
                lable.config(text="")
    
#clear box function    
def clear_box():
    end_index=box.index('end')
    if end_index != 0:
        box.delete(0,END)
        stop_song()
#pause fuction 
global paused
paused = False
def pause_song(is_paused):
    global paused
    paused=is_paused

    if paused:
        mixer.music.unpause()
        paused=False
        pause_btn.config(text="PAUSE")
    else:
        mixer.music.pause()
        paused=True
        pause_btn.config(text="RESUME")

    


#fuction for playing the selected songs           
def play_song():  
    
    lable.config(text=box.get(ACTIVE))
    mixer.music.load(box.get(ACTIVE))
    mixer.music.play(loops=0)
    #activate the time_info fuction everytime we start a new song so we get the elaspsed time of it 
    time_info()

    #slider_position=int(song_length)
    my_slider.config(value=0)
global stopped
stopped= False

def Delete_song():
    delete_song=box.curselection()
    if delete_song:
        box.delete(delete_song)
    stop_song()    

#function to stop the song 
def stop_song():
    mixer.music.stop()
    box.select_clear('active')
    lable.config(text="")
    status_bar.config(text="")
    my_slider.config(value=0)
    pause_btn.config(text="PAUSE")
    # set stop variable to true
    global stopped
    stopped = True
    
# fuction to play the next song 
def next_play():
    next_song=box.curselection()
    my_slider.config(value=0)
    if next_song:
        next_song=next_song[0]+1
        next_song_name=box.get(next_song)
        lable.config(text= next_song_name)
        mixer.music.load(next_song_name)
        mixer.music.play()
        box.selection_clear(0,END)
        box.activate(next_song)
        box.select_set(next_song,last=None)
    else:
        lable.config(text= "No more songs")
        box.selection_clear(0,END)
#function to play the previous song         
def prev_play():
       
    prev_song=box.curselection()
    my_slider.config(value=0)
    if prev_song: 
        prev_song=prev_song[0]-1
        prev_song_name=box.get(prev_song)
        lable.config(text= prev_song_name)
        mixer.music.load(prev_song_name)
        mixer.music.play()
        box.selection_clear(0,END)
        box.activate(prev_song)
        box.select_set(prev_song,last=None)
    else:
        lable.config(text= "No more songs")
        box.selection_clear(0,END)
#slider get 
def slide(x):
    #lider_lable.config(text=f'{int(my_slider.get())} of {int(song_length)}')    
    mixer.music.load(box.get(ACTIVE))
    mixer.music.play(loops=0,start=int(my_slider.get()))  
def music_volume(y):
    mixer.music.set_volume(volume_slider.get())
  
    

#Playlist box 
my_frame=Frame(canvas)
my_scrollbar=Scrollbar(my_frame,orient=VERTICAL)

box=tk.Listbox(my_frame,fg='#00db00',bg='black',width="100",yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=box.yview)
my_scrollbar.pack(side=RIGHT,fill=Y)
box.pack(padx="15",pady="15")
my_frame.pack()
my_frame.place(x=10,y=70)
#box.place(x=30,y=70)

#lable box of the song playing
lable=tk.Label(canvas, bg="#eeeeee",fg="#00db00",font=(18))
lable.pack(padx=5,pady=5, anchor='center')
lable.place(x=100,y=290)


#frame for the Control buttons
control_panel=tk.Frame(canvas,bg='#eeeeee')
control_panel.pack(padx=5,pady=5, anchor='center')
control_panel.place(x=180,y=380)
#previous button
prev_btn=Button(canvas, text='PREV',command=prev_play)
prev_btn.pack(padx=10, in_=control_panel, side= 'left')
#next button
next_btn=Button(canvas, text='NEXT', command=next_play)
next_btn.pack(padx=10, in_=control_panel, side= 'left')
#stop button
stop_btn=Button(canvas, text='STOP',command=stop_song)
stop_btn.pack(padx=10, in_=control_panel, side= 'left')
#start button
start_btn=Button(canvas, text='START',command=play_song)
start_btn.pack(padx=10, in_=control_panel, side= 'left')

 
pause_btn=Button(canvas, text='PAUSE',command= lambda: pause_song(paused) )
pause_btn.pack(padx=10, in_=control_panel, side= 'right')
#clear box
clear_btn=Button(canvas, text='Clear',width=15,height=2,font=("arial",10,"bold"),fg="white",bg="#5c5757",command=clear_box).place(x=200, y=20)
#delete song 
Delete_btn=Button(canvas, text='Delete song',width=15,height=2,font=("arial",10,"bold"),fg="white",bg="#5c5757",command=Delete_song).place(x=380, y=20)


#locate folder button 
btn=Button(canvas,text='Open Folder',width=15,height=2,font=("arial",10,"bold"),fg="white",bg="#5c5757",command=open_folder).place(x=30, y=20) #Button to locate thefolder where the files are stored 
#status bar
status_bar=Label(canvas,text='',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)


#music slider 
my_slider=ttk.Scale(canvas,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=500)
my_slider.pack()
my_slider.place(x=80,y=480)

#Volume slider
volume_slider_text=Label(canvas,text="Volume:")
volume_slider_text.pack()
volume_slider_text.place(x=30,y=520)
volume_slider=ttk.Scale(canvas,from_=0,to=1,orient=HORIZONTAL,value=1,command=music_volume,length=100)
volume_slider.pack()
volume_slider.place(x=90, y=520)





canvas.mainloop()