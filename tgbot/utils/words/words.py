# another
WELCOME_USER = ("Assalomu alaykum !\nMafia botga xush kelibsiz. do'stlaringiz bilan <b>Mafia</b> o'yini"
                " o'ynash uchun meni gruppangizga qo'shing va admin huquqini bering. Omad!")

WELCOME_ADMIN = "Assalomu alaykum! {name}! Siz adminsiz. /help orqali buyruqlarni ko'rishingiz mumkin."
JOIN_GAME = "Siz o'yinga omadli qo'shildingiz <b>{group_name}</b>"

NIGHT = "Ko'chaga faqat jasur va qo'rqmas odamlar chiqishdi. Ertalab tirik qolganlarni sanaymiz..."
DAY = "🏙 {day_count}-kun\nQuyosh chiqib, tunda to'kilgan qonlarni quritdi..."


# roles
PEOPLE_ROLE = "Siz - 👨🏼 Tinch axolisiz.\nSizning vazifangiz mafiani topish va ovoz berish jarayonida ularni osish"
DETECTIVE_ROLE = "Siz- 🕵️‍ Komissar Katani!\nShaharning asosiy ximoyachisi va mafia kushandasi..."
DOCTOR_ROLE = "Siz- 👨🏼‍⚕️ Shifokorsiz!\nTunda kimnidir qutqarib qolishingiz mumkin..."
DON_ROLE = "Siz- 🤵🏻 Donsiz (Mafia sardori)!\nBu tunda kim o'lishini siz xal qilasiz..."
MAFIA_ROLE = ("Siz - 🤵🏼 Mafiasiz!\nDonga bo'ysunasiz va sizga qarshilik qilganlarni o'ldirasiz. Don o'lsa siz yangi "
              "Don bo'lishingiz mumkin.")
LUCKY_ROLE = ("Siz - 🤞 Omadli.\nSizning vazifangiz mafia va yovuzlarni shahar yig'ilishida osish. Agar omadingiz "
              "kelsa, siz omon qolasiz.")
WOLF_ROLE = "Siz - 🐺bo'risiz!\n Sizni Mafia o'ldirsa <b>mafia</b> bo'lasiz. Komisar o'ldirsa <b>komisar</b> bo'lasiz."
LADY_ROLE = """Siz- 💃🏼 Ma'shuqasiz!\nBu shavqatsiz shaxarda tirik qolishingiz kerak. Bir kun davomida har qanday
            shaxsni zararsizlantirish uchun o'z maxoratingizni ko'rsating :)"""
TRIPPER_ROLE = (
    "Siz - 🧙🏼‍♂️ Daydisiz!\nSiz xoxlagan odamning uyiga shisha olish uchun borishingiz va qotillikning guvohi"
    " bo'lib qolishingiz mumkin.")

# actions
DETECTIVE_FIND_ACTION = "Komisar Kotani yovuzlarni qidirishga ketdi"
DETECTIVE_KILL_ACTION = "Komisar Kotani pistoletini o'qladi. Qon to'kilishi aniq"
MAFIA_CHOOSE_ACTION = "Mafia o'ljasini tanladi"
MAFIA_DID_NOT_CHOOSE = "Mafia hech kimni tanlamaslikka qaror qildi"
DIED_ACTION = "Sizni shavqatsizlarcha o'ldirishdi. So'nggi so'zingizni aytishingiz mumkin:"
HANGED_ACTION = "Sizni shavqatsizlarcha osishdi. So'nggi so'zingizni aytishingiz mumkin:"
SCREAM_ACTION = "O'limidan oldin {name}ni qichqirgani eshitildi:\n<i>{scream_text_user}</i>"
LADY_ACTION = "Ma'shuqa o'z ishini boshladi..."
TRIPPER_ACTION = "Siz {player} dan shishalarni oldingiz va orqangizga qaytdingiz. Shubxali narsa sodir bo'lmadi."
TRIPPER_WITNESS_ACTION = ""
TRIPPER_MEET_ACTION = "Tunda siz shisha uchun {player1} ga keldingiz va u yerda {player2} ni ko'rdingiz"

# help words
REMEMBER_PARTNERS = "sheriklaringizni eslab qoling"
TRIPPER = "Don keyingi qurboni uchun ovoz berish o'tkazyapti:"
NO_DIED = "🤷 Ishonish qiyin, lekin bu tunda hech kim o'lmadi"
ELECTION_TIME = "Aybdorlarni aniqlash va jazolash vaqti keldi.\nOvoz berish uchun 60 sekund"
LIVE_PLAYERS = "Ulardan kimlar:\n {tirik o'yinchilar rollari}\nJami: {count}kishi."
VOTED_TO_PLAYER = "{player1} - {player2}ga ovoz berdi"
END_ELECTION = "Rostdan xam {player}ni osmoqchimisiz?"
RESULT_ELECTION = "Ovoz berish natijalari:\n{count_like} 👍  |  {count_dislike} 👎{player} - ni osamiz! :)"
CANNOT_MAKE_DECISION = ("Aholi kelisha olmadi ({count_like} 👍 | {count_dislike} 👎 )... "
                        "Kelisha olmaslik oqibatida hech kim osilmadi...")
