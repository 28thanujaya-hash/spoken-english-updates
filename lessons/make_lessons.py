"""Lessons v3: the fresh 8-week plan (mentor 12 Nov), Day 0 + Week 1.

Every day has the same six parts (sessions), each with an overview (why, what you'll do):
  shadow · phrases · talk321 · talk (conversation) · listen · review.
A shorter day keeps the parts marked "short" (shadowing, 3-2-1 talk, conversation).
Week 2 onwards is written from his learner profile.

Step types the app understands:
  info, model, drill, react, listen, chat, freechat, record, miccheck, agree, speed, sayagain, test  (as before)
  shadow  : Sam/Maya say short lines; he repeats right after each (voice only)
  talk321 : the day's topic three times: 3 min, 2 min, 1 min, recorded; round 1 vs last round
  compare : today's 3-2-1 talk next to yesterday's (review)
Run: python3 make_lessons.py  (writes index.json and week-1.json)
"""
import json

V = 3

def info(title, en, si="", examples=None):
    return {"type": "info", "title": title, "en": en, "si": si, "examples": examples or []}

def model(who, lines, note=""):
    return {"type": "model", "who": who, "lines": lines, "note": note}

def drill(who, prompt, models, point="", si=""):
    return {"type": "drill", "who": who, "prompt": prompt, "models": models, "point": point, "si": si}

def react(who, items):
    return {"type": "react", "who": who, "items": [{"news": n, "feel": f} for n, f in items]}

def listen(who, title, script, questions, retell=None):
    return {"type": "listen", "who": who, "title": title, "script": script, "questions": questions + (["Retell: " + retell] if retell else [])}

def chat(who, mode, where, en, si, goal, turns, brief, opener, title, whoLine, scored=True):
    return {"type": "chat", "who": who, "mode": mode, "where": where, "en": en, "si": si, "goal": goal, "minTurns": turns,
            "brief": brief, "opener": opener, "scored": scored, "title": title, "whoLine": whoLine}

def freechat(who, ideas, brief=""):
    return {"type": "freechat", "who": who, "ideas": ideas, "brief": brief}

def shadow(who, lines):
    return {"type": "shadow", "who": who, "lines": lines}

def talk321(topic, points):
    return {"type": "talk321", "topic": topic, "points": points}

def part(pid, title, why, what, steps, short=False, mode=""):
    return {"id": pid, "title": title, "why": why, "what": [{"name": a, "desc": b, "mode": c} for a, b, c in what],
            "steps": steps, "short": short, "mode": mode}

PRIVACY_EN = ("Your voice goes to Google's speech service, which turns it into words. Your words go to Google's free Gemini AI, "
              "so Sam and Maya can understand and help you. Google may use what you say on the free service to improve its AI, so don't say "
              "private things like passwords or bank numbers. Your recordings, words and results stay on this phone until you remove the app.")
PRIVACY_SI = ("ඔබේ හඬ Google හි කථන සේවාවට යයි; එය ඔබේ කතාව වචන බවට පත් කරයි. ඔබේ වචන Google හි නොමිලේ ලැබෙන Gemini AI වෙත යයි, "
              "Sam සහ Maya ට ඔබව තේරුම් ගෙන උදව් කිරීමට. නොමිලේ සේවාවේදී ඔබ කියන දේ Google තම AI දියුණු කිරීමට භාවිතා කළ හැකියි, එබැවින් "
              "මුරපද හෝ බැංකු අංක වැනි පුද්ගලික දේ කියන්න එපා. ඔබේ හඬ පටිගත කිරීම්, වචන සහ ප්‍රතිඵල ඔබ යෙදුම ඉවත් කරන තුරු මෙම දුරකථනයේම තිබේ.")

REACT_SOUNDS = info(
    "Reaction sounds",
    "Real listeners make small sounds. A flat \"Oh.\" sounds bored; a rising \"Oh!\" sounds interested.\n"
    "• Oh! / Oh, really? — surprise, interest\n• Oh no! / I'm sorry to hear that. — bad news\n"
    "• Wow! / Oh, nice! / That's great! — good news\n• Ah, I see. / Right. / Uh-huh. — I'm listening\n"
    "• Hmm… — thinking\n• No way! — shocking or funny",
    "සැබෑ සවන්දෙන්නෝ කුඩා ශබ්ද කරති. \"Oh.\" පැතලි නම් කම්මැලි ලෙස ඇසේ; ඉහළ යන \"Oh!\" උනන්දුවක් පෙන්වයි.\n"
    "• Oh! — පුදුමය, උනන්දුව\n• Oh no! — නරක පුවතක්\n• Wow! / Oh, nice! — හොඳ පුවතක්\n"
    "• Ah, I see. / Uh-huh. — මම අහගෙන ඉන්නවා\n• Hmm… — හිතනවා\n• No way! — විහිළුවක් හෝ කම්පනයක්")

ASKING = info(
    "When you don't catch something, ask!",
    "Never go silent. Ask in English:\n• Too fast: \"Sorry, could you slow down a bit?\"\n"
    "• Didn't catch it: \"Sorry, I didn't catch that.\"\n• One word: \"Sorry, what does ___ mean?\"\n"
    "• Hear it again: \"Again, please.\" / \"One more time?\"\nAsking is a good conversation skill. It never loses points.",
    "කවදාවත් නිශ්ශබ්ද වෙන්න එපා. ඉංග්‍රීසියෙන් අහන්න:\n• වේගවත් නම්: \"Sorry, could you slow down a bit?\"\n"
    "• ඇහුණේ නැත්නම්: \"Sorry, I didn't catch that.\"\n• එක වචනයක්: \"Sorry, what does ___ mean?\"\n"
    "• නැවත අහන්න: \"Again, please.\"\nඇසීම හොඳ කතා කිරීමේ හැකියාවක්. ලකුණු අඩු වෙන්නේ නැහැ.")

SHADOW_WHY = "Repeating right after Sam or Maya, at their speed, makes English rhythm your own. You stop translating and start copying how real people sound."
PHRASES_WHY = "Ready-made phrases come out fast. Learn them as whole blocks, and you don't have to build sentences word by word."
T321_WHY = "The same talk three times, each time shorter. Each round comes out smoother, so you feel what fast, easy speaking is like."
LISTEN_WHY = "Real people talk fast and long. Listen to the whole thing, answer, then tell it back in your own words."
REVIEW_WHY = "The phrases that keep coming back, said again from memory. Then you hear today's talk next to yesterday's."

def shadow_part(who, lines):
    return part("shadow", "Shadowing", SHADOW_WHY,
                [("Listen", f"{'Sam' if who == 'sam' else 'Maya'} says short lines", "voice only"),
                 ("Echo", "repeat right after each line, at the same speed", "you talk")],
                [shadow(who, lines)], short=True)

def phrases_part(who, intro_en, intro_si, model_lines, drills):
    return part("phrases", "Learn today's phrases", PHRASES_WHY,
                [("Listen", f"{'Sam' if who == 'sam' else 'Maya'} uses today's phrases", "voice only"),
                 ("Understand", "when to use each", "read · EN | සිං"),
                 ("Practise", "answer Sam and Maya with them", "you talk")],
                [info("Today's phrases", intro_en, intro_si), model(who, model_lines)] + drills)

def t321_part(topic, points):
    return part("talk321", "3-2-1 talk", T321_WHY,
                [("Round 1", "talk about it for 3 minutes", "recorded"), ("Round 2", "the same in 2 minutes", "recorded"),
                 ("Round 3", "the same in 1 minute", "recorded"), ("Compare", "hear round 1 next to the last round", "listen")],
                [talk321(topic, points)], short=True)

def talk_part(title, c, mode_word):
    return part("talk", title, "This is the real thing: a real-life situation, and you don't know what they'll say. Use today's phrases and keep it going.",
                [("Before you talk", "the situation, who, your goal", "read · EN | සිං"),
                 ("Talk", mode_word, "you talk"), ("Summary", "what happened and one better sentence", "read")],
                [c], short=True, mode=c.get("mode", "free"))

def listen_part(title, l, reacts):
    return part("listen", title, LISTEN_WHY,
                [("Listen", "a natural-speed story", "voice only"), ("Answer", "3 questions out loud", "you talk"),
                 ("Retell", "tell it back in 4–5 sentences", "you talk"), ("Quick reactions", "react to short news", "you talk")],
                [l, react("both", reacts)])

def review_part():
    return part("review", "Review", REVIEW_WHY,
                [("Say them again", "the phrases that keep coming back", "you talk"), ("Then and now", "today's talk next to yesterday's", "listen")],
                [{"type": "sayagain"}, {"type": "compare"}])

def day(n, title, overview, by_end, phrases, companion, parts):
    return {"day": n, "title": title, "overview": overview, "byTheEnd": by_end, "phrases": phrases, "companion": companion, "sessions": parts}

# ---------------------------------------------------------------- Day 0
day0 = day(0, "Getting started",
    "Meet Sam and Maya, set up your voice, and record where you start. It takes about an hour, and nothing is scored.",
    "By the end, Sam and Maya know you, and you have your Day 0 voice to compare with later.",
    ["My name is…", "I'm from…", "Again, please.", "Sorry, could you slow down?"], "both", [
    part("about", "About you", "Sam and Maya are your classmates. What you tell them today, they remember.",
         [("Meet Sam and Maya", "two classmates say hello", "voice only"), ("About you", "your name, studies, family, town, what you like", "you talk")], [
        info("Welcome!", "In this app you learn by speaking. Every day has the same parts: shadowing, phrases, a 3-2-1 talk, a conversation, listening and a review.\n"
             "Tap the mic to speak English. When you're stuck, tap සිං and say it in Sinhala: the app helps you say it in English.",
             "මෙම යෙදුමේ ඔබ ඉගෙන ගන්නේ කතා කරමින්. සෑම දිනකම එකම කොටස් තියෙනවා: shadowing, වාක්‍ය ඛණ්ඩ, 3-2-1 කතාව, සංවාදයක්, ඇහුම්කන් දීම සහ නැවත බැලීම.\n"
             "ඉංග්‍රීසියෙන් කතා කරන්න mic එක ඔබන්න. හිරවුණොත් සිං ඔබා සිංහලෙන් කියන්න: යෙදුම එය ඉංග්‍රීසියෙන් කියන්න උදව් කරයි."),
        model("sam", ["Hey! I'm Sam. I'm in your English class. I live in Kandy with my parents and two little brothers, and I love cricket. Oh, and Marvel films!"]),
        model("maya", ["Hi, I'm Maya. I'm in your class too. I work part-time in a café in the evenings, and on weekends I like to travel. Nice to meet you!"]),
        drill("sam", "So, what's your name? Where are you from?", ["Hi Sam! I'm [his name]. I'm from Kandy.", "My name is [his name]. I'm from a small town near Galle."],
              "Your name and where you're from."),
        drill("maya", "What do you do? Are you studying, or working?", ["I'm studying IT at a college.", "At the moment I'm working in a shop."],
              "What you do now."),
        drill("sam", "Who do you live with?", ["I live with my parents and my sister.", "I live with my family: my mother, my father and my younger brother."],
              "Your family."),
        drill("maya", "What do you like doing in your free time?", ["I like watching films and playing cricket.", "I love films, especially action films."],
              "One or two things you like."),
    ]),
    part("voice", "Your voice", "A quick check that the app hears you well, how fast you understand, and a first try at shadowing.",
         [("Mic check", "say one sentence; see what the app heard", "you talk"), ("Agreement", "how your voice is used", "read · EN | සිං"),
          ("Listening speed", "five sentences, slow to fast", "you talk"), ("First shadowing", "echo three short lines", "you talk")], [
        {"type": "miccheck"},
        {"type": "agree", "en": PRIVACY_EN, "si": PRIVACY_SI},
        ASKING,
        {"type": "speed"},
        shadow("maya", ["Nice to meet you.", "I'm from Kandy.", "How about you?"]),
    ]),
    part("start", "Your starting point", "Just do your best. In a week you'll hear this again and see how far you've come.",
         [("About yourself", "talk for 2 minutes, recorded", "recorded"), ("Five quick moments", "answer however you can", "you talk"),
          ("First 3-2-1 talk", "one topic, 3 then 2 then 1 minute", "recorded"), ("Easy chat", "5 minutes with Maya, no score", "you talk")], [
        {"type": "record", "topic": "Tell me about yourself: who you are, what you do, your family, what you like.", "saveAs": "baseline-talk", "who": "maya"},
        drill("sam", "Nice shirt!", [], "Answer however you can."),
        drill("maya", "Do you know where the library is?", [], "Answer however you can."),
        drill("sam", "Oh no, I failed my driving test today.", [], "Answer however you can."),
        drill("maya", "(At a bus stop. Someone is waiting next to you. Speak first.)", [], "Answer however you can."),
        drill("sam", "So yesterday after class I went to my cousin's place and we had rice and curry and then we watched the match and—", [],
              "Answer however you can."),
        talk321("My day today", ["when I got up", "what I did", "who I met", "what I ate", "how I feel"]),
        freechat("maya", ["Your town", "Your family", "A film you like"], "First taste: an easy chat. Ask him about his town and family. No score."),
    ]),
])

# ---------------------------------------------------------------- Week 1 · Unlock: talk about yourself and react
d1 = day(1, "Me: introduce yourself",
    "Learn a few ready phrases to say who you are, practise them with Sam and Maya, meet a new classmate at the canteen, and hear Maya's story.",
    "By the end you can talk about yourself and ask back, without stopping.",
    ["I'm from…", "I live in…", "At the moment I'm…", "I'm really into…", "To be honest…", "How about you?"], "sam", [
    shadow_part("sam", ["Hi, I'm Sam. Nice to meet you.", "I'm from Kandy, but I live in Colombo now.", "At the moment I'm studying English.",
                        "To be honest, I'm a bit nervous.", "I'm really into cricket.", "How about you?"]),
    phrases_part("sam",
        "Six blocks to talk about yourself:\n• I'm from… (your home town)\n• I live in… (where you live now)\n• At the moment I'm… (studying, working, looking for a job)\n"
        "• I'm really into… (something you love)\n• To be honest… (before a true feeling)\n• How about you? (always hand it back)",
        "ඔබ ගැන කියන්න කොටස් හයක්:\n• I'm from… (ඔබේ උපන් ගම)\n• I live in… (දැන් ජීවත් වන තැන)\n• At the moment I'm… (දැන් කරන දේ)\n"
        "• I'm really into… (ගොඩක් කැමති දෙයක්)\n• To be honest… (ඇත්ත හැඟීමක් කියන්න කලින්)\n• How about you? (හැමවිටම ආපහු අහන්න)",
        ["I'm from Kandy, but I live in Colombo now. At the moment I'm studying English. I'm really into cricket. To be honest, I'm a bit nervous today. How about you?"],
        [drill("sam", "Where are you from?", ["I'm from Galle, but I live in Colombo now. How about you?", "I'm from Kandy. I live there with my family."], "I'm from… + How about you?"),
         drill("maya", "So what do you do?", ["At the moment I'm studying IT at a college in Kandy.", "At the moment I'm looking for a job."], "At the moment I'm…"),
         drill("sam", "What do you do in your free time?", ["I'm really into films, especially action films. How about you?", "I'm really into cricket. I play every weekend."], "I'm really into…"),
         drill("maya", "How do you feel about this class?", ["To be honest, I'm a bit nervous, but I'm happy to be here.", "To be honest, it's a bit hard, but I like it."], "To be honest…"),
         drill("sam", "Tell me a little about yourself!", ["I'm from Kandy and at the moment I'm studying IT. I'm really into films. How about you?"], "Three phrases in one answer.")]),
    t321_part("Who I am", ["name", "from", "now", "family", "likes", "a plan"]),
    talk_part("Meet a new classmate", chat("sam", "face", "The college canteen, your first day",
        "It's your first day in a new class. At the canteen, Sam comes over and sits with you. Introduce yourself, ask about him, and keep it going.",
        "අද නව පන්තියේ ඔබේ පළමු දිනයයි. ආපනශාලාවේදී Sam ඔබ ළඟට ඇවිත් ඉඳගන්නවා. ඔබව හඳුන්වා දෙන්න, ඔහු ගැන අහන්න, කතාව දිගටම ගෙනියන්න.",
        "Say who you are, and ask back at least 3 times.", 8,
        "He is new in class; you meet him in the canteen. Ask where he's from, what he does, his family, what he likes. Tell him about you too. "
        "Once, speak a little fast on purpose so he practises asking you to slow down.",
        "Hey! You're new, right? I'm Sam. Mind if I sit here?", "New classmate", "Sam, a classmate"), "Face to face"),
    listen_part("Listen to Maya", listen("maya", "Maya introduces herself",
        "Okay, so, about me. I'm from Jaffna, but I moved to Colombo two years ago for work. At the moment I work in a small café near the beach, "
        "and to be honest, I love it, because I meet so many people. My family is still in Jaffna: my mum, my dad and my grandmother, who makes the best "
        "crab curry in the world. I miss her cooking a lot. In my free time I'm really into travelling. Last month I went to Ella with two friends and we "
        "climbed Little Adam's Peak at six in the morning. It was so cold! Next year I want to go to India. So that's me. How about you?",
        ["Where is Maya from?", "What does she do now?", "What's one thing she misses?"], "tell me about Maya in 4 or 5 sentences."),
        [("I just moved here from Jaffna.", "interest"), ("I got the job!", "good"), ("I lost my wallet on the bus.", "bad"), ("My grandmother is 92!", "surprise")]),
    review_part(),
])

d2 = day(2, "My family",
    "Phrases to talk about the people at home, a video call with Maya about your family, and Sam's story about a big family lunch.",
    "By the end you can describe your family and say what you usually do together.",
    ["I live with…", "My brother is the kind of person who…", "We usually…", "We get on well.", "He's older than me.", "What about your family?"], "maya", [
    shadow_part("maya", ["I live with my parents and my brother.", "My brother is the kind of person who never stops talking.",
                         "We usually eat together on Sundays.", "We get on really well.", "My sister is older than me.", "What about your family?"]),
    phrases_part("maya",
        "Phrases for family:\n• I live with… (who is at home)\n• My brother is the kind of person who… (describe someone)\n• We usually… (what you do together)\n"
        "• We get on well. (you like each other)\n• He's older / younger than me.\n• What about your family? (hand it back)",
        "පවුල ගැන වාක්‍ය:\n• I live with… (ගෙදර ඉන්නේ කවුද)\n• My brother is the kind of person who… (කෙනෙක් ගැන විස්තර කරන්න)\n• We usually… (එකට කරන දේ)\n"
        "• We get on well. (අපි හොඳින් ඉන්නවා)\n• He's older / younger than me. (මට වඩා වැඩිමල් / බාල)\n• What about your family? (ආපහු අහන්න)",
        ["I live with my mum, my dad and my two little brothers. My brother Kavi is the kind of person who eats everything in the fridge! We usually eat together on Sundays. We get on well. What about your family?"],
        [drill("maya", "Who do you live with?", ["I live with my parents and my younger sister.", "I live with my mother and my grandmother."], "I live with…"),
         drill("sam", "Tell me about someone in your family.", ["My brother is the kind of person who always makes us laugh.", "My mother is the kind of person who works very hard."], "…is the kind of person who…"),
         drill("maya", "What do you do together as a family?", ["We usually eat together in the evening and watch TV.", "We usually visit my grandmother on Sundays."], "We usually…"),
         drill("sam", "Do you fight with your brother or sister?", ["Sometimes, but we get on well. He's older than me.", "Not really. We get on really well."], "We get on well · older than me"),
         drill("maya", "I've got three sisters. It's always noisy at home!", ["Wow, three! What about your family? Is it noisy too?", "Oh, I can imagine! I've only got one brother. What are your sisters like?"], "React, then ask back.")]),
    t321_part("My family", ["who", "names", "what they do", "what they're like", "what we do together"]),
    talk_part("Video call with Maya", chat("maya", "video", "A video call from Maya in the evening",
        "Maya video-calls you in the evening. She wants to know about your family. Tell her, and ask about hers.",
        "සවස Maya ඔබට වීඩියෝ ඇමතුමක් ගන්නවා. ඇයට ඔබේ පවුල ගැන දැනගන්න ඕනේ. ඇයට කියන්න, ඇගේ පවුල ගැනත් අහන්න.",
        "Greet her first, talk about your family, ask about hers, and say goodbye before you hang up.", 10,
        "Video-call him in the evening. Ask about his family: who he lives with, what they're like, what they do together. Share about your family in Jaffna. "
        "End warmly when it's time.",
        "", "Maya's video call", "Maya, a classmate"), "Video call"),
    listen_part("Sam's big family lunch", listen("sam", "Sam's big family lunch",
        "So last Sunday was crazy. My aunt came from Kurunegala with her whole family, so we were sixteen people in our small house! My mum cooked from six in the morning: "
        "rice, chicken curry, dhal, and of course her famous pol sambol. My little brothers had to sit on the floor because there weren't enough chairs. "
        "My uncle is the kind of person who tells the same joke every time, and everyone laughs anyway. After lunch we all watched the cricket match together, "
        "and when Sri Lanka won, my grandfather danced! It was noisy and tiring, but honestly, it was the best day this month.",
        ["How many people were in Sam's house?", "What did his mum cook?", "What did his grandfather do?"], "tell me about Sam's family lunch in 4 or 5 sentences."),
        [("My sister is getting married!", "good"), ("My grandfather is in hospital.", "bad"), ("We're sixteen people at home on Sunday!", "surprise"), ("My brother wants to be a pilot.", "interest")]),
    review_part(),
])

d3 = day(3, "Reacting and buying time",
    "Learn how to react to news and how to buy time instead of freezing, then Maya calls you with her news.",
    "By the end you react naturally and never go silent: you buy time and then answer.",
    ["Really?", "Oh no!", "That's great!", "Let me think…", "How can I put it…", "Well, actually…"], "maya", [
    shadow_part("maya", ["Really? That's great!", "Oh no, I'm sorry to hear that.", "Let me think for a second.", "Hmm, how can I put it…",
                         "Well, actually, I'm not sure.", "That's a good question."]),
    phrases_part("maya",
        "React first, then answer. When you need time, say it out loud instead of going silent:\n• Really? / Oh no! / That's great! (react)\n"
        "• Let me think… / How can I put it… (buy time)\n• Well, actually… (start an answer)\n• That's a good question. (more time)",
        "මුලින්ම ප්‍රතිචාර දක්වන්න, ඊට පස්සේ පිළිතුරු දෙන්න. වෙලාව ඕනේ නම් නිශ්ශබ්ද වෙනවා වෙනුවට එය කියන්න:\n• Really? / Oh no! / That's great!\n"
        "• Let me think… / How can I put it… (හිතන්න වෙලාව)\n• Well, actually… (පිළිතුර පටන් ගන්න)\n• That's a good question.",
        ["Really? That's great news! Hmm, let me think… how can I put it… Well, actually, I'm really happy for you."],
        [drill("maya", "I got the job at the hotel!", ["Really? That's great! When do you start?", "Wow, that's great news! Congratulations!"], "React to good news, then ask."),
         drill("sam", "My bike got stolen yesterday.", ["Oh no! I'm sorry to hear that. Where was it?", "Oh no, that's terrible! Did you go to the police?"], "React to bad news, then ask."),
         drill("maya", "What's the best thing about your town?", ["Let me think… Well, actually, the food is really good.", "Hmm, how can I put it… it's quiet and green."], "Buy time, then answer."),
         drill("sam", "Why do you want to learn English?", ["That's a good question. Let me think… I want a better job.", "Well, actually, I want to travel and talk to people."], "That's a good question + answer."),
         drill("maya", "Guess what? My cousin is moving to Canada.", ["Really? Wow! When is she going?", "Oh, really? Are you sad?"], "Really? + a question.")]),
    t321_part("A good thing and a bad thing this week", ["the good thing", "what happened", "the bad thing", "how I felt", "what now"]),
    talk_part("Maya's news", chat("maya", "phone", "A phone call from Maya",
        "Maya calls you. She has some news, good and bad. React to each piece, ask questions, and keep the call going.",
        "Maya ඔබට කතා කරනවා. ඇයට හොඳ සහ නරක පුවත් තියෙනවා. සෑම එකකටම ප්‍රතිචාර දක්වන්න, ප්‍රශ්න අහන්න, කතාව ගෙනියන්න.",
        "React to each piece of news and ask a follow-up question each time.", 10,
        "Phone him with three pieces of news, one at a time: you got a pay rise at the café (good), your phone screen broke (bad), your cousin is getting married next month (surprise). "
        "Let him react and ask before you give the next one. Ask him one hard question so he must buy time.",
        "Hey! It's Maya. Have you got a minute? I've got so much news!", "Maya's news", "Maya, on the phone"), "Phone call"),
    listen_part("Three pieces of news", listen("sam", "Sam's three pieces of news",
        "Okay, three things happened this week. First, the good news: I finally passed my driving test! Third time, but who's counting? "
        "Second, the bad news: on the way home I dropped my phone in a puddle, and now the screen is completely black. My mum says it's karma. "
        "And third, the strange news: my neighbour's dog followed me to college on Wednesday, and he sat outside the classroom all morning. "
        "The teacher thought it was my dog! So, yeah, a busy week.",
        ["What was Sam's good news?", "What happened to his phone?", "What did the dog do?"], "tell me Sam's three pieces of news."),
        [("I passed my exam!", "good"), ("The bus left without me.", "bad"), ("I saw an elephant on the road!", "surprise"), ("I'm thinking of learning to cook.", "interest")]),
    review_part(),
])

d4 = day(4, "Free time and films",
    "Phrases to say what you like and don't like, a chat with a stranger in a cinema queue, and Sam's review of a film.",
    "By the end you can say what you like, what you don't, and recommend something.",
    ["I'm really into…", "I'm not a big fan of…", "You should watch…", "It's about…", "I'd give it…", "Have you seen…?"], "sam", [
    shadow_part("sam", ["I'm really into action films.", "I'm not a big fan of horror.", "You should watch it, it's great.", "It's about a guy who loses everything.",
                        "Have you seen it yet?", "I'd give it eight out of ten."]),
    phrases_part("sam",
        "Phrases for what you like:\n• I'm really into… (you love it)\n• I'm not a big fan of… (polite: you don't like it)\n• You should watch / try… (recommend)\n"
        "• It's about… (the story in one line)\n• I'd give it 8 out of 10.\n• Have you seen…? (ask)",
        "කැමති දේ ගැන වාක්‍ය:\n• I'm really into… (ගොඩක් කැමතියි)\n• I'm not a big fan of… (ආචාරශීලීව: අකමැතියි)\n• You should watch / try… (නිර්දේශ කරන්න)\n"
        "• It's about… (කතාව එක පේළියකින්)\n• I'd give it 8 out of 10.\n• Have you seen…? (අහන්න)",
        ["I'm really into action films, but I'm not a big fan of horror. You should watch Jailer. It's about a retired man who protects his family. I'd give it nine out of ten. Have you seen it?"],
        [drill("sam", "What kind of films do you like?", ["I'm really into action films, especially Tamil ones.", "I'm really into comedies. I like to laugh."], "I'm really into…"),
         drill("maya", "Do you like horror films?", ["Not really. I'm not a big fan of horror. I get scared!", "To be honest, I'm not a big fan of them."], "I'm not a big fan of…"),
         drill("sam", "I'm bored. What should I watch tonight?", ["You should watch Vikram. It's about a police officer who…", "You should watch a comedy. Have you seen 3 Idiots?"], "You should watch… It's about…"),
         drill("maya", "What do you do on weekends, apart from films?", ["I'm really into cricket. I play with my friends on Saturdays.", "I usually go out with my friends."], "Free time, not only films."),
         drill("sam", "Was it good? Out of ten?", ["I'd give it seven out of ten. The story was good, but it was too long.", "I'd give it nine! You should see it."], "I'd give it…")]),
    t321_part("My favourite film and why", ["the name", "it's about", "the best part", "why I like it", "who should watch it"]),
    talk_part("In the cinema queue", chat("sam", "face", "A cinema ticket queue",
        "You're in a long queue for a film. The person behind you (Sam plays a stranger) looks friendly. Start a conversation: comment, ask, and talk about films.",
        "ඔබ චිත්‍රපටයකට දිගු පෝලිමක ඉන්නවා. ඔබ පිටුපස කෙනා (Sam නාඳුනන කෙනෙක් ලෙස) මිත්‍රශීලීයි. කතාවක් පටන් ගන්න: අදහසක් කියන්න, අහන්න, චිත්‍රපට ගැන කතා කරන්න.",
        "You speak first. Say what you like and don't like, and recommend one film.", 8,
        "Play a friendly stranger in a cinema ticket queue (not his classmate). Wait for him to start. You like comedies and you're not a fan of horror. "
        "Ask what he recommends.",
        "", "Cinema queue", "A stranger (Sam plays him)"), "Face to face"),
    listen_part("Sam reviews a film", listen("sam", "Sam's film review",
        "So last night I watched a film called The Lost Train. It's about a boy who gets on the wrong train and ends up in a tiny village in the hills. "
        "At first he's scared and angry, but the people in the village are so kind that he doesn't want to leave. The best part is the old station master, "
        "who is really funny. To be honest, the middle is a bit slow, and I'm not a big fan of sad endings, but the music is beautiful. "
        "I'd give it seven out of ten. You should watch it with your family on a rainy day.",
        ["What is the film about?", "What's the best part, for Sam?", "What doesn't he like?"], "tell me about Sam's film in 4 or 5 sentences."),
        [("I got two free tickets!", "good"), ("The cinema is closed this week.", "bad"), ("The film is four hours long!", "surprise"), ("I'm thinking of making a short film.", "interest")]),
    review_part(),
])

d5 = day(5, "My town",
    "Phrases to describe where you live, a video call where Maya plans a visit to your town, and Maya's trip to Kandy.",
    "By the end you can describe your town and give simple directions and tips.",
    ["There's a… near my house.", "It's famous for…", "It takes about…", "You can…", "It's a bit…", "Have you ever been to…?"], "maya", [
    shadow_part("maya", ["There's a big temple near my house.", "My town is famous for its tea.", "It takes about an hour by bus.",
                         "You can walk around the lake.", "It's a bit quiet at night.", "Have you ever been there?"]),
    phrases_part("maya",
        "Phrases for your town:\n• There's a… near my house.\n• It's famous for…\n• It takes about… (time to get there)\n• You can… (things to do)\n"
        "• It's a bit… (quiet, busy, hot)\n• Have you ever been to…? (ask)",
        "ඔබේ නගරය ගැන වාක්‍ය:\n• There's a… near my house. (ගෙදර ළඟ…)\n• It's famous for… (…ට ප්‍රසිද්ධයි)\n• It takes about… (යන්න ගතවන කාලය)\n"
        "• You can… (කරන්න පුළුවන් දේ)\n• It's a bit… (ටිකක් නිස්කලංක, කාර්යබහුල, රස්නේ)\n• Have you ever been to…? (අහන්න)",
        ["I live in Kandy. There's a big lake near my house. It's famous for the Temple of the Tooth. It takes about three hours from Colombo by train. You can walk around the lake in the evening. Have you ever been there?"],
        [drill("maya", "Where do you live? What's it like?", ["I live in Kandy. It's a bit busy, but it's beautiful.", "I live in a small town near Galle. It's quiet and green."], "It's a bit…"),
         drill("sam", "What's near your house?", ["There's a temple and a small shop near my house.", "There's a big school and a bus stand near my house."], "There's a… near my house."),
         drill("maya", "What's your town famous for?", ["It's famous for its beaches and fish.", "It's famous for the temple and the lake."], "It's famous for…"),
         drill("sam", "How do I get there from Colombo?", ["You can take the train. It takes about three hours.", "It takes about two hours by bus."], "It takes about…"),
         drill("maya", "I'm going to Galle next week!", ["Really? Have you ever been there before? You can see the fort.", "Nice! You should try the seafood there."], "Have you ever been…? / You can…")]),
    t321_part("My town", ["where", "what's near my house", "famous for", "how to get there", "what to do"]),
    talk_part("Maya plans a visit", chat("maya", "video", "A video call: Maya wants to visit your town",
        "Maya video-calls you. She wants to visit your town next month. Tell her what it's like, how to get there and what to do. Ask what she likes.",
        "Maya ඔබට වීඩියෝ ඇමතුමක් ගන්නවා. ඇයට ඊළඟ මාසේ ඔබේ නගරයට එන්න ඕනේ. එය කොහොමද, එන්නේ කොහොමද, කරන්න තියෙන දේ කියන්න. ඇය කැමති දේ අහන්න.",
        "Greet her first, describe your town, give 2 tips, and say goodbye before you hang up.", 10,
        "Video-call him: you want to visit his town next month. Ask what it's like, how long it takes from Colombo, where to eat, what to see. "
        "Ask him to repeat once if something is unclear.",
        "", "Maya's visit", "Maya, a classmate"), "Video call"),
    listen_part("Maya's trip to Kandy", listen("maya", "Maya's trip to Kandy",
        "Last weekend I finally went to Kandy. I took the early train from Colombo, and it took about three hours, but the views were amazing. "
        "First I walked around the lake. There are so many monkeys there! Then I visited the Temple of the Tooth, which was really peaceful. "
        "For lunch, a man at the market told me about a small place near the clock tower, and they had the best kottu I've ever had. "
        "In the evening it started raining, so I sat in a café and watched the people. It's a bit busy, but I'd love to go back.",
        ["How long did the train take?", "What did Maya see at the lake?", "What happened in the evening?"], "tell me about Maya's day in Kandy."),
        [("They're building a new park in my town.", "good"), ("The road to my village is closed.", "bad"), ("I saw a leopard near Yala!", "surprise"), ("I'm thinking of moving to Galle.", "interest")]),
    review_part(),
])

d6 = day(6, "Mission: a first meeting",
    "A mission day: everything from this week in real situations. Compliments, questions, and your week so far, with both Sam and Maya.",
    "By the end you can meet someone new and keep a 10-minute chat going on your own.",
    ["Thanks, actually…", "By the way…", "Nice to meet you.", "Anyway…", "It was nice talking to you.", "See you soon!"], "both", [
    shadow_part("sam", ["Thanks! Actually, I got it yesterday.", "By the way, where are you from?", "Nice to meet you.", "Anyway, how was your week?",
                        "It was nice talking to you.", "See you soon!"]),
    phrases_part("sam",
        "Mission phrases for a first meeting:\n• Thanks, actually… (accept a compliment and add something)\n• By the way… (change the topic)\n• Nice to meet you.\n"
        "• Anyway… (move on)\n• It was nice talking to you. / See you soon! (end politely)",
        "පළමු හමුවීමක් සඳහා වාක්‍ය:\n• Thanks, actually… (ප්‍රශංසාවක් පිළිගෙන යමක් එකතු කරන්න)\n• By the way… (මාතෘකාව වෙනස් කරන්න)\n• Nice to meet you.\n"
        "• Anyway… (ඉදිරියට යන්න)\n• It was nice talking to you. / See you soon! (ආචාරශීලීව අවසන් කරන්න)",
        ["Oh, thanks! Actually, my sister gave it to me. Nice to meet you, I'm Sam. By the way, are you in Maya's class? Anyway, it was nice talking to you. See you soon!"],
        [drill("maya", "Nice shirt!", ["Thanks! Actually, I got it for my birthday.", "Oh, thanks! Actually, it's my brother's."], "Thanks, actually…"),
         drill("sam", "Hi! I'm Sam, Maya's friend.", ["Hi Sam, nice to meet you. I'm [his name]. How do you know Maya?", "Nice to meet you! I'm in her English class."], "Nice to meet you + a question."),
         drill("maya", "…and that's why I hate the rain.", ["Ha, I understand. Anyway, how was your week?", "Me too! By the way, are you free on Sunday?"], "Anyway / By the way"),
         drill("sam", "Oh, my bus is here!", ["Oh, OK! It was nice talking to you. See you soon!", "No problem. Nice to meet you, see you!"], "End politely.")]),
    t321_part("My week so far", ["Monday to now", "the best moment", "something new", "something hard", "next week"]),
    talk_part("Free chat with both", freechat("both", ["Your week so far", "Something new you learned", "Plans for Sunday"],
        "Mission: a relaxed chat. Sam and Maya give him a compliment, ask about his week, and bring up things he told them earlier this week. No score.") | {"title": "With Sam and Maya"}, "Free chat"),
    listen_part("Two friends meet after years", listen("maya", "Two friends meet after years",
        "Yesterday something lovely happened. I was waiting for the bus in Pettah when a man said, \"Maya? Is that you?\" It was Dilan, my best friend from school! "
        "We hadn't seen each other for eight years. He looks so different now: he has a beard and he's much taller. He told me he works as a nurse in a big hospital, "
        "and he's getting married in March. We were so busy talking that I missed my bus, and then the next one too! In the end we had tea together, "
        "and he invited me to the wedding. Anyway, we promised to meet every month.",
        ["Who did Maya meet?", "What does he do now?", "Why did she miss her bus?"], "tell me Maya's story in 4 or 5 sentences."),
        [("I'm invited to a wedding!", "good"), ("I missed two buses.", "bad"), ("My old teacher is on TV!", "surprise"), ("I'm thinking of growing a beard.", "interest")]),
    review_part(),
])

d7 = day(7, "Review and weekly test",
    "Go over the week's phrases, then do the weekly test: an 8-turn chat with a stranger and a short piece of news. You'll also hear yourself next to Day 0.",
    "By the end you see how far you've come since Day 0.",
    ["I'm from…", "We usually…", "Let me think…", "I'm really into…", "It's famous for…", "By the way…"], "both", [
    shadow_part("maya", ["I'm from Kandy, but I live in Colombo.", "We usually eat together on Sundays.", "Let me think for a second.",
                         "I'm really into cricket.", "It's famous for its tea.", "By the way, how was your week?"]),
    part("phrases", "Week 1 phrases", "All this week's phrases once more, before the test.",
         [("Say them again", "the phrases that keep coming back", "you talk")], [
        info("Review", "Today you go over the week, then do the weekly test. The test is about communication: being understood, keeping it going, asking when lost. Asking is never a minus.",
             "අද ඔබ සතිය නැවත බලා සතිපතා පරීක්ෂණය කරයි. පරීක්ෂණය සන්නිවේදනය ගැනයි: තේරුම් ගන්න පුළුවන් වීම, කතාව ගෙනයාම, නොතේරුණොත් ඇසීම. ඇසීම කවදාවත් අඩුවක් නොවේ."),
        {"type": "sayagain"},
    ]),
    part("talk321", "Then and now", "The same talk as Day 0. Your Day 0 recording is played next to today's.",
         [("Talk", "tell me about yourself, 3 then 2 then 1 minute", "recorded"), ("Compare", "Day 0 next to today", "listen")],
         [talk321("Tell me about yourself", ["from", "now", "family", "likes", "town", "a plan"])], short=True),
    part("test", "Weekly test", "Scored on being understood, keeping it going and asking when lost, not on perfect grammar.",
         [("Respond", "short remarks", "you talk"), ("Start", "speak first", "you talk"), ("Keep it going", "react and ask", "you talk"),
          ("Chat", "8 turns with a stranger", "you talk"), ("Listen", "short news, 3 questions", "you talk")], [
        {"type": "test", "parts": "A respond · B start · C keep it going · D full conversation · E listening", "pass": 70},
        drill("sam", "Nice bag!", [], "A. Respond"),
        drill("maya", "You look happy today!", [], "A. Respond (unseen)"),
        drill("sam", "(At the bus stop. An old man is waiting next to you. Speak first.)", [], "B. Start (unseen)"),
        drill("maya", "Guess what? My brother is moving to Dubai next week.", [], "C. Keep it going: react + follow-up"),
        chat("maya", "face", "Unseen: a stranger at a wedding",
             "At a cousin's wedding, a young woman you don't know sits next to you. Introduce yourself, find out how she knows the family, talk for a while, and close politely.",
             "ඥාති සහෝදරයෙකුගේ මංගල උත්සවයකදී ඔබ නොදන්නා තරුණියක් ඔබ ළඟ ඉඳගන්නවා. ඔබව හඳුන්වා දී, ඇය පවුලට සම්බන්ධ කොහොමද කියා දැනගෙන, ටික වෙලාවක් කතා කර, ආචාරශීලීව අවසන් කරන්න.",
             "Start → ask → share → close; 8+ turns.", 8,
             "Play a friendly stranger at a wedding who is the bride's colleague. Wait for him to speak first.", "", "At a wedding", "A stranger (Maya plays her)", True),
        listen("sam", "Short news", "Here's the local news. The new bus station in Kandy opens next Monday. Buses to Colombo will leave every thirty minutes, "
               "from five in the morning. Tickets will cost two hundred rupees, and students get half price.",
               ["When does the bus station open?", "How often do buses go to Colombo?", "How much do students pay?"])
    ]),
    review_part(),
])

week1 = {"week": 1, "title": "Unlock: talk about yourself and react", "days": [day0, d1, d2, d3, d4, d5, d6, d7]}
index = {"version": V, "updated": "2026-11-12", "weeks": [{"week": 1, "file": "week-1.json"}]}
with open("week-1.json", "w", encoding="utf-8") as f:
    json.dump(week1, f, ensure_ascii=False, indent=1)
with open("index.json", "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=1)
print("ok", V)
