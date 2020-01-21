const passport = require('passport');
const express = require ("express");
const router = express.Router();
const dbManger = require('./dbManager');
const bcrypt = require('bcryptjs');

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
      const result = await dbManger.saveUser({name : req.body.name , email :  req.body.email , password : hashedPassword , gneder:req.body.gender , phoneNo:req.body.phoneNo , age:req.body.age});
      if(result.success)
        return res.status(201).json({message:"Created successfully"});
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