import Post_Scraper
import post_preprocessor
import csv
from io import StringIO

people = {'anthony': [0, 1579064061],
          'alex': [1, 1575158399],
          'edward': [2, 1572566399],
          'lucien': [3, 1569887999],
          'nicole': [4, 1567295999],
          'sebastian': [5, 1564531199],
          '': [6, 1562025599]}


def getlines(text, width):
    if len(text) <= width:
        return text
    pos = width
    for i in range(width, 0, -1):
        if text[i] == ' ':
            pos = i
            break
    return text[0:pos] + "\n" + getlines(text[pos+1:], width)


name = input("Enter your first name: ").lower()
last_date = people[name][1]
keyList = list(people.keys())
first_date = people[keyList[people[name][0] + 1]][1]
posts, last_date = Post_Scraper.get_posts(num_posts=-1, last_date=last_date, first_date=first_date)

OUTPUT_FILE = name + "flaired.csv"

try:
    with open(OUTPUT_FILE, 'r') as file1:
        lines = file1.readlines()
        if len(lines):
            last_id = list(csv.reader(StringIO(lines[-1]), delimiter=','))[0][0]
            for i in range(0, len(posts)):
                if posts[i]['id'] == last_id:
                    break
            posts = posts[i:]
except FileNotFoundError:
    1  # I don't know what I'm doing, this works but probably isn't the way to do it

print("You have %d posts waiting to be classified\n\n" % len(posts))
File = open(OUTPUT_FILE, 'a')

# put the start utc time in front of file.
File.write("%s,%s\n" % (posts[0]['id'], posts[0]['created_utc']))

flairs = ['Academic Life', 'Discussion', 'Employment', 'General Question', 'Humor', 'Image', 'IV/Goleta/SB', 'News',
          'Social Life', 'Incoming Students', 'Course Questions']
count = 0

for post in posts:
    if not post_preprocessor.__valid_post(post['selftext']):
        continue

    print("------------------------------------------------------------------\n" + post['title'])
    print(getlines(post['selftext'], 60))
    print()
    for i in range(len(flairs)):
        print(" %d %s" % (i + 1, flairs[i]))
    value = int(input("Input your value (-1 for skip, 0 to end): "))

    if value == -1:
        continue
    if value == 0:
        File.write("%s,%d\n" % (post['id'], post['created_utc']))
        break

    File.write("%s,%s,%s\n" % (post['id'], post['created_utc'], flairs[value - 1]))
    count += 1

File.close()

print("\n\nYou identified %d posts! %d remaining" % (count, len(posts) - count))
