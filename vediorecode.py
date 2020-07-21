# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 14:24:22 2020

@author: Jeff-Tesi
"""
import shutil
from mhmovie.code import * 
#import numpy as np
import cv2 as cv
import datetime
#import sys
import os
import pyaudio
import wave
from moviepy.editor import *
from moviepy.audio.fx import all
import time

#回傳錄音狀態
def callback(in_data, frame_count, time_info, status):
    wf.writeframes(in_data)
    if recording :
        return (in_data, pyaudio.paContinue)
    else:
        return (in_data, pyaudio.paComplete)
    
def combine_audio(vidname, audname, outname, fps=25):
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps=fps)
def time_count(time_now,time_old): 
    return int((time_now-time_old).seconds)

frist_open=False    
CHUNK=1024
FORMAT=pyaudio.paInt16
CHANNELS =1
RATE =44100
p=pyaudio.PyAudio()

#print("*recording")
cap =cv.VideoCapture(1 + cv.CAP_DSHOW)
#frame_size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),
#int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
#print(frame_size)
#print(cv.CAP_PROP_FPS)

print("歡迎來到智能監視系統")
print("請輸入你的webcam長寬值")
print("備註:輸入的長寬值不一定符合你的webcam需求")
hight=input("長: ")
weight=input("寬: ")
cap.set(3,float(hight))
cap.set(4,float(weight))
cap.set(5, 60.0)

if cap.get(3)!=hight:
    print("無法符合你的要求")
    print("自動幫你轉換成相近的需求")
    print("長: ",hight,"=> ",cap.get(3))
    print("寬: ",weight,"=> ",cap.get(4))
    hight=cap.get(3)
    weight=cap.get(4)
    
outputFolder_video = "video"
outputFolder_Screenshots="Screenshots"
outputFolder_audio="audio"
combine_audio_video="DICM"

outputCounter_video =0
outputCounter_Screenshots =0
outputCounter_audio=0
combine_audio_video_counter=0
#影像檔案格式 .mp4 (備註:這裡使用小寫)
fourcc =cv.VideoWriter_fourcc(*'mp4v')
#偵測是否第一次錄影，方便座次放資源使用
recording = False
#檢測攝像頭是否開啟or別的程式占用
check_time=0


record_text=False
record_text_count=0

def check_Folder():
    global outputCounter_video, outputCounter_Screenshots,outputCounter_audio,combine_audio_video_counter
    if not os.path.exists(outputFolder_video):
        try:
            os.makedirs(outputFolder_video)
        except:
            print("can't not makedirs folder : ",outputFolder_video)
    else:
        #try:
            all_file_list = os.listdir("./%s"%(outputFolder_video)) 
            #print(all_file_list)
            for file_name in all_file_list:
                p#rint(file_name)
                fname_list = file_name.split('.')
                fname_list=str(fname_list[0])
                if fname_list[:4]=="DICM":
                    #print("88888888888")
                    continue
                #print(fname_list)

                outputCounter_video=int(fname_list[-4:])+1
                #print(outputCounter_video)
           
        #except :
            #print("ERROR")            
    if not os.path.exists(outputFolder_Screenshots):
        try:
            os.makedirs(outputFolder_Screenshots)
        except:
            print("can't not makedirs folder : ",outputFolder_Screenshots)
    else:
        all_file_list = os.listdir("./%s"%(outputFolder_Screenshots))
        for file_name in all_file_list :
            fname_list = file_name.split('.')
            fname_list=str(fname_list[0])
            outputCounter_Screenshots=int(fname_list[-4:])+1
        
    if not os.path.exists(outputFolder_audio):
        try:
            os.makedirs(outputFolder_audio)
        except:
            print("can't not makedirs folder : ",outputFolder_audio)
    else:
        all_file_list = os.listdir("./%s"%(outputFolder_audio))
        for file_name in all_file_list :
            fname_list = file_name.split('.')
            fname_list=str(fname_list[0])
            outputCounter_audio=int(fname_list[-4:])+1
    if not os.path.exists(combine_audio_video):
        try:
            os.makedirs(combine_audio_video)
        except :
            print("test")
    else:
        all_file_list = os.listdir("./%s"%(combine_audio_video))
        for file_name in all_file_list :
            fname_list = file_name.split('.')
            fname_list=str(fname_list[0])
            combine_audio_video_counter=int(fname_list[-4:])+1
check_Folder()
time_old=datetime.datetime.now()
while cap.isOpened():
    ret,frame=cap.read()
    if not ret:
        print("Cant receive frame (stream end ?).Wait...,check time= %d ,(max =3)" %(check_time))
        time.sleep(2)
        check_time+=1
        if check_time ==3:
            print("ERROR,Please check your camera connect")
            print("program Exit....")
            cap.release()
            p.terminate()
            break
        continue
    #預設字體
    font=cv.FONT_HERSHEY_SIMPLEX
    #攝像頭轉向
    frame=cv.flip(frame ,90)
    #取得現在時間
    datatime_old=datetime.datetime.now()
    #轉換自訂時間格式格式
    datatime_new=datatime_old.strftime("%Y/%m/%d %H:%M:%S")
    #轉換成字串輸出
    datet= str(datatime_new)
    #改寫照片(加時間)
    frame = cv.putText(frame,datet,(10,40),font,0.7,(0,255,255),2,cv.LINE_AA)
    
    
    if recording :
        out.write(frame)
        time_now=datetime.datetime.now()
        
       # print("now :",time_now,"old :",time_old)
       # print( time_count(time_now,time_old))
        if time_count(time_now,time_old)>=1:
            
            time_old=time_now
            if record_text==True:
                record_text=False
            else:
                record_text=True
    if record_text :
        #print("recording...")
        frame = cv.putText(frame,"recording...",(360,40),font,0.7,(0,255,255),2,cv.LINE_AA)
    cv.imshow('frame',frame)   
    if(cv.waitKey(1)&0xFF)==ord('r'):
        #print("你按了r鍵")
        #print(recording)
        if recording :
            record_text=False
            print("結束錄影")
            #print(recording)
            recording=False
            while stream.is_active():
                time.sleep(1)
            print("影片存在於","%s/output_%04d.mp4"% (outputFolder_video, outputCounter_video))
            
            out.release() 
            stream.stop_stream()
            print("音樂存在於","%s/output_%04d.wav"% (outputFolder_audio, outputCounter_audio))            
            #stream.close()
            #p.terminate()
            print("video audio merge!!!!!")
            #audioclip = AudioFileClip("%s/output_%04d_.wav"% (outputFolder_voice, outputCounter_voice))          
            # =  VideoFileClip("%s/output_%04d.mp4"% (outputFolder, outputCounter_movie))
            #videoclip = videoclip.set_fps(9.5) 
            #audioclip2 = CompositeAudioClip([audioclip])
            #videoclip.audio=audioclip2
            #videoclip.set_audio(audioclip)
            #videoclip2 = videoclip.set_audio(audioclip)
            #videoclip2=videoclip2.speed
            #video = CompositeVideoClip([videoclip2]).set_audio("%s/output_%04d_.wav"% (outputFolder_voice, outputCounter_voice))
            #if not os.path.exists(My_video_output):
                #os.makedirs(My_video_output)
            #videoclip.write_videofile("%s/video_%04d.mp4"% (My_video_output, outputCounter_video))
            #audio="%s/output_%04d_.wav"% (outputFolder_voice, outputCounter_voice),codec='mpeg4',audio_codec='‘pcm_s16le'
            m=movie("%s/output_%04d.mp4"% (outputFolder_video, outputCounter_video))
            mu=music("%s/output_%04d.wav"% (outputFolder_audio, outputCounter_audio))
            #final=folder('\\my_vedio')
            final=m+mu
            final.save("%s_"%(combine_audio_video)+"%04d"%(combine_audio_video_counter)+".mp4" )
            #video_file=os.path.join(os.getcwd(),"$s"% (outputFolder)+"/movie_"+"%04d"%(outputCounter_video)+".mp4")
            
            #print (os.sep("\\"))
            #print(os.path.dirname("./"))
            try:
                #os.chdir("./"+outputFolder)
                #print(os.getcwd())
                #os.path.isfile("%s\\movie_%04d.mp4"% (outputFolder, outputCounter_video))
                #print("文件已存在")
                #file1="./%s/movie_%04d.mp4"% (outputFolder, outputCounter_movie)
                #print(file1)
                shutil.move("./%s"%(outputFolder_video)+"/%s_"%(combine_audio_video)+"%04d.mp4"% (outputCounter_video),"./%s"%(combine_audio_video))
                print("merge success. Creat in %s/%s_%s.mp4"%(combine_audio_video,combine_audio_video,outputCounter_video))
            except :
                print("ERROR, can't not merge ")
            #My_video_output + "\\" + "output_%04d"%(outputCounter_movie) + ".mp4"
            #final.clear()
            #print("852")
            
            
            outputCounter_video+=1
            outputCounter_audio+=1
            combine_audio_video_counter+=1
        else:
            print("開始錄影")
            frist_open=True
            #print(recording)

           
            wf = wave.open("%s/output_%04d.wav"% (outputFolder_audio, outputCounter_audio), 'wb') 
            wf.setnchannels(CHANNELS) 
            wf.setsampwidth(p.get_sample_size(FORMAT)) 
            wf.setframerate(RATE) 
            stream=p.open(format=FORMAT, 
              channels=CHANNELS,
              rate=RATE,
              input=True,
              stream_callback=callback)

            out =cv.VideoWriter("%s/output_%04d.mp4"% (outputFolder_video, outputCounter_video),fourcc,15,(int(hight),int(weight)))    
            
            recording =True
            stream.start_stream()
            #stream.start_stream()
            #print(recording)
           # out.write(frame)
           # data = stream.read(CHUNK)
           # frames.append(data)
            
    if(cv.waitKey(1)& 0xFF)==ord('q'):
        if not frist_open :
            cap.release()
            cv.destroyAllWindows()
            p.terminate()
           
        else:
            out.release()
            stream.close()
            cap.release()
            cv.destroyAllWindows()
            wf.close()
            p.terminate()
            os.close
            
            #audioclip.close()
            #videoclip.close()
            #videoclip2.close()
            #video.close()
        print("關閉程式")
        
        break
    if(cv.waitKey(1) & 0xFF)==ord('s'):
        print("截圖中.....")
        #if not os.path.exists(outputpicture):
                #os.makedirs(outputpicture)
        cv.imwrite("%s/output_%04d.jpg"% (outputFolder_Screenshots, outputCounter_Screenshots),frame)
        print("圖片存在於","%s/output_%04d.jpg"% (outputFolder_Screenshots, outputCounter_Screenshots))
        outputCounter_Screenshots+=1
       # print(frame_size)
       # print("長 :",cap.get(3))
       # print("寬 :",cap.get(4))
        print("fps :",cap.get(5))


