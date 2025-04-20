export function text(userId: string): string {
    return `<@${userId}> 本日のチェックインがありませんでした`;
}

export function blocks(
    { userId, totalPoints, pointChange }: {
        userId: string,
        totalPoints: number,
        pointChange: number
    }
): Array<any> {
    const pointChangeText = pointChange > 0
        ? `+${pointChange}`
        : `${pointChange}`;

    const pointChangeEmoji = pointChange > 0
        ? ":star:"
        : ":rotating_light:";

    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": `<@${userId}>`
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "本日のチェックインがありませんでした"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": `${pointChangeEmoji} *\`${pointChangeText}\` pt*`
                    // "text": ":christmas_tree: *`${pointChangeText}pt`*"
                },
                {
                    "type": "mrkdwn",
                    "text": `今週の合計 *${totalPoints} pt*`
                }
            ]
        }
    ];
}
