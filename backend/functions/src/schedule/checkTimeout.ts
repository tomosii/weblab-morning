import { onSchedule } from "firebase-functions/v2/scheduler";
import { logger } from "firebase-functions";

import { TARGET_CHANNEL_ID } from "../constants/channels";
import { db } from "../repositories/firestore";
import { slackClient } from "../repositories/slack";
import { attendanceRepository } from "../repositories";
import { getCurrentJpDate, getDateKey, getOngoingOrLastWeekdays } from "../utils/date";
import { getTotalPointsAndPenalty } from "../utils/point";
import * as timeoutNotification from "../views/timeoutNotification";



/*
Every 1 hour from 11:00 to 17:00 on weekdays
Cron: "0 11-17 * * 1-5"
*/
exports.checkTimeout = onSchedule({
    schedule: "0 11-17 * * 1-5",
    timeZone: "Asia/Tokyo",
}, async (event) => {
    logger.log("Cron job checkTimeout started");

    const currentDate = getCurrentJpDate();
    const currentDateKey = getDateKey(currentDate);

    // Get commitment data from /commitments/%Y-%m-%d
    const commitmentsRef = db.collection("commitments").doc(currentDateKey);
    const commitmentsDoc = await commitmentsRef.get();
    if (!commitmentsDoc.exists) {
        logger.log("/commitments/" + currentDateKey + " does not exist");
        return;
    }
    logger.log("Get data from /commitments/" + currentDateKey);
    const allCommitments = commitmentsDoc.data();
    logger.log(JSON.stringify(allCommitments));

    // Get attendance data from /attendances/%Y-%m-%d
    const allAttendances = await attendanceRepository.getAttendances([currentDate]);
    logger.log(JSON.stringify(allAttendances));

    // For each user in allCommitments
    for (const userId in allCommitments) {
        const commitment = allCommitments[userId];
        if (!commitment["enabled"]) {
            logger.log("User " + userId + " is not enabled");
            continue;
        }

        // Has user already checked in?
        const attendance = allAttendances.find((attendance) => attendance.userId === userId);
        if (attendance) {
            logger.log("User " + userId + " has already checked in");
            continue;
        }
        logger.log("User " + userId + " has not checked in yet");

        // Calculate time difference in hours
        const commitmentTime = commitment["time"]; // HH:MM
        const [commitmentHour, commitmentMinute] = commitmentTime.split(':').map(Number);
        const commitmentDate = new Date(currentDate)
        commitmentDate.setHours(commitmentHour, commitmentMinute, 0, 0);
        const timeDiffInHours = (currentDate.getTime() - commitmentDate.getTime()) / (1000 * 60 * 60);
        if (timeDiffInHours < 4) {
            logger.log(`It has not been 4 hours since ${commitmentTime} yet`);
            continue;
        }

        // ==== TIMEOUT (More than 4 hours have passed) ====
        logger.log(`TIMEOUT: More than 4 hours have passed since ${commitmentTime}`);

        // Write attendance record
        await attendanceRepository.putAttendance(
            {
                userId: userId,
                userName: allCommitments[userId]["userName"],
                checkInAt: currentDate,
                commitmentTime: commitmentTime,
                ipAddress: "",
                latitude: 0,
                longitude: 0,
                placeName: "",
                timeDifferenceSeconds: 10000000000,
                timeout: true,
            }
        );

        const ongoingActivityDates = getOngoingOrLastWeekdays();
        const attendances = await attendanceRepository.getAttendances(ongoingActivityDates);
        const [totalPoints, penalty] = getTotalPointsAndPenalty(userId, attendances);
        logger.log(`Total points: ${totalPoints}`);
        logger.log(`Penalty: ${penalty}`);

        // Send notification to Slack
        slackClient.chat.postMessage({
            channel: TARGET_CHANNEL_ID,
            blocks: timeoutNotification.blocks({
                userId: userId,
                totalPoints: totalPoints,
                pointChange: -3,
            }),
            text: timeoutNotification.text(userId),
        });
        logger.log("Sent Slack notification for user " + userId);

        // Update point record
        const pointRef = db.collection("points").doc(getDateKey(ongoingActivityDates[0]));
        const pointDoc = await pointRef.get();
        if (!pointDoc.exists) {
            await pointRef.set({});
        }

        await pointRef.update({
            [userId]: {
                userId: userId,
                userName: allCommitments[userId]["userName"],
                point: totalPoints,
                penalty: penalty,
            },
        });
        logger.log("Updated point record for user " + userId);
    }

    logger.log("Cron job checkTimeout finished");
});
