const router = require("express").Router();
const authController = require("../controllers/user/auth");
const authenticate = require("../middleware/authenticate");

router.post("/register", authController.register);

router.post("/login", authController.login);

router.get("/logout", authenticate, authController.logout);

router.get("/checkuser", authenticate, (req, res) => {
    res.send(req.rootUser);
});

module.exports = router;