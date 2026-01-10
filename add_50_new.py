#!/usr/bin/env python3
import sqlite3

DB_PATH = "data/manhwa.db"

# 50 BRAND NEW manhwa NOT in your database
NEW_MANHWA = [
    ("Villain to Kill", "action,supernatural,revenge", "anti-hero,revenge,powers", "A villain possesses the body of a hero and seeks revenge while hiding his identity."),
    ("Trash of the Count's Family", "fantasy,isekai,comedy", "smart-mc,found-family,comedy", "A man transmigrates into a trashy character and uses his knowledge to survive."),
    ("The Greatest Estate Developer", "isekai,comedy,fantasy", "construction,comedy,smart-mc", "An engineering student transmigrates and uses modern knowledge to develop an estate."),
    ("Return of the Disaster-Class Hero", "action,fantasy,betrayal", "overpowered-mc,revenge,returned-hero", "A betrayed hero returns after 20 years to take revenge on former allies."),
    ("Study Group", "school,psychological,thriller", "survival,death-game,smart-mc", "Students must pass impossible tests or face death."),
    ("Leveling With the Gods", "action,fantasy,tower", "tower-climbing,regression,gods", "A man returns to climb the tower and reach the gods."),
    ("Player Who Returned 10,000 Years Later", "action,fantasy,overpowered", "overpowered-mc,returned-hero,demons", "After 10,000 years in hell, he returns to Earth incredibly powerful."),
    ("The Player That Can't Level Up", "action,fantasy,unique", "unique-power,dungeon,mystery", "A player who can't level up discovers a hidden power."),
    ("Limit Breaker", "action,fantasy,martial-arts", "weak-to-strong,determination,training", "A weak boy breaks his limits through extreme training."),
    ("Warrior High School", "action,school,dungeon", "school-life,dungeon,comedy", "A dungeon appears under a high school, changing everything."),
    
    ("Seoul Station's Necromancer", "action,fantasy,necromancer", "necromancer,overpowered-mc,modern-fantasy", "A necromancer returns to Earth after years in another world."),
    ("The Book Eating Magician", "fantasy,magic,academy", "magic,books,smart-mc", "A magician gains power by eating magical books."),
    ("Arcane Sniper", "action,game,sniper", "sniper,game-elements,smart-mc", "A skilled sniper dominates a VR game world."),
    ("Kill the Hero", "action,fantasy,betrayal", "revenge,anti-hero,regression", "Betrayed by his party leader, he returns to get revenge."),
    ("The Regressed Demon Lord is Kind", "isekai,fantasy,comedy", "demon-lord,regression,wholesome", "A demon lord returns to the past and decides to be kind."),
    ("Auto Hunting", "action,fantasy,game", "auto-battle,overpowered-mc,leveling", "A glitch gives him an auto-hunting ability that makes him unstoppable."),
    ("Reincarnation of the Suicidal Battle God", "action,fantasy,regression", "regression,overpowered-mc,gods", "The last human returns to the past to change humanity's fate."),
    ("The Great Mage Returns After 4000 Years", "fantasy,magic,reincarnation", "overpowered-mc,reincarnation,magic", "A legendary mage reincarnates after 4000 years."),
    ("Survival Story of a Sword King", "isekai,action,fantasy", "overpowered-mc,stuck-tutorial,comedy", "A man is stuck in the beginner zone for years and becomes overpowered."),
    ("Her Summon", "romance,fantasy,comedy", "summoning,cute,reverse-harem", "A girl accidentally summons multiple handsome demons."),
    
    ("Seasons of Blossom", "romance,school,drama", "school-life,youth,emotional", "Interconnected stories of high school students through the seasons."),
    ("The Makeup Remover", "romance,comedy,supernatural", "makeup,transformation,comedy", "A boy who can see through makeup meets various girls."),
    ("Swimming Lessons for a Mermaid", "romance,fantasy,mermaid", "mermaid,transformation,cute", "A mermaid learns to swim from a human swimming coach."),
    ("Elixir of the Sun", "romance,fantasy,historical", "alchemy,reincarnation,revenge", "An alchemist returns to the past to change her tragic fate."),
    ("Charlotte Has Five Disciples", "romance,fantasy,magic", "teacher,magic,reverse-harem", "A powerful mage raises five disciples who all fall for her."),
    ("Positively Yours", "romance,slice-of-life,pregnancy", "pregnancy,contract-relationship,healing", "A one-night stand leads to unexpected pregnancy and love."),
    ("Spirit Fingers", "slice-of-life,school,art", "art,friendship,growth", "A girl joins an art club and discovers herself."),
    ("Annarasumanara", "psychological,drama,magic", "magic,coming-of-age,mystery", "A mysterious magician helps a girl rediscover wonder."),
    ("The Girl Downstairs", "romance,slice-of-life,neighbors", "neighbors,slow-burn,wholesome", "A college student and his neighbor develop feelings."),
    ("Refund High School", "action,school,time-loop", "time-loop,survival,school", "Students must survive deadly challenges to escape a time loop."),
    
    ("Medical Return", "drama,medical,regression", "doctor,time-travel,medical", "A failed doctor returns to his youth to become a great surgeon."),
    ("Dr. Frost", "psychological,mystery,detective", "psychology,detective,cases", "A genius psychologist solves cases with his cold logic."),
    ("Life Completely Ruined", "drama,psychological,bullying", "bullying,revenge,dark", "A bullied student's life spirals after a tragic incident."),
    ("The Horizon", "horror,thriller,supernatural", "monsters,survival,apocalypse", "Humanity fights for survival against mysterious monsters."),
    ("Rotten", "horror,zombie,survival", "zombies,survival,dark", "Survivors navigate a world overrun by zombies."),
    ("Everything Was a Mistake", "romance,drama,misunderstanding", "contract-marriage,misunderstanding,healing", "A contract marriage based on a mistake leads to real love."),
    ("Marriage of Convenience", "romance,historical,contract", "contract-marriage,aristocracy,slow-burn", "A marriage of convenience becomes something more."),
    ("Men of the Harem", "romance,isekai,reverse-harem", "reverse-harem,isekai,comedy", "A woman becomes empress with multiple male consorts."),
    ("Shadow Queen", "romance,fantasy,revenge", "revenge,reincarnation,empress", "A betrayed queen returns to take revenge and protect herself."),
    ("The Villainess's Maker", "isekai,romance,fantasy", "creator,isekai,plot-twist", "The creator of a novel enters her own story as the villainess."),
    
    ("The World After the Fall", "action,fantasy,apocalypse", "overpowered-mc,survival,tower", "After the Tower falls, a man who rejected the system must survive in a broken world."),
    ("Teenage Mercenary", "action,school,mercenary", "mercenary,overpowered-mc,school-life", "A teenage mercenary returns to normal life but can't escape his past."),
    ("Lookism", "action,drama,school", "body-swap,bullying,two-bodies", "An overweight boy wakes up with a second handsome body and lives a double life."),
    ("Under the Oak Tree", "romance,fantasy,character-growth", "arranged-marriage,knight,stutter", "A shy princess with a stutter marries a legendary knight and learns to find her own strength."),
    ("The Villainess Is a Marionette", "isekai,romance,fantasy", "manipulation,female-lead,revenge", "A woman regresses and becomes a master manipulator to control her own destiny."),
    ("I'll Be the Matriarch in This Life", "isekai,fantasy,regression", "family-politics,merchant,smart-female-lead", "A woman returns to her childhood in a merchant family to prevent their downfall."),
    ("Roxana", "isekai,dark-fantasy,revenge", "villain-family,manipulation,dark", "A woman reincarnates into a family of villains and must survive using cunning."),
    ("The Villainess Turns the Hourglass", "isekai,romance,revenge", "time-travel,revenge,aristocracy", "A villainess uses an hourglass to travel back and outsmart her enemies."),
    ("Father, I Don't Want This Marriage", "isekai,comedy,romance", "father-daughter,misunderstanding,comedy", "A woman reincarnates and must prevent her engagement while dealing with her overprotective father."),
    ("Seduce the Villain's Father", "isekai,romance,comedy", "time-travel,prevent-tragedy,romance", "A woman goes back in time to prevent a tragedy by seducing the villain's father before he becomes evil."),
]

def main():
    print("=" * 70)
    print("📚 ADDING 50 BRAND NEW MANHWA (NO DUPLICATES)")
    print("=" * 70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    added = 0
    skipped = 0
    
    for title, genres, tropes, description in NEW_MANHWA:
        try:
            cursor.execute("""
                INSERT INTO manhwa (title, genres, tropes, description)
                VALUES (?, ?, ?, ?)
            """, (title, genres, tropes, description))
            added += 1
            print(f"✓ Added: {title}")
        except sqlite3.IntegrityError:
            skipped += 1
            print(f"⊘ Skipped (duplicate): {title}")
    
    conn.commit()
    
    # Add to trending_scores
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
    print("✅ COMPLETE!")
    print(f"📊 Added: {added} new titles")
    print(f"⊘ Skipped: {skipped} duplicates")
    print(f"📚 Total manhwa: {total}")
    print("=" * 70)

if __name__ == "__main__":
    main()
