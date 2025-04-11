import { setGlobalOptions } from "firebase-functions/v2";

setGlobalOptions({ region: "asia-northeast1" });


const checkTimeout = require("./schedule/checkTimeout");
exports.checkTimeout = checkTimeout.checkTimeout;