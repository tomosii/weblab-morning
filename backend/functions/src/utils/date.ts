
import * as holiday_jp from '@holiday-jp/holiday_jp';
import { logger } from 'firebase-functions';

const jpDaysOfWeek = {
    0: "日",
    1: "月",
    2: "火",
    3: "水",
    4: "木",
    5: "金",
    6: "土",
}


// Get the current date in Japan timezone
function getCurrentJpDate(): Date {
    const now = new Date();
    const jpDateString = now.toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' });
    const jpDate = new Date(jpDateString);
    return jpDate;
}

// Get the date string in the format YYYY-MM-DD
function getDateKey(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}


function isJpWeekday(date: Date): boolean {
    const day = date.getDay();
    if (day === 0 || day === 6) {
        return false;
    }
    if (holiday_jp.isHoliday(date)) {
        return false;
    }
    return true;
}

function getJpDateString(date: Date, withDayOfWeek: boolean = true): string {
    if (withDayOfWeek) {
        return `${date.getMonth() + 1}/${date.getDate()} (${getJpDayOfWeek(date)})`;
    }
    return `${date.getMonth() + 1}/${date.getDate()}`;
}

function getJpDayOfWeek(date: Date): string {
    return jpDaysOfWeek[date.getDay()];
}

function getOngoingOrLastWeekdays(): Date[] {
    /*
    開催中なら開催中の日付を，開催中でなければ前回の開催日を返す
    (結果の確認などに使う)
    */
    const today = getCurrentJpDate();
    let todayDayOfWeek = today.getDay();

    // 今週の月曜日から金曜日のうち、平日の日付を取得
    const thisMonday = new Date(today.getFullYear(), today.getMonth(), today.getDate() - todayDayOfWeek + 1);
    const thisWeekdays = [];
    for (let i = 0; i < 5; i++) {
        const date = new Date(thisMonday);
        date.setDate(thisMonday.getDate() + i);
        if (isJpWeekday(date)) {
            thisWeekdays.push(date);
        }
    }
    logger.log("This weekdays:", thisWeekdays);

    // 今週の開催がもう始まっていれば、今週の開催日を返す
    if (thisWeekdays.length != 0 && thisWeekdays[0] <= today) {
        return thisWeekdays;
    }

    // まだ開催されていない場合は、前回の開催日を返す
    const lastMonday = new Date(thisMonday.getFullYear(), thisMonday.getMonth(), thisMonday.getDate() - 7);
    const lastWeekdays = [];
    for (let i = 0; i < 5; i++) {
        const date = new Date(lastMonday);
        date.setDate(lastMonday.getDate() + i);
        if (isJpWeekday(date)) {
            lastWeekdays.push(date);
        }
    }
    logger.log("Last weekdays:", lastWeekdays);
    return lastWeekdays;
}



export { getCurrentJpDate, getDateKey, isJpWeekday, getJpDateString, getJpDayOfWeek, getOngoingOrLastWeekdays };