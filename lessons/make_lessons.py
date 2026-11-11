"""Builds the lesson files (Day 0 + Week 1) from week-1-lessons.md.

Step types the app understands:
  info    : a card the app shows (title, en, si), Next
  model   : Sam/Maya says model lines by voice (Again / Next); words hidden
  drill   : a partner says a prompt; he answers by voice; the AI marks Good / Understandable / Try again
  react   : news items; he reacts with the right sound
  listen  : a partner speaks a short script; he answers questions by voice
  chat    : Before you talk (situation EN|සිං) -> conversation (face / video / phone) -> result
  freechat: relaxed chat, no score
  record  : daily review recording (talk on a topic, no score, compared with last time)
  agree   : the Day 0 agreement (tap I agree)
  speed   : listening speed test (Day 0)
  test    : marks the weekly test (its steps are scored together)
Run: python3 make_lessons.py  (writes index.json, day-0.json, week-1.json)
"""
import json

V = 1  # bump when lessons change, so the app shows "New lessons"

def info(title, en, si="", examples=None):
    return {"type": "info", "title": title, "en": en, "si": si, "examples": examples or []}

def model(who, lines, note=""):
    return {"type": "model", "who": who, "lines": lines, "note": note}

def drill(who, prompt, models, point="", si=""):
    return {"type": "drill", "who": who, "prompt": prompt, "models": models, "point": point, "si": si}

def react(who, items):
    return {"type": "react", "who": who, "items": [{"news": n, "feel": f} for n, f in items]}

def listen(who, title, script, questions):
    return {"type": "listen", "who": who, "title": title, "script": script, "questions": questions}

def chat(who, mode, where, en, si, goal, turns, brief, opener, scored=True):
    return {"type": "chat", "who": who, "mode": mode, "where": where, "en": en, "si": si,
            "goal": goal, "minTurns": turns, "brief": brief, "opener": opener, "scored": scored}

def freechat(who, ideas, brief=""):
    return {"type": "freechat", "who": who, "ideas": ideas, "brief": brief}

def record(topic):
    return {"type": "record", "topic": topic}

def session(sid, title, effort, steps):
    return {"id": sid, "title": title, "effort": effort, "steps": steps}

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

# ---------------------------------------------------------------- Day 0
day0 = {
    "day": 0, "title": "Day 0: Set-up and starting point", "companion": "both",
    "sessions": [
        session("welcome", "Welcome", "easy", [
            info("Welcome!", "In this app you learn by speaking. Every day has 4 sessions: Learn, Meet someone and talk, "
                 "Listen and react, and Free chat. You talk to Sam and Maya, two friends from your class.\n"
                 "Tap the mic to speak English. Tap සිං when you're stuck and say it in Sinhala: the app helps you say it in English.",
                 "මෙම යෙදුමේ ඔබ කතා කරමින් ඉගෙන ගන්නවා. සෑම දිනකම සැසි 4ක් තියෙනවා: ඉගෙනීම, කෙනෙක් හමුවී කතා කිරීම, "
                 "අහලා ප්‍රතිචාර දැක්වීම, සහ නිදහස් කතාව. ඔබ කතා කරන්නේ ඔබේ පන්තියේ යාළුවන් දෙදෙනෙක් වන Sam සහ Maya සමඟ.\n"
                 "ඉංග්‍රීසියෙන් කතා කිරීමට mic එක ඔබන්න. හිරවුණොත් සිං ඔබා සිංහලෙන් කියන්න: යෙදුම එය ඉංග්‍රීසියෙන් කියන්න උදව් කරයි."),
            model("sam", ["Hey! I'm Sam. I'm in your English class. I'm a huge Marvel fan. Iron Man, Thor, all of them!"]),
            model("maya", ["Hi, I'm Maya. I'm in your class too. I love Hannibal, and Batman is way better than Marvel. Sorry, Sam!"]),
            drill("sam", "So, what's your name? Tell me a little about yourself!", [
                "Hi Sam! I'm [his name]. I'm a student, and I really love movies.",
                "Hi! My name is [his name]. Nice to meet you. I like movies, especially the Avengers."],
                "Say hello, your name, and one thing about you."),
            {"type": "agree", "en": "Your voice (and later your camera, only in video calls) goes to Google's AI to help you learn. Nothing is shared with anyone else.",
             "si": "ඔබට ඉගෙන ගැනීමට උදව් කිරීමට ඔබේ හඬ (පසුව වීඩියෝ ඇමතුම්වලදී පමණක් කැමරාව) Google හි AI වෙත යයි. වෙන කිසිවෙකු සමඟ බෙදා ගන්නේ නැහැ."},
        ]),
        session("asking", "Asking for help", "easy", [
            ASKING,
            drill("sam", "So yesterday I went to the cinema with my cousins and we watched the new Marvel film and it was absolutely incredible and then we went for pizza and—",
                  ["Whoa, slow down a bit!", "Sorry, could you slow down a bit?"],
                  "Sam is talking too fast on purpose. Ask him to slow down."),
            drill("maya", "Lecter is such an enigmatic character, don't you think?",
                  ["Sorry, what does 'enigmatic' mean?", "What's 'enigmatic'?"],
                  "Maya used a word you may not know. Ask what it means."),
            drill("maya", "Tell me one thing you did today. If a word is missing, tap සිං and say that part in Sinhala.",
                  ["I watched a movie today.", "I went to class and then I came home."],
                  "Practise the switch: English, then සිං for the missing word, then back to EN."),
        ]),
        session("favourites", "Your favourites", "easy", [
            {"type": "record", "topic": "What movies do you love? Thor? Batman? Mad Max? Tell Maya about your favourite movies and why you like them.",
             "saveAs": "favourites", "who": "maya"},
            {"type": "speed"},
        ]),
        session("diagnostic", "Starting test", "medium", [
            info("Your starting point", "Just do your best. These answers are your starting point: at the end of the week you'll hear them again and see how far you've come.",
                 "ඔබට හැකි උපරිමය කරන්න. මෙම පිළිතුරු ඔබේ ආරම්භක ලක්ෂ්‍යයයි: සතිය අවසානයේ ඔබට ඒවා නැවත අසා ඔබ කොතරම් දියුණු වී ඇත්දැයි බලන්න පුළුවන්."),
            drill("sam", "Nice haircut!", [], "Answer however you can.", ""),
            drill("maya", "You look tired today.", [], "Answer however you can."),
            drill("sam", "Hey, are you a movie fan?", [], "Answer however you can."),
            drill("maya", "Your English is good!", [], "Answer however you can."),
            drill("sam", "Long time no see!", [], "Answer however you can."),
            {"type": "record", "topic": "Tell me about yourself: who you are, what you do, what you like.", "saveAs": "baseline-talk", "who": "maya"},
            freechat("both", ["Which is better: Marvel or Batman?", "A movie you watched recently"],
                     "First taste: an easy chat. Sam and Maya disagree about a film and ask what he thinks. No score."),
        ]),
    ],
}

# ---------------------------------------------------------------- Week 1
def day(n, title, companion, connectors, sound, sessions, review):
    return {"day": n, "title": title, "companion": companion, "connectors": connectors, "sound": sound,
            "review": review, "sessions": sessions}

d1 = day(1, "Respond to compliments and a first meeting", "sam", ["actually", "because", "by the way"],
         "v / w: very, movie, Avengers vs well, wow, watch, what", [
    session("learn", "Learn", "hard", [
        info("Today: respond, don't just answer", "When someone says something nice or surprising, don't stop at \"Thanks.\"\n"
             "Pattern: React → add a detail with a connector → bounce it back.\nNew connectors: actually · because · by the way.\n"
             "Long reply for friends; short reply (\"Oh, thanks!\" + a smile) when the moment is short.",
             "කවුරුහරි හොඳ හෝ පුදුම දෙයක් කිව්වම \"Thanks.\" කියලා නවතින්න එපා.\nරටාව: ප්‍රතිචාරය → connector එකක් සමඟ විස්තරයක් → ආපසු ප්‍රශ්නයක්.\n"
             "නව connectors: actually (ඇත්තටම) · because (නිසා; ඉංග්‍රීසියේ හේතුව පස්සේ) · by the way (කතාවට).\nයාළුවන්ට දිගු පිළිතුරක්; කෙටි මොහොතකට කෙටි පිළිතුරක්."),
        model("sam", ["Nice haircut!", "Oh, thanks! I actually got it yesterday, because I have an interview next week. By the way, I like your shirt.",
                      "Or, if there's no time: Oh, thanks!"], "Listen to the pattern: react, detail with actually and because, bounce back."),
        drill("sam", "Nice haircut!", ["Oh, thanks! I actually got it yesterday, because I have an interview next week. By the way, I like your shirt.",
               "Oh, thank you! I actually got it this morning, because it was too long. By the way, where do you get yours cut?"],
              "React, add a detail with because, bounce it back.", "ප්‍රතිචාරය + because සමඟ හේතුව + ආපසු ප්‍රශ්නයක්."),
        drill("sam", "Did you cut it yourself?", ["No, I got it at the barber.", "Haha, no! I got it at the barber near my house."],
              "\"I cut it\" means YOU cut it. Say \"I got it…\"", "\"I cut it\" කිව්වොත් ඔබම කැපුවා කියන එකයි. \"I got it…\" කියන්න."),
        drill("maya", "Hi! You must be new in this class.", ["Oh, yes! I actually started today. I'm [his name], by the way. How long have you been here?",
               "Yes, it's my first day, actually. I'm [his name]. Is the teacher strict?"], "Detail + your name + bounce it back."),
        drill("sam", "Hey, are you a movie fan?", ["Oh, yes! I actually love movies, especially the Avengers, but my favourite is Hannibal. What about you?",
               "Yes, a big one! I watch a movie almost every night, because it helps me relax. By the way, have you seen Endgame?"],
              "Use especially and but."),
        drill("maya", "Your English is good!", ["Oh, really? Thanks! I'm practising every day, because I want to watch movies without subtitles. How did you learn yours?",
               "Oh, thank you! I'm still learning."], "Accept the compliment. Don't say \"No, it's bad.\""),
    ]),
    session("talk", "Meet someone and talk", "hard", [
        chat("sam", "face", "The college canteen, your first day in a new class",
             "It's your first day in a new class. At the canteen, Sam (from your class) comes over. He'll give you a few compliments, then talk about movies. "
             "You don't know exactly what he'll say. Use the pattern, ask him things back, and keep it going.",
             "අද නව පන්තියේ ඔබේ පළමු දිනයයි. ආපනශාලාවේදී Sam (ඔබේ පන්තියෙන්) ඔබ ළඟට එනවා. ඔහු ප්‍රශංසා කිහිපයක් කර චිත්‍රපට ගැන කතා කරයි. "
             "ඔහු කියන දේ හරියටම දන්නේ නැහැ. රටාව භාවිත කරන්න, ආපසු ප්‍රශ්න අහන්න, කතාව දිගටම ගෙනියන්න.",
             "Use the pattern; ask back 3+ times; 8+ turns.", 8,
             "You meet him on his first day in a new class at the canteen. Give him 3 compliments (haircut, shirt, his English) one at a time, "
             "then talk about movies. Once, speak a little fast on purpose so he practises asking you to slow down.",
             "Hey! You're new, right? Nice haircut, by the way!"),
    ]),
    session("listen", "Listen and react", "medium", [
        listen("maya", "Why Maya loves Batman",
               "Okay, so, why do I love Batman? Well, first, he has no superpowers. He's just a man, and he's really smart. "
               "Second, the stories are dark and serious, not silly. My favourite is The Dark Knight, because the Joker is brilliant. "
               "And honestly, Batman is just cooler than Iron Man. Sorry, Sam!",
               ["Why does Maya say Batman is special?", "Do you agree with her? Why or why not?", "Ask Maya one question about Batman."]),
        REACT_SOUNDS,
        react("maya", [("I passed my driving test yesterday!", "good"), ("My phone fell in the lake.", "bad"),
                       ("They're making a new Hannibal film!", "surprise"), ("I'm thinking of learning the guitar.", "interest")]),
    ]),
    session("free", "Free chat", "relaxed", [
        freechat("maya", ["Your clothes today", "Your favourite movie", "Your first day in class"]),
        record("Tell Maya about yourself and the movies you love."),
    ]),
], "Tell Maya about yourself and the movies you love.")

d2 = day(2, "Respond to comments, catching up and teasing", "maya", ["so", "that's why", "anyway"],
         "f / p: film, favourite, funny vs pen, park, popcorn", [
    session("learn", "Learn", "hard", [
        info("Today: comments and teasing", "Friends say things like \"You look tired\" or \"Late again?\". Laugh → admit it or play along → add a detail → move on with \"anyway\".\n"
             "New connectors: so · that's why · anyway.",
             "යාළුවන් \"You look tired\" හෝ \"Late again?\" වගේ දේවල් කියනවා. හිනාවෙන්න → පිළිගන්න නැත්නම් විහිළුවට එකඟ වෙන්න → විස්තරයක් → \"anyway\" සමඟ ඉදිරියට.\n"
             "නව connectors: so (ඒ නිසා) · that's why (ඒකයි) · anyway (කොහොම හරි)."),
        drill("maya", "You look tired.", ["Yeah, a bit. I slept late because I was watching Infinity War again. Have you seen it?",
               "Honestly, yes. I had a long day, that's why. But I'm OK!"], "\"a bit\" makes it softer; \"that's why\" goes at the end."),
        drill("maya", "Long time no see!", ["Oh, yes! It's been ages! I was busy at home, so I didn't go out much. How have you been?",
               "I know! I was studying a lot. Anyway, how are you?"], "\"It's been ages!\" + so."),
        drill("maya", "Late again?", ["Haha, sorry! The bus was late because of the rain. Anyway, I'm here now!", "Sorry, sorry! The bus!"],
              "Laugh first; because of + a thing; anyway."),
        drill("sam", "Hannibal again? Aren't you scared?", ["Haha, no way! I actually like it, because Lecter is so clever and calm. Anyway, you should watch it!",
               "A little, honestly! But the story is so good, so I keep watching."], "Laugh, play along, move on with anyway."),
    ]),
    session("talk", "Meet someone and talk", "hard", [
        chat("maya", "video", "A video call from Maya after a long time",
             "Maya calls you on video after a long time. She wants to catch up, and she'll tease you a couple of times (about Marvel!). Laugh, play along, and keep it going.",
             "බොහෝ කාලෙකට පස්සේ Maya ඔබට වීඩියෝ ඇමතුමක් ගන්නවා. ඇයට අලුත් විස්තර දැනගන්න ඕනේ, ඇය ඔබට (Marvel ගැන!) දෙපාරක් විහිළු කරයි. හිනාවෙන්න, එකඟ වෙන්න, කතාව ගෙනියන්න.",
             "Laugh and play along; 10+ turns.", 10,
             "You call him on video after a long time to catch up. Tease him twice, e.g. \"Still watching Marvel? Batman is better!\".",
             "Hey! Long time no see! Where have you been?"),
    ]),
    session("listen", "Listen and react", "medium", [
        listen("sam", "Sam's voice message",
               "Hey, it's Sam! So, my weekend was crazy. On Saturday I went to my cousin's birthday party, and we played cricket till it got dark. "
               "Then on Sunday I watched Thor: Ragnarok again. It's so funny! Anyway, call me back, okay?",
               ["What did Sam do on Saturday?", "What do you think of Sam's weekend?", "Ask Sam one question about his weekend."]),
        react("sam", [("I lost my wallet on the bus.", "bad"), ("I got tickets for the new Avengers film!", "good"),
                      ("My little brother ate my birthday cake.", "funny"), ("I'm moving to Kandy next month.", "surprise")]),
    ]),
    session("free", "Free chat", "relaxed", [
        freechat("maya", ["How your week has been", "What you watched recently", "Something funny that happened"]),
        record("How have you been this week? What did you watch?"),
    ]),
], "How have you been this week? What did you watch?")

d3 = day(3, "Start a conversation (openers)", "both", ["isn't it?", "huh?", "how about you?"],
         "th: think, thanks, three, Thor and this, that, the, they", [
    session("learn", "Learn", "hard", [
        info("Today: you speak first", "Pattern: Notice → comment or question → add yourself → hand over.\n"
             "Example: \"Hot today, isn't it? I'm actually sweating already. How about you?\"\n"
             "If the other person answers coldly (\"Yes.\"), ask a second question. If it's going nowhere: \"Anyway, nice talking to you!\"",
             "රටාව: දකින්න → අදහසක් හෝ ප්‍රශ්නයක් → ඔබ ගැන ටිකක් → අනෙකාට භාර දෙන්න.\n"
             "isn't it? = නේද? · How about you? = ඔයාට කොහොමද?\nඅනෙකා සීතල ලෙස පිළිතුරු දුන්නොත් (\"Yes.\"), දෙවන ප්‍රශ්නයක් අහන්න."),
        drill("sam", "(A hot day. You're standing next to a stranger. Speak first.)", ["Hot today, isn't it? I'm actually sweating already. How about you? Do you like this weather?"],
              "Notice → comment → add yourself → hand over."),
        drill("maya", "(A bus stop. The bus is late. Speak first to the woman next to you.)", ["Excuse me, are you waiting for the 138 too? It's really late today, huh? Do you take this bus every day?"],
              "Use \"huh?\" to sound friendly."),
        drill("sam", "(A cinema ticket queue for the new Marvel film. Speak first.)", ["Excuse me, are you here for the Marvel film too? I've been waiting for it for weeks, so I'm really excited. How about you?"],
              "Add yourself with \"so\"."),
        drill("maya", "(Someone is wearing a superhero T-shirt. Speak first.)", ["Nice T-shirt! Are you a Marvel fan? Me too, actually. Who's your favourite?"],
              "Compliment + question."),
        drill("sam", "Yes.", ["Oh, cool. Do you come here often?", "Nice. Which part did you like most?"],
              "A cold answer! Don't give up: ask a second question."),
    ]),
    session("talk", "Meet someone and talk", "hard", [
        chat("maya", "face", "A cinema queue: you speak first to a stranger",
             "You're in the ticket queue for a new Marvel film. Next to you is a young woman you don't know. Start the conversation yourself: notice, comment, add yourself, hand over. "
             "She may be chatty or a bit cold. If she talks fast, ask her politely to slow down.",
             "ඔබ නව Marvel චිත්‍රපටයක ටිකට් පෝලිමේ ඉන්නවා. ඔබ ළඟ ඔබ නොදන්නා තරුණියක් ඉන්නවා. කතාව ඔබම පටන් ගන්න: දකින්න, අදහසක්, ඔබ ගැන, භාර දෙන්න. "
             "ඇය කතාබහට කැමති හෝ ටිකක් සීතල වෙන්න පුළුවන්. ඇය වේගයෙන් කතා කළොත් ආචාරශීලීව සෙමින් කතා කරන්න කියන්න.",
             "He speaks first; opener + add yourself + hand over; rescue one cold reply; 8+ turns.", 8,
             "Play a stranger (not Maya) in a cinema queue. HE must speak first: wait for him. Be a little cold at first (short answers), then warm up if he asks good questions. Once, speak a little fast.",
             ""),
    ]),
    session("listen", "Listen and react", "medium", [
        listen("sam", "A cinema announcement",
               "Good evening, everyone. The seven o'clock show of Avengers: Endgame is now open in Screen 2. Please have your tickets ready. "
               "The nine fifteen show is sold out. Popcorn and drinks are available near the entrance. Enjoy the film!",
               ["Which screen is Endgame in?", "Would you rather see the 7 o'clock show or a later one? Why?", "Ask a question you would ask the ticket staff."]),
        react("maya", [("The bus is forty minutes late!", "bad"), ("I found a hundred rupees in my old jeans!", "good"),
                       ("They say it'll rain all week.", "bad"), ("Guess what? I'm learning to cook!", "interest")]),
    ]),
    session("free", "Free chat", "relaxed", [
        freechat("sam", ["Places where you meet new people", "The weather today", "A film you want to see"]),
        record("Start a conversation with someone in a cinema queue."),
    ]),
], "Start a conversation with someone in a cinema queue.")

d4 = day(4, "Keep the other person talking (\"Oh!\" day)", "maya", ["really?", "and then?", "what happened next?"],
         "word endings -s / -ed: movies, likes, watched, finished", [
    session("learn", "Learn", "hard", [
        info("Today: keep them talking", "React with the right sound, then ask a follow-up question.\n"
             "• What happened: And then? · What did you do?\n• Feelings: How did you feel? · Were you scared?\n• Details: Where was that? · Who was with you?\n"
             "• Opinion: Did you like it?\nEcho questions: \"I went to Kandy.\" → \"Oh, Kandy? What did you do there?\"",
             "හරි ශබ්දයෙන් ප්‍රතිචාර දක්වා ඊළඟ ප්‍රශ්නයක් අහන්න.\nEcho ප්‍රශ්න: ඔවුන්ගේ ප්‍රධාන වචනය නැවත කියා අහන්න: \"Oh, Kandy? What did you do there?\""),
        drill("maya", "Last Saturday I went to see a film…", ["Oh, nice! Which film?"], "React + follow-up."),
        drill("maya", "…a Batman film. But in the middle, the power went off!", ["Oh no! What happened next?"], "Right sound for bad news + follow-up."),
        drill("maya", "We waited forty minutes in the dark!", ["Forty minutes? Really? Did they give your money back?"], "Echo question."),
        drill("sam", "I went to Kandy last weekend.", ["Oh, Kandy? What did you do there?"], "Echo question."),
        drill("sam", "I watched The Dark Knight again yesterday.", ["Oh, The Dark Knight? How many times have you seen it?"], "Echo question."),
    ]),
    session("talk", "Meet someone and talk", "hard", [
        chat("maya", "phone", "A phone call from Maya with news",
             "Maya phones you with some news: something good, something bad and something funny (one about a film). On the phone there's no face to help, so react with your voice, ask follow-up questions, and ask when you don't catch something.",
             "Maya ඔබට දුරකථනයෙන් පුවත් කිහිපයක් කියයි: හොඳ දෙයක්, නරක දෙයක් සහ විහිළු දෙයක් (එකක් චිත්‍රපටයක් ගැන). දුරකථනයේදී මුහුණක් නැති නිසා හඬින් ප්‍රතිචාර දක්වා, ප්‍රශ්න අසා, නොතේරුණොත් අහන්න.",
             "Right reaction every time; 6+ follow-ups; ask once when unsure; 12+ turns.", 12,
             "You phone him with news, one piece at a time: good news, then bad news, then something funny about a film. Pause after each piece so he reacts and asks.",
             "Hey! It's Maya. You won't believe what happened today!"),
    ]),
    session("listen", "Listen and react", "medium", [
        listen("sam", "Sam's story (guess what happens)",
               "So, last week I was at the cinema with my brother. The film started, and suddenly a cat walked in front of the screen! "
               "Everyone started laughing. Then the cat sat down in the front row, like it wanted to watch the film too!",
               ["What happened at the cinema?", "What would you do if a cat sat next to you in the cinema?", "Ask Sam a follow-up question about the cat."]),
        react("sam", [("I broke my phone screen.", "bad"), ("I won a free pizza!", "good"), ("My teacher sang in class today!", "funny"),
                      ("I met an actor at the airport!", "surprise"), ("My grandmother is in hospital.", "bad")]),
    ]),
    session("free", "Free chat", "relaxed", [
        freechat("maya", ["Something that happened to you this week", "A trip you took", "A funny family story"]),
        record("React to news: tell Maya about something that happened recently, and ask her about her week."),
    ]),
], "Tell Maya about something that happened recently, and ask about her week.")

d5 = day(5, "Hold a longer turn (a 1-minute story)", "sam", ["meanwhile", "suddenly", "in the end"],
         "word stress: YES-ter-day, a-VEN-gers, DAN-ger-ous, re-VENGE, e-SCAPE", [
    session("learn", "Learn", "hard", [
        info("Words first", "brilliant = very, very clever · dangerous = can hurt you · revenge = hurting someone back · enemy = a person against you · escape = get away",
             "brilliant = ඉතා දක්ෂ · dangerous = අනතුරුදායක · revenge = පළිගැනීම · enemy = සතුරා · escape = පැනයාම"),
        info("Story shape", "Hook → first → then → meanwhile → suddenly → in the end → how I felt.\n"
             "Hooks: \"You won't believe what happened…\" · \"Guess what?\" · \"Have you seen…? It's about…\"",
             "කතාවේ හැඩය: ආකර්ෂණය → මුලින්ම → ඊට පස්සේ → ඒ අතරේ (meanwhile) → හදිස්සියේම (suddenly) → අන්තිමට (in the end) → මට දැනුණු දේ."),
        model("sam", ["You won't believe what happened yesterday. First, I woke up late, because my phone was dead. Then I ran to the bus stop, but the bus was leaving. "
                      "Meanwhile, it started raining! Suddenly, my friend stopped his bike and gave me a ride. In the end, I was only five minutes late. I was so lucky!"],
              "A 1-minute story from life. Listen for meanwhile, suddenly, in the end."),
        drill("sam", "So, what happened to you this week? Tell me a short story!", [], "Use first, then, suddenly, in the end."),
        drill("sam", "I've never seen Hannibal. What's it about?", ["Hannibal is about a brilliant but dangerous man called Hannibal Lecter. At the start, he's living secretly in Italy. "
               "Meanwhile, an FBI agent called Clarice is in trouble at work. Then a rich man who wants revenge starts hunting Lecter. Suddenly, Lecter is caught, but Clarice saves him, even though he's her enemy. "
               "In the end, he escapes again. I love it because Lecter is so calm and clever."], "Retell the film in about a minute."),
    ]),
    session("talk", "Meet someone and talk", "hard", [
        chat("sam", "video", "A video call: Sam hasn't seen Hannibal",
             "Sam hasn't seen Hannibal and thinks it's too scary. Tell him a story from your life and retell the film. Answer his questions and try to convince him to watch it.",
             "Sam Hannibal බලලා නැහැ, ඔහු හිතන්නේ එය බය හිතෙන චිත්‍රපටයක් කියලා. ඔබේ ජීවිතයෙන් කතාවක් කියා චිත්‍රපටය නැවත කියන්න. ඔහුගේ ප්‍රශ්නවලට පිළිතුරු දී එය බලන්න ඔහුව ඒත්තු ගන්වන්න.",
             "Tell 2 stories; answer follow-ups; convince Sam.", 10,
             "You haven't seen Hannibal and think it's too scary. Ask him what it's about, react with Oh! and And then?, ask follow-ups, and let him convince you.",
             "Hey! So everyone keeps talking about Hannibal. What's it about? Isn't it too scary?"),
    ]),
    session("listen", "Listen and react", "medium", [
        listen("maya", "Nila tells a famous story",
               "Long ago, a clever boy called Aladdin found an old lamp in a cave. When he rubbed it, a genie came out and offered him three wishes. "
               "Aladdin used his wishes wisely, and in the end, he set the genie free.",
               ["Retell the story in three sentences.", "What would your three wishes be?", "Ask one question about the story."]),
        react("maya", [("I finished my first painting!", "good"), ("Our trip got cancelled.", "bad"), ("A monkey stole my sandwich!", "funny"), ("I'm getting a puppy!", "good")]),
    ]),
    session("free", "Free chat", "relaxed", [
        freechat("sam", ["The best film you've ever seen", "A lucky day", "A scary moment"]),
        record("Retell your favourite film in one minute."),
    ]),
], "Retell your favourite film in one minute.")

d6 = day(6, "Full conversations", "both", ["well", "let me think", "I mean"],
         "questions that go up: Really? ↗ Are you a Marvel fan? ↗", [
    session("learn", "Learn", "hard", [
        info("Today: the whole conversation", "Start → respond → keep it going → tell a story → close.\n"
             "Buy time instead of freezing: \"Well…\" · \"Let me think…\" · \"I mean…\"\n"
             "Close politely: \"Anyway, I'd better go. It was nice talking to you!\" · \"Sorry, my bus is here. Nice meeting you!\"",
             "පටන් ගන්න → ප්‍රතිචාර දක්වන්න → දිගටම ගෙනියන්න → කතාවක් කියන්න → අවසන් කරන්න.\nහිර නොවී කාලය ගන්න: \"Well…\" · \"Let me think…\" · \"I mean…\"\n"
             "ආචාරශීලීව අවසන් කරන්න: \"Anyway, I'd better go. It was nice talking to you!\""),
        drill("sam", "So, when are YOU getting married?", ["Haha, well… let me think… not for a long time, I hope! I mean, I'm still studying. What about you?"],
              "A surprise question: buy time, then answer."),
        drill("maya", "Better than Endgame? What do YOU think?", ["Hmm, well, I mean, Endgame was amazing, but this one was really fun too. Let's just say both are great!"],
              "Give an opinion and keep the peace."),
        drill("sam", "(It's time to go. Close the conversation politely.)", ["Anyway, I'd better go. It was nice talking to you!", "Oh, look at the time! I have to run. See you tomorrow!"],
              "Close politely."),
    ]),
    session("talk", "Meet someone and talk", "hard", [
        chat("maya", "face", "A cousin's wedding: talking to your uncle",
             "You're at your cousin's wedding. Your uncle comes over to chat, and he likes to tease. He might ask when YOU are getting married! Start or respond naturally, keep it going, tell a short story, and close politely.",
             "ඔබ ඔබේ ඥාති සහෝදරයාගේ මංගල උත්සවයේ. ඔබේ මාමා කතා කරන්න එනවා, ඔහු විහිළු කරන්න කැමතියි. ඔහු \"ඔයා කවදද කසාද බඳින්නේ?\" කියා අහන්න පුළුවන්! ස්වාභාවිකව කතා කර, කතාවක් කියා, ආචාරශීලීව අවසන් කරන්න.",
             "Reaction sounds, follow-ups, one longer answer, a time-buyer instead of silence, a polite close; 12+ turns.", 12,
             "Play his uncle (not Maya) at a cousin's wedding: friendly, a bit of a tease. Ask about his studies and films, and at some point ask: \"So, when are YOU getting married?\"",
             "Ah, there you are! Look at you, all dressed up! How have you been?"),
    ]),
    session("listen", "Listen and react", "medium", [
        listen("sam", "Two people at a bus stop",
               "Excuse me, is this the bus to Colombo? Yes, it is, but it's always late. Oh no, I have an interview at ten! "
               "Really? Good luck! What's the job? It's at a bank. Oh, nice! Well, here it comes now. Finally!",
               ["Who are the two people and what are they talking about?", "Have you ever been late for something important?", "Ask one question you'd ask the person with the interview."]),
        react("maya", [("I got the job!", "good"), ("I failed my exam.", "bad"), ("Did you know? Thor's hammer has a name: Mjolnir.", "interest"), ("My cat learned to open the fridge!", "funny")]),
    ]),
    session("free", "Free chat", "relaxed", [
        freechat("both", ["Which realm of Thor's world would you visit?", "A family wedding", "Your plans for next week"]),
        record("Talk about your week: what you learned, what was hard, what was fun."),
    ]),
], "Talk about your week.")

d7 = day(7, "Review and weekly test", "both", [], "review", [
    session("learn", "Review", "medium", [
        info("Review", "Today you go over the week, then do the weekly test. The test is about communication: being understood, keeping it going, asking when lost. Asking is never a minus.",
             "අද ඔබ සතිය නැවත බලා සතිපතා පරීක්ෂණය කරයි. පරීක්ෂණය සන්නිවේදනය ගැනයි: තේරුම් ගන්න පුළුවන් වීම, කතාව ගෙනයාම, නොතේරුණොත් ඇසීම. ඇසීම කවදාවත් අඩුවක් නොවේ."),
        {"type": "sayagain"},
    ]),
    session("test", "Weekly test", "hard", [
        {"type": "test", "parts": "A respond · B start · C keep it going · D long turn · E full conversation", "pass": 70},
        drill("sam", "Nice shirt!", [], "A. Respond"),
        drill("maya", "You look happy today!", [], "A. Respond (unseen)"),
        drill("sam", "Late again?", [], "A. Respond"),
        drill("maya", "Is that a new phone?", [], "A. Respond (unseen)"),
        drill("sam", "(A lift. A man with a Batman bag. Speak first.)", [], "B. Start (unseen)"),
        drill("maya", "(The college canteen is very crowded today. Speak first.)", [], "B. Start"),
        drill("maya", "Guess what? Yesterday I went to the beach, and suddenly a huge wave took my bag!", [], "C. Keep it going: react + follow-up"),
        drill("sam", "Tell me a 1-minute story: something from your life, or your favourite film.", [], "D. Long turn"),
        chat("maya", "face", "Unseen: a misunderstanding at the cinema",
             "At the cinema, a young woman says you're sitting in her seat. Sort out the misunderstanding politely, then chat a little about the film, and close politely.",
             "සිනමා ශාලාවේදී තරුණියක් කියනවා ඔබ ඇගේ ආසනයේ ඉඳගෙන ඉන්නවා කියලා. වැරදි වැටහීම ආචාරශීලීව විසඳා, චිත්‍රපටය ගැන ටිකක් කතා කර, ආචාරශීලීව අවසන් කරන්න.",
             "Start → sort it out → story → close; 12+ turns.", 12,
             "Play a stranger at the cinema who thinks he is in her seat (seat H7). Be polite but firm; it turns out his ticket says H8. Then chat about the film.",
             "Excuse me, sorry, I think you're in my seat?", True),
    ]),
    session("free", "Free chat", "relaxed", [
        freechat("both", ["What was hardest this week?", "Your favourite moment this week", "What you want to learn next"]),
        record("Tell me about yourself: who you are, what you do, what you like."),
    ]),
], "Then vs now: tell me about yourself.")

week1 = {"week": 1, "title": "Week 1: Respond, Start, Keep It Going", "version": V,
         "note": "Each week is written at the end of the previous one, from his results.",
         "days": [day0, d1, d2, d3, d4, d5, d6, d7]}

index = {"version": V, "updated": "2026-11-11", "weeks": [{"week": 1, "file": "week-1.json"}]}

with open("week-1.json", "w", encoding="utf-8") as f:
    json.dump(week1, f, ensure_ascii=False, indent=1)
with open("index.json", "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=1)
print("ok", sum(len(s["steps"]) for d in week1["days"] for s in d["sessions"]), "steps")
