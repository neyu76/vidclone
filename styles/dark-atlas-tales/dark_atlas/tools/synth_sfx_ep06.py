"""synth_sfx_ep06.py — EP06 La Mala Hora signature SFX, synthesised locally (no credits) because no Magnific connector
was available on 22/11/2026. Replace with Magnific/ElevenLabs versions later if the user wants (quote: 8 s = 40 credits).
Usage: python -I synth_sfx_ep06.py <dark_atlas_dir>
Writes assets/sfx/ep06_la_mala_hora/{church_bell_toll_single, mala_hora_breath_rasp, rebozo_rustle_gravel}.mp3
"""
import sys, os, subprocess, numpy as np, scipy.signal as ss
SR = 44100
ROOT = sys.argv[1]; OUT = os.path.join(ROOT, "assets", "sfx", "ep06_la_mala_hora"); os.makedirs(OUT, exist_ok=True)
LIB = os.path.join(ROOT, "assets", "sfx")
rng = np.random.default_rng(6)

def save(name, x):
    x = x / (np.abs(x).max() + 1e-9) * 0.89
    tmp = os.path.join(OUT, name + ".wav")
    import wave
    w = wave.open(tmp, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-b:a", "160k", os.path.join(OUT, name + ".mp3")], check=True); os.remove(tmp)
    print("wrote", name, round(len(x) / SR, 2), "s")

def load(path, pitch=0.0):
    af = [f"asetrate={SR}*{2 ** (pitch / 12):.5f},aresample={SR}"] if pitch else []
    cmd = ["ffmpeg", "-v", "error", "-i", path] + (["-af", ",".join(af)] if af else []) + ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()

def reverb(x, secs=2.2, wet=0.35):
    n = int(secs * SR); ir = rng.normal(0, 1, n) * np.exp(-np.linspace(0, 7, n)); ir = ss.lfilter(*ss.butter(2, 4000 / (SR / 2)), ir)
    y = ss.fftconvolve(x, ir); y = np.pad(y, (0, max(0, len(x) + n - len(y))))[: len(x) + n]; y = y / (np.abs(y).max() + 1e-9) * np.abs(x).max()
    return np.pad(x, (0, n)) * (1 - wet) + y * wet

# 1) single deep toll of an old church bell: inharmonic partials (hum, prime, tierce, quint, nominal ...) + strike
t = np.arange(int(4.0 * SR)) / SR; f0 = 146.8
bell = np.zeros_like(t)
for ratio, amp, dec in ((0.5, 0.9, 0.6), (1.0, 1.0, 0.9), (1.19, 0.6, 1.3), (1.5, 0.45, 1.7), (2.0, 0.7, 1.4), (2.52, 0.35, 2.4), (3.0, 0.25, 3.0), (4.17, 0.18, 4.0)):
    det = 1 + rng.uniform(-0.002, 0.002)
    bell += amp * np.sin(2 * np.pi * f0 * ratio * det * t + rng.uniform(0, 6.28)) * np.exp(-t * dec) * (1 + 0.08 * np.sin(2 * np.pi * 1.3 * t))
strike = rng.normal(0, 1, len(t)) * np.exp(-t * 60) * 0.4
save("church_bell_toll_single", reverb(bell + strike, 1.8, 0.3))

# 2) La Mala Hora's own sound: slow raspy ghostly exhale (formant-filtered noise, pulsed rasp) + the library whisper pitched down
n = int(2.8 * SR); t = np.arange(n) / SR
noise = rng.normal(0, 1, n)
rasp = noise * (0.55 + 0.45 * np.sign(np.sin(2 * np.pi * (38 + 6 * t) * t)))                 # vocal-fry like pulses
vox = np.zeros(n)
for fc, bw, g in ((520, 140, 1.0), (980, 220, 0.7), (2450, 400, 0.45), (3300, 500, 0.25)):
    b, a = ss.butter(2, [(fc - bw) / (SR / 2), (fc + bw) / (SR / 2)], btype="band"); vox += g * ss.lfilter(b, a, rasp)
env = np.minimum(1, t / 0.25) * np.exp(-np.maximum(0, t - 0.4) * 1.1)
vox *= env
try:
    wh = load(os.path.join(LIB, "horror", "whispers.mp3"), -6)[:n]; wh = np.pad(wh, (0, n - len(wh))) * np.minimum(1, t / 0.4) * np.exp(-t * 0.7)
    vox = vox / (np.abs(vox).max() + 1e-9) + 0.55 * wh / (np.abs(wh).max() + 1e-9)
except Exception as e:
    print("whisper layer skipped:", e)
save("mala_hora_breath_rasp", reverb(vox, 1.2, 0.25))

# 3) heavy dark shawl rustling in the wind + slow footsteps on dry gravel
n = int(2.5 * SR); t = np.arange(n) / SR
fab = ss.lfilter(*ss.butter(2, [900 / (SR / 2), 6000 / (SR / 2)], btype="band"), rng.normal(0, 1, n))
mod = np.abs(ss.lfilter(*ss.butter(1, 6 / (SR / 2)), rng.normal(0, 1, n))); fab *= mod / (mod.max() + 1e-9)
steps = np.zeros(n)
for st in (0.35, 1.15, 1.95):
    i = int(st * SR)
    for _ in range(40):
        j = i + int(rng.uniform(0, 0.12) * SR); L = int(0.004 * SR)
        if j + L < n: steps[j:j + L] += rng.normal(0, 1, L) * np.exp(-np.linspace(0, 6, L)) * rng.uniform(0.3, 1.0)
steps = ss.lfilter(*ss.butter(2, [400 / (SR / 2), 5000 / (SR / 2)], btype="band"), steps)
save("rebozo_rustle_gravel", 0.6 * fab / (np.abs(fab).max() + 1e-9) + steps / (np.abs(steps).max() + 1e-9))
