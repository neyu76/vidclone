"""Narration: words with timestamps (faster-whisper), pace, pauses, sentences, hook."""
import os, re, numpy as np
from .common import dist, save, load

MODEL = os.environ.get('VIDCLONE_WHISPER', 'small')

def transcribe(wav16, out_json, script=None):
    if os.path.exists(out_json): return load(out_json)
    from faster_whisper import WhisperModel
    import soundfile as sf
    m = WhisperModel(MODEL, device='cpu', compute_type='int8')
    pcm, _ = sf.read(wav16, dtype='float32')  # 16 kHz mono; avoids faster-whisper's PyAV decoder
    segs, info = m.transcribe(pcm, word_timestamps=True, vad_filter=True,
                              initial_prompt=script[:800] if script else None)
    words = []
    for s in segs:
        for w in s.words or []:
            words.append({'w': w.word.strip(), 's': round(w.start, 3), 'e': round(w.end, 3), 'p': round(w.probability, 3)})
    r = {'language': info.language, 'lang_prob': round(info.language_probability, 3), 'words': words}
    save(r, out_json)
    return r

def analyze(tr, dur):
    W = tr['words']
    if len(W) < 5:
        return {'has_speech': False, 'language': tr.get('language')}
    text = ' '.join(w['w'] for w in W)
    span = W[-1]['e'] - W[0]['s']
    gaps = [b['s'] - a['e'] for a, b in zip(W, W[1:])]
    # sentences: split after words ending with . ! ?
    sents, cur = [], []
    for w in W:
        cur.append(w)
        if re.search(r'[.!?]["\')\]]?$', w['w']):
            sents.append(cur); cur = []
    if cur: sents.append(cur)
    S = [{'s': x[0]['s'], 'e': x[-1]['e'], 'n': len(x), 'text': ' '.join(w['w'] for w in x)} for x in sents]
    hook = S[:1]
    while len(hook) < len(S) and hook[-1]['e'] < 2.5: hook.append(S[len(hook)])
    closer = S[-1]
    words_per_s = np.histogram([w['s'] for w in W], bins=np.arange(0, dur + 1, 1.0))[0]
    return {
        'has_speech': True, 'language': tr['language'],
        'word_count': len(W), 'text': text,
        'wpm': round(len(W) / span * 60, 1),
        'speech_start': W[0]['s'], 'speech_end': W[-1]['e'], 'tail_after_speech': round(dur - W[-1]['e'], 2),
        'speech_coverage': round(sum(w['e'] - w['s'] for w in W) / dur, 3),
        'pause_count_per_min': round(sum(g > 0.25 for g in gaps) / span * 60, 1),
        'pause_len': dist([g for g in gaps if g > 0.25]),
        'longest_pause': round(max(gaps), 2) if gaps else 0,
        'sentence_words': dist([s['n'] for s in S]),
        'sentences': S,
        'hook': {'text': ' '.join(s['text'] for s in hook), 'words': sum(s['n'] for s in hook), 'end': hook[-1]['e']},
        'closer': {'text': closer['text'], 'words': closer['n']},
        'questions': sum(s['text'].strip().endswith('?') for s in S),
        'second_person': sum(1 for w in W if re.sub(r'\W', '', w['w'].lower()) in ('you', "you're", 'your', 'youre')),
        'words_per_second': [int(x) for x in words_per_s],
    }
