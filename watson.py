from watson_developer_cloud import SpeechToTextV1, DiscoveryV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud.tone_analyzer_v3 import ToneInput
from watson_developer_cloud import PersonalityInsightsV3
import user_err

def run_watson(wav_path: str) -> dict:
    language = 'US-EN'
    model_dict = {'US-EN': 'en-US_BroadbandModel', 'UK-EN': 'en-UK-BroadbandModel'}

    speech_to_text, tone_analyzer, personality_analyzer = initiate_watson()
    
    text = ''

    for i in range(5):
        wav_path = 'joe' + str(i + 1) +'.wav'
        words = transcribe_audio(speech_to_text, wav_path, model_dict, language)
        text = text +  words + ' '

    user_err.check_word_count(text)
    

    results = get_insights(tone_analyzer, personality_analyzer, text)

    return text, results
    

def get_insights(tone_analyzer, personality_analyzer, text: str) -> dict:

    tones = tone_analyzer.tone(
        tone_input = text, 
        tones = ['emotion', 'language', 'social'], 
        content_type="text/plain").get_result()['document_tone']['tone_categories']

    profile = personality_analyzer.profile(
        text,
        content_type='text/plain',
        consumption_preferences=True,
        raw_scores=True).get_result()

    output = dict()
    
    for i in range(len(tones)):
        for j in range(len(tones[i]['tones'])):
            temp = tones[i]['tones'][j]
            output['tone_' + temp['tone_id']] = temp['score']

    feats = ['personality','needs','values']
    for feat in feats:
        for i in range(len(profile[feat])):
            temp = profile[feat][i]
            output[temp['trait_id']+'_raw'] = temp['raw_score']
            output[temp['trait_id']+ '_percentile'] = temp['percentile']
            output[temp['trait_id']+ '_significant'] = temp['significant']
            if feat == 'personality':
                for j in range(len(temp['children'])):
                    temp_c = temp['children'][j]
                    output[temp_c['trait_id']+'_raw'] = temp_c['raw_score']
                    output[temp_c['trait_id']+'_percentile'] = temp_c['percentile']
                    output[temp_c['trait_id']+'_significant'] = temp_c['significant']

    return output


def initiate_watson():
    """Establishes connection with API
    """
    watson_dict = {
        'ibm_api': 'kzL_ZWnn4T0xxQ_A6bUTBdqdh7yvljTJsWO2qraw-nDa', 
        'ibm_url': 'https://stream.watsonplatform.net/speech-to-text/api', 
        'ibm_version': '2018-08-01', 
        'ibm_api_ta': 'I5yNi3pszexgabF6cCc4BIM1_QS5Fm63jAwnnDGl7j-j', 
        'ibm_url_ta': 'https://gateway.watsonplatform.net/tone-analyzer/api', 
        'ibm_version_ta': '2016-05-19', 'ibm_api_per': 'VwVF3pMl1j_OWcKbKTB_teau5OA4hSj3KSizWYTXIrRQ', 
        'ibm_url_per': 'https://gateway.watsonplatform.net/personality-insights/api', 
        'ibm_version_per': '2017-10-13'}

    speech_to_text = SpeechToTextV1(iam_apikey=watson_dict['ibm_api'])    

    tone_analyzer = ToneAnalyzerV3(
        url = watson_dict['ibm_url_ta'],
        version = watson_dict['ibm_version_ta'],
        iam_apikey = watson_dict['ibm_api_ta'])

    personality_analyzer = PersonalityInsightsV3(
        version = watson_dict['ibm_version_per'],
        url = watson_dict['ibm_url_per'],
        iam_apikey = watson_dict['ibm_api_per'])

    tone_analyzer.set_detailed_response(True)

    return speech_to_text, tone_analyzer, personality_analyzer


def transcribe_audio(speech_to_text, wav_path: str, model_dict: dict, language: str):
    
    audio_file = open(wav_path, 'rb')
    speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/wav',
        model=model_dict[language],
        word_confidence=False,
        timestamps = False,
        smart_formatting=False,
        interim_results=False,
        speaker_labels = False).get_result()
    audio_file.close()    

    text = ''
    spoken = speech_recognition_results['results']

    for i in range(len(spoken)):
        text = text + spoken[i]['alternatives'][0]['transcript']

    text = text.replace('%HESITATION', '')
    text = text.replace('  ', ' ')

    return text