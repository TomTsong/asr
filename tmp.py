import datetime

import arrow
import os
import torch
import whisper
import pandas as pd
import threading


def sr(filepath, model_type="base", start_time=None, device="cpu"):
    # device = torch.device(device)
    model = whisper.load_model(model_type)
    if start_time:
        now = arrow.get(start_time)
    else:
        now = arrow.now()
    # # load audio and pad/trim it to fit 30 seconds
    # audio = whisper.load_audio(filepath)
    # audio = whisper.pad_or_trim(audio, )
    #
    # # make log-Mel spectrogram and move to the same device as the model
    # mel = whisper.log_mel_spectrogram(audio).to(device)
    #
    # # detect the spoken language
    # _, probs = model.detect_language(mel)
    # print(f"Detected language: {max(probs, key=probs.get)}")
    #
    # # decode the audio
    # options = whisper.DecodingOptions(fp16=False)
    # print(options)
    # result = whisper.decode(model, mel, options)
    # print the recognized text
    # print(result.text)
    result = model.transcribe(filepath, fp16=False, language="Chinese")
    for segment in result["segments"]:
        start = now.shift(seconds=segment["start"]).format("YYYY-MM-DD HH:mm:ss")
        end = now.shift(seconds=segment["end"]).format("YYYY-MM-DD HH:mm:ss")
        print("【" + start + "->" + end + "】：" + segment["text"])

    return result


def recognize(file):
    model = whisper.load_model("large")
    for i in range(100):
        p, ext = file.rsplit(".", 1)
        new_file = f"{p}-{i + 1}.{ext}"
        model.transcribe(new_file, language="Chinese", verbose=True)


def multi(files):
    model = whisper.load_model("large", device="cpu")
    model.share_memory()
    ts = [
        threading.Thread(target=model.transcribe, args=(f,), kwargs={"language": "Chinese", "verbose": True})
        for f in files
    ]
    for t in ts:
        t.start()

    for t in ts:
        t.join()


def rrr(model, file):
    print(id(model), file)
    model.transcribe(file, language="Chinese", verbose=True)



def multi2(files):
    model = whisper.load_model("large", device=None)
    model.share_memory()
    ps = []
    for f in files:
        # p = torch.multiprocessing.Process(
        #     target=model.transcribe,
        #     args=(f,),
        #     kwargs={"language": "Chinese", "verbose": True}
        # )
        p = torch.multiprocessing.Process(target=rrr, args=(model, f))
        p.start()
        ps.append(p)

    for p in ps:
        p.join()


if __name__ == "__main__":
    # path = "/Users/congdaxia/tools/multi_download"
    # # filename = "20230221_114814.m4a"
    # # filename = "c939df1d243791579861068255-f0.aac"
    # filename = "802d7181243791579853455483-f0.aac"
    # # filename = "de47bddc243791579844314367-f0.aac"
    # # filename = "9ad90acb243791579843745789-f0.aac"
    # # filename = "654b9fbd243791579863135582-f0.aac"
    # # filename = "20230221_155642.m4a"
    # filepath = os.path.join(path, filename)
    # print(filepath)
    # result = sr(filepath, "base")
    # # print(dir(result))
    # # print(result["text"])
    # file = "./download/9ad6ba91243791579843741011-f0-13.aac"
    # # recognize(file)
    # now = datetime.datetime.now()
    # print(now)
    # # sr(file, "large")
    # sr(file, "large")
    # end = datetime.datetime.now()
    # print(end)
    # print(end - now)

    fs = [
        "./download/20230221_114814.m4a",
        "./download/1.m4a",
        "./download/2.m4a",
        "./download/3.m4a",
    ]
    now = datetime.datetime.now()
    print(now)
    # multi(fs)
    multi2(fs)
    end = datetime.datetime.now()
    print(end)
    print(end - now)

