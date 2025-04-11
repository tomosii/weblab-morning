import { GeoPoint } from 'firebase-admin/firestore';
import { logger } from 'firebase-functions/v2';

import { db } from './firestore';
import { Attendance } from '../models/attendance';
import { getDateKey } from '../utils/date';

export class AttendanceRepository {
    private collection = db.collection('attendances');

    async getAttendance(date: Date): Promise<Attendance[]> {
        const dateKey = getDateKey(date);
        const docRef = this.collection.doc(dateKey);
        const doc = await docRef.get();

        if (!doc.exists) {
            return [];
        }

        const attendances: Attendance[] = Object.values(doc.data() || {}).map((data: any) => ({
            date,
            userId: data.userId,
            userName: data.userName,
            checkInAt: data.checkInAt.toDate(),
            commitmentTime: data.commitmentTime,
            ipAddress: data.ipAddress,
            latLng: data.latLng,
            placeName: data.placeName,
            timeDifferenceSeconds: data.timeDifferenceSeconds,
            timeout: data.timeout,
        }));

        logger.log(`[Firestore] Get ${attendances.length} attendances of ${dateKey}`);
        return attendances;
    }

    async getAttendances(dates: Date[]): Promise<Attendance[]> {
        const attendances: Attendance[] = [];
        for (const date of dates) {
            const dayAttendances = await this.getAttendance(date);
            attendances.push(...dayAttendances);
        }
        return attendances;
    }

    async putAttendance(
        {
            userId,
            userName,
            checkInAt,
            commitmentTime,
            ipAddress,
            latitude,
            longitude,
            placeName,
            timeDifferenceSeconds,
            timeout,
        }: {
            userId: string;
            userName: string;
            checkInAt: Date;
            commitmentTime: string;
            ipAddress: string;
            latitude: number;
            longitude: number;
            placeName: string;
            timeDifferenceSeconds: number;
            timeout: boolean;
        }): Promise<void> {
        const dateKey = getDateKey(checkInAt);
        const docRef = this.collection.doc(dateKey);
        const doc = await docRef.get();

        // Create empty document if not exists
        if (!doc.exists) {
            await docRef.set({});
        }

        await docRef.update({
            [userId]: {
                userId,
                userName,
                checkInAt,
                commitmentTime,
                ipAddress,
                latLng: new GeoPoint(latitude, longitude),
                placeName,
                timeDifferenceSeconds,
                timeout,
            },
        });

        logger.log(`[Firestore] Put attendance of ${userId} on ${dateKey}`);
    }
}
