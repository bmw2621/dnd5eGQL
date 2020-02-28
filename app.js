const express = require('express');
const graphqlHTTP = require('express-graphql');
const schema = require('./schema/schema');
const cors = require('cors')


const app = express();

app.use(cors());
app.use('/graphql', graphqlHTTP({
  schema,
  graphiql: true
}));

const PORT_NUMBER = 4000;

app.listen(PORT_NUMBER, () => {
  console.log(`Now listening for requests on port ${PORT_NUMBER}`)
})
