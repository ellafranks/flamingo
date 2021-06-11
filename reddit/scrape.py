import json
import os

from psaw import PushshiftAPI
import datetime as dt


class RedditCollector:
    def __init__(self, subreddit, output_path, start_date, end_date):
        self.api = PushshiftAPI()
        self.subreddit = subreddit
        self.output_path = output_path
        self.start_date = start_date  # as datetime object
        self.end_date = end_date  # as datetime object
        self.search_limit = 450
        self.start_dates_list = []
        self.delta = dt.timedelta(days=1)

    def _fetch_and_persist_single_day(self, start_date, end_date):
        return list(self.api.search_comments(before=start_date,
                                             atfer=end_date,
                                             subreddit=self.subreddit,
                                             limit=self.search_limit))

    def _create_date_list(self):
        start_date = self.start_date
        while start_date <= self.end_date:
            self.start_dates_list.append(start_date)
            start_date += self.delta

    def write(self):
        self._create_date_list()
        print('Collecting comments from day {} to {}'.format(self.start_date, self.end_date))
        for date in self.start_dates_list:
            all_results = self._fetch_and_persist_single_day(start_date=date,
                                                             end_date=int((date + self.delta).timestamp()))
            for _id, result in enumerate(all_results):
                self.dump_json(date, result._asdict(), _id)

    def dump_json(self, date, result, _id):

        file_name = '{}_{}.json'.format(date.strftime("%Y-%m-%d"), _id)
        out_path = os.path.join(self.output_path, file_name)
        with open(out_path, 'w') as f:
            json.dump(result, f)
