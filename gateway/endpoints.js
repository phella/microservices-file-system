const passport = require('passport');
const express = require ("express");
const router = express.Router();
const dbManger = require('./dbManager');
const bcrypt = require('bcryptjs');
const redis = require('redis');
const redisUrl = "redis://127.0.0.1:6379";
const util = require("util");
const client = redis.createClient(redisUrl);
client.hget = util.promisify(client.hget);

router.post('/login', passport.authenticate('local',{
    successRedirect: '/',
    failureRedirect: '/login',
    failureFlash:true
}))

router.post('/register',  async (req, res) => {
      if(!req.body.email || !req.body.password || !req.body.gender || !req.body.name || !req.body.phoneNo || !req.body.age){
        return res.status(400).json({error:"Payload missing"});  
      }
      const hashedPassword = await bcrypt.hash(req.body.password, 10);
      let result = await dbManger.findUser({email:req.body.email} , 1);
      result.success &= (await dbManger.findUser({phoneNo: req.body.phoneNo},1)).success; 
      //const result = await dbManger.saveUser({name : req.body.name , email :  req.body.email , password : hashedPassword , gneder:req.body.gender , phoneNo:req.body.phoneNo , age:req.body.age});
      if(result.success){
        const randomCode =Math.random().toString().substring(2,6);
        client.set( 'confirm' + randomCode , JSON.stringify(result.users) , 'EX', 60 * 60 );
        return res.status(201).json({message:"Created successfully"});
      }
      return res.status(400).json({error:`${result.error} already used`});
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
    next(req,res)
  }

  module.exports = router;