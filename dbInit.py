import json
import os
import sqlite3
from sqlite3 import Error


def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_class_spellcasting_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS class_spellcasting_link (
            class_id TEXT,
            spellcasting_id TEXT
        )
    '''

    create_table(conn, statement)


def create_class_subclass_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS class_subclass_link (
            class_id TEXT,
            subclass_id TEXT
        )
    '''

    create_table(conn, statement)


def create_class_saving_throws_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS class_saving_throws (
            class_id TEXT,
            ability_scores_id TEXT
        )
    '''

    create_table(conn, statement)


def create_class_starting_equipment_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS class_starting_equipment_link (
            class_id TEXT,
            starting_equipment_id TEXT
        )
    '''

    create_table(conn, statement)


def create_class_proficiencies_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS class_proficiencies_link (
            class_id TEXT,
            proficiency_id TEXT
        )
    '''

    create_table(conn, statement)


def create_class_proficiency_choice_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS class_proficiency_choice_link (
            choose INTEGER,
            choice_group INTEGER,
            class_id TEXT,
            proficiency_id TEXT
        )
    '''

    create_table(conn, statement)


def create_level_class_specific_sneak_attack_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS level_class_specific_sneak_attack (
            level_id INTEGER,
            dice_count INTEGER,
            dice_value INTEGER
        )
    '''

    create_table(conn, statement)


def create_level_class_specific_martial_arts_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS level_class_specific_martial_arts (
            level_id INTEGER,
            dice_count INTEGER,
            dice_value INTEGER
        )
    '''

    create_table(conn, statement)


def create_level_class_specific_creating_spell_slots_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS level_class_specific_creating_spell_slots (
            level_id INTEGER,
            spell_slot_level_1_sorcery_point_cost INTEGER,
            spell_slot_level_2_sorcery_point_cost INTEGER,
            spell_slot_level_3_sorcery_point_cost INTEGER,
            spell_slot_level_4_sorcery_point_cost INTEGER,
            spell_slot_level_5_sorcery_point_cost INTEGER
        )
    '''

    create_table(conn, statement)


def create_level_spellcasting_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS level_spellcasting (
            class_id TEXT,
            level INT,
            level_id INTEGER,
            cantrips_known INTEGER,
            spell_slots_level_1 INTEGER,
            spell_slots_level_2 INTEGER,
            spell_slots_level_3 INTEGER,
            spell_slots_level_4 INTEGER,
            spell_slots_level_5 INTEGER,
            spell_slots_level_6 INTEGER,
            spell_slots_level_7 INTEGER,
            spell_slots_level_8 INTEGER,
            spell_slots_level_9 INTEGER,
            spells_known INTEGER
        )
    '''

    create_table(conn, statement)


def create_class_specifics_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS class_specifics (
            level INTEGER,
            class_id TEXT,
            level_id INTEGER,
            action_surges INTEGER,
            arcane_recovery_levels INTEGER,
            aura_range INTEGER,
            bardic_inspiration_die INTEGER,
            brutal_critical_dice INTEGER,
            channel_divinity_charges INTEGER,
            destroy_undead_cr INTEGER,
            extra_attacks INTEGER,
            favored_enemies INTEGER,
            favored_terrain INTEGER,
            indomitable_uses INTEGER,
            invocations_known INTEGER,
            ki_points INTEGER,
            magical_secrets_max_5 INTEGER,
            magical_secrets_max_7 INTEGER,
            magical_secrets_max_9 INTEGER,
            metamagic_known INTEGER,
            mystic_arcanum_level_6 INTEGER,
            mystic_arcanum_level_7 INTEGER,
            mystic_arcanum_level_8 INTEGER,
            mystic_arcanum_level_9 INTEGER,
            rage_count INTEGER,
            rage_damage_bonus INTEGER,
            song_of_rest_die INTEGER,
            sorcery_points INTEGER,
            unarmored_movement INTEGER,
            wild_shape_fly BOOLEAN,
            wild_shape_max_cr REAL,
            wild_shape_swim BOOLEAN
        )
    '''

    create_table(conn, statement)


def create_subclass_specifics_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS subclass_specifics (
            class_id TEXT,
            level INT,
            level_id INTEGER,
            additional_magical_secrets_max_lvl INTEGER
        )
    '''

    create_table(conn, statement)


def create_levels_feature_choices_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS levels_feature_choices_link(
            class_id TEXT,
            level INT,
            level_id INT,
            feature_id TEXT
        ) 
    '''

    create_table(conn, statement)


def create_levels_feature_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS levels_feature_link(
            class_id TEXT,
            level INT,
            level_id INT,
            feature_id TEXT
        ) 
    '''

    create_table(conn, statement)


def create_levels_table(conn):
    create_class_specifics_table(conn)
    create_levels_feature_choices_link_table(conn)
    create_levels_feature_link_table(conn)
    create_subclass_specifics_table(conn)
    create_level_spellcasting_table(conn)
    create_level_class_specific_creating_spell_slots_table(conn)
    create_level_class_specific_martial_arts_table(conn)
    create_level_class_specific_sneak_attack_table(conn)

    statement = '''
        CREATE TABLE IF NOT EXISTS levels (
            ability_score_bonuses INTEGER,
            class_id TEXT,
            id INTEGER,
            level INTEGER,
            prof_bonus INTEGER,
            spell_slots_level_1 INTEGER,
            spell_slots_level_2 INTEGER,
            spell_slots_level_3 INTEGER,
            spell_slots_level_4 INTEGER,
            spell_slots_level_5 INTEGER,
            subclass TEXT
        )
    '''

    create_table(conn, statement)

    with open('src/5e-SRD-Levels.json', 'r') as f:
        data = json.load(f)

    c = conn.cursor()

    statement = '''
        INSERT INTO levels (
            ability_score_bonuses,
            class_id,
            id,
            level,
            prof_bonus,
            spell_slots_level_1,
            spell_slots_level_2,
            spell_slots_level_3,
            spell_slots_level_4,
            spell_slots_level_5,
            subclass
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
    '''

    for level in data:
        record = (
            level["ability_score_bonuses"] if "ability_score_bonuses" in level.keys() else None,
            level["class"]["url"].split("/")[-1] if "class" in level.keys() else None,
            level["index"],
            level["level"],
            level["prof_bonus"] if "prof_bonus" in level.keys() else None,
            level["spell_slots_level_1"] if "spell_slots_level_1" in level.keys() else None,
            level["spell_slots_level_2"] if "spell_slots_level_2" in level.keys() else None,
            level["spell_slots_level_3"] if "spell_slots_level_3" in level.keys() else None,
            level["spell_slots_level_4"] if "spell_slots_level_4" in level.keys() else None,
            level["spell_slots_level_5"] if "spell_slots_level_5" in level.keys() else None,
            level["subclass"]["url"] if "url" in level["subclass"].keys() else None,
        )

        c.execute(statement, record)

        if "feature_choices" in level.keys():
            for feature in level["feature_choices"]:
                statement2 = 'INSERT INTO levels_feature_choices_link (class_id, level, level_id, feature_id) VALUES (?,?,?,?)'
                record2 = (level["class"]["url"].split('/')[-1], level["level"], level["index"], feature["url"].split("/")[-1])
                c.execute(statement2, record2)

        if "features" in level.keys():
            for feature in level["features"]:
                statement2 = 'INSERT INTO levels_feature_link (class_id, level, level_id, feature_id) VALUES (?,?,?,?)'
                record2 = (level["class"]["url"].split("/")[-1], level["level"], level["index"], feature["url"].split("/")[-1])
                c.execute(statement2, record2)

        if "class_specific" in level.keys():
            cs = level["class_specific"]
            statement3 = '''
                INSERT INTO class_specifics (
                    level,
                    class_id,
                    level_id,
                    action_surges,
                    arcane_recovery_levels,
                    aura_range,
                    bardic_inspiration_die,
                    brutal_critical_dice,
                    channel_divinity_charges,
                    destroy_undead_cr,
                    extra_attacks,
                    favored_enemies,
                    favored_terrain,
                    indomitable_uses,
                    invocations_known,
                    ki_points,
                    magical_secrets_max_5,
                    magical_secrets_max_7,
                    magical_secrets_max_9,
                    metamagic_known,
                    mystic_arcanum_level_6,
                    mystic_arcanum_level_7,
                    mystic_arcanum_level_8,
                    mystic_arcanum_level_9,
                    rage_count,
                    rage_damage_bonus,
                    song_of_rest_die,
                    sorcery_points,
                    unarmored_movement,
                    wild_shape_fly,
                    wild_shape_max_cr,
                    wild_shape_swim
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            '''

            record3 = (
                level["level"],
                level["class"]["url"].split("/")[-1],
                level["index"],
                cs["action_surges"] if "action_surges" in cs.keys() else None,
                cs["arcane_recovery_levels"] if "arcane_recovery_levels" in cs.keys() else None,
                cs["aura_range"] if "aura_range" in cs.keys() else None,
                cs["bardic_inspiration_die"] if "bardic_inspiration_die" in cs.keys() else None,
                cs["brutal_critical_dice"] if "brutal_critical_dice" in cs.keys() else None,
                cs["channel_divinity_charges"] if "channel_divinity_charges" in cs.keys() else None,
                cs["destroy_undead_cr"] if "destroy_undead_cr" in cs.keys() else None,
                cs["extra_attacks"] if "extra_attacks" in cs.keys() else None,
                cs["favored_enemies"] if "favored_enemies" in cs.keys() else None,
                cs["favored_terrain"] if "favored_terrain" in cs.keys() else None,
                cs["indomitable_uses"] if "indomitable_uses" in cs.keys() else None,
                cs["invocations_known"] if "invocations_known" in cs.keys() else None,
                cs["ki_points"] if "ki_points" in cs.keys() else None,
                cs["magical_secrets_max_5"] if "magical_secrets_max_5" in cs.keys() else None,
                cs["magical_secrets_max_7"] if "magical_secrets_max_7" in cs.keys() else None,
                cs["magical_secrets_max_9"] if "magical_secrets_max_9" in cs.keys() else None,
                cs["metamagic_known"] if "metamagic_known" in cs.keys() else None,
                cs["mystic_arcanum_level_6"] if "mystic_arcanum_level_6" in cs.keys() else None,
                cs["mystic_arcanum_level_7"] if "mystic_arcanum_level_7" in cs.keys() else None,
                cs["mystic_arcanum_level_8"] if "mystic_arcanum_level_8" in cs.keys() else None,
                cs["mystic_arcanum_level_9"] if "mystic_arcanum_level_9" in cs.keys() else None,
                cs["rage_count"] if "rage_count" in cs.keys() else None,
                cs["rage_damage_bonus"] if "rage_damage_bonus" in cs.keys() else None,
                cs["song_of_rest_die"] if "song_of_rest_die" in cs.keys() else None,
                cs["sorcery_points"] if "sorcery_points" in cs.keys() else None,
                cs["unarmored_movement"] if "unarmored_movement" in cs.keys() else None,
                cs["wild_shape_fly"] if "wild_shape_fly" in cs.keys() else None,
                cs["wild_shape_max_cr"] if "wild_shape_max_cr" in cs.keys() else None,
                cs["wild_shape_swim"] if "wild_shape_swim" in cs.keys() else None
            )

            c.execute(statement3, record3)

            if "creating_spell_slots" in cs.keys():
                statement6 = '''
                    INSERT INTO level_class_specific_creating_spell_slots (
                        level_id,
                        spell_slot_level_1_sorcery_point_cost,
                        spell_slot_level_2_sorcery_point_cost,
                        spell_slot_level_3_sorcery_point_cost,
                        spell_slot_level_4_sorcery_point_cost,
                        spell_slot_level_5_sorcery_point_cost
                    ) VALUES (?,?,?,?,?,?)
                '''

                record6 = (
                    level["index"],
                    2,
                    3,
                    5,
                    6,
                    7
                )

                c.execute(statement6, record6)

            if "martial_arts" in cs.keys():
                statement7 = '''
                    INSERT INTO level_class_specific_martial_arts (
                        level_id,
                        dice_count,
                        dice_value
                    ) VALUES (?,?,?)
                '''

                record7 = (
                    level["index"],
                    1,
                    cs["martial_arts"]["dice_value"]
                )

                c.execute(statement7, record7)

            if "sneak_attack" in cs.keys():
                statement8 = '''
                    INSERT INTO level_class_specific_sneak_attack (
                        level_id,
                        dice_count,
                        dice_value
                    ) VALUES (?,?,?)
                '''

                record8 = (
                    level["index"],
                    cs["sneak_attack"]["dice_count"],
                    cs["sneak_attack"]["dice_value"]
                )

                c.execute(statement8, record8)

        if "subclass_specific" in level.keys():
            scs = level["subclass_specific"]

            statement4 = '''
                INSERT INTO subclass_specifics (class_id, level, level_id, additional_magical_secrets_max_lvl) VALUES (?,?,?,?)
            '''

            record4 = (
                level["class"]["url"].split('/')[-1],
                level["level"],
                level["index"],
                scs[
                    "additional_magical_secrets_max_lvl"] if "additional_magical_secrets_max_lvl" in scs.keys() else None
            )

            c.execute(statement4, record4)

        if "spellcasting" in level.keys() and len(level["spellcasting"].keys()) > 0:
            sc = level["spellcasting"]
            statement5 = '''
                INSERT INTO level_spellcasting (
                    class_id,
                    level,
                    level_id,
                    cantrips_known,
                    spell_slots_level_1,
                    spell_slots_level_2,
                    spell_slots_level_3,
                    spell_slots_level_4,
                    spell_slots_level_5,
                    spell_slots_level_6,
                    spell_slots_level_7,
                    spell_slots_level_8,
                    spell_slots_level_9,
                    spells_known
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            '''

            record5 = (
                level["class"]["url"].split('/')[-1],
                level["level"],
                level["index"],
                sc["cantrips_known"] if "cantrips_known" in sc.keys() else None,
                sc["spell_slots_level_1"] if "spell_slots_level_1" in sc.keys() else None,
                sc["spell_slots_level_2"] if "spell_slots_level_2" in sc.keys() else None,
                sc["spell_slots_level_3"] if "spell_slots_level_3" in sc.keys() else None,
                sc["spell_slots_level_4"] if "spell_slots_level_4" in sc.keys() else None,
                sc["spell_slots_level_5"] if "spell_slots_level_5" in sc.keys() else None,
                sc["spell_slots_level_6"] if "spell_slots_level_6" in sc.keys() else None,
                sc["spell_slots_level_7"] if "spell_slots_level_7" in sc.keys() else None,
                sc["spell_slots_level_8"] if "spell_slots_level_8" in sc.keys() else None,
                sc["spell_slots_level_9"] if "spell_slots_level_9" in sc.keys() else None,
                sc["spells_known"] if "spells_known" in sc.keys() else None
            )

            c.execute(statement5, record5)


def create_classes_table(conn):
    create_levels_table(conn)
    create_class_proficiencies_link_table(conn)
    create_class_proficiency_choice_link_table(conn)
    create_class_saving_throws_table(conn)
    create_class_starting_equipment_link_table(conn)
    create_class_subclass_link_table(conn)
    create_class_spellcasting_link_table(conn)

    statement = '''
        CREATE TABLE IF NOT EXISTS classes (
            hit_die INTEGER,
            id TEXT,
            name TEXT
        )
    '''

    create_table(conn, statement)

    c = conn.cursor()

    with open('src/5e-SRD-Classes.json', 'r') as f:
        data = json.load(f)

    for dnd_class in data:
        statement = '''
            INSERT INTO classes (hit_die, id, name) VALUES (?,?,?)
        '''

        record = (dnd_class["hit_die"], dnd_class["index"], dnd_class["name"])

        c.execute(statement, record)

        for prof in dnd_class["proficiencies"]:
            statement2 = '''
                INSERT INTO class_proficiencies_link (class_id, proficiency_id) VALUES (?,?)
            '''

            record2 = (dnd_class["index"], prof["url"].split("/")[-1])

            c.execute(statement2, record2)

        choice_group = 1

        for prof_choice in dnd_class["proficiency_choices"]:
            statement3 = '''
                INSERT INTO class_proficiency_choice_link (
                    choose, 
                    choice_group, 
                    class_id, 
                    proficiency_id
                ) VALUES (?,?,?,?)
            '''

            for choose_from in prof_choice["from"]:
                record3 = (prof_choice["choose"], choice_group, dnd_class["index"], choose_from["url"].split("/")[-1])

                c.execute(statement3, record3)

            choice_group += 1

        del choice_group

        for saving_throw in dnd_class["saving_throws"]:
            statement4 = '''
                INSERT INTO class_saving_throws ( 
                    class_id, 
                    ability_scores_id
                ) VALUES (?,?)
            '''

            record4 = (dnd_class["index"], saving_throw["url"].split("/")[-1])

            c.execute(statement4, record4)

        statement5 = '''
            INSERT INTO class_starting_equipment_link (class_id, starting_equipment_id) VALUES (?,?)
        '''
        record5 = (dnd_class["index"], dnd_class["starting_equipment"]["url"].split("/")[-1])
        c.execute(statement5, record5)

        for subclass in dnd_class["subclasses"]:
            statement6 = '''
                        INSERT INTO class_subclass_link (class_id, subclass_id) VALUES (?,?)
                    '''
            record6 = (dnd_class["index"], subclass["url"].split("/")[-1])

            c.execute(statement6, record6)

        if len(dnd_class["spellcasting"].keys()) > 0:
            statement7 = '''
                        INSERT INTO class_spellcasting_link (class_id, spellcasting_id) VALUES (?,?)
                    '''
            record7 = (
                dnd_class["index"],
                dnd_class["spellcasting"]["url"].split("/")[-1]
            )

            c.execute(statement7, record7)


def create_skills_table(conn):

    statement = '''CREATE TABLE IF NOT EXISTS skills (
        id TEXT,
        name TEXT,
        description TEXT
    )'''

    create_table(conn, statement)

    statement = '''INSERT INTO skills(
            id,
            name,
            description
        ) VALUES (?,?,?)'''

    with open('src/5e-SRD-Skills.json', 'r') as f:
        data = json.load(f)

    for skill in data:
        record = (
            skill["index"],
            skill["name"],
            skill["desc"][0]
        )

        c = conn.cursor()
        c.execute(statement, record)


def create_skills_as_link_table(conn):

    statement = '''CREATE TABLE IF NOT EXISTS skills_ability_score_link (
        ability_score_id TEXT,
        skill_id TEXT
    )'''

    create_table(conn, statement)


def create_ability_scores_table(conn):
    statement = '''CREATE TABLE IF NOT EXISTS ability_scores (
        id TEXT,
        name TEXT,
        full_name TEXT,
        description TEXT,
        check_description TEXT
    )'''

    create_table(conn, statement)

    with open('src/5e-SRD-Ability-Scores.json', 'r') as f:
        data = json.load(f)

    statement = '''INSERT INTO ability_scores (
            id,
            name,
            full_name,
            description,
            check_description
        ) VALUES (?,?,?,?,?)'''

    for a_s in data:

        record = (
            a_s["index"],
            a_s["name"],
            a_s["full_name"],
            a_s["desc"][0],
            a_s["desc"][1]
        )

        c = conn.cursor()
        c.execute(statement, record)

        for skill in a_s["skills"]:
            c.execute('INSERT INTO skills_ability_score_link (ability_score_id, skill_id) VALUES (?,?)',(a_s["index"], skill["url"].split("/")[-1]))



def create_monster_sense_link_table(conn):

    statement = '''CREATE TABLE IF NOT EXISTS monster_senses_link (
        monster_id TEXT,
        sense TEXT
    )'''

    create_table(conn, statement)


def create_monster_reactions_link_table(conn):

    statement = '''CREATE TABLE IF NOT EXISTS monster_reactions_link (
        monster_id TEXT,
        reaction TEXT,
        description TEXT
    )'''

    create_table(conn, statement)


def create_monster_proficiencies_link_table(conn):

    statement = '''CREATE TABLE IF NOT EXISTS monster_proficiencies_link (
        monster_id TEXT,
        proficiency TEXT
    )'''

    create_table(conn, statement)


def create_condition_immunities_link_table(conn):

    sql_create_prop_equip_link_table = '''CREATE TABLE IF NOT EXISTS conditional_immunities (
        monster_id TEXT,
        condition TEXT
    )'''

    create_table(conn, sql_create_prop_equip_link_table)


def create_monsters_table(conn):

    create_skills_as_link_table(conn)
    create_skills_table(conn)
    create_ability_scores_table(conn)
    create_monster_reactions_link_table(conn)
    create_monster_sense_link_table(conn)
    create_condition_immunities_link_table(conn)
    create_monster_proficiencies_link_table(conn)

    sql_create_monster_table = """
        CREATE TABLE IF NOT EXISTS monsters (
            alignment TEXT,
            armor_class INTEGER,
            challenge_rating INTEGER,
            charisma INTEGER,
            constitution INTEGER,
            damage_immunities TEXT,
            damage_resistances TEXT,
            damage_vulnerabilities TEXT,
            dexterity INTEGER,
            hit_dice TEXT,
            hit_points INTEGER,
            id TEXT PRIMARY KEY NOT NULL,
            intelligence INTEGER,
            languages TEXT,
            name TEXT NOT NULL,
            other_speeds TEXT,
            size TEXT,
            speed_climb TEXT,
            speed_hover TEXT,
            speed_walk TEXT,
            speed_burrow TEXT,
            speed_fly TEXT,
            speed_swim TEXT,
            strength INTEGER,
            subtype TEXT,
            type TEXT,
            wisdom INTEGER
        );
    """
    create_table(conn, sql_create_monster_table)

    with open('src/5e-SRD-Monsters.json') as f:
        data = json.load(f)

    for monster in data:
        statement = '''
            INSERT INTO monsters(
                alignment,
                armor_class,
                challenge_rating,
                charisma,
                constitution,
                damage_immunities,
                damage_resistances,
                damage_vulnerabilities,
                dexterity,
                hit_dice,
                hit_points,
                id,
                intelligence,
                languages,
                name,
                other_speeds,
                size,
                speed_climb,
                speed_hover,
                speed_walk,
                speed_burrow,
                speed_fly,
                speed_swim,
                strength,
                subtype,
                type,
                wisdom
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

        record = (
            monster["alignment"] if "alignment" in monster.keys() else None,
            monster["armor_class"] if "armor_class" in monster.keys() else None,
            monster["challenge_rating"] if "challenge_rating" in monster.keys() else None,
            monster["charisma"] if "charisma" in monster.keys() else None,
            monster["constitution"] if "constitution" in monster.keys() else None,
            ", ".join(monster["damage_immunities"]) if "damage_immunities" in monster.keys() else None,
            ", ".join(monster["damage_resistances"]) if "damage_resistances" in monster.keys() else None,
            ", ".join(monster["damage_vulnerabilities"]) if "damage_vulnerabilities" in monster.keys() else None,
            monster["dexterity"] if "dexterity" in monster.keys() else None,
            monster["hit_dice"] if "hit_dice" in monster.keys() else None,
            monster["hit_points"] if "hit_points" in monster.keys() else None,
            monster["index"] if "index" in monster.keys() else None,
            monster["intelligence"] if "intelligence" in monster.keys() else None,
            monster["languages"] if "languages" in monster.keys() else None,
            monster["name"] if "name" in monster.keys() else None,
            "; ".join([f'{form["form"]}: walk - {form["speed"]["walk"]} climb - {form["speed"]["climb"] if "climb" in form["speed"].keys() else ""}' for form in monster["other_speeds"]]) if "other_speeds" in monster.keys() else None,
            monster["size"] if "size" in monster.keys() else None,
            monster["speed"]["climb"] if "climb" in monster["speed"].keys() else None,
            monster["speed"]["hover"] if "hover" in monster["speed"].keys() else None,
            monster["speed"]["walk"] if "walk" in monster["speed"].keys() else None,
            monster["speed"]["burrow"] if "burrow" in monster["speed"].keys() else None,
            monster["speed"]["fly"] if "fly" in monster["speed"].keys() else None,
            monster["speed"]["swim"] if "swim" in monster["speed"].keys() else None,
            monster["strength"] if "strength" in monster.keys() else None,
            monster["subtype"] if "subtype" in monster.keys() else None,
            monster["type"] if "type" in monster.keys() else None,
            monster["wisdom"] if "wisdom" in monster.keys() else None
        )

        c = conn.cursor()
        c.execute(statement, record)

        if "senses" in monster.keys():
            for sense in monster["senses"]:
                statement = '''INSERT INTO monster_senses_link(monster_id, sense) VALUES (?,?)'''
                record = (monster["index"], f'{sense} - {monster["senses"][sense]}')
                c.execute(statement, record)

        if "reactions" in monster.keys():
            for reaction in monster["reactions"]:
                statement = '''INSERT INTO monster_reactions_link(monster_id, reaction, description) VALUES (?,?,?)'''
                record = (monster["index"], reaction["name"], reaction["desc"])
                c.execute(statement, record)

        if len(monster["condition_immunities"]) > 0:
            for condition in monster["condition_immunities"]:
                statement = '''INSERT INTO conditional_immunities(monster_id, condition) VALUES (?,?)'''
                record = (monster["index"], condition["url"].split("/")[-1])
                c.execute(statement, record)

        if len(monster["proficiencies"]) > 0:
            for proficiency in monster["proficiencies"]:
                statement = '''INSERT INTO monster_proficiencies_link(monster_id, proficiency) VALUES (?,?)'''
                record = (monster["index"], proficiency["url"].split("/")[-1])
                c.execute(statement, record)


def create_prop_equip_link_table(conn):

    sql_create_prop_equip_link_table = '''CREATE TABLE IF NOT EXISTS property_equipment_link (
        equipment_id TEXT,
        property TEXT
    )'''

    create_table(conn, sql_create_prop_equip_link_table)


def damage_types_table(conn):

    sql_create_damage_types_table = '''CREATE TABLE IF NOT EXISTS damage_types (
        id TEXT,
        name TEXT,
        description TEXT
    )'''

    create_table(conn, sql_create_damage_types_table)

    with open('src/5e-SRD-Damage-Types.json') as f:
        data = json.load(f)

    for damage_type in data:
        statement = '''INSERT INTO damage_types (id, name, description) VALUES (?,?,?)'''
        record = (damage_type["index"], damage_type["name"], damage_type["desc"][0])
        c = conn.cursor()
        c.execute(statement, record)


def create_weapon_properties_table(conn):

    sql_create_damage_types_table = '''CREATE TABLE IF NOT EXISTS weapon_properties (
        id TEXT,
        name TEXT,
        description TEXT
    )'''

    create_table(conn, sql_create_damage_types_table)

    with open('src/5e-SRD-Weapon-Properties.json') as f:
        data = json.load(f)

    for weapon_property in data:
        statement = '''INSERT INTO weapon_properties (id, name, description) VALUES (?,?,?)'''
        record = (weapon_property["index"], weapon_property["name"], weapon_property["desc"][0])
        c = conn.cursor()
        c.execute(statement, record)


def create_equipment_contents_link_table(conn):

    sql_create_prop_equip_link_table = '''CREATE TABLE IF NOT EXISTS equipment_contents_link (
        equipment_id TEXT,
        content_id TEXT
    )'''

    create_table(conn, sql_create_prop_equip_link_table)

def create_equipment_table(conn):

    create_weapon_properties_table(conn)
    damage_types_table(conn)
    create_equipment_contents_link_table(conn)
    create_prop_equip_link_table(conn)
    create_equipment_categories_table(conn)

    sql_create_equipment_table = """ 
        CREATE TABLE IF NOT EXISTS equipment (
            armor_category TEXT,
            armor_class_base INTEGER,
            armor_class_dex_bonus BOOLEAN,
            armor_class_max_bonus INTEGER,
            capacity TEXT,
            category_range TEXT,
            cost TEXT,
            damage_dice_2h TEXT,
            damage_bonus_2h INTEGER,
            damage_type_2h TEXT,
            damage_dice TEXT,
            damage_bonus INTEGER,
            damage_type TEXT,
            description TEXT,
            equipment_category TEXT,
            equipment_category_id TEXT,
            gear_category TEXT,
            id TEXT PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            range_normal INTEGER,
            range_long INTEGER,
            special TEXT,
            speed TEXT,
            stealth_disadvantage BOOLEAN,
            str_minimum INTEGER,
            throw_range_normal INTEGER,
            throw_range_long INTEGER,
            tool_category TEXT,
            vehicle_category TEXT,
            weapon_category TEXT,
            weapon_range TEXT,
            weight INTEGER
        );
    """
    create_table(conn, sql_create_equipment_table)

    with open('src/5e-SRD-Equipment.json') as f:
        data = json.load(f)

    for equipment in data:
        e_record = (
            equipment["armor_category"] if "armor_category" in equipment.keys() else None,
            equipment["armor_class"]["base"] if "armor_class" in equipment.keys() else None,
            equipment["armor_class"]["dex_bonus"] if "armor_class" in equipment.keys() else None,
            equipment["armor_class"]["max_bonus"] if "armor_class" in equipment.keys() else None,
            equipment["capacity"] if "capacity" in equipment.keys() else None,
            equipment["category_range"] if "category_range" in equipment.keys() else None,
            f'{equipment["cost"]["quantity"]} {equipment["cost"]["unit"]}' if "cost" in equipment.keys() else None,
            equipment["2h_damage"]["damage_dice"] if "2h_damage" in equipment.keys() else None,
            equipment["2h_damage"]["damage_bonus"] if "2h_damage" in equipment.keys() else None,
            equipment["2h_damage"]["damage_type"]["name"] if "2h_damage" in equipment.keys() else None,
            equipment["damage"]["damage_dice"] if "damage" in equipment.keys() else None,
            equipment["damage"]["damage_bonus"] if "damage" in equipment.keys() else None,
            equipment["damage"]["damage_type"]["name"] if "damage" in equipment.keys() else None,
            equipment["desc"][0] if "desc" in equipment.keys() else None,
            equipment["equipment_category"] if "equipment_category" in equipment.keys() else None,
            equipment["equipment_category"].lower().replace(" ","-") if "equipment_category" in equipment.keys() else None,
            equipment["gear_category"] if "gear_category" in equipment.keys() else None,
            equipment["index"],
            equipment["name"],
            equipment["range"]["normal"] if "range" in equipment.keys() else None,
            equipment["range"]["long"] if "range" in equipment.keys() else None,
            equipment["special"][0] if "special" in equipment.keys() else None,
            f'{equipment["speed"]["quantity"]} {equipment["speed"]["unit"]}' if "speed" in equipment.keys() else None,
            equipment["stealth_disadvantage"] if "stealth_disadvantage" in equipment.keys() else None,
            equipment["str_minimum"] if "str_minimum" in equipment.keys() else None,
            equipment["throw_range"]["normal"] if "throw_range" in equipment.keys() else None,
            equipment["throw_range"]["long"] if "throw_range" in equipment.keys() else None,
            equipment["tool_category"] if "tool_category" in equipment.keys() else None,
            equipment["vehicle_category"] if "vehicle_category" in equipment.keys() else None,
            equipment["weapon_category"] if "weapon_category" in equipment.keys() else None,
            equipment["weapon_range"] if "weapon_range" in equipment.keys() else None,
            equipment["weight"] if "weight" in equipment.keys() else None
        )

        e_statement = '''
            INSERT INTO equipment(
                armor_category,
                armor_class_base,
                armor_class_dex_bonus,
                armor_class_max_bonus,
                capacity,
                category_range,
                cost,
                damage_dice_2h,
                damage_bonus_2h,
                damage_type_2h,
                damage_dice,
                damage_bonus,
                damage_type,
                description,
                equipment_category,
                equipment_category_id,
                gear_category,
                id,
                name,
                range_normal,
                range_long,
                special,
                speed,
                stealth_disadvantage,
                str_minimum,
                throw_range_normal,
                throw_range_long,
                tool_category,
                vehicle_category,
                weapon_category,
                weapon_range,
                weight
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

        c = conn.cursor()
        c.execute(e_statement, e_record)

        if "properties" in equipment.keys():
            for property in equipment["properties"]:
                statement = '''INSERT INTO property_equipment_link(equipment_id, property) VALUES (?,?)'''
                record = (equipment["index"], property["name"])
                c.execute(statement, record)

        if "contents" in equipment.keys():
            for content in equipment["contents"]:
                statement = '''INSERT INTO equipment_contents_link(equipment_id, content_id) VALUES (?,?)'''
                record = (equipment["index"], content["item_url"].split("/")[-1])
                c.execute(statement, record)


def create_feature_choice_link_table(conn):
    statement='''
        CREATE TABLE IF NOT EXISTS  feature_choice_link (
            feature_id TEXT,
            choose INTEGER,
            from_feature_id TEXT
        )
    '''
    create_table(conn, statement)


def create_spellcasting_info_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS spellcasting_info (
            spellcasting_id TEXT,
            name TEXT,
            description TEXT
        )
    '''

    create_table(conn, statement)


def create_spellcasting_ability_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS spellcasting_ability_link (
            spellcasting_id TEXT,
            ability_id TEXT
        )
    '''

    create_table(conn, statement)


def create_feature_class_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS feature_class_link (
            feature_id TEXT,
            class_id TEXT,
            level INTEGER
        )
    '''

    create_table(conn, statement)


def create_feature_subclass_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS feature_subclass_link (
            feature_id TEXT,
            subclass_id TEXT
        )
    '''

    create_table(conn, statement)


def create_spellcasting_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS spellcasting (
            id TEXT,
            class_id TEXT,
            level INTEGER
        )
    '''

    create_table(conn, statement)

    statement = '''
        INSERT INTO spellcasting (id, class_id, level) VALUES (?,?,?)
    '''

    with open('src/5e-SRD-Spellcasting.json', 'r') as f:
        data = json.load(f)

    for spell in data:
        record = (
            spell["index"],
            spell["class"]["url"].split('/')[-1],
            spell["level"]
        )

        c = conn.cursor()
        c.execute(statement, record)

        for info_object in spell["info"]:
            statement2 = '''
                INSERT INTO spellcasting_info (spellcasting_id, name, description) VALUES (?,?,?)
            '''

            record2 = (
                spell["index"],
                info_object["name"],
                "\n".join(info_object["desc"])
            )
            c.execute(statement2, record2)

        statement3 = '''
            INSERT INTO spellcasting_ability_link (spellcasting_id, ability_id) VALUES (?,?)
        '''
        record3 = (
            spell["index"],
            spell["spellcasting_ability"]["url"].split('/')[-1]
        )

        c.execute(statement3, record3)


def create_features_table(conn):

    create_feature_choice_link_table(conn)
    create_spellcasting_info_table(conn)
    create_spellcasting_ability_link_table(conn)
    create_feature_class_link_table(conn)
    create_feature_subclass_link_table(conn)
    create_spellcasting_table(conn)

    statement = '''
        CREATE TABLE IF NOT EXISTS features (
            description TEXT,
            feature_group TEXT,
            id TEXT,
            level INTEGER,
            name TEXT,
            prerequisites TEXT
        )
    '''

    create_table(conn, statement)

    statement = '''INSERT INTO features (
                description,
                feature_group,
                id,
                level,
                name,
                prerequisites
            ) VALUES (?,?,?,?,?,?)'''

    c = conn.cursor()

    with open('src/5e-SRD-Features.json', 'r') as f:
        data = json.load(f)

    for feature in data:
        record = (
            "\n".join(feature["desc"]),
            feature["group"] if "group" in feature.keys() else None,
            feature["index"],
            feature["level"] if "level" in feature.keys() else None,
            feature["name"],
            ", ".join([f'{p["type"]}: {p[p["type"].lower()]}' if p["type"] == "level" else f'{p["type"]}: {p[p["type"].lower()].split("/")[-1]}' for p in feature["prerequisites"]]) if "prerequisites" in feature.keys() and len(feature["prerequisites"]) > 0 else None
        )

        c.execute(statement, record)

        if "class" in feature.keys():
            statement2 = '''
                INSERT INTO feature_class_link (feature_id, class_id, level) VALUES (?,?,?)
            '''

            record2 = (
                feature["index"],
                feature["class"]["url"].split("/")[-1],
                feature["level"] if "level" in feature.keys() else None
            )

            c.execute(statement2, record2)

        if "subclass" in feature.keys() and len(feature["subclass"].keys()) > 0:
            statement3 = '''
                INSERT INTO feature_subclass_link (feature_id, subclass_id) VALUES (?,?)
            '''

            record3 = (
                feature["index"],
                feature["subclass"]["url"].split("/")[-1]
            )

            c.execute(statement3, record3)

        if "choice" in feature.keys():
            statement4 = '''
                INSERT INTO feature_choice_link (feature_id, choose, from_feature_id) VALUES (?,?,?)
            '''

            for choice in feature["choice"]["from"]:
                record4 = (
                    feature["index"],
                    feature["choice"]["choose"],
                    choice["url"].split("/")[-1]
                )

                c.execute(statement4, record4)


def create_subclass_feature_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS subclass_feature_link (
            subclass_id TEXT,
            feature_id TEXT
        )
    '''

    create_table(conn, statement)


def create_subclass_spells_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS subclass_spells_link (
            subclass_id TEXT,
            prerequisites TEXT,
            spell_id TEXT
        )
    '''

    create_table(conn, statement)


def create_subclasses_table(conn):
    create_subclass_feature_link_table(conn)
    create_subclass_spells_link_table(conn)

    statement = '''
        CREATE TABLE IF NOT EXISTS subclasses (
            id TEXT,
            class_id TEXT,
            name TEXT,
            subclass_flavor TEXT,
            description TEXT
        )
    '''

    create_table(conn, statement)

    c = conn.cursor()

    with open('src/5e-SRD-Subclasses.json', 'r') as f:
        data = json.load(f)

    for sc in data:

        statement = '''
            INSERT INTO subclasses (id, class_id, name, subclass_flavor, description) VALUES (?,?,?,?,?)
        '''

        record = (
            sc["index"],
            sc["class"]["url"].split('/')[-1],
            sc["name"],
            sc["subclass_flavor"],
            sc["desc"][0]
        )

        c.execute(statement, record)

        for feature in sc["features"]:
            statement2 = '''
                INSERT INTO subclass_feature_link (subclass_id, feature_id) VALUES (?,?)
            '''

            record2 = (
                sc["index"],
                feature["url"].split('/')[-1]
            )

            c.execute(statement2, record2)

        if "spells" in sc.keys():
            for spell in sc["spells"]:
                statement3 = '''
                    INSERT INTO subclass_spells_link (subclass_id, spell_id, prerequisites) VALUES (?,?,?)
                '''

                record3 = (
                    sc["index"],
                    spell["spell"]["url"].split('/')[-1],
                    '; '.join([
                                  f'{prereq["url"].split("/")[-2]}: {prereq["name"]}' if "name" in prereq.keys() else f'{prereq["url"].split("/")[-2]}: {prereq["url"].split("/")[-1]}'
                                  for prereq in spell["prerequisites"]])
                )

                c.execute(statement3, record3)


def create_starting_equipment_choices_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS starting_equipment_choices (
            class_id TEXT,
            choice_id INT,
            choose INT,
            choice_group INT,
            equipment_id TEXT
        )
    '''

    create_table(conn, statement)


def create_starting_equipment_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS starting_equipment_link (
            class_id TEXT,
            equipment_id TEXT
        )
    '''

    create_table(conn, statement)


def create_starting_equipment_table(conn):

    create_starting_equipment_choices_table(conn)
    create_starting_equipment_link_table(conn)

    statement = '''
        CREATE TABLE IF NOT EXISTS starting_equipment (
            choices_to_make INT,
            class_id TEXT,
            id INT
        )
    '''

    create_table(conn, statement)

    c = conn.cursor()

    with open('src/5e-SRD-StartingEquipment.json', 'r') as f:
        data = json.load(f)

    statement = '''
        INSERT INTO starting_equipment (id, class_id, choices_to_make) VALUES (?,?,?)
    '''

    for se in data:
        record = (
            se["index"],
            se["class"]["url"].split('/')[-1],
            se["choices_to_make"]
        )

        c.execute(statement, record)

        choice_indexes = ["choice_1", "choice_2", "choice_3", "choice_4", "choice_5"]

        for choice_index in choice_indexes:
            if choice_index in se.keys():
                choice_number = choice_index[-1]
                choice_group = 1
                for choice in se[choice_index]:
                    for equipment in choice["from"]:
                        equipment_item = equipment["item"]["url"].split('/')[-1]
                        statement2 = '''
                            INSERT INTO starting_equipment_choices (class_id, choice_id, choose, choice_group, equipment_id) VALUES (?,?,?,?,?)
                        '''
                        record2 = (
                            se["class"]["url"].split('/')[-1],
                            choice_number,
                            choice["choose"],
                            choice_group,
                            equipment_item
                        )

                        c.execute(statement2, record2)

                    choice_group += 1

        for equipment in se["starting_equipment"]:
            statement3 = '''
                INSERT INTO starting_equipment_link (class_id, equipment_id) VALUES (?,?)
            '''
            record3 = (
                se["class"]["url"].split('/')[-1],
                equipment["item"]["url"].split('/')[-1]
            )
            c.execute(statement3, record3)


def create_race_ability_bonuses_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS race_ability_bonuses (
            race_id TEXT,
            ability_score_id TEXT,
            bonus INTEGER
        )
    '''

    create_table(conn, statement)


def create_race_language_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS race_language_link (
            race_id TEXT,
            language_id TEXT
        )
    '''

    create_table(conn, statement)


def create_race_language_options_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS race_language_options (
            race_id TEXT,
            language_id TEXT,
            choose INTEGER
        )
    '''

    create_table(conn, statement)


def create_race_trait_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS race_trait_link (
            race_id TEXT,
            trait_id TEXT
        )
    '''

    create_table(conn, statement)


def create_race_trait_options_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS race_trait_options (
            race_id TEXT,
            trait_id TEXT,
            choose INTEGER
        )
    '''

    create_table(conn, statement)


def create_race_starting_proficiencies_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS race_starting_proficiencies (
            race_id TEXT,
            proficiency_id TEXT
        )
    '''

    create_table(conn, statement)


def create_race_starting_proficiency_options_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS race_starting_proficiency_options (
            race_id TEXT,
            proficiency_id TEXT,
            choose INTEGER
        )
    '''

    create_table(conn, statement)


def create_race_ability_bonus_options_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS race_ability_bonus_options (
            race_id TEXT,
            ability_score_id TEXT,
            choose INTEGER
        )
    '''

    create_table(conn, statement)


def create_race_subrace_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS race_subrace_link (
            race_id TEXT,
            subrace_id TEXT
        )
    '''

    create_table(conn, statement)


def create_races_table(conn):
    create_race_ability_bonuses_table(conn)
    create_race_ability_bonus_options_table(conn)
    create_race_starting_proficiencies_table(conn)
    create_race_starting_proficiency_options_table(conn)
    create_race_language_link_table(conn)
    create_race_language_options_table(conn)
    create_race_trait_link_table(conn)
    create_race_trait_options_table(conn)
    create_race_subrace_link_table(conn)

    statement = '''
        CREATE TABLE IF NOT EXISTS races (
            age TEXT,
            alignment TEXT,
            id TEXT,
            language_description TEXT,
            name TEXT,
            size TEXT,
            size_description TEXT,
            speed INTEGER
        )
    '''

    create_table(conn, statement)

    c = conn.cursor()

    with open('src/5e-SRD-Races.json', 'r') as f:
        data = json.load(f)

    for race in data:
        statement = '''
            INSERT INTO races (
                age,
                alignment,
                id,
                language_description,
                name,
                size,
                size_description,
                speed
            ) VALUES (?,?,?,?,?,?,?,?)
        '''

        record = (
            race["age"],
            race["alignment"],
            race["index"],
            race["language_desc"],
            race["name"],
            race["size"],
            race["size_description"],
            race["speed"]
        )

        c.execute(statement, record)

        for ab in race["ability_bonuses"]:
            statement2 = '''
                INSERT INTO race_ability_bonuses (race_id, ability_score_id, bonus) VALUES (?,?,?)
            '''

            record2 = (race["index"], ab["url"].split('/')[-1], ab["bonus"])

            c.execute(statement2, record2)

        if len(race["ability_bonus_options"].keys()) > 0:
            for abo in race["ability_bonus_options"]["from"]:
                statement3 = '''
                    INSERT INTO race_ability_bonus_options (race_id, ability_score_id, choose) VALUES (?,?,?)
                '''

                record3 = (race["index"], abo["url"].split('/')[-1], race["ability_bonus_options"]["choose"])

                c.execute(statement3, record3)

        for sp in race["starting_proficiencies"]:
            statement4 = '''
                INSERT INTO race_starting_proficiencies (race_id, proficiency_id) VALUES (?,?)
            '''
            record4 = (race["index"], sp["url"].split("/")[-1])

            c.execute(statement4, record4)

        if len(race["starting_proficiency_options"].keys()) > 0:
            statement5 = '''
                INSERT INTO race_starting_proficiency_options (race_id, proficiency_id, choose) VALUES (?,?,?)
            '''

            for spo in race["starting_proficiency_options"]["from"]:
                record5 = (race["index"], spo["url"].split('/')[-1], race["starting_proficiency_options"]["choose"])

                c.execute(statement5, record5)

        for lang in race["languages"]:
            statement6 = '''
                INSERT INTO race_language_link (race_id, language_id) VALUES (?,?)
            '''

            record6 = (race["index"], lang["url"].split('/')[-1])

            c.execute(statement6, record6)

        if len(race["language_options"].keys()) > 0:
            statement7 = '''
                INSERT INTO race_language_options (race_id, language_id, choose) VALUES (?,?,?)
            '''

            for lo in race["language_options"]["from"]:
                record7 = (race["index"], lo["url"].split('/')[-1], race["language_options"]["choose"])

                c.execute(statement7, record7)

        for trait in race["traits"]:
            statement8 = '''
                INSERT INTO race_trait_link (race_id, trait_id) VALUES (?,?)
            '''
            record8 = (race["index"], trait["url"].split('/')[-1])

            c.execute(statement8, record8)

        if "trait_options" in race.keys() and len(race["trait_options"].keys()) > 0:
            statement9 = '''
                INSERT INTO race_trait_options (race_id, trait_id, choose) VALUES (?,?,?)
            '''

            for to in race["trait_options"]["from"]:
                record9 = (race["index"], to["url"].split("/")[-1], race["trait_options"]["choose"])

                c.execute(statement9, record9)

        for sr in race["subraces"]:
            statement10 = '''
                INSERT INTO race_subrace_link (race_id, subrace_id) VALUES (?,?)
            '''

            record10 = (race["index"], sr["url"].split("/")[-1])

            c.execute(statement10, record10)


def create_language_typical_speakers_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS language_typical_speakers (
            language_id TEXT,
            speaker TEXT
        )
    '''

    create_table(conn, statement)


def create_languages_table(conn):
    create_language_typical_speakers_table(conn)

    statement = '''
        CREATE TABLE IF NOT EXISTS languages (
            id TEXT,
            name TEXT,
            type TEXT,
            script TEXT
        )
    '''

    create_table(conn, statement)

    c = conn.cursor()

    with open('src/5e-SRD-Languages.json', 'r') as f:
        data = json.load(f)

    for language in data:
        statement = '''
            INSERT INTO languages (id, name, type, script) VALUES (?,?,?,?)
        '''

        record = (language["index"], language["name"], language["type"],language["script"])

        c.execute(statement, record)

        for speaker in language["typical_speakers"]:
            statement2 = '''
                INSERT INTO language_typical_speakers (language_id, speaker) VALUES (?,?)
            '''

            record2 = (language["index"], speaker)

            c.execute(statement2, record2)


def create_proficiency_race_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS proficiency_race_link (
            proficiency_id TEXT,
            race_id TEXT
        )
    '''

    create_table(conn, statement)


def create_proficiencies_table(conn):
    create_proficiency_race_link_table(conn)

    statement = '''
        CREATE TABLE IF NOT EXISTS proficiencies (
            id TEXT,
            name TEXT,
            type TEXT
        )
    '''

    create_table(conn, statement)

    c = conn.cursor()

    with open('src/5e-SRD-Proficiencies.json', 'r') as f:
        data = json.load(f)

    for prof in data:
        statement = '''
            INSERT INTO proficiencies (id, name, type) VALUES (?,?,?)
        '''

        record = (prof["index"], prof["name"], prof["type"])

        c.execute(statement, record)

        for race in prof["races"]:
            statement2 = '''
                INSERT INTO proficiency_race_link (proficiency_id, race_id) VALUES (?,?)
            '''

            record2 = (prof["index"], race["url"].split("/")[-1])

            c.execute(statement2, record2)


def create_subrace_ability_bonuses_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS subrace_ability_bonuses (
            subrace_id TEXT,
            ability_score_id TEXT,
            bonus INTEGER
        )
    '''

    create_table(conn, statement)


def create_subrace_starting_proficiencies_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS subrace_starting_proficiencies (
            subrace_id TEXT,
            proficiency_id TEXT
        )
    '''

    create_table(conn, statement)


def create_subrace_language_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS subrace_language_link (
            subrace_id TEXT,
            language_id TEXT
        )
    '''

    create_table(conn, statement)


def create_subrace_language_options_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS subrace_language_options (
            subrace_id TEXT,
            language_id TEXT,
            choose INTEGER
        )
    '''

    create_table(conn, statement)


def create_subrace_traits_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS subrace_traits (
            subrace_id TEXT,
            trait_id TEXT
        )
    '''

    create_table(conn, statement)


def create_subrace_trait_options_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS subrace_trait_options (
            subrace_id TEXT,
            trait_id TEXT,
            choose INTEGER
        )
    '''

    create_table(conn, statement)


def create_subraces_table(conn):
    create_subrace_ability_bonuses_table(conn)
    create_subrace_starting_proficiencies_table(conn)
    create_subrace_language_link_table(conn)
    create_subrace_language_options_table(conn)
    create_subrace_traits_table(conn)
    create_subrace_trait_options_table(conn)

    statement = '''
        CREATE TABLE IF NOT EXISTS subraces (
            description TEXT,
            id TEXT,
            name TEXT,
            race TEXT
        )
    '''

    create_table(conn, statement)

    c = conn.cursor()

    with open('src/5e-SRD-Subraces.json', 'r') as f:
        data = json.load(f)

    for subrace in data:
        statement = '''
            INSERT INTO subraces (id, name, race, description) VALUES (?,?,?,?)
        '''

        record = (subrace["index"], subrace["name"], subrace["race"]["url"].split("/")[-1], subrace["desc"])

        c.execute(statement, record)

        for ab in subrace["ability_bonuses"]:
            statement2 = '''
                INSERT INTO subrace_ability_bonuses (subrace_id, ability_score_id, bonus) VALUES (?,?,?)
            '''
            record2 = (subrace["index"], ab["url"].split("/")[-1], ab["bonus"])

            c.execute(statement2, record2)

        for sp in subrace["starting_proficiencies"]:
            statement3 = '''
                INSERT INTO subrace_starting_proficiencies (subrace_id, proficiency_id) VALUES (?,?)
            '''

            record3 = (subrace["index"], sp["url"].split("/")[-1])

            c.execute(statement3, record3)

        for language in subrace["languages"]:
            statement4 = '''
                INSERT INTO subrace_language_link (subrace_id, language_id) VALUES (?,?)
            '''

            record4 = (subrace["index"], language["url"].split("/")[-1])

            c.execute(statement4, record4)

        if "language_options" in subrace.keys() and len(subrace["language_options"].keys()) > 0:
            statement5 = '''
                INSERT INTO subrace_language_options (subrace_id, language_id, choose) VALUES (?,?,?)
            '''

            for lo in subrace["language_options"]["from"]:

                record5 = (subrace["index"], lo["url"].split("/")[-1], subrace["language_options"]["choose"])

                c.execute(statement5, record5)

        for rt in subrace["racial_traits"]:
            statement6 = '''
                INSERT INTO subrace_traits (subrace_id, trait_id) VALUES (?,?)
            '''
            record6 = (subrace["index"], rt["url"].split("/")[-1])

            c.execute(statement6, record6)

        if len(subrace["racial_trait_options"].keys()) > 0:
            statement7 = '''
                INSERT INTO subrace_trait_options (subrace_id, trait_id, choose) VALUES (?,?,?)
            '''

            for to in subrace["racial_trait_options"]["from"]:
                record7 = (subrace["index"], to["url"].split("/")[-1], subrace["racial_trait_options"]["choose"])

                c.execute(statement7, record7)


def create_traits_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS traits (
            description TEXT,
            id TEXT,
            name TEXT
        )
    '''

    create_table(conn, statement)

    c = conn.cursor()

    with open('src/5e-SRD-Traits.json', 'r') as f:
        data = json.load(f)

    for trait in data:
        statement = '''
            INSERT INTO traits (id, name, description) VALUES (?,?,?)
        '''

        record = (
            trait["index"],
            trait["name"],
            "\n".join(trait["desc"])
        )

        c.execute(statement, record)


def create_spell_class_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS spell_class_link (
            spell_id TEXT,
            class_id TEXT
        )
    '''

    create_table(conn, statement)


def create_spell_subclass_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS spell_subclass_link (
            spell_id TEXT,
            subclass_id TEXT
        )
    '''

    create_table(conn, statement)


def create_spell_magic_school_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS spell_magic_school_link (
            spell_id TEXT,
            school_id TEXT
        )
    '''

    create_table(conn, statement)


def create_spell_components_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS spell_components (
            spell_id TEXT,
            component TEXT
        )
    '''

    create_table(conn, statement)


def create_magic_schools_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS magic_schools (
            id TEXT,
            name TEXT,
            description TEXT
        )
    '''

    create_table(conn, statement)

    c = conn.cursor()

    with open('src/5e-SRD-Magic-Schools.json', 'r') as f:
        data = json.load(f)

    for school in data:
        statement = '''
            INSERT INTO magic_schools (id, name, description) VALUES (?,?,?)
        '''
        record = (school["index"], school["name"], school["desc"])

        c.execute(statement, record)


def create_spells_table(conn):
    create_spell_class_link_table(conn)
    create_spell_components_table(conn)
    create_spell_magic_school_link_table(conn)
    create_spell_subclass_link_table(conn)
    create_magic_schools_table(conn)

    statement = '''
        CREATE TABLE IF NOT EXISTS spells (
            casting_time TEXT,
            concentration BOOLEAN,
            description TEXT,
            duration TEXT,
            higher_level TEXT,
            id TEXT,
            level INTEGER,
            material TEXT,
            name TEXT,
            page TEXT,
            range TEXT,
            ritual BOOLEAN
        )
    '''

    create_table(conn, statement)

    c = conn.cursor()

    with open('src/5e-SRD-Spells.json', 'r') as f:
        data = json.load(f)

    for spell in data:
        statement = '''
            INSERT INTO spells (
                casting_time,
                concentration,
                description,
                duration,
                higher_level,
                id,
                level,
                material,
                name,
                page,
                range,
                ritual
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        '''

        record = (
            spell['casting_time'],
            spell['concentration'],
            "\n".join(spell['desc']),
            spell['duration'],
            "\n".join(spell['higher_level']) if "higher_level" in spell.keys() else None,
            spell['index'],
            spell['level'],
            spell['material'] if "material" in spell.keys() else None,
            spell['name'],
            spell['page'],
            spell['range'],
            spell['ritual']
        )

        c.execute(statement, record)

        for cls in spell["classes"]:
            statement2 = '''
                INSERT INTO spell_class_link (spell_id, class_id) VALUES (?,?)
            '''
            record2 = (spell["index"], cls["url"].split('/')[-1])

            c.execute(statement2, record2)

        for subclass in spell["subclasses"]:
            statement3 = '''
                INSERT INTO spell_subclass_link (spell_id, subclass_id) VALUES (?,?)
            '''
            record3 = (spell["index"], subclass["url"].split('/')[-1])

            c.execute(statement3, record3)

        for component in spell["components"]:
            statement4 = '''
                INSERT INTO spell_components (spell_id, component) VALUES (?,?)
            '''
            record4 = (spell["index"], component)

            c.execute(statement4, record4)

        statement5 = '''
            INSERT INTO spell_magic_school_link (spell_id, school_id) VALUES (?,?)
        '''

        record5 = (spell["index"], spell["school"]["url"].split('/')[-1])

        c.execute(statement5, record5)


def create_conditions_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS conditions (
            id TEXT,
            name TEXT,
            description TEXT
        )
    '''

    create_table(conn, statement)

    c = conn.cursor()

    with open('src/5e-SRD-Conditions.json', 'r') as f:
        data = json.load(f)

    for condition in data:
        statement = '''
            INSERT INTO conditions (id, name, description) VALUES (?,?,?)
        '''
        record = (condition["index"], condition["name"], "\n".join(condition["desc"]))

        c.execute(statement, record)


def create_equipment_category_link_table(conn):
    statement = '''
        CREATE TABLE IF NOT EXISTS equipment_category_link (
            equipment_id TEXT,
            category_id TEXT
        )
    '''

    create_table(conn, statement)


def create_equipment_categories_table(conn):
    create_equipment_category_link_table(conn)

    statement = '''
        CREATE TABLE IF NOT EXISTS equipment_categories (
            id TEXT,
            name TEXT
        )
    '''

    create_table(conn, statement)

    with open('src/5e-SRD-Equipment-Categories.json', 'r') as f:
        data = json.load(f)

        c = conn.cursor()

    for ec in data:
        statement = '''
            INSERT INTO equipment_categories (id, name) VALUES (?,?)
        '''

        record = (ec["index"], ec["name"])

        c.execute(statement, record)

        for item in ec["equipment"]:
            statement2 = '''
                INSERT INTO equipment_category_link (category_id, equipment_id) VALUES (?,?)
            '''
            record2 = (ec["index"], item["url"].split('/')[-1])
            c.execute(statement2, record2)


def main():
    database = 'dnd5e.db'

    if os.path.exists(database):
        os.remove(database)


    db_conn = create_connection(database)

    create_features_table(db_conn)
    create_monsters_table(db_conn)
    create_equipment_table(db_conn)
    create_classes_table(db_conn)
    create_subclasses_table(db_conn)
    create_starting_equipment_table(db_conn)
    create_races_table(db_conn)
    create_languages_table(db_conn)
    create_proficiencies_table(db_conn)
    create_subraces_table(db_conn)
    create_traits_table(db_conn)
    create_spells_table(db_conn)
    create_conditions_table(db_conn)

    db_conn.commit()
    db_conn.close()

if __name__ == '__main__':
    main()