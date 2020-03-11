# Dungeons and Dragons GraphQL API

This repository forked data source files from [Bagel Bits DnD5eAPI](https://github.com/bagelbits/5e-database) and transforms it from a RESTful API to a GraphQL API.

Orginal data is formatted for an unstructured MongoDB database.  GraphQL schema requires a structured schema, so efforts are currently organized on reshaping data into a SQLite3 database.

## Usage

To use the API in its current state, and test currently available endpoints:

- `git clone https://github.com/bmw2621/dnd5eGQL.git`
- `cd dnd5eGQL`
- `npm install`
- `node app.js`
- navigate to [http://localhost:4000/graphql](http://localhost:4000/graphql)
- GraphIQL is currently enabled and queries can be made in the interactive interface

## TODO

- [X] Races endpoint and in schema
- [X] Subraces endpoint and in schema
- [X] Magic Schools endpoint and in schema
- [ ] Equipment Category and link to Equipment Type in schema
- [X] Language Type in schema and in schema
- [X] Conditions Type in schema and endpoint
- [X] Proficiency Type in schema
- [X] Spells endpoint and in schema
- [X] Traits endpoint and in schema (Update Race and Subrace traits to graph to Traits Type)
- [ ] Weapons Properties endpoint and in schema