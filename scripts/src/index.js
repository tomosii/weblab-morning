var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var _a = require('firebase-admin/app'), initializeApp = _a.initializeApp, applicationDefault = _a.applicationDefault, cert = _a.cert;
var _b = require('firebase-admin/firestore'), getFirestore = _b.getFirestore, Timestamp = _b.Timestamp, FieldValue = _b.FieldValue, Filter = _b.Filter;
var serviceAccount = require('../serviceAccount.json');
initializeApp({
    credential: cert(serviceAccount)
});
var db = getFirestore();
// const USER_ID = 'U9E5HUXEU';
// const USER_NAME = 'taniguchi';
// const TIME = '09:30';
var USER_ID = 'TEST_USER_ID';
var USER_NAME = 'test';
var TIME = '00:00';
var DATES = [
    // '2025-01-27',
    // '2025-01-28',
    // '2025-01-29',
    // '2025-01-30',
    // '2025-01-31',
    "2025-04-12"
];
function addCommitments() {
    return __awaiter(this, void 0, void 0, function () {
        var collection, _i, DATES_1, date, docRef, doc;
        var _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    collection = db.collection('commitments');
                    _i = 0, DATES_1 = DATES;
                    _b.label = 1;
                case 1:
                    if (!(_i < DATES_1.length)) return [3 /*break*/, 7];
                    date = DATES_1[_i];
                    docRef = collection.doc(date);
                    return [4 /*yield*/, docRef.get()];
                case 2:
                    doc = _b.sent();
                    if (!!doc.exists) return [3 /*break*/, 4];
                    return [4 /*yield*/, docRef.set({})];
                case 3:
                    _b.sent();
                    _b.label = 4;
                case 4: return [4 /*yield*/, docRef.update((_a = {},
                        _a[USER_ID] = {
                            userId: USER_ID,
                            userName: USER_NAME,
                            time: TIME,
                            enabled: true,
                        },
                        _a))];
                case 5:
                    _b.sent();
                    console.log("Added commitment for ".concat(date));
                    _b.label = 6;
                case 6:
                    _i++;
                    return [3 /*break*/, 1];
                case 7: return [2 /*return*/];
            }
        });
    });
}
addCommitments();
// To run:
// tsc index.ts && node index.js
