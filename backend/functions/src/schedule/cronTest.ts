import { onSchedule } from "firebase-functions/v2/scheduler";
import { logger } from "firebase-functions";
import { WebClient } from "@slack/web-api";

const slackToken = process.env.SLACK_BOT_TOKEN;
const slackChannelId = "C0616PTQ6AF";

const slack_client = new WebClient(slackToken);

exports.cronEveryTest = onSchedule("*/2 * * * *", async (event) => {
    logger.info("Cron job test (every 2 minutes)", {
        structuredData: true,
    });
    logger.info("Event: ", JSON.stringify(event));
    const now = new Date().toLocaleString("ja-JP", {
        timeZone: "Asia/Tokyo",
    });
    logger.info("Now: ", now);

    logger.info("Sending message to Slack...");
    await slack_client.chat.postMessage({
        channel: slackChannelId,
        text: "現在時刻は " + now + " です。",
    });
    return;
});

exports.cronAtTest = onSchedule(
    {
        schedule: "0 16 * * *",
        timeZone: "Asia/Tokyo",
    },
    async (event) => {
        logger.info("Cron job test (at 16:00)", { structuredData: true });
        logger.info("Event: ", JSON.stringify(event));
        const now = new Date().toLocaleString("ja-JP", {
            timeZone: "Asia/Tokyo",
        });
        logger.info("Now: ", now);
        return null;
    }
);
