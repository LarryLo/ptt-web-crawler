![travis_ci](https://travis-ci.org/LarryLo/ptt-web-crawler.svg?branch=master)

# ptt-web-crawler
This is a simple web crawler to gather data from PTT.

## Configuration
```
# /etc/config.ini
# You can modify some main settings in /etc/config.ini files
```

## How to use it?

### Build a docker image
```
$ docker build -t ptt-crawler:latest .
```

### Run and mount host's directory to store log and data
```
$ docker run -d -v /tmp:/tmp -v $PWD:/opt/ptt-crawler --name ptt-crawler --network host ptt-crawler:latest
```

### Check log on host /tmp folder
```
$ tail -f /tmp/ptt-crawler.log

# If success, you will see logs like the following sample
2017-09-15 06:13:59 elasticsearch INFO     POST http://192.168.10.185:9200/_bulk [status:200 request:5.788s]
2017-09-15 06:13:59 web_crawler/ptt.py INFO     Index 180/25658: 6.097028970718384 seconds
2017-09-15 06:14:44 web_crawler/ptt.py INFO     Round 181/25658: 43.48200988769531 seconds
2017-09-15 06:15:30 web_crawler/ptt.py INFO     Round 182/25658: 44.91555738449097 seconds
2017-09-15 06:16:14 web_crawler/ptt.py INFO     Round 183/25658: 41.860851764678955 seconds
2017-09-15 06:17:04 web_crawler/ptt.py INFO     Round 184/25658: 48.13930678367615 seconds
2017-09-15 06:17:57 web_crawler/ptt.py INFO     Round 185/25658: 52.328588247299194 seconds
2017-09-15 06:18:50 web_crawler/ptt.py INFO     Round 186/25658: 49.02532911300659 seconds
2017-09-15 06:19:42 web_crawler/ptt.py INFO     Round 187/25658: 51.062992095947266 seconds
2017-09-15 06:20:37 web_crawler/ptt.py INFO     Round 188/25658: 52.719457387924194 seconds
2017-09-15 06:21:22 web_crawler/ptt.py INFO     Round 189/25658: 43.51210141181946 seconds
2017-09-15 06:22:16 web_crawler/ptt.py INFO     Round 190/25658: 52.21781849861145 seconds
2017-09-15 06:23:06 web_crawler/ptt.py INFO     Round 191/25658: 48.40325427055359 seconds
2017-09-15 06:23:59 web_crawler/ptt.py INFO     Round 192/25658: 51.04237246513367 seconds
2017-09-15 06:24:52 web_crawler/ptt.py INFO     Round 193/25658: 51.39613461494446 seconds
2017-09-15 06:25:34 web_crawler/ptt.py INFO     Round 194/25658: 40.014158725738525 seconds
2017-09-15 06:26:21 web_crawler/ptt.py INFO     Round 195/25658: 46.00677728652954 seconds
2017-09-15 06:27:18 web_crawler/ptt.py INFO     Round 196/25658: 54.73074436187744 seconds
2017-09-15 06:28:09 web_crawler/ptt.py INFO     Round 197/25658: 49.2486617565155 seconds
2017-09-15 06:28:52 web_crawler/ptt.py INFO     Round 198/25658: 41.596322774887085 seconds
2017-09-15 06:29:43 web_crawler/ptt.py INFO     Round 199/25658: 49.597779750823975 seconds
2017-09-15 06:30:30 web_crawler/ptt.py INFO     Round 200/25658: 44.820817947387695 seconds
2017-09-15 06:30:35 elasticsearch INFO     POST http://192.168.10.202:9200/_bulk [status:200 request:4.946s]
```
