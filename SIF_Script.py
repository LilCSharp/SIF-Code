from heapq import nlargest
import re
import csv

info = []

with open("USvideos.csv", mode = 'r') as csv_file:
    csv_data = csv.DictReader(csv_file)

    for row in csv_data:
        info.append(row)

# This function gets the net amount of trending videos in the dataset
def get_sample_size(data):
    return len(data)

# This function calculates the sum of all trending videos in a category
def get_category_sum(data):
    categories = dict()

    for row in data:
        if row["category_id"] in categories:
            categories[row["category_id"]] += 1
        else:
            categories[row["category_id"]] = 1
    
    return categories

# This function determines how often a tag appears alongside a category
def relate_tag_to_category(data):
    tags_in_category = dict()
    result = dict()

    for row in data:
        tags = parse_tags(row["tags"])

        for tag in tags:
            if row["category_id"] in tags_in_category:
                if tag in tags_in_category[row["category_id"]]:
                    tags_in_category[row["category_id"]][tag] += 1
                else:
                    tags_in_category[row["category_id"]][tag] = 1
            else:
                tags_in_category[row["category_id"]] = {tag: 1}
    
    for key in tags_in_category:
        result[key] = nlargest(5, tags_in_category[key], tags_in_category[key].get)

    return result

# This returns an array of parsed tags from a string of tags
def parse_tags(tags):
    tag_list = []

    tag_list = tags.split("\"|\"")

    return tag_list

# This function creates a histogram of publishing times for the trending videos
def get_histogram_of_time(data):
    time_data = dict()

    for row in data:
        hours = re.search("T(.{2}):" , row["publish_time"])

        hour = hours.group(1)

        if hour is not None:
            if int(hour) in time_data:
                time_data[int(hour)] += 1
            else:
                time_data[int(hour)] = 1

    return nlargest(10, time_data, time_data.get)

# This function records the number of videos with all caps in the titles
def eval_clickbait(data):
    count = 0

    for row in data:
        caps = re.findall(" [A-Z]+ |^[A-Z]+ |[A-Z]+$", row["title"])

        if len(caps) > 0:
            count += 1

    return count

# This function records the number of music videos that are on trending
def get_music_vids(data):
    count = 0

    for row in data:
        title = re.findall("Official", row["title"])
        desc = re.findall("Official", row["tags"])

        if len(title) > 0 or len(desc) > 0:
            count += 1
    
    return count

# This function records the Youtubers that trend the most overall
def get_top_youtubers_overall(data):
    youtubers = dict()

    for row in data:
        if row["channel_title"] in youtubers:
            youtubers[row["channel_title"]] += 1
        else:
            youtubers[row["channel_title"]] = 1
    
    return nlargest(10, youtubers, youtubers.get)


# This function records the Youtubers that trend by category
def get_top_youtubers_categorical(data):
    categories_with_tubers = dict()
    result = dict()

    for row in data:

        if row["category_id"] in categories_with_tubers:
            if row["channel_title"] in categories_with_tubers[row["category_id"]]:
                categories_with_tubers[row["category_id"]][row["channel_title"]] += 1
            else:
                categories_with_tubers[row["category_id"]][row["channel_title"]] = 1
        else:
            categories_with_tubers[row["category_id"]] = {row["channel_title"]: 1}
    
    for key in categories_with_tubers:
        result[key] = nlargest(5, categories_with_tubers[key], categories_with_tubers[key].get)

    return result

# This function draws a correlation between posting hours and category
def get_fanbase_active_hours(data):
    active_hours = dict()
    result = dict()

    for row in data:
        hours = re.search("T(.{2}):", row["publish_time"])
        hour = hours.group(1)

        if hour is not None:
            if row["category_id"] in active_hours:
                if int(hour) in active_hours[row["category_id"]]:
                    active_hours[row["category_id"]][int(hour)] += 1
                else:
                    active_hours[row["category_id"]][int(hour)] = 1
            else:
                active_hours[row["category_id"]] = {int(hour): 1}
    
    for key in active_hours:
        result[key] = nlargest(3, active_hours[key], active_hours[key].get)

    return result

print("Sample size: ", get_sample_size(info))
print("The top ten times for trending videos being posted are: ", get_histogram_of_time(info), "\n")
print("The number of trending videos that have title verification for being official: ", get_music_vids(info), "\n")
print("The number of trending videos with all caps in the title is: ", eval_clickbait(info), "\n")
print("The most common YouTubers to trend are: ", get_top_youtubers_overall(info), "\n")
print("The most commmon posting time by category of video is: ", get_fanbase_active_hours(info), "\n")
print("The most common YouTubers to appear on trending by category are: ", get_top_youtubers_categorical(info), "\n")
print("The most common tags by category are: ", relate_tag_to_category(info), "\n")