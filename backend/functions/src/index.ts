import { onRequest } from "firebase-functions/v2/https";
// import { onCall } from "firebase-functions/v2/https";
import * as logger from "firebase-functions/logger";
// import { initializeApp } from "firebase-admin/app";
// import { getFirestore, FieldValue } from "firebase-admin/firestore";
// import { onDocumentCreated } from "firebase-functions/v2/firestore";
import { setGlobalOptions } from "firebase-functions/v2";

setGlobalOptions({ region: "asia-northeast1" });

const express = require("express");
const app = express();

app.get("/hello", (request, response) => {
    logger.info("Hello logs!", { structuredData: true });
    response.send("Hello from Firebase Functions!");
});

exports.api = onRequest(app);

// export * from "./schedule/cronTest";
