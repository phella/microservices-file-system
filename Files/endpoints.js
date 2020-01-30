const express = require ("express");
require('dotenv').config();
const fs = require('fs');
const router = express.Router();

router.get('/content', (req,res)=>{
  if(req.query.path == null)
    res.status(400).json({error:"empty path"});
    fs.readdir("", (err, files) => {
      console.log(files);
      res.status(200).json(files);
    });
});

module.exports = router;
