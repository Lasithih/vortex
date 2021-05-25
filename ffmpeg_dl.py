import logging
import ffmpeg

def video_trim(start_time, end_time, video_input, audio_input, output):
    try: 
        durationSeconds = end_time - start_time
        main_video = ffmpeg.input(video_input)
        main_audio = ffmpeg.input(audio_input)
        
        v1 = main_video.video.filter('trim', start = start_time, duration=durationSeconds)
        v1 = ffmpeg.setpts(v1,'PTS-STARTPTS')
        a1 = main_audio.audio.filter('atrim', start = start_time, duration=durationSeconds).filter('asetpts', 'PTS-STARTPTS')

        joined = ffmpeg.concat(v1, a1, v=1, a=1).node

        outputStream = ffmpeg.output(joined[0], joined[1], output)
        outputStream.run()
    except Exception as e:
        logging.error("Error while trimming video_trim(start_time, end_time, input, output). Exception:{}".format(str(e)))
        raise e

def audio_trim(start_time, end_time, input, output):
    try:
        durationSeconds = end_time - start_time
        main_video = ffmpeg.input(input)

        a1 = main_video.audio.filter('atrim', start = start_time, duration=durationSeconds).filter('asetpts', 'PTS-STARTPTS')

        outputStream = ffmpeg.output(a1, output)
        outputStream.run()
    except Exception as e:
        logging.error("Error while trimming audio_trim(start_time, end_time, input, output). Exception:{}".format(str(e)))
        raise e