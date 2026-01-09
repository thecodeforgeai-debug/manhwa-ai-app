#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = "data/manhwa.db"

MANHWA_LIST = [
    ("Tower of God", "action,fantasy,adventure", "overpowered-mc,underdog-to-hero", "A boy enters a mysterious tower to find his friend, facing increasingly difficult tests and powerful enemies on each floor."),
    ("The Beginning After The End", "action,fantasy,isekai", "reincarnation,overpowered-mc,magic", "A king reincarnates into a world of magic and monsters, using his past life's knowledge to become powerful."),
    ("Omniscient Reader's Viewpoint", "action,fantasy,apocalypse", "game-elements,smart-mc,survival", "A man finds himself living in the world of a web novel he was the only reader of, using his knowledge to survive."),
    ("Nano Machine", "action,martial-arts,sci-fi", "overpowered-mc,weak-to-strong,revenge", "An outcast descendant receives a nanomachine from the future, revolutionizing martial arts."),
    ("Return of the Frozen Player", "action,fantasy,apocalypse", "returned-hero,overpowered-mc,game-elements", "After being frozen for 25 years, a legendary player returns to fight the monsters that destroyed humanity."),
    ("Hardcore Leveling Warrior", "action,fantasy,game", "fall-from-grace,redemption,game-elements", "The #1 ranked player loses everything and must climb back to the top from level 1."),
    ("Legendary Moonlight Sculptor", "action,fantasy,game", "poor-to-rich,hardworking-mc,game-elements", "A poor man plays a VR game to support his family, becoming a legendary sculptor and warrior."),
    ("Second Life Ranker", "action,fantasy,game", "revenge,tower-climbing,overpowered-mc", "A man climbs the tower to find out what happened to his twin brother and take revenge."),
    ("The Breaker", "action,martial-arts,school", "weak-to-strong,master-student,martial-arts", "A bullied student becomes the disciple of a legendary martial artist, entering the dangerous martial arts world."),
    ("The Breaker: New Waves", "action,martial-arts,school", "overpowered-mc,martial-arts,student-becomes-master", "Continuation of The Breaker as the protagonist grows stronger and faces greater threats."),
    ("True Beauty", "romance,comedy,school", "transformation,love-triangle,self-discovery", "A girl becomes popular after mastering makeup, hiding her bare face while navigating love and friendship."),
    ("What's Wrong with Secretary Kim", "romance,comedy,office", "boss-employee,misunderstanding,past-trauma", "A secretary decides to quit after 9 years, making her boss realize his feelings for her."),
    ("A Business Proposal", "romance,comedy,office", "fake-dating,contract-relationship,boss-employee", "A woman goes on a blind date pretending to be her friend, not knowing the man is her company's CEO."),
    ("My ID is Gangnam Beauty", "romance,drama,school", "plastic-surgery,self-acceptance,bullying", "A girl gets plastic surgery to escape bullying but faces new challenges in college."),
    ("Cheese in the Trap", "romance,drama,psychological", "complicated-relationship,campus-life,mystery", "A college student returns to school and gets entangled with a popular but mysterious senior."),
    ("I Love Yoo", "romance,drama,slice-of-life", "found-family,slow-burn,trauma", "A cynical girl who doesn't believe in love finds herself surrounded by people who change her perspective."),
    ("Siren's Lament", "romance,fantasy,supernatural", "curse,transformation,love-triangle", "A girl is turned into a siren and must navigate love while hiding her new identity."),
    ("Lore Olympus", "romance,fantasy,mythology", "age-gap,power-imbalance,greek-mythology", "A modern retelling of Hades and Persephone's romance in a vibrant, stylized world."),
    ("Let's Play", "romance,comedy,gaming", "game-developer,online-hate,slow-burn", "A female game developer faces harassment from a famous streamer who doesn't know she's his neighbor."),
    ("Age Matters", "romance,drama,age-gap", "boss-employee,maturity-gap,healing", "A young woman falls for her older boss while dealing with workplace challenges."),
    ("The Villainess Lives Twice", "isekai,romance,fantasy", "time-travel,political-intrigue,redemption", "A villainess goes back in time to change her fate and prevent her family's downfall."),
    ("Beware the Villainess", "isekai,romance,comedy", "strong-female-lead,subversion,comedy", "A woman wakes up as a villainess and decides to ignore the useless male leads and protect the heroine."),
    ("Death Is The Only Ending For The Villainess", "isekai,romance,fantasy", "hard-mode,survival,multiple-endings", "A girl is trapped in a game as the villainess on hard mode where every choice leads to death."),
    ("I'm the Villainess, So I'm Taming the Final Boss", "isekai,romance,comedy", "villainess-route,demon-king,comedy", "A reincarnated villainess decides to avoid her doom by winning over the demon king instead."),
    ("The Reason Why Raeliana Ended up at the Duke's Mansion", "isekai,romance,mystery", "contract-relationship,mystery,survival", "A woman reincarnated into a novel must avoid her character's death by striking a deal with the male lead."),
    ("Doctor Elise: The Royal Lady with the Lamp", "isekai,romance,medical", "doctor,redemption,second-chance", "A queen reincarnates as a doctor, then back to her original world, using medical knowledge to change her fate."),
    ("Survive as the Hero's Wife", "isekai,romance,fantasy", "supporting-character,survival,romance", "A woman reincarnates as the hero's wife who dies early and must survive while supporting the hero."),
    ("I Became the Wife of the Male Lead", "isekai,romance,fantasy", "obsessive-male-lead,survival,romance", "A woman becomes the wife of an obsessive male lead from a novel she read."),
    ("The Abandoned Empress", "isekai,romance,fantasy", "time-travel,betrayal,revenge", "An empress travels back in time after being executed by her husband to change her tragic fate."),
    ("Who Made Me a Princess", "isekai,fantasy,family", "father-daughter,magic,cute", "A girl reincarnates as a princess whose father will kill her, and must survive while winning his affection."),
    ("Sweet Home", "horror,action,psychological", "monsters,survival,apartment", "Residents of an apartment must survive as people turn into monsters based on their desires."),
    ("Bastard", "thriller,psychological,horror", "serial-killer,father-son,suspense", "A boy discovers his father is a serial killer and must decide whether to stop him or help hide the crimes."),
    ("Distant Sky", "horror,apocalypse,mystery", "survival,darkness,mystery", "A man wakes up in a world covered in darkness with monsters everywhere, searching for other survivors."),
    ("DICE: The Cube That Changes Everything", "action,supernatural,school", "game-elements,transformation,bullying", "Students use mysterious dice to change their stats and abilities in reality."),
    ("The Gamer", "action,fantasy,game", "game-elements,leveling,smart-mc", "A student gains the ability to see the world as a video game and level up his skills."),
    ("Noblesse", "action,supernatural,fantasy", "vampire,nobility,comedy", "An ancient noble awakens after 820 years and adapts to modern life while protecting his friends."),
    ("Eleceed", "action,supernatural,comedy", "mentor-student,powers,comedy", "A kind but powerful boy with super speed meets a mysterious cat who's actually a powerful awakener."),
    ("Kubera", "fantasy,action,mythology", "gods,mystery,complex-plot", "A girl seeks revenge for her destroyed village in a world where gods and humans coexist."),
    ("God of Blackfield", "action,military,revenge", "mercenary,high-school,smart-mc", "A legendary mercenary is killed but wakes up in a high school student's body seeking revenge."),
    ("Mercenary Enrollment", "action,school,military", "overpowered-mc,school-life,mercenary", "A mercenary returns to Korea as a high school student to find his family, hiding his past."),
    ("Legend of the Northern Blade", "action,martial-arts,revenge", "clan-restoration,overpowered-mc,revenge", "The son of a destroyed clan trains in secret to restore his family's honor and take revenge."),
    ("Volcanic Age", "action,martial-arts,regression", "time-travel,second-chance,martial-arts", "A martial artist returns to his youth after living a regretful life, seeking to change history."),
    ("Peerless Dad", "action,martial-arts,family", "single-father,overpowered-mc,wholesome", "A powerful martial artist hides his strength while raising his children peacefully."),
    ("Return of the Mount Hua Sect", "action,martial-arts,comedy", "regression,sect-restoration,comedy", "A disciple of a destroyed sect returns to the past to save his sect from decline."),
    ("The Return of the Crazy Demon", "action,martial-arts,comedy", "regression,overpowered-mc,unhinged-mc", "A chef and secret martial arts master goes back in time with all his powers and knowledge."),
    ("Chronicles of Heavenly Demon", "action,martial-arts,revenge", "reincarnation,demon-sect,revenge", "A loyal warrior is betrayed and reincarnated in the body of a demon sect's weak young master."),
    ("Murim Login", "action,martial-arts,game", "game-elements,modern-hunter,martial-arts", "A weak hunter discovers a VR game that teaches real martial arts from the Murim world."),
    ("Weak Hero", "action,school,psychological", "bullying,smart-mc,revenge", "A physically weak but cunning student takes down bullies using strategy and intelligence."),
    ("How to Fight", "action,school,streaming", "fighting,streamer,weak-to-strong", "A bullied student learns to fight through a mysterious YouTube channel."),
    ("Jungle Juice", "action,supernatural,school", "insect-powers,abilities,survival", "Students with insect-based abilities attend a special school while hiding from the government."),
    ("Viral Hit", "action,school,streaming", "fighting,streamer,weak-to-strong", "A student makes money by fighting on camera, learning various martial arts styles."),
    ("Teen Mercenary", "action,school,mercenary", "mercenary,overpowered-mc,school-life", "A teenage mercenary returns to normal life and school after years of combat."),
    ("Get Schooled", "action,school,teacher", "teacher,justice,violence", "Teachers with combat skills are hired to discipline violent students through force."),
    ("Manager Kim", "action,office,martial-arts", "overpowered-manager,comedy,slice-of-life", "A convenience store manager with a mysterious past deals with troublemakers using martial arts."),
    ("The Boxer", "sports,psychological,action", "boxing,genius,existential", "A boy with incredible reflexes is recruited by a mysterious coach to become the best boxer."),
    ("Yumi's Cells", "romance,comedy,slice-of-life", "cells-personification,relatable,cute", "A woman's daily life shown through the perspective of personified cells in her brain."),
    ("The Sound of Your Heart", "comedy,slice-of-life,absurd", "absurd-comedy,family,meta", "Absurd and hilarious stories based on the author's daily life and imagination."),
    ("My Giant Nerd Boyfriend", "romance,comedy,slice-of-life", "height-difference,gamer,cute", "A short girl and her very tall nerdy boyfriend's cute daily life together."),
    ("Adventures of God", "comedy,fantasy,religion", "god,comedy,satire", "God and his friends deal with running the universe in comedic ways."),
    ("Boyfriend of the Dead", "horror,comedy,romance", "zombies,survival,comedy", "A girl survives the zombie apocalypse with her zombie boyfriend who maintains his consciousness."),
    ("Your Throne", "fantasy,drama,body-swap", "female-rivalry,revenge,political-intrigue", "Two rival women swap bodies and must work together to survive in a dangerous political world."),
    ("Tomb Raider King", "action,fantasy,adventure", "tomb-raiding,artifacts,overpowered-mc", "A man returns to the past when tombs and relics started appearing, seeking legendary artifacts."),
    ("SSS-Class Suicide Hunter", "action,fantasy,tower", "tower-climbing,copy-ability,determined-mc", "A hunter with the ability to copy skills through death climbs the tower to the top."),
    ("Solo Max-Level Newbie", "action,fantasy,game", "game-knowledge,overpowered-mc,tutorial", "A man who mastered a game finds himself inside it with knowledge of everything."),
    ("The Max Level Hero Has Returned", "action,fantasy,isekai", "returned-hero,overpowered-mc,revenge", "A summoned hero returns to Earth after becoming max level and seeks revenge."),
    ("Dungeon Reset", "action,fantasy,survival", "dungeon,survival,crafting", "A man is left behind in a dungeon that resets, allowing him to exploit its mechanics."),
    ("The Tutorial Tower of the Advanced Player", "action,fantasy,tower", "tutorial,time-loop,overpowered-mc", "A player is trapped in the tutorial for 12 years, becoming incredibly powerful."),
    ("FFF-Class Trashero", "action,fantasy,isekai", "anti-hero,overpowered-mc,dark-comedy", "A hero forced to redo his journey becomes a villain to escape the world quickly."),
    ("Dungeon House", "action,fantasy,dungeon", "dungeon-home,survival,unique", "A man's home becomes a dungeon entrance, giving him unique opportunities."),
    ("Seoul Station Druid", "action,fantasy,apocalypse", "druid,returned-hero,modern-fantasy", "A man returns after 50 years in another world as a powerful druid."),
    ("The Tutorial Is Too Hard", "action,fantasy,dungeon", "tutorial,difficulty,survival", "A man chooses Hell difficulty for the tutorial and must survive impossible challenges."),
    ("The S-Classes That I Raised", "action,fantasy,regression", "tamer,family,regression", "A weak hunter returns to the past and raises S-class hunters and monsters."),
    ("I Am the Sorcerer King", "action,fantasy,modern", "awakening,magic,overpowered-mc", "A man awakens memories of his past life as a sorcerer king and gains immense power."),
    ("A Returner's Magic Should Be Special", "action,fantasy,school", "time-travel,magic-school,prevent-apocalypse", "A man returns to magic school to prevent the apocalypse he experienced."),
    ("The Live", "horror,thriller,supernatural", "streaming,death-game,survival", "A man finds a cursed livestream app that forces him to complete deadly missions."),
    ("Pigpen", "psychological,thriller,horror", "cult,mystery,manipulation", "A detective investigates a mysterious cult that manipulates people's minds."),
    ("Tales of the Unusual", "horror,anthology,supernatural", "anthology,mystery,urban-legends", "Anthology series featuring creepy and mysterious stories with twist endings."),
    ("#Killstagram", "horror,thriller,social-media", "influencer,horror,obsession", "A social media influencer encounters horrifying events while chasing views."),
]

def main():
    print("=" * 70)
    print("📚 ADDING 80+ MANHWA TO DATABASE")
    print("=" * 70)
    
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS manhwa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            genres TEXT NOT NULL,
            tropes TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    added = 0
    skipped = 0
    
    for title, genres, tropes, description in MANHWA_LIST:
        try:
            cursor.execute("""
                INSERT INTO manhwa (title, genres, tropes, description)
                VALUES (?, ?, ?, ?)
            """, (title, genres, tropes, description))
            added += 1
            print(f"✓ Added: {title}")
        except sqlite3.IntegrityError:
            skipped += 1
            print(f"⊘ Skipped: {title}")
    
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM manhwa")
    total = cursor.fetchone()[0]
    conn.close()
    
    print()
    print("=" * 70)
    print("✅ COMPLETE!")
    print(f"📊 Added: {added} new titles")
    print(f"⊘ Skipped: {skipped} duplicates")
    print(f"📚 Total: {total} manhwa")
    print("=" * 70)

if __name__ == "__main__":
    main()
