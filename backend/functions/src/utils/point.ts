import { logger } from "firebase-functions";

import { Attendance } from "../models/attendance";
import { getDateKey } from "./date";

export function getPointChange(timeDifferenceSeconds: number): number {
    if (timeDifferenceSeconds < 0) {
        return 1;
    }

    const lateHour = timeDifferenceSeconds / 3600;
    logger.log(`Late hour: ${lateHour.toFixed(1)}`);
    const penalty = Math.floor(lateHour / 2) + 1;
    return -Math.min(penalty, 3);
}

export function getTotalPointsAndPenalty(userId: string, attendances: Attendance[]): [number, number] {
    let totalPoints = 0;
    let penalty = 0;

    for (const attendance of attendances) {
        if (attendance.userId !== userId) {
            continue;
        }

        const pointChange = getPointChange(attendance.timeDifferenceSeconds);
        logger.log(`${getDateKey(attendance.date)} ${pointChange}`);
        totalPoints += pointChange;

        if (pointChange < 0) {
            penalty += pointChange;
        }
    }

    return [totalPoints, penalty];
}
