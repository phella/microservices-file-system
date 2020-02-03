const express = require('express');
const chalk = require('chalk');
const debug = require('debug')('app');
const morgan = require('morgan');
const bodyParser = require("body-parser");
require('dotenv').config();


const app = express();

app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());

const port = process.env.PORT || 3000;
// add /files in path
app.use('/files',require('./endpoints'));
app.use(morgan('tiny'));



/*Mongoose.connect('mongodb://localhost:27017/market',{useNewUrlParser:true , useUnifiedTopology: true },
	debug("Connected to database")
);
Mongoose.set('useCreateIndex', true);
*/
app.listen(port, () => {
  debug(`Listenning on port ${chalk.green(port)}`);
});