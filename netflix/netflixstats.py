import json
import httplib2
import json
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections
from datetime import datetime

class ViewItem(Document):
    videoTitle: Keyword()
    title: Text(analyzer='snowball')
    seriesTitle: Text(analyzer='snowball')
    country: Keyword()
    date: Date()
    bookmark: Integer()
    deviceType: Integer()
    movieID: Integer()
    duration: Integer()
    episodeTitle: Keyword()

    class Index:
        name = 'netflix'
        settings = {
            "number_of_shards": 1,
        }

    def save(self, **kwargs):
        return super(ViewItem, self).save(**kwargs)


def export_netflix_viewhistory(config):
    all_viewed_items = []
    http = httplib2.Http()
    headers = {'Cookie': 'NetflixId={0}'.format(str(config['cookie']))}
    page_has_view_items = True
    page = 0
    while page_has_view_items:
        url = 'https://www.netflix.com/shakti/vb850f007/viewingactivity?pg={0}'.format(str(page))
        response, content = http.request(url, 'GET', headers=headers)
        data = json.loads(content)
        if len(data['viewedItems']) > 0:
            all_viewed_items.extend(data['viewedItems'])
            page_has_view_items = True
            page += 1
            print("Page {0} parsed.".format(str(page)))
        else:
            page_has_view_items = False
            print("Parsing Done")

    with open(config['datafile'], 'w', newline='') as file:
        file.write(json.dumps(all_viewed_items, indent=4, sort_keys=True))


def import_elasticsearch(config):
    connections.create_connection(hosts=[config['elastic_host']])
    ViewItem.init()
    with open(config['datafile']) as json_file:
        data = json.load(json_file)
        total = len(data)
        count = 0
        for item in data:
            view_item = ViewItem(videoTitle=item['videoTitle'],
                                 title=item['title'],
                                 country=item['country'],
                                 date=datetime.fromtimestamp(item['date'] / 1000),
                                 bookmark=item['bookmark'],
                                 deviceType=item['deviceType'],
                                 movieID=item['movieID'],
                                 duration=item['duration'])
            if 'seriesTitle' in item:
                view_item.seriesTitle = item['seriesTitle']
            if 'episodeTitle' in item:
                view_item.episodeTitle = item['episodeTitle']
            view_item.save()
            count += 1
            print("Saved #{0} of {1}".format(str(count)))
    print("Import to elastic finished.")

def main():
    with open("config.json") as config_file:
        config = json.load(config_file)
        export_netflix_viewhistory(config=config)
        import_elasticsearch(config=config)

if __name__ == '__main__':
    main()

