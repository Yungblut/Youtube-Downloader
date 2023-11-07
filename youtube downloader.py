import customtkinter
from tkinter import ttk, filedialog
from pytube import YouTube, Playlist
from pytube.exceptions import AgeRestrictedError, MembersOnly, VideoPrivate, VideoRegionBlocked, VideoUnavailable
import os
from PIL import ImageTk, Image
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio
import re
         
         
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        def dondeguardar():
          global directory
          directory = filedialog.askdirectory()
          print(directory)


        def descargarmp3():
          url = mp3_frame_link.get()
          print(url)
          video = YouTube(url, use_oauth=False, allow_oauth_cache=True)
          if mp3_frame_esplaylist.get() == 0:              #NO es playlist
            try:
                stream = video.streams.filter(only_audio=True).first()
                VideoTitle =  video.title
                emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
                VideoTitle = emoji_pattern.sub(r'', VideoTitle) # no emoji
                VideoTitle = re.sub('[^A-Za-z0-9 ]+', '', VideoTitle)
                VideoTitle.encode('ascii', 'ignore').decode('ascii')
                #stream.download(output_path=directory, filename=f"{VideoTitle}.mp3") #metodo 1 descargar mp3
                video.streams.get_by_itag(140).download(output_path=directory, filename=f"{VideoTitle} 128k.mp3") #metodo 2 descargar mp3 en 128k
                print(VideoTitle)
                print("DESCARGA COMPLETA")
            except AgeRestrictedError:
                print(f"{video.title} ---- is age restricted.")
            except MembersOnly:
                print(f"{video.title} ---- Video is members-only.")
            except VideoPrivate:
                print(f"{video.title} ---- video privado")
            except VideoRegionBlocked:
                print(f"{video.title} ---- video no disponible para arg")
            except VideoUnavailable:
                print(f"{video.title} ---- video no disponible")
            except Exception:
                print('ERROR DESCONOCIDO')
          else:                            #SI es playlist
            p = Playlist(str(url))
            print(f'Descargando la playlist: {p.title}')
            print('Cantidad de videos: %s' % len(p.video_urls))
            for video in p.videos:
                try:
                  stream = video.streams.filter(only_audio=True).first()
                  VideoTitle =  video.title
                  emoji_pattern = re.compile("["
                  u"\U0001F600-\U0001F64F"  # emoticons
                  u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                  u"\U0001F680-\U0001F6FF"  # transport & map symbols
                  u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
                  VideoTitle = emoji_pattern.sub(r'', VideoTitle) # no emoji
                  VideoTitle = re.sub('[^A-Za-z0-9 ]+', '', VideoTitle)
                  VideoTitle.encode('ascii', 'ignore').decode('ascii')
                  #stream.download(output_path=directory, filename=f"{VideoTitle}.mp3") #metodo 1 descargar mp3
                  video.streams.get_by_itag(140).download(output_path=directory, filename=f"{VideoTitle} 128k.mp3") #metodo 2 descargar mp3 en 128k
                  print(VideoTitle)
                except AgeRestrictedError:
                  print(f"{video.title} ---- is age restricted.")
                except MembersOnly:
                  print(f"{video.title} ---- Video is members-only.")
                except VideoPrivate:
                  print(f"{video.title} ---- video privado")
                except VideoRegionBlocked:
                  print(f"{video.title} ---- video no disponible para arg")
                except VideoUnavailable:
                  print(f"{video.title} ---- video no disponible")
                except Exception:
                  print('ERROR DESCONOCIDO')
            print("DESCARGA COMPLETA")
        
        def descargarvideo() :
          url = video_frame_link.get()
          print(url)
          video = YouTube(url, use_oauth=False, allow_oauth_cache=True)
          if video_frame_esplaylist.get() == 0:              #NO es playlist
            try:
               resolucion = resolmenu.get()
               stream = video.streams.filter(adaptive=True, file_extension='mp4', res=resolucion).first()
               VideoTitle =  video.title
               emoji_pattern = re.compile("["
               u"\U0001F600-\U0001F64F"  # emoticons
               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
               u"\U0001F680-\U0001F6FF"  # transport & map symbols
               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
               VideoTitle = emoji_pattern.sub(r'', VideoTitle) # no emoji
               VideoTitle = re.sub('[^A-Za-z0-9 ]+', '', VideoTitle)
               VideoTitle.encode('ascii', 'ignore').decode('ascii')
               #print(video.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution'))
               stream.download(output_path=directory, filename=f"{VideoTitle}.mp4")
               video.streams.get_by_itag(140).download(output_path=directory, filename="audio.mp3") #itag 140 = 128k
               video_clip = VideoFileClip(os.path.join(directory, f"{VideoTitle}.mp4"))
               audio_clip = AudioFileClip(os.path.join(directory, "audio.mp3"))
               ffmpeg_merge_video_audio(os.path.join(directory, f"{VideoTitle}.mp4"), #metodo 2 para hacer merge de audio y video
                         os.path.join(directory, "audio.mp3"),                        #es muy efectivo 1 hora de video = 1 minuto para merge
                         os.path.join(directory, f"{VideoTitle} {resolucion}.mp4"),
                         vcodec='copy',
                         acodec='copy',
                         ffmpeg_output=False,
                         logger=None)
               #video_clip.audio = audio_clip                             metodo 1 para hacer merge de audio y video
               #video_clip.write_videofile("final.mp4", threads = 8)      el rendimiento es pesimo 11min video = 2 min para merge
               video_clip.close()
               audio_clip.close()
               os.remove(os.path.join(directory, "audio.mp3"))
               os.remove(os.path.join(directory, f"{VideoTitle}.mp4"))
               print(VideoTitle)
               print("DESCARGA COMPLETA")
            except AttributeError:
               resoluciones = str(video.streams.filter(adaptive=True, file_extension='mp4'))
               resolucion='720p'
               if resolucion not in resoluciones:
                    resolucion = '480p'
               if resolucion not in resoluciones:
                    resolucion = '360p'
               if resolucion not in resoluciones:
                    resolucion = '240p'
               if resolucion not in resoluciones:
                    resolucion = '144p'
               #print(resolucion)
               #print(resoluciones)
               stream = video.streams.filter(adaptive=True, file_extension='mp4', res=resolucion).first()
               VideoTitle =  video.title
               emoji_pattern = re.compile("["
               u"\U0001F600-\U0001F64F"  # emoticons
               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
               u"\U0001F680-\U0001F6FF"  # transport & map symbols
               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
               VideoTitle = emoji_pattern.sub(r'', VideoTitle) # no emoji
               VideoTitle = re.sub('[^A-Za-z0-9 ]+', '', VideoTitle)
               VideoTitle.encode('ascii', 'ignore').decode('ascii')
               #print(video.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution'))
               stream.download(output_path=directory, filename=f"{VideoTitle}.mp4")
               video.streams.get_by_itag(140).download(output_path=directory, filename="audio.mp3") #itag 140 = 128k
               video_clip = VideoFileClip(os.path.join(directory, f"{VideoTitle}.mp4"))
               audio_clip = AudioFileClip(os.path.join(directory, "audio.mp3"))
               ffmpeg_merge_video_audio(os.path.join(directory, f"{VideoTitle}.mp4"), #metodo 2 para hacer merge de audio y video
                         os.path.join(directory, "audio.mp3"),                     #es muy efectivo 1 hora de video = 1 minuto para merge
                         os.path.join(directory, f"{VideoTitle} {resolucion}.mp4"),
                         vcodec='copy',
                         acodec='copy',
                         ffmpeg_output=False,
                         logger=None)
               #video_clip.audio = audio_clip                             metodo 1 para hacer merge de audio y video
               #video_clip.write_videofile("final.mp4", threads = 8)      el rendimiento es muy pesimo 11min video = 2 min para merge
               video_clip.close()
               audio_clip.close()
               os.remove(os.path.join(directory, "audio.mp3"))
               os.remove(os.path.join(directory, f"{VideoTitle}.mp4"))
               print(VideoTitle)
               print("DESCARGA COMPLETA")
            except AgeRestrictedError:
               print(f"{video.title} ---- is age restricted.")
            except MembersOnly:
               print(f"{video.title} ---- Video is members-only.")
            except VideoPrivate:
               print(f"{video.title} ---- video privado")
            except VideoRegionBlocked:
               print(f"{video.title} ---- video no disponible para arg")
            except VideoUnavailable:
               print(f"{video.title} ---- video no disponible")
            except Exception:
               print('ERROR DESCONOCIDO')
          else:                            #SI es playlist
            p = Playlist(str(url))
            print(f'Descargando la playlist: {p.title}')
            print('Cantidad de videos: %s' % len(p.video_urls))
            for video in p.videos:
              try:
                 resolucion = resolmenu.get()
                 stream = video.streams.filter(adaptive=True, file_extension='mp4', res=resolucion).first()
                 VideoTitle =  video.title
                 emoji_pattern = re.compile("["
                 u"\U0001F600-\U0001F64F"  # emoticons
                 u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                 u"\U0001F680-\U0001F6FF"  # transport & map symbols
                 u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
                 VideoTitle = emoji_pattern.sub(r'', VideoTitle) # no emoji
                 VideoTitle = re.sub('[^A-Za-z0-9 ]+', '', VideoTitle)
                 VideoTitle.encode('ascii', 'ignore').decode('ascii')
                 #print(video.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution'))
                 stream.download(output_path=directory, filename=f"{VideoTitle}.mp4")
                 video.streams.get_by_itag(140).download(output_path=directory, filename="audio.mp3") #itag 140 = 128k
                 video_clip = VideoFileClip(os.path.join(directory, f"{VideoTitle}.mp4"))
                 audio_clip = AudioFileClip(os.path.join(directory, "audio.mp3"))
                 ffmpeg_merge_video_audio(os.path.join(directory, f"{VideoTitle}.mp4"), #metodo 2 para hacer merge de audio y video
                         os.path.join(directory, "audio.mp3"),                     #es muy efectivo 1 hora de video = 1 minuto para merge
                         os.path.join(directory, f"{VideoTitle} {resolucion}.mp4"),
                         vcodec='copy',
                         acodec='copy',
                         ffmpeg_output=False,
                         logger=None)
                 #video_clip.audio = audio_clip                             metodo 1 para hacer merge de audio y video
                 #video_clip.write_videofile("final.mp4", threads = 8)      el rendimiento es muy pesimo 11min video = 2 min para merge
                 video_clip.close()
                 audio_clip.close()
                 os.remove(os.path.join(directory, "audio.mp3"))
                 os.remove(os.path.join(directory, f"{VideoTitle}.mp4"))
                 print(VideoTitle)
              except AttributeError:
                 resoluciones = str(video.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution'))
                 resolucion='720p'
                 if resolucion not in resoluciones:
                   resolucion = '480p'
                 if resolucion not in resoluciones:
                   resolucion = '360p'
                 if resolucion not in resoluciones:
                   resolucion = '240p'
                 if resolucion not in resoluciones:
                   resolucion = '144p'
                 stream = video.streams.filter(adaptive=True, file_extension='mp4', res=resolucion).first()
                 emoji_pattern = re.compile("["
                 u"\U0001F600-\U0001F64F"  # emoticons
                 u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                 u"\U0001F680-\U0001F6FF"  # transport & map symbols
                 u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                             "]+", flags=re.UNICODE)
                 VideoTitle = emoji_pattern.sub(r'', VideoTitle) # no emoji
                 VideoTitle = re.sub('[^A-Za-z0-9 ]+', '', VideoTitle)
                 VideoTitle.encode('ascii', 'ignore').decode('ascii')
                 print(VideoTitle)
                 #print(video.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution'))
                 stream.download(output_path=directory, filename=f"{VideoTitle}.mp4")
                 video.streams.get_by_itag(140).download(output_path=directory, filename="audio.mp3") #itag 140 = 128k
                 video_clip = VideoFileClip(os.path.join(directory, f"{VideoTitle}.mp4"))
                 audio_clip = AudioFileClip(os.path.join(directory, "audio.mp3"))
                 ffmpeg_merge_video_audio(os.path.join(directory, f"{VideoTitle}.mp4"), #metodo 2 para hacer merge de audio y video
                         os.path.join(directory, "audio.mp3"),                     #es muy efectivo 1 hora de video = 1 minuto para merge
                         os.path.join(directory, f"{VideoTitle} {resolucion}.mp4"),
                         vcodec='copy',
                         acodec='copy',
                         ffmpeg_output=False,
                         logger=None)
                 #video_clip.audio = audio_clip                             metodo 1 para hacer merge de audio y video
                 #video_clip.write_videofile("final.mp4", threads = 8)      el rendimiento es muy pesimo 11min video = 2 min para merge
                 video_clip.close()
                 audio_clip.close()
                 os.remove(os.path.join(directory, "audio.mp3"))
                 os.remove(os.path.join(directory, f"{VideoTitle}.mp4"))
                 VideoTitle =  video.title
              except AgeRestrictedError:
               print(f"{video.title} ---- is age restricted.")
              except MembersOnly:
               print(f"{video.title} ---- Video is members-only.")
              except VideoPrivate:
               print(f"{video.title} ---- video privado")
              except VideoRegionBlocked:
               print(f"{video.title} ---- video no disponible para arg")
              except VideoUnavailable:
               print(f"{video.title} ---- video no disponible")
              except Exception:
               print('ERROR DESCONOCIDO')
            print("DESCARGA COMPLETA")



        #CENTERS THE WINDOW
        app_width = 800
        app_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        self.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        #DESACTIVA RESIZE
        self.resizable(False,False)
        #TITULO
        self.title("Youtube Downloader - Ivan Yungblut - v1.0")
        #TEMATICA COLOR
        customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        #se divide el espacio en una fila horizontal y dos columnas verticales
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        #carga imagenes
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "yt.png")), size=(30, 30))
        self.home_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "home.png")), size=(20, 20))
        self.mp3 = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "audio.png")), size=(20, 20))
        self.video = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "video.png")), size=(20, 20))
        self.live = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "live.png")), size=(20, 20))
        #imagen de la app
        self.iconpath = ImageTk.PhotoImage(file=os.path.join(image_path,"yt.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)
        #crea el nav frame de la izquierda
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="HOME",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.mp3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="MP3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.mp3, anchor="w", command=self.mp3_button_event)
        self.mp3_button.grid(row=2, column=0, sticky="ew")

        self.video_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="VIDEO",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.video, anchor="w", command=self.video_button_event)
        self.video_button.grid(row=3, column=0, sticky="ew")

        self.live_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="LIVE",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.live, anchor="w", command=self.live_button_event, state='disabled')
        self.live_button.grid(row=4, column=0, sticky="ew")

        #boton HOME
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        label = customtkinter.CTkLabel(self.home_frame, text="made w customtkinter, pytube, moviepy", fg_color="transparent")
        label.place(relx=0.05, rely=0.05)

        #boton MP3
        self.mp3_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.mp3_frame.grid_rowconfigure(0, weight=1)
        ###crea tick para playlist
        mp3_frame_esplaylist = customtkinter.CTkCheckBox(master=self.mp3_frame, text="Playlist?")
        mp3_frame_esplaylist.grid(row=0, column=1, pady=30, padx=30, sticky="wn")
        ###ruta guardado
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.carpeta = customtkinter.CTkImage(Image.open(os.path.join(image_path, "carpeta.png")), size=(30, 30))
        self.mp3_frame_guardado = customtkinter.CTkButton(self.mp3_frame, text="Ruta de guardado", image=self.carpeta, compound="right", command=dondeguardar)
        self.mp3_frame_guardado.grid(row=0, column=3, padx=30, pady=23, sticky="en")
        ####crea el texto para pegar el link
        mp3_frame_link = customtkinter.CTkEntry(self.mp3_frame, placeholder_text="Ingresar el URL del vivo/video/playlist de youtube", width=440)
        mp3_frame_link.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        ####crea el boton para descargar
        mp3_frame_download = customtkinter.CTkButton(self.mp3_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Download", command=descargarmp3)
        mp3_frame_download.grid(row=2, column=3, padx=30, pady=(20, 20), sticky="sw")


        #boton VIDEO
        self.video_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.video_frame.grid_rowconfigure(0, weight=1)
        ###crea tick para playlist
        video_frame_esplaylist = customtkinter.CTkCheckBox(master=self.video_frame, text="Playlist?") #command=esplaylist
        video_frame_esplaylist.grid(row=0, column=0, pady=30, padx=30, sticky="wn")
        ###ruta guardado
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.carpeta = customtkinter.CTkImage(Image.open(os.path.join(image_path, "carpeta.png")), size=(30, 30))
        self.video_frame_guardado = customtkinter.CTkButton(self.video_frame, text="Ruta de guardado", image=self.carpeta, compound="right", command=dondeguardar)
        self.video_frame_guardado.grid(row=0, column=1, padx=330, pady=23, sticky="nw")
        ####crea el texto para pegar el link
        video_frame_link = customtkinter.CTkEntry(self.video_frame, placeholder_text="Ingresar el URL del vivo/video/playlist de youtube", width=440)
        video_frame_link.grid(row=1, column=0, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="sw")
        ####crea el boton para descargar
        video_frame_download = customtkinter.CTkButton(self.video_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Download", command=descargarvideo)
        video_frame_download.grid(row=1, column=1, padx=330, pady=(20, 20), sticky="sw")
        ###crea nav para resolucion del video
        resolmenu = customtkinter.CTkOptionMenu(self.video_frame, dynamic_resizing=False,
                                                values=["1080p", "720p", "480p", "360p", "240p", "144p"])
        resolmenu.grid(row=0, column=1, padx=80, pady=28, sticky="nw")


        #boton LIVE
        self.live_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        #FRAME POR DEFAULT
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        #color al seleccionar un frame
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.mp3_button.configure(fg_color=("gray75", "gray25") if name == "mp3" else "transparent")
        self.video_button.configure(fg_color=("gray75", "gray25") if name == "video" else "transparent")
        self.live_button.configure(fg_color=("gray75", "gray25") if name == "live" else "transparent")

        # mostrar el frame clickeado
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "mp3":
            self.mp3_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.mp3_frame.grid_forget()
        if name == "video":
            self.video_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.video_frame.grid_forget()
        if name == "live":
            self.live_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.live_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def mp3_button_event(self):
        self.select_frame_by_name("mp3")

    def video_button_event(self):
        self.select_frame_by_name("video")

    def live_button_event(self):
        self.select_frame_by_name("live")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


app = App()
app.mainloop()