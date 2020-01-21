const user = require('./user.model');

class dbManager{
	
	async findUser(conditions , projectionStr , numberOfusers){
		if(values.length !== queryKeys.length)
			return false;
		if(numberOfusers === 1 ){
			return await user.findOne(conditions , projectionStr);
		}else{
			return await user.find(conditions , projectionStr ).limit(numberOfusers); 
		}
	}
	async saveUser(account){
		const result = new user(account);
		try { 
			await result.save();
		} catch(err){
			if(err.errors.phoneNo)
				return {success:false,error:"Phone number"};
			else if(err.errors.email)
				return {success:false,error:"Email"};
		}
		return {success:true}
	}
};

module.exports = new dbManager();
