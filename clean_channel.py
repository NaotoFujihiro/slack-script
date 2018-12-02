#!/usr/bin/env python

from pprint import pprint
from utils.slack import SlackBase


class CleanChannel(SlackBase):
    def run(self):
        channel_id = self.config['clean_channel']['channel_id'] 

        # retrieve all messages in the channel
        res = self.slack.api_call(
            'channels.history',
            channel=channel_id
        )
        self.validate_slack_response(res)

        for message in res['messages']:
            # delete the file attached to the message
            for file in message.get('files', []):
                pprint(file)

                if file['mode'] == 'tombstone':
                    continue

                res = self.slack.api_call(
                    'files.delete',
                    file=file['id']
                )
                self.validate_slack_response(res)

            # delete messages
            print(message['ts'])
            res = self.slack.api_call(
                'chat.delete',
                channel=channel_id,
                ts=message['ts']
            )
            self.validate_slack_response(res)


if __name__ == '__main__':
    CleanChannel().run()
