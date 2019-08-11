# -*- coding: utf-8 -*-
import custom_errors as ERR

def check_word_count(text: str):
    if len(text.split(' ')) < 600:
        raise ERR.UserErr("We need you to give some more detailed answers for this to work. Please try again.")
    return 
    