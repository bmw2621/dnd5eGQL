const graphql = require('graphql');
const sqlite3 = require('sqlite3').verbose()

// Establish Connectino to SQLite Database

const db = new sqlite3.Database('./dnd5e.db', sqlite3.OPEN_READONLY, (err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Connected to the dnd5e database.');
  });


// Abstract simple list query

const runQueryList = (statement, params = {}) => {
  return new Promise((resolve, reject) => {
    db.all(statement, params,(err, rows) => {  
      if(err){
          reject([]);
      }
      resolve(rows);
    });
  });
}

const runQueryElement = (statement, params = {}) => {
  return new Promise((resolve, reject) => {
    db.all(statement, params,(err, rows) => {  
      if(err){
          reject([]);
      }
      resolve(rows[0]);
    });
  });
}

const {
  GraphQLObjectType,
  GraphQLInt,
  GraphQLID,
  GraphQLString,
  GraphQLSchema,
  GraphQLList,
  GraphQLBoolean,
  GraphQLFloat
} = graphql;

const AbilityScoreType = new GraphQLObjectType({
  name: 'AbilityScore',
  fields: () => ({
    id: {type: GraphQLString},
    name: {type: GraphQLString},
    full_name: {type: GraphQLString},
    description: {type: GraphQLString},
    check_description: {type: GraphQLString},
    skills: {
      type: GraphQLList(SkillType),
      resolve(parent, args){
        return runQueryList("SELECT s.* FROM skills s JOIN skills_ability_score_link sasl ON sasl.skill_id = s.id JOIN ability_scores a ON a.id = sasl.ability_score_id WHERE a.id = $id",{$id: parent.id})
      }
    }
  })
})

const CharacterClassType = new GraphQLObjectType({
  name: 'CharacterClass',
  fields: () => ({
    id: {type: GraphQLString},
    name: {type: GraphQLString},
    hit_die: {type: GraphQLInt},
    proficiency_choices: {
      type: GraphQLList(ProficiencyChoiceGroupType),
      resolve(parent,args){
        return runQueryList('SELECT choose, choice_group, class_id FROM class_proficiency_choice_link WHERE class_id = $id GROUP BY choice_group', {$id: parent.id})
      }
    },
    proficiencies: {
      type: GraphQLList(GraphQLString),
      resolve(parent, args){
        return new Promise((resolve, reject) => {
          return db.all('SELECT proficiency_id FROM class_proficiencies_link WHERE class_id = $id', {$id: parent.id},(err, rows) => {  
            if(err){
                reject([]);
            }
            resolve(rows.map(row => row.proficiency_id));
          });
        });
      }
    },
    saving_throws: {
      type: GraphQLList(AbilityScoreType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM ability_scores WHERE id IN (SELECT ability_scores_id FROM class_saving_throws WHERE class_id = $id)', {$id: parent.id})
      }
    },
    starting_equipment: {
      type: GraphQLList(StartingEquipmentType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM starting_equipment WHERE class_id = $id', {$id: parent.id})
      }
    },
    class_levels: {
      type: GraphQLList(LevelType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM levels WHERE class_id = $id', {$id: parent.id})
      }
    },
    subclasses: {
      type: SubclassType,
      resolve(parent, args){
        return runQueryElement('SELECT * from subclasses WHERE class_id = $id', {$id: parent.id})
      }
    },
    spellcasting: {
      type: SpellcastingType,
      resolve(parent, args){
        return runQueryElement('SELECT * FROM spellcasting WHERE class_id = $id', {$id: parent.id})
      }
    },
  })
})

const ClassSpecificType = new GraphQLObjectType({
  name: 'ClassSpecific',
  fields: () => ({
    level: {type: GraphQLInt},
    class_id: {type: GraphQLString},
    level_id: {type: GraphQLInt},
    action_surges: {type: GraphQLInt},
    arcane_recovery_levels: {type: GraphQLInt},
    aura_range: {type: GraphQLInt},
    bardic_inspiration_die: {type: GraphQLInt},
    brutal_critical_dice: {type: GraphQLInt},
    channel_divinity_charges: {type: GraphQLInt},
    creating_spell_slots: {
      type: CreateSpellSlotClassSpecificType,
      resolve(parent, args){
        return runQueryElement("SELECT * FROM level_class_specific_creating_spell_slots WHERE level_id = $id", {$id: parent.level_id})
      }
    },
    destroy_undead_cr: {type: GraphQLInt},
    extra_attacks: {type: GraphQLInt},
    favored_enemies: {type: GraphQLInt},
    favored_terrain: {type: GraphQLInt},
    indomitable_uses: {type: GraphQLInt},
    invocations_known: {type: GraphQLInt},
    ki_points: {type: GraphQLInt},
    magical_secrets_max_5: {type: GraphQLInt},
    magical_secrets_max_7: {type: GraphQLInt},
    magical_secrets_max_9: {type: GraphQLInt},
    martial_arts: {
      type: MartialArtsClassSpecificType,
      resolve(parent, args){
        return runQueryElement("SELECT * FROM level_class_specific_martial_arts WHERE level_id = $id", {$id: parent.level_id})
      }
    },
    metamagic_known: {type: GraphQLInt},
    mystic_arcanum_level_6: {type: GraphQLInt},
    mystic_arcanum_level_7: {type: GraphQLInt},
    mystic_arcanum_level_8: {type: GraphQLInt},
    mystic_arcanum_level_9: {type: GraphQLInt},
    rage_count: {type: GraphQLInt},
    rage_damage_bonus: {type: GraphQLInt},
    sneak_attack: {
      type: SneakAttackClassSpecificType,
      resolve(parent, args){
        return runQueryElement("SELECT * FROM level_class_specific_sneak_attack WHERE level_id = $id", {$id: parent.level_id})
      }
    },
    song_of_rest_die: {type: GraphQLInt},
    sorcery_points: {type: GraphQLInt},
    unarmored_movement: {type: GraphQLInt},
    wild_shape_fly: {type: GraphQLBoolean},
    wild_shape_max_cr: {type: GraphQLFloat},
    wild_shape_swim: {type: GraphQLBoolean},
  })
})

const CreateSpellSlotClassSpecificType = new GraphQLObjectType({
  name: 'CreateSpellSlot',
  fields: () => ({
    level_id: {type: GraphQLInt},
    spell_slot_level_1_sorcery_point_cost: {type: GraphQLInt},
    spell_slot_level_2_sorcery_point_cost: {type: GraphQLInt},
    spell_slot_level_3_sorcery_point_cost: {type: GraphQLInt},
    spell_slot_level_4_sorcery_point_cost: {type: GraphQLInt},
    spell_slot_level_5_sorcery_point_cost: {type: GraphQLInt},
  })
})

const DamageTypeType = new GraphQLObjectType({
  name: 'DamageType',
  fields: () => ({
    id: {type: GraphQLString},
    name: {type: GraphQLString},
    description: {type: GraphQLString}
  })
})

const EquipmentType = new GraphQLObjectType({
  name: 'Equipment',
  fields: () => ({
    armor_category: {type: GraphQLString},
    armor_class_base: {type: GraphQLInt},
    armor_class_dex_bonus: {type: GraphQLBoolean},
    armor_class_max_bonus: {type: GraphQLInt},
    capacity: {type: GraphQLString},
    category_range: {type: GraphQLString},
    cost: {type: GraphQLString},
    contents: {
      type: GraphQLList(EquipmentType),
      resolve(parent, args){
        return runQueryList("SELECT * FROM equipment WHERE id IN (SELECT content_id FROM equipment_contents_link WHERE equipment_id = $id)",{$id: parent.id})
      }
    },
    damage_dice_2h: {type: GraphQLString},
    damage_bonus_2h: {type: GraphQLInt},
    damage_type_2h: {type: GraphQLString},
    damage_dice: {type: GraphQLString},
    damage_bonus: {type: GraphQLInt},
    damage_type: {
      type: DamageTypeType,
      resolve(parent,args){
        return runQueryElement("SELECT * FROM damage_types WHERE id=(SELECT LOWER(damage_type) FROM equipment WHERE id=$id)", {$id: parent.id})
      }
    },
    description: {type: GraphQLString},
    equipment_category: {type: GraphQLString},
    gear_category: {type: GraphQLString},
    id: {type: GraphQLString},
    name: {type: GraphQLString},
    properties: {
      type: GraphQLList(WeaponPropertyType),
      resolve(parent,args){
        return runQueryList("SELECT * FROM weapon_properties WHERE id IN (SELECT LOWER(property) FROM property_equipment_link WHERE equipment_id = $id)",{$id: parent.id})
      }
    },
    range_normal: {type: GraphQLInt},
    range_long: {type: GraphQLInt},
    special: {type: GraphQLString},
    speed: {type: GraphQLString},
    stealth_disadvantage: {type: GraphQLBoolean},
    str_minimum: {type: GraphQLInt},
    throw_range_normal: {type: GraphQLInt},
    throw_range_long: {type: GraphQLInt},
    tool_category: {type: GraphQLString},
    vehicle_category: {type: GraphQLString},
    weapon_category: {type: GraphQLString},
    weapon_range: {type: GraphQLString},
    weight: {type: GraphQLFloat},
  })
})

const FeatureType = new GraphQLObjectType({
  name: 'Feature',
  fields: () => ({
    choice_num: {
        type: GraphQLInt,
        resolve(parent, args){
          return new Promise((resolve, reject) => {
            db.all('SELECT choose FROM feature_choice_link WHERE feature_id = $id LIMIT 1', {$id: parent.id},(err, rows) => {  
              if(err){
                  reject([]);
              }
              resolve(rows.length > 0 ? rows[0].choose : 0);
            });
          });
        }
      },
    choice_from: {
      type: GraphQLList(FeatureType),
      resolve(parent, args) {
        //return runQueryList('SELECT * FROM features WHERE id IN (SELECT from_feature_id FROM feature_choice_link WHERE feature_id = $id)', {$id: parent.id})
        return new Promise((resolve, reject) => {
            db.all('SELECT * FROM features WHERE id IN (SELECT from_feature_id FROM feature_choice_link WHERE feature_id = $id)', {$id: parent.id},(err, rows) => {  
              if(err){
                  reject([]);
              }
              resolve(rows.length > 0 ? rows : null);
            });
          });
      }
    },
    class: {
      //TODO:Update when ClassType is complete
      type: GraphQLList(GraphQLString),
      resolve(parent, args){
        //TODO:Update when ClassType is complete
        return new Promise((resolve, reject) => {
            db.all('SELECT class_id FROM feature_class_link WHERE feature_id = $id AND level = $level', {$id: parent.id, $level: parent.level},(err, rows) => {  
              if(err){
                  reject([]);
              }
              resolve(rows.length > 0 ? rows.map(a => a.class_id) : null);
            });
          });
      }
    },
    description: {type: GraphQLString},
    feature_group: {type: GraphQLString},
    id: {type: GraphQLString},
    level: {type: GraphQLInt},
    name: {type: GraphQLString},
    prerequisites: {type: GraphQLString},
    subclass: {
      type: GraphQLString,
      resolve(parent, args){
        // return runQueryElement('SELECT subclass_id FROM feature_subclass_link WHERE feature_id = $id', {$id: parent.id})
        return new Promise((resolve, reject) => {
            db.all('SELECT subclass_id FROM feature_subclass_link WHERE feature_id = $id', {$id: parent.id},(err, rows) => {  
              if(err){
                  reject([]);
              }
              resolve(rows.length > 0 ? rows[0].subclass_id : null);
            });
          });
      }
    }
  })
})

const LevelType = new GraphQLObjectType({
  name: 'Level',
  fields: () => ({
    ability_score_bonuses: {type: GraphQLInt},
    class_id: {type: GraphQLString},
    class_specific: {
      type: GraphQLList(ClassSpecificType),
      resolve(parent,args){
        return runQueryList('SELECT * FROM class_specifics WHERE class_id = $id AND level = $level', {$id: parent.class_id, $level: parent.level})
      }
    },
    feature_choices: {
      type: GraphQLList(FeatureType),
      resolve(parent, args){
        return runQueryList('SELECT * from features WHERE id IN (SELECT feature_id FROM levels_feature_choices_link WHERE class_id = $id AND level = $level)',{$id: parent.class_id, $level: parent.level})
      }
    },
    features: {
      type: GraphQLList(FeatureType),
      resolve(parent, args){
        return runQueryList('SELECT * from features WHERE id IN (SELECT feature_id FROM levels_feature_link WHERE class_id = $id AND level = $level)',{$id: parent.class_id, $level: parent.level})
      }
    },
    id: {type: GraphQLInt},
    level: {type: GraphQLInt},
    prof_bonus: {type: GraphQLInt},
    spell_slots_level_1: {type: GraphQLInt},
    spell_slots_level_2: {type: GraphQLInt},
    spell_slots_level_3: {type: GraphQLInt},
    spell_slots_level_4: {type: GraphQLInt},
    spell_slots_level_5: {type: GraphQLInt},
    spellcasting: {
      type: GraphQLList(LevelSpellcastingType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM level_spellcasting WHERE class_id = $id AND level = $level', {$id: parent.class_id, $level: parent.level})
      }
    },
    subclass: {type: GraphQLString},
    subclass_specific: {
      type: SubclassSpecificType,
      resolve(parent, args){
        return runQueryElement('SELECT * from subclass_specifics WHERE class_id = $id AND level = $level', {$id: parent.class_id, $level: parent.level})
      }
    },
  })
})

const LevelSpellcastingType = new GraphQLObjectType({
  name: 'LevelSpellcasting',
  fields: () => ({
    class_id: {type: GraphQLInt},
    level: {type: GraphQLInt},
    level_id: {type: GraphQLInt},
    cantrips_known: {type: GraphQLInt},
    spell_slots_level_1: {type: GraphQLInt},
    spell_slots_level_2: {type: GraphQLInt},
    spell_slots_level_3: {type: GraphQLInt},
    spell_slots_level_4: {type: GraphQLInt},
    spell_slots_level_5: {type: GraphQLInt},
    spell_slots_level_6: {type: GraphQLInt},
    spell_slots_level_7: {type: GraphQLInt},
    spell_slots_level_8: {type: GraphQLInt},
    spell_slots_level_9: {type: GraphQLInt},
    spells_known: {type: GraphQLInt}
  })
})

const MartialArtsClassSpecificType = new GraphQLObjectType({
  name: 'MartialArts',
  fields: () => ({
    level_id: {type: GraphQLInt},
    dice_count: {type: GraphQLInt},
    dice_value: {type: GraphQLInt},
  })
})

const MonsterType = new GraphQLObjectType({
  name: 'Monster',
  fields: () => ({
    alignment: {type:GraphQLString},
    armor_class: {type:GraphQLInt},
    challenge_rating: {type:GraphQLInt},
    charisma: {type:GraphQLInt},
    constitution: {type:GraphQLInt},
    damage_immunities: {type:GraphQLString},
    damage_resistances: {type:GraphQLString},
    damage_vulnerabilities: {type:GraphQLString},
    dexterity: {type:GraphQLInt},
    hit_dice: {type:GraphQLString},
    hit_points: {type:GraphQLInt},
    id: {type:GraphQLString},
    intelligence: {type:GraphQLInt},
    languages: {type:GraphQLString},
    name: {type:GraphQLString},
    other_speeds: {type:GraphQLString},
    reactions: {
      type: GraphQLList(ReactionType),
      resolve(parent,args){
        return runQueryList("SELECT * FROM monster_reactions_link WHERE monster_id = $id;",{$id: parent.id})
      }
    },
    size: {type:GraphQLString},
    speed_climb: {type:GraphQLString},
    speed_hover: {type:GraphQLString},
    speed_walk: {type:GraphQLString},
    speed_burrow: {type:GraphQLString},
    speed_fly: {type:GraphQLString},
    speed_swim: {type:GraphQLString},
    strength: {type:GraphQLInt},
    subtype: {type:GraphQLString},
    type: {type:GraphQLString},
    wisdom: {type:GraphQLInt},
  })
})

const ProficiencyChoiceGroupType = new GraphQLObjectType({
  name: 'ProficiencyChoiceGroup',
  fields: () => ({
    choose: {type: GraphQLInt},
    choice_group: {type: GraphQLInt},
    class_id: {type: GraphQLString},
    // TODO: Update when ProficiencyType is created
    proficiency_id: {
      type: GraphQLList(GraphQLString),
      resolve(parent, args){
        return new Promise((resolve, reject) => {
          return db.all('SELECT proficiency_id FROM class_proficiency_choice_link WHERE class_id = $id AND choice_group = $choiceGroup', {$id: parent.class_id, $choiceGroup: parent.choice_group},(err, rows) => {  
            if(err){
                reject([]);
            }
            resolve(rows.map(row => row.proficiency_id));
          });
        });
      }
    }
  })
})

const RaceType = new GraphQLObjectType({
  name: 'Race',
  fields: () => ({
    age: {type: GraphQLString},
    alignment: {type: GraphQLString},
    id: {type: GraphQLString},
    language_description: {type: GraphQLString},
    name: {type: GraphQLString},
    size: {type: GraphQLString},
    size_description: {type: GraphQLString},
    speed: {type: GraphQLInt},
    ability_bonus: {
      type: GraphQLList(RaceAbilityBonusType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM race_ability_bonuses WHERE race_id = $id', {$id: parent.id})
      }
    },
    ability_bonus_options: {
      type: GraphQLList(RaceAbilityBonusOptionType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM race_ability_bonus_options WHERE race_id = $id GROUP BY race_id', {$id: parent.id})
      }
    },
    // TODO: Update when Language Type is created
    languages: {
      type: GraphQLList(GraphQLString),
      resolve(parent, args){
        return new Promise((resolve, reject) => {
          db.all('SELECT language_id FROM race_language_link WHERE race_id = $id', {$id: parent.id},(err, rows) => {  
            if(err){
                reject([]);
            }
            resolve(rows.map(row => row.language_id));
          });
        });
      }
    },
    language_options: {
      type: GraphQLList(RaceLanguageOptionType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM race_language_options WHERE race_id = $id GROUP BY race_id', {$id: parent.id})
      }
    },
    starting_proficiencies: {
      // TODO: Update when Proficiency Type is created
      type: GraphQLList(GraphQLString),
      resolve(parent, args){
        return new Promise((resolve, reject) => {
          db.all('SELECT proficiency_id FROM race_starting_proficiencies WHERE race_id = $id', {$id: parent.id},(err, rows) => {  
              if(err){
                  reject([]);
              }
              resolve(rows.map(row => row.proficiency_id));
            });
          });
      }
    },
    starting_proficiency_options: {
      type: GraphQLList(RaceStartingProficiencyOptionType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM race_starting_proficiency_options WHERE race_id = $id GROUP BY race_id', {$id: parent.id})
      }
    },
    traits: {
       // TODO: Update when Proficiency Type is created
      type: GraphQLList(GraphQLString),
      resolve(parent, args){
        return new Promise((resolve, reject) => {
          db.all('SELECT trait_id FROM race_trait_link WHERE race_id = $id', {$id: parent.id},(err, rows) => {  
              if(err){
                  reject([]);
              }
              resolve(rows.map(row => row.trait_id));
            });
          });
      }
    },
    trait_options: {
      type: GraphQLList(RaceTraitOptionType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM race_trait_options WHERE race_id = $id GROUP BY race_id', {$id: parent.id})
      }
    },
    subraces: {
      type: GraphQLList(GraphQLString),
      // TODO: Update when Subrace Type created
      resolve(parent, args){
        return new Promise((resolve, reject) => {
          db.all('SELECT subrace_id FROM race_subrace_link WHERE race_id = $id', {$id: parent.id},(err, rows) => {  
              if(err){
                  reject([]);
              }
              resolve(rows.map(row => row.subrace_id));
            });
          });
      }
    },
  })
})

const RaceAbilityBonusType = new GraphQLObjectType({
  name: 'RaceAbilityBonus',
  fields: () => ({
    race_id: {type: GraphQLString},
    ability_score_id: {type: GraphQLString},
    ability_score: {
      type: AbilityScoreType,
      resolve(parent, args){
        return runQueryElement('SELECT * FROM ability_scores WHERE id = $id', {$id: parent.ability_score_id})
      }
    },
    bonus: {type: GraphQLInt}
  })
})

const RaceAbilityBonusOptionType = new GraphQLObjectType({
  name: 'RaceAbilityBonusOption',
  fields: () => ({
    race_id: {type: GraphQLString},
    ability_score_id: {type: GraphQLString},
    choose: {type: GraphQLInt},
    ability_score: {
      type: GraphQLList(AbilityScoreType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM ability_scores WHERE id IN (SELECT ability_score_id FROM race_ability_bonus_options WHERE race_id = $id)', {$id: parent.race_id})
      }
    },
    bonus: {type: GraphQLInt}
  })
})

const RaceLanguageOptionType = new GraphQLObjectType({
  name: 'RaceLanguageOption',
  fields: () => ({
    race_id: {type: GraphQLString},
    choose: {type: GraphQLInt},
    // TODO: Update when Language Type is created
    language: {
      type: GraphQLList(GraphQLString),
      resolve(parent, args){
        return new Promise((resolve, reject) => {
          db.all('SELECT language_id FROM race_language_options WHERE race_id = $id', {$id: parent.race_id},(err, rows) => {  
              if(err){
                  reject([]);
              }
              resolve(rows.map(row => row.language_id));
            });
          });
      }
    },
  })
})

const RaceStartingProficiencyOptionType = new GraphQLObjectType({
  name: 'RaceStartingProficiencyOption',
  fields: () => ({
    race_id: {type: GraphQLString},
    choose: {type: GraphQLInt},
    // TODO: Update when Proficiency Type is created
    proficiencies: {
      type: GraphQLList(GraphQLString),
      resolve(parent, args){
        return new Promise((resolve, reject) => {
          db.all('SELECT proficiency_id FROM race_starting_proficiency_options WHERE race_id = $id', {$id: parent.race_id},(err, rows) => {  
              if(err){
                  reject([]);
              }
              resolve(rows.map(row => row.proficiency_id));
            });
          });
      }
    },
  })
})

const RaceTraitOptionType = new GraphQLObjectType({
  name: 'RaceTraitOption',
  fields: () => ({
    race_id: {type: GraphQLString},
    choose: {type: GraphQLInt},
    // TODO: Update when Trait Type is created
    traits: {
      type: GraphQLList(GraphQLString),
      resolve(parent, args){
        return new Promise((resolve, reject) => {
          db.all('SELECT trait_id FROM race_trait_options WHERE race_id = $id', {$id: parent.race_id},(err, rows) => {  
              if(err){
                  reject([]);
              }
              resolve(rows.map(row => row.trait_id));
            });
          });
      }
    },
  })
})

const ReactionType = new GraphQLObjectType({
  name: 'Reaction',
  fields: () => ({
    monster_id: {type: GraphQLString},
    reaction: {type: GraphQLString},
    description: {type: GraphQLString}
  })
})

const SkillType = new GraphQLObjectType({
  name: 'Skill',
  fields: () => ({
    id: {type: GraphQLString},
    name: {type: GraphQLString},
    description: {type: GraphQLString},
    abilities: {
      type: AbilityScoreType,
      resolve(parent,args){
        return runQueryElement("SELECT a.* FROM skills_ability_score_link l JOIN ability_scores a ON l.ability_score_id = a.id WHERE l.skill_id = $id", {$id: parent.id})
      }
    }
  })
})

const SneakAttackClassSpecificType = new GraphQLObjectType({
  name: 'SneakAttack',
  fields: () => ({
    level_id: {type: GraphQLInt},
    dice_count: {type: GraphQLInt},
    dice_value: {type: GraphQLInt},
  })
})

const SpellcastingType = new GraphQLObjectType({
  name: 'Spellcasting',
  fields: () => ({
    id: {type: GraphQLInt},
    class_id: {type: GraphQLString},
    character_class: {
      type: CharacterClassType,
      resolve(parent, args){
        return runQueryElement('SELECT * FROM classes WHERE id = $id', {$id: parent.class_id})
      }
    },
    level: {type: GraphQLInt},
    spellcasting_ability: {
      type: AbilityScoreType,
      resolve(parent, args){
        return runQueryElement('SELECT * FROM ability_scores WHERE id = (SELECT ability_id FROM spellcasting_ability_link WHERE spellcasting_id = $id LIMIT 1)',{$id: parent.id})
      }
    },
    info: {
      type: GraphQLList(SpellcastingInfoType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM spellcasting_info WHERE spellcasting_id = $id',{$id: parent.id})
      }
    }
  })
})

const SpellcastingInfoType = new GraphQLObjectType({
  name: 'SpellcastingInfo',
  fields: () => ({
    spellcasting_id: {type: GraphQLInt},
    name: {type: GraphQLString},
    description: {type: GraphQLString}
  })
})

const SubclassType = new GraphQLObjectType({
  name: 'Subclass',
  fields: () => ({
    id: {type: GraphQLString},
    class_id: {type: GraphQLString},
    description: {type: GraphQLString},
    features: {
      type: GraphQLList(FeatureType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM features WHERE id IN (SELECT feature_id FROM subclass_feature_link WHERE subclass_id = $id)', {$id: parent.id})
      }
    },
    // TODO: Update when Spells Type is created
    spells: {
      type: GraphQLList(GraphQLString),
      resolve(parent, args){
        // return runQueryList('SELECT spell_id FROM subclass_spells_link WHERE subclass_id = $id', {$id: parent.id})
        return new Promise((resolve, reject) => {
          db.all('SELECT spell_id FROM subclass_spells_link WHERE subclass_id = $id', {$id: parent.id},(err, rows) => {  
            if(err){
                reject([]);
            }
            resolve(rows.map(spell => spell.spell_id));
          });
        });
      }
    },
    name: {type: GraphQLString},
    subclass_flavor: {type: GraphQLString},
  })
})

const SubclassSpecificType = new GraphQLObjectType({
  name: 'SubclassSpecific',
  fields: () => ({
    class_id: {type: GraphQLString},
    level: {type: GraphQLInt},
    level_id: {type: GraphQLInt},
    additional_magical_secrets_max_lvl: {type: GraphQLInt}
  })
})

const StartingEquipmentType = new GraphQLObjectType({
  name: 'StartingEquipment',
  fields: () => ({
    id: {type: GraphQLInt},
    class_id: {type: GraphQLString},
    choices_to_make: {type: GraphQLInt},
    chosen_equipment_1: {
      type: GraphQLList(StartingEquipmentChoiceType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM starting_equipment_choices WHERE class_id = $id AND choice_id = 1 GROUP BY choice_group', {$id: parent.class_id})
      }
    },
    chosen_equipment_2: {
      type: GraphQLList(StartingEquipmentChoiceType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM starting_equipment_choices WHERE class_id = $id AND choice_id = 2 GROUP BY choice_group', {$id: parent.class_id})
      }
    },
    chosen_equipment_3: {
      type: GraphQLList(StartingEquipmentChoiceType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM starting_equipment_choices WHERE class_id = $id AND choice_id = 3 GROUP BY choice_group', {$id: parent.class_id})
      }
    },
    chosen_equipment_4: {
      type: GraphQLList(StartingEquipmentChoiceType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM starting_equipment_choices WHERE class_id = $id AND choice_id = 4 GROUP BY choice_group', {$id: parent.class_id})
      }
    },
    chosen_equipment_5: {
      type: GraphQLList(StartingEquipmentChoiceType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM starting_equipment_choices WHERE class_id = $id AND choice_id = 5 GROUP BY choice_group', {$id: parent.class_id})
      }
    },
    starting_equipment: {
      type: GraphQLList(EquipmentType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM equipment WHERE id IN (SELECT equipment_id FROM starting_equipment_link WHERE class_id = $id)', {$id: parent.class_id})
      }
    }
  })
})

const StartingEquipmentChoiceType = new GraphQLObjectType({
  name: 'StartingEquipmentChoice',
  fields: () => ({
    choose: {type: GraphQLInt},
    choice_group: {type: GraphQLInt},
    choice_id: {type: GraphQLInt},
    choose_from: {
      type: GraphQLList(EquipmentType),
      resolve(parent, args){
        return runQueryList('SELECT * FROM equipment WHERE id IN (SELECT equipment_id FROM starting_equipment_choices WHERE class_id = $id AND choice_id = $choice_id AND choice_group = $choice_group)', {$id: parent.class_id, $choice_id: parent.choice_id, $choice_group: parent.choice_group})
      }
    },
    class_id: {type: GraphQLString}
  })
})

const WeaponPropertyType = new GraphQLObjectType({
  name: 'WeaponProperty',
  fields: () => ({
    id: {type: GraphQLString},
    name: {type: GraphQLString},
    description: {type: GraphQLString}
  })
})

const RootQuery = new GraphQLObjectType({
  name: 'RootQuery',
  fields: {
    AllEquipment: {
      type: GraphQLList(EquipmentType),
      args: {},
      resolve(parent, args){
        return runQueryList("SELECT * FROM equipment;")
      }
    },
    Equipment: {
      type: EquipmentType,
      args: {
        id: {type: GraphQLString}
      },
      resolve(parent, args){
        return runQueryElement("SELECT * FROM equipment WHERE id=$id;", {$id: args.id})
      }
    },
    AllMonsters: {
      type: GraphQLList(MonsterType),
      args: {},
      resolve(parent, args){
        return runQueryList("SELECT * FROM monsters;")
      }
    },
    Monster: {
      type: MonsterType,
      args: {
        id: {type: GraphQLString}
      },
      resolve(parent, args){
        return runQueryElement("SELECT * FROM monsters WHERE id=$id;", {$id: args.id})
      }
    },
    AllSkills: {
      type: GraphQLList(SkillType),
      args: {},
      resolve(parent, args){
        return runQueryList("SELECT * FROM skills;")
      }
    },
    Skill: {
      type: SkillType,
      args: {
        id: {type: GraphQLString}
      },
      resolve(parent, args){
        return runQueryElement("SELECT * FROM skills WHERE id=$id;", {$id: args.id})
      }
    },
    AllAbilityScores: {
      type: GraphQLList(AbilityScoreType),
      args: {},
      resolve(parent, args){
        return runQueryList("SELECT * FROM ability_scores;")
      }
    },
    AbilityScore: {
      type: AbilityScoreType,
      args: {
        id: {type: GraphQLString}
      },
      resolve(parent, args){
        return runQueryElement("SELECT * FROM ability_scores WHERE id=$id;", {$id: args.id})
      }
    },
    AllFeatures: {
      type: GraphQLList(FeatureType),
      args: {},
      resolve(parent, args){
        return runQueryList("SELECT * FROM features;")
      }
    },
    Feature: {
      type: FeatureType,
      args: {
        id: {type: GraphQLString}
      },
      resolve(parent, args){
        return runQueryElement("SELECT * FROM features WHERE id=$id;", {$id: args.id})
      }
    },
    AllCharacterClasses: {
      type: GraphQLList(CharacterClassType),
      args: {},
      resolve(parent, args){
        return runQueryList("SELECT * FROM classes;")
      }
    },
    CharacterClass: {
      type: CharacterClassType,
      args: {
        id: {type: GraphQLString}
      },
      resolve(parent, args){
        return runQueryElement("SELECT * FROM classes WHERE id=$id;", {$id: args.id})
      }
    },
    AllRaces: {
      type: GraphQLList(RaceType),
      args: {},
      resolve(parent, args){
        return runQueryList("SELECT * FROM races;")
      }
    },
    Race: {
      type: RaceType,
      args: {
        id: {type: GraphQLString}
      },
      resolve(parent, args){
        return runQueryElement("SELECT * FROM races WHERE id=$id;", {$id: args.id})
      }
    },
  }
})

module.exports = new GraphQLSchema({
  query: RootQuery
})

