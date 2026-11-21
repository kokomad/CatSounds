# Generates 100 synthetic cat sounds (WAV) + CatSounds.kt. Run: python3 tools/generate_sounds.py
import numpy as np, wave, os
SR = 22050
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app", "src", "main")
RAW = os.path.join(ROOT, "res", "raw"); KT = os.path.join(ROOT, "java", "com", "khader", "catsounds", "CatSounds.kt")
rng = np.random.default_rng(42)

CATS = [
("❤️ حب وسعادة", [
("مواء حنون","😻","meow",480,.8,None,1),("أنا سعيدة","😸","meow",520,.6,[.9,1.2,1.3,1],1),
("صباح الخير","☀️","meow",450,.8,[.8,1,1.2,.9],1),("اشتقت لك","🥰","meow",420,1,[1,1.2,1.1,.9,.8],1),
("حضن دافئ","🤗","purr",28,1.4,None,1),("أحبك","💕","meow",500,.9,[.8,1.1,1.1,1],1),
("شكراً","🙏","trill",400,.35,None,1),("مرحباً يا صديقي","👋","trill",450,.5,None,1),
("فرحة اللقاء","🎉","chirp",600,.4,None,2),("دلع","😽","meow",560,.8,[1,1.3,1.1,1.4],1)]),
("🍽️ جوع وطعام", [
("أنا جائع","🍗","meow",520,1,[.9,1.2,1.2,1,.9],1),("أطعمني الآن","😾","meow",600,.9,[1,1.3,1.4,1.2],1),
("أريد الماء","💧","meow",440,.7,None,1),("وجبة لذيذة","😋","trill",380,.4,None,1),
("أين صحني؟","🥣","meow",500,1.1,[1,.9,1.3,1],1),("سمك!","🐟","chirp",650,.35,None,2),
("حلوى لو سمحت","🍮","meow",580,.8,None,1),("ما زلت جائعة","😿","meow",480,1.1,[1,1.2,.9,1.1,.8],1),
("عشاء متأخر","🌙","meow",400,.9,None,1),("ألحّ بالطلب","🔁","meow",520,.5,None,3)]),
("📢 نداء وانتباه", [
("مياو عالٍ","📣","meow",600,1,None,1),("تعال هنا","👉","meow",520,.7,[.8,1.1,1],1),
("هل من أحد؟","🔔","meow",480,1.2,None,1),("انتبه لي","👀","meow",650,.5,None,1),
("افتح الباب","🚪","meow",500,.6,None,2),("أنا هنا","📍","chirp",550,.35,None,1),
("ناداك القط","📞","meow",460,.9,None,1),("سؤال؟","❓","meow",450,.7,[.8,1,1.3,1.6],1),
("استمع!","👂","meow",700,.4,None,1),("وين رحت؟","🏃","meow",500,.7,None,2)]),
("😾 غضب وتحذير", [
("فحيح","🐍","hiss",0,.9,None,1),("زمجرة منخفضة","😠","growl",90,1.2,None,1),
("ابتعد!","🚫","hiss",0,.5,None,1),("غضب شديد","💢","growl",110,1,[1,1.3,1.1],1),
("تحذير أخير","⚠️","growl",80,1.5,None,1),("أنا غاضبة","😡","growl",130,.9,[1.2,1,.8],1),
("لا تلمسني","✋","hiss",0,.7,None,1),("دفاع عن المنطقة","🏴","yowl",420,1.4,None,1),
("بصقة","💦","spit",0,.2,None,1),("مواجهة","⚔️","yowl",330,1.6,None,1)]),
("😿 خوف وألم", [
("خائفة","😨","meow",700,.6,[1.1,1.3,1.1],1),("أنا متألمة","🤕","meow",600,.9,[1.2,.9,.8],1),
("ساعدني","🆘","yowl",650,1,None,1),("صوت مفاجئ","😱","yowl",800,.4,None,1),
("حزينة","😢","meow",420,1.3,[1,.9,.8,.6],1),("وحيدة","🌧️","meow",400,1.5,[.9,1.1,.9,.7],1),
("مرتبكة","😵","meow",500,.8,None,2),("خوف من الغريب","👤","growl",130,.6,None,1),
("بكاء خفيف","💧","soft",640,1,[1.1,1,.9,.7],1),("توتر","😬","trill",520,.5,None,2)]),
("🎾 لعب ومرح", [
("هيا نلعب","🧶","trill",500,.4,None,1),("كرة الصوف","🎾","chirp",700,.3,None,1),
("مطاردة","🏃‍♀️","chirp",650,.25,None,3),("اصطياد","🦋","chirp",800,.25,None,1),
("قفزة!","🤸","chirp",600,.3,[.7,1.5],1),("مرح مجنون","🤪","trill",560,.4,None,2),
("مشاكسة","😜","meow",620,.5,[1,1.4,1],1),("هجوم لطيف","🐾","trill",450,.35,None,1),
("طير!","🐦","chirp",900,.18,None,6),("فاز القط","🏆","trill",480,.6,None,1)]),
("😴 استرخاء ونوم", [
("خرخرة هادئة","😌","purr",26,2,None,1),("خرخرة عميقة","🛋️","purr",22,2.5,None,1),
("نعسانة","😴","soft",350,1,None,1),("حلم جميل","💭","purr",30,1.5,None,1),
("تمدد","🧘","soft",380,1.2,[.7,1,.7],1),("ليلة سعيدة","🌙","soft",330,1.2,None,1),
("دفء الشمس","🌞","purr",27,2,None,1),("على الحضن","🛏️","purr",25,2.2,None,1),
("استرخاء تام","😇","purr",20,2.5,None,1),("تثاؤب","🥱","soft",300,1.2,[.6,1.2,1,.6],1)]),
("🔍 فضول واستكشاف", [
("ما هذا؟","🔎","meow",450,.6,[.8,1,1.3,1.6],1),("رائحة غريبة","👃","trill",400,.4,None,1),
("أرى شيئاً","👁️","chirp",600,.3,None,1),("استكشاف","🧭","meow",480,.6,None,1),
("نافذة مفتوحة","🪟","chirp",800,.18,None,4),("عصفور!","🐤","chirp",950,.15,None,5),
("ظل غامض","🕵️","meow",420,.7,[1,.8,1.1],1),("صوت في الخارج","🔊","meow",520,.5,None,1),
("حقيبة جديدة","🛍️","trill",430,.45,None,1),("حيرة","🤔","meow",460,.9,[1,1.2,1,1.2],1)]),
("🌙 نداء وحنين", [
("غناء الليل","🎶","yowl",450,2,None,1),("عواء حنين","🌕","yowl",500,1.8,None,1),
("نداء بعيد","🏔️","yowl",420,1.6,None,1),("شوق طويل","💫","yowl",480,2,None,1),
("مواء ليلي","🌃","meow",440,1.4,None,1),("رد الجواب","💬","meow",500,.8,None,1),
("تنهيدة","😮‍💨","soft",350,1,None,1),("صدى الصوت","📡","meow",480,.6,None,2),
("حنين للبيت","🏠","meow",420,1.2,None,1),("سيرينادا","🎤","yowl",520,2.2,None,1)]),
("🍼 القطط الصغيرة", [
("صغير يموء","🍼","kitten",900,.4,None,1),("جائع صغير","🥛","kitten",950,.4,None,2),
("أين أمي؟","🐈","kitten",1000,.6,None,1),("مواء رضيع","👶","kitten",850,.35,None,1),
("زقزقة صغيرة","🐣","chirp",1100,.2,None,3),("خرخرة صغيرة","🧸","purr",36,1.5,None,1),
("لعبة الصغار","🎈","kitten",950,.3,None,3),("نعاس الصغار","💤","soft",800,.8,None,1),
("صغير خائف","😰","kitten",1100,.5,[1.1,1.3,1.1],1),("كل شيء بخير","✅","kitten",900,.5,None,1)]),
]
# kind: (F1 path, F2 path, breath, attack, release, vibrato(hz,depth), jitter, am(hz,depth), default contour, gain)
K = {
"meow":  ([450,850,600],[2300,1750,1200],.03,.12,.35,None,0,None,[.8,1.1,1,.75],1),
"soft":  ([450,800,550],[2200,1700,1200],.22,.25,.5,None,0,None,[.9,.8,.7],.6),
"kitten":([600,1000,750],[2800,2300,1700],.03,.1,.3,None,0,None,[.85,1.15,1.05,.8],1),
"yowl":  ([500,900,700,600],[1900,1600,1300,1200],.04,.15,.3,(5.5,.035),.01,None,[.8,1.2,1,1.1,.7],1),
"trill": ([500,700],[1900,1600],.03,.1,.3,(24,.12),0,None,[.9,1.1,1.25],1),
"chirp": ([800,1000],[2600,2200],.02,.15,.4,None,0,None,[.8,1.4],1),
"growl": ([500,600],[1100,1000],.15,.1,.3,None,.04,(32,.6),[1,.95,1],1),
"purr":  ([180,220],[450,500],.1,.25,.3,None,.01,None,[1,1,1],1),
}
def sm(x, w): return np.convolve(x, np.ones(w)/w, mode="same")
def curve(p, n): p = np.array(p, float); return np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(p)), p)
def envl(n, a, r):
    t = np.linspace(0, 1, n); return np.sin(np.clip(np.minimum(1, t/a)*np.minimum(1, (1-t)/r), 0, 1)*np.pi/2)
def hiss(dur, attack):
    n = int(SR*dur); X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1/SR)
    y = np.fft.irfft(X*np.clip((f-2500)/1500, 0, 1)*np.exp(-((f-6500)/3500)**2), n)
    return y/np.abs(y).max()*envl(n, attack, .4)
def one(kind, f0, dur, cont):
    if kind == "hiss": return hiss(dur, .08)
    if kind == "spit": return hiss(dur, .02)
    F1, F2, br, a, r, vib, jit, am, dc, gain = K[kind]
    n = int(SR*dur); f = sm(f0*curve(cont or dc, n), 401)
    if vib: f = f*(1+vib[1]*np.sin(2*np.pi*vib[0]*np.arange(n)/SR))
    if jit: f = f*(1+jit*17*sm(rng.standard_normal(n), 300))
    f1, f2 = curve(F1, n), curve(F2, n); ph = 2*np.pi*np.cumsum(f)/SR; y = np.zeros(n)
    for k in range(1, int(min(90, 7000/f.min()))+1):
        fk = k*f
        g = np.exp(-((fk-f1)/(150+.2*f1))**2)+.6*np.exp(-((fk-f2)/300)**2)+.25*np.exp(-fk/1500)
        y += g/k**.3*np.sin(k*ph)*(fk < 9500)
    y = y/(np.abs(y).max()+1e-9)+br*sm(rng.standard_normal(n), 3)
    if am: y *= 1-am[1]+am[1]*(.5+.5*np.sin(2*np.pi*am[0]*np.arange(n)/SR))
    return y/np.abs(y).max()*envl(n, a, r)*gain
def make(kind, f0, dur, cont, rep):
    parts = []
    for i in range(rep):
        parts.append(one(kind, f0*(1+.05*rng.standard_normal()) if f0 else 0, dur, cont))
        if i < rep-1: parts.append(np.zeros(int(SR*.07)))
    y = np.concatenate(parts); y = y/np.abs(y).max()*.85
    fd = int(SR*.005); y[:fd] *= np.linspace(0, 1, fd); y[-fd:] *= np.linspace(1, 0, fd); return y
os.makedirs(RAW, exist_ok=True); lines = []; i = 0
for ci, (cn, items) in enumerate(CATS):
    for (name, emo, kind, f0, dur, cont, rep) in items:
        i += 1
        y = (make(kind, f0, dur, cont, rep)*32767).astype(np.int16)
        with wave.open(os.path.join(RAW, "cat_%03d.wav" % i), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())
        lines.append('    Cat(%d, %d, "%s", "%s")' % (i, ci, emo, name))
with open(KT, "w", encoding="utf-8") as f:
    f.write("package com.khader.catsounds\n\ndata class Cat(val id: Int, val cat: Int, val emoji: String, val name: String)\n\n")
    f.write("val CATEGORIES = listOf(\n" + ",\n".join('    "%s"' % c[0] for c in CATS) + "\n)\n\n")
    f.write("val CATS = listOf(\n" + ",\n".join(lines) + "\n)\n")
print("generated", i)
