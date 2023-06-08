import os
import sys

from tqdm import tqdm
import time
from spider import hotTopic, analyse, hotSearch, topicDetail

if __name__ == '__main__':
    os.chdir("E:\myCodes\weibo\spider")
    count = 1
    while True:

        print(f"-------------------第{count}次执行开始-------------------")
        start = time.time()

        hotTopic.run()
        topicDetail.run()
        hotSearch.run()
        # searchTrend.run()
        analyse.run()

        end = time.time()
        print("用时：", end - start)
        print(f"-------------------第{count}次执行结束-------------------")

        count += 1
        for batch in tqdm(range(100), total=100, position=0, file=sys.stdout, desc="Waiting", colour="yellow"):
            time.sleep(3)
