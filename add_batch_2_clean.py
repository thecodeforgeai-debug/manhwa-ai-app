#!/usr/bin/env python3
import sqlite3

DB_PATH = "data/manhwa.db"

# Batch 2: 50 brand new manhwa (duplicates removed, replacements added)
BATCH_2 = [
    ("The Dark Magician Transmigrates After 66666 Years", "action,fantasy,reincarnation", "overpowered-mc,magic,reincarnation", "A dark magician awakens after 66666 years in a changed world."),
    ("Return of the SSS-Class Ranker", "action,fantasy,regression", "regression,overpowered-mc,game-elements", "The strongest ranker returns to the past to change everything."),
    ("The Constellation That Returned From Hell", "action,fantasy,constellation", "overpowered-mc,gods,revenge", "A constellation escapes hell and seeks revenge."),
    ("Doom Breaker", "action,fantasy,time-loop", "time-loop,demon-king,sacrifice", "A warrior repeats his death to defeat the demon king."),
    ("Return of the 8th Class Magician", "fantasy,magic,regression", "regression,magic,overpowered-mc", "The strongest magician returns to his youth."),
    ("Slave B", "action,fantasy,slavery", "slavery,revenge,dark", "A slave fights for freedom in a brutal world."),
    ("The Ember Knight", "action,fantasy,knight", "knight,weak-to-strong,determination", "A weak knight discovers hidden power within."),
    ("Memoir of the King of War", "action,fantasy,war", "war,strategy,overpowered-mc", "A legendary warrior's memories and battles."),
    ("Youngest Son of the Renowned Magic Clan", "fantasy,magic,family", "reincarnation,magic,family-politics", "Reborn as the youngest son of a powerful magic family."),
    ("Bug Player", "action,game,glitch", "glitch,game-elements,overpowered-mc", "A player exploits bugs to become unbeatable."),
    
    ("The Return of the Superhero", "action,superhero,modern", "superhero,returned-hero,powers", "A retired superhero returns to save the world."),
    ("Bowblade Spirit", "action,martial-arts,archery", "archery,spirit,weak-to-strong", "An archer bonds with a spirit to gain power."),
    ("Lightning Degree", "action,martial-arts,lightning", "lightning,martial-arts,revenge", "A martial artist wielding lightning seeks revenge."),
    ("Mercenary's War", "action,military,mercenary", "mercenary,war,strategy", "A mercenary navigates brutal conflicts."),
    ("Descent of the Demon Master", "action,martial-arts,reincarnation", "reincarnation,martial-arts,overpowered-mc", "A demon master reincarnates in modern times."),
    ("The Academy's Undercover Professor", "fantasy,academy,mystery", "professor,undercover,magic", "An undercover professor hides his true identity."),
    ("The Heavenly Demon Can't Live a Normal Life", "action,martial-arts,regression", "regression,martial-arts,overpowered-mc", "A heavenly demon tries to live normally but can't."),
    ("Past Life Regressor", "action,fantasy,regression", "regression,second-chance,overpowered-mc", "A regressor uses past knowledge to change fate."),
    ("I Became the Tyrant of a Defense Game", "action,strategy,game", "strategy,tower-defense,smart-mc", "Transmigrated into a tower defense game as the tyrant."),
    ("Academy's Genius Swordsman", "action,academy,sword", "sword,academy,genius", "A genius swordsman dominates the academy."),
    
    ("Martial Artist Lee Gwak", "action,martial-arts,underdog", "weak-to-strong,martial-arts,determination", "An overlooked martial artist rises to greatness."),
    ("The Great Warrior Wall", "action,fantasy,war", "war,wall,survival", "Humanity's last defense against monsters."),
    ("Ultimate Outcast", "action,school,powers", "outcast,powers,revenge", "An outcast gains powers and fights back."),
    ("Reformation of the Deadbeat Noble", "fantasy,isekai,redemption", "redemption,weak-to-strong,noble", "A lazy noble reforms and becomes powerful."),
    ("The Lord's Coins Aren't Decreasing", "fantasy,isekai,economics", "economics,territory-management,smart-mc", "A lord uses infinite money to develop his territory."),
    ("Return of the Shattered Constellation", "action,fantasy,constellation", "constellation,overpowered-mc,revenge", "A broken constellation returns for revenge."),
    ("The Max-Level Player's 100th Regression", "action,fantasy,regression", "regression,overpowered-mc,max-level", "After 100 regressions, he's finally ready."),
    ("Damn Reincarnation", "action,fantasy,reincarnation", "reincarnation,revenge,overpowered-mc", "A warrior reincarnates for revenge."),
    ("I Became a Renowned Family's Sword Prodigy", "action,fantasy,sword", "sword,prodigy,family", "Reborn as a sword prodigy in a famous family."),
    ("The Knight King Who Returned with a God", "action,fantasy,knight", "knight,returned-hero,gods", "A knight king returns with divine power."),
    
    ("Murim RPG Simulation", "action,martial-arts,game", "game-elements,martial-arts,simulation", "A martial arts world becomes an RPG."),
    ("Worthless Regression", "action,fantasy,regression", "regression,weak-mc,growth", "A seemingly worthless regression turns powerful."),
    ("Reaper of the Drifting Moon", "action,martial-arts,assassin", "assassin,martial-arts,dark", "A deadly assassin navigates the martial arts world."),
    ("The Heavenly Demon Instructor", "action,martial-arts,teacher", "teacher,demon,martial-arts", "A heavenly demon becomes an instructor."),
    ("I Became the Academy's Genius Swordmaster", "action,academy,sword", "sword,genius,academy", "Transmigrated as the genius swordmaster."),
    ("The Lone Necromancer", "action,fantasy,necromancer", "necromancer,overpowered-mc,dark", "A necromancer fights alone against the world."),
    ("Immortal Swordsman in the Reverse World", "action,fantasy,reverse-world", "immortal,sword,reverse-gender", "An immortal swordsman in a world where genders are reversed."),
    ("Return of the Elemental Lord", "action,fantasy,elements", "elemental-magic,overpowered-mc,revenge", "An elemental lord returns for revenge."),
    ("The Return of the Disaster-Class Villain", "action,fantasy,villain", "villain-protagonist,overpowered-mc,revenge", "A villain returns more powerful than ever."),
    ("Absolute Sword Sense", "action,martial-arts,sword", "sword,unique-power,martial-arts", "A swordsman with absolute sword sense."),
    
    ("Chronicles of the Demon Faction", "action,martial-arts,demons", "demon-faction,martial-arts,dark", "Chronicles from the demon faction's perspective."),
    ("The World's Best Assassin", "action,assassin,isekai", "assassin,isekai,overpowered-mc", "The world's best assassin is reincarnated."),
    ("Wandering Warrior of Wudang", "action,martial-arts,wanderer", "wanderer,martial-arts,adventure", "A Wudang warrior wanders the martial world."),
    ("I Became a Munchkin", "action,game,comedy", "game-elements,munchkin,comedy", "Becoming the ultimate min-maxer in a game world."),
    ("The Undefeatable Swordsman", "action,martial-arts,sword", "sword,revenge,martial-arts", "An undefeatable swordsman seeks justice."),
    ("Infinite Mage", "fantasy,magic,overpowered", "magic,overpowered-mc,infinite-power", "A mage with infinite potential."),
    ("The First Hunter", "action,fantasy,hunter", "first-hunter,overpowered-mc,monsters", "The very first hunter in a monster-filled world."),
    ("My Civil Servant Life Reborn in the Strange World", "isekai,comedy,slice-of-life", "civil-servant,isekai,comedy", "A civil servant is reborn in a fantasy world."),
    ("Skeleton Soldier Couldn't Protect the Dungeon", "action,fantasy,skeleton", "skeleton,time-loop,determination", "A skeleton soldier loops through time to protect his dungeon."),
    ("Overgeared", "action,game,crafting", "blacksmith,game-elements,overpowered-mc", "A blacksmith becomes the strongest player through crafting."),
]

def main():
    print("=" * 70)
    print("📚 BATCH 2: ADDING 50 MORE MANHWA (CLEAN - NO DUPLICATES)")
    print("=" * 70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    added = 0
    skipped = 0
    
    for title, genres, tropes, description in BATCH_2:
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
    
    cursor.execute("""
        INSERT OR IGNORE INTO trending_scores (title, recommendation_count)
        SELECT title, 0 FROM manhwa WHERE title NOT IN (SELECT title FROM trending_scores)
    """)
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM manhwa")
    total = cursor.fetchone()[0]
    
    conn.close()
    
    print()
    print("=" * 70)
    print("✅ BATCH 2 COMPLETE!")
    print(f"📊 Added: {added} new titles")
    print(f"⊘ Skipped: {skipped} duplicates")
    print(f"📚 Total: {total} manhwa")
    print(f"🎯 Progress: {total}/1000 ({total/10:.1f}%)")
    print("=" * 70)

if __name__ == "__main__":
    main()
