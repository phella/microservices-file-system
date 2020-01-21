const localStrategy = require('passport-local').Strategy;
const bcrypt = require('bcryptjs');
const dbManager = require('./dbManager');

function init(passport) {
	
	const authenticateUsers = (email, password, done) => {
		const checkUser = async (user) => {
			if (user == null) {
				return done(null, false, { message: "No user found." });
			}
			// Wrap async in try catch 
			try {
				const flag = await bcrypt.compare(password, user.password);
				if (flag) {
					return done(null, user);
				} else {
					return done(null, false, { message: "Wronng password" });
				}
			} catch (e) {
				return done(e);
			}
		};
	
		dbManager.findUser([email], ['email'], 1 ).then(checkUser(user));
	};
	passport.use(new localStrategy({ usernameField: 'email' }, authenticateUsers));
	passport.serializeUser((user, done) => done(null , user.email));
	passport.deserializeUser(async (email, done) => {
		const user = await findUser([email], ['email'], 1 );
		return done(null, user);
	});
}

module.exports = init;