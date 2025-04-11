import { GeoPoint } from "firebase-admin/firestore";

export interface Attendance {
    date: Date;
    userId: string;
    userName: string;
    checkInAt: Date;
    commitmentTime: string;
    ipAddress: string;
    latLng: GeoPoint;
    placeName: string;
    timeDifferenceSeconds: number;
    timeout?: boolean;
}
