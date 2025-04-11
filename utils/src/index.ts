const { initializeApp, applicationDefault, cert } = require('firebase-admin/app');
const { getFirestore, Timestamp, FieldValue, Filter } = require('firebase-admin/firestore');

const serviceAccount = require('../serviceAccount.json');

initializeApp({
    credential: cert(serviceAccount)
});

const db = getFirestore();


const USER_ID = 'TEST_USER_ID';
const USER_NAME = 'test';
const TIME = '00:00';

const DATES = [
    // '2025-01-27',
    // '2025-01-28',
    // '2025-01-29',
    // '2025-01-30',
    // '2025-01-31',
    "2025-04-12"
]



async function addCommitments() {
    const collection = db.collection('commitments');
    for (const date of DATES) {
        const docRef = collection.doc(date);

        const doc = await docRef.get();
        if (!doc.exists) {
            await docRef.set({});
        }

        await docRef.update({
            [USER_ID]: {
                userId: USER_ID,
                userName: USER_NAME,
                time: TIME,
                enabled: true,
            }
        });
        console.log(`Added commitment for ${date}`);
    }
}






addCommitments();



// To run:
// tsc index.ts && node index.js