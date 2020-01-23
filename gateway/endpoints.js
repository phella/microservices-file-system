const passport = require('passport');
const express = require ("express");
const router = express.Router();
const Nexmo = require('nexmo');
const dbManger = require('./dbManager');
const bcrypt = require('bcryptjs');
const redis = require('redis');
const redisUrl = "redis://127.0.0.1:6379";
const util = require("util");
const client = redis.createClient(redisUrl);
client.hget = util.promisify(client.hget);
const debug = require('debug')('auth');
require('dotenv').config();

const nexmo = new Nexmo({
  apiKey: process.env.apiKey,
  apiSecret: process.env.apiSecret,
});

router.post('/login', passport.authenticate('local',{
    successRedirect: '/',
    failureRedirect: '/login'
}))

router.post('/register', checkNotAuthenticated, async (req, res) => {
      if(!req.body.email || !req.body.password || !req.body.gender || !req.body.name || !req.body.phoneNo || !req.body.age){
        return res.status(400).json({error:"Payload missing"});  
      }
      const hashedPassword = await bcrypt.hash(req.body.password, 10);
      let result = await dbManger.findUser({email:req.body.email} , 1);
      result.success &= (await dbManger.findUser({phoneNo: req.body.phoneNo},1)).success; 
      if(result.success){
        const randomCode =Math.random().toString().substring(2,6);
        const newAcc = {name : req.body.name ,
                        email :  req.body.email ,
                        password : hashedPassword ,
                        gneder:req.body.gender ,
                        phoneNo:req.body.phoneNo,
                        age:req.body.age }
        client.set( 'confirm' + randomCode , JSON.stringify(newAcc) , 'EX', 60 * 60 );
        send_sms(req.body.phoneNo , randomCode);
        return res.status(201).json({message:"Created successfully"});
      }
      return res.status(400).json({error:`${result.error} already used`});
  })

  router.post('/confirm',async(req,res)=>{
    if(!req.randomCode)
      return res.status(400).json({error:"Payload missing"});
    const acc = await client.get( 'randomcode' + randomCode );
    if(!acc){
      return res.status(400).json({error:"Account request expired"})
    }
    const result = await dbManger.saveUser(acc);
    if(result.success)
      res.header(200).json({message:"Account activated"});
    res.header(400).json({message:"Account already activated"});
  })

  router.get('/login',async(req,res)=>{
    res.status(200).send("hi");
  })
  function checkAuthenticated(req, res, next) {
    if (req.isAuthenticated()) {
      return next()
    }
  
    res.redirect('/login')
  }
  
  function checkNotAuthenticated(req, res, next) {
    if (req.isAuthenticated()) {
      return res.redirect('/')
    }
    next()
  }

function send_sms(to , code){
  const from = 'Market Microservices';
  const text = 'Confirmation code'+code;
  nexmo.message.sendSms(from, to, text);
}
  module.exports = router;
