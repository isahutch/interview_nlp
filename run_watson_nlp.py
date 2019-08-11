# -*- coding: utf-8 -*-
import os
import media
from . import user_err
from . import watson


def run_challenge_5(path:str, vertical:bool) -> dict:
    """Run challenge 5 (interview)

    =args=
        -path: path to interview video
    =returns= 
        -dictionary containing spoken words as string and nested dict containing evaluation (watson assessment of personality and tone)
    """

    #Save wav to same path as video 
    wav_path = media.convert_mov_to_wav(path)

    #Run full IBM analysis on wav file
    spoken_words, evaluation = watson.run_watson(wav_path)

    return {'interview_transcript': spoken_words, 'ibm_evaluation': evaluation}
