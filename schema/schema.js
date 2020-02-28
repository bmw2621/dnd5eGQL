const graphql = require('graphql');
const sqlite3 = require('sqlite3').verbose()

const db = new sqlite3.Database('./dnd5e.db', sqlite3.OPEN_READONLY, (err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Connected to the dnd5e database.');
  });

const runQuery = (statement, params = {}) => {
  return new Promise((resolve, reject) => {
    db.all(statement, params,(err, rows) => {  
      if(err){
          reject([]);
      }
      resolve(rows);
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
        return runQuery("SELECT * FROM equipment WHERE id IN (SELECT content_id FROM equipment_contents_link WHERE equipment_id = $id)",{$id: parent.id})
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
        return new Promise((resolve, reject) => {
                    db.all("SELECT * FROM damage_types WHERE id=(SELECT LOWER(damage_type) FROM equipment WHERE id=$id)", {$id: parent.id},(err, rows) => {  
                        if(err){
                            reject([]);
                        }
                        resolve(rows[0]);
                    });
                });
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
        return runQuery("SELECT * FROM weapon_properties WHERE id IN (SELECT LOWER(property) FROM property_equipment_link WHERE equipment_id = $id)",{$id: parent.id})
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

const WeaponPropertyType = new GraphQLObjectType({
  name: 'WeaponProperty',
  fields: () => ({
    id: {type: GraphQLString},
    name: {type: GraphQLString},
    description: {type: GraphQLString}
  })
})

const RootQuery = new GraphQLObjectType({
  name: 'RootQueryType',
  fields: {
    AllEquipment: {
      type: GraphQLList(EquipmentType),
      args: {},
      resolve(parent, args){
        return runQuery("SELECT * FROM equipment;")
      }
    },
    Equipment: {
      type: EquipmentType,
      args: {
        id: {type: GraphQLString}
      },
      resolve(parent, args){
        return new Promise((resolve, reject) => {
                    db.all("SELECT * FROM equipment WHERE id=$id;", {$id: args.id}, (err, rows) => {  
                        if(err){
                            reject([]);
                        }
                        resolve(rows[0]);
                    });
                });
      }
    },
  }
})

module.exports = new GraphQLSchema({
  query: RootQuery
})

