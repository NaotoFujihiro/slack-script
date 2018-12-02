from pathlib import Path
from slackclient import SlackClient
import yaml


class SlackBase:
    def __init__(self):
        script_path = Path(__file__).parent

        with (script_path / '../credentials.yml').open() as f:
            self.credentials = yaml.load(f)

        with (script_path / '../config.yml').open() as f:
            self.config = yaml.load(f)

        self.slack = SlackClient(self.credentials['slack_token'])

    def validate_slack_response(self, res):
        if not res['ok']:
            raise Exception('Slack message is not sended: {}'.format(res['error']))
