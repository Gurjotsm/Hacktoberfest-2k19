# scrapping data from youtube trending page
import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter
try:

    req = requests.get('https://www.youtube.com/feed/trending')
    link_data = req.content
    beautiful_link_data = BeautifulSoup(link_data, 'html.parser')
    #print(link_data)
    #print(beautiful_link_data)

    watch = []
    link = []
    no_of_links = 0
    no_of_images = 0

    # loop for all video links
    for links in beautiful_link_data.find_all('a'):
        link = links.get('href')
        link = str(link)
        if link.startswith('/watch?v=') and "https://www.youtube.com" + link not in watch:
            watch.append("https://www.youtube.com" + link)
    no_of_links = len(watch)
    #for i in range(no_of_links):
    #   print(watch[i])
    #print(no_of_links)
    image_source_list = []

    # loop for all image links
    for images in beautiful_link_data.find_all('img'):
        image_source = images.get('src')
        image_source_other = images.get('data-thumb')
        if image_source != None and image_source.startswith("https://i.ytimg.com/"):
            image_source_list.append(image_source)
        if image_source_other != None and image_source_other.startswith('https://i.ytimg.com/'):
            image_source_list.append(image_source_other)
    #for z in range(len(image_source_list)):
    #    print(image_source_list[z])
    #print(len(image_source_list))

    channel_name = []
    video_title = []
    dislikes = []
    likes = []
    views = []
    video_links = []
    print("Data: ")
    for video_link in watch:
        print()
        video_links.append(video_link)
        print(video_link)
        response = requests.get(video_link)
        data = response.content
        soup = BeautifulSoup(data, 'html.parser')
        pretty_data = soup.prettify()
        #print(soup)
        #print(pretty_data)

        # loop for video title
        for title in soup.find_all('title'):
            video_title.append(title.string)
            print(title.string)
            break

        # loop for channel name
        channel_info = []
        for channel in soup.find_all('a', {'class': "yt-uix-sessionlink spf-link"}):
            channel_info.append(channel.next)
        # print(channel_info)
        if "#" in channel_info[0]:
            print(channel_info[1])
            channel_name.append(channel_info[1])
        else:
            print(channel_info[0])
            channel_name.append(channel_info[0])
        # print(len(channel_name))

        # checking views
        for link_views in soup.find_all("div", {'class': 'watch-view-count'}):
            views.append(link_views.next)
            print(link_views.next)

        # loop for checking likes
        for link_likes in soup.find_all('button'):
            link_like = link_likes.get('aria-label')
            if str(link_like).startswith("like") :
                likes.append(str(link_like).split()[5])
                print(str(link_like).split()[5] + " people liked the video! ")
                break

        # loop for checking dislikes
        for link_dislikes in soup.find_all('button'):
            link_dislike = link_dislikes.get('aria-label')
            if str(link_dislike).startswith("dislike"):
                dislikes.append(str(link_dislike).split()[5])
                print(str(link_dislike).split()[5] + " people disliked the video! ")
                break

    # downloading and creating image name
    download_img = []
    for z in range(len(image_source_list)):
        download_img.append(str(z)+".jpeg")
    key = 0
    for image in image_source_list:
        img_response = requests.get(image)
        img_content = img_response.content
        with open(download_img[key],'wb') as f:
            f.write(img_content)
            key += 1
    # writing all the data in an excel file
    df = pd.DataFrame({'Title': video_title, 'Video-Link': video_links, 'Channel': channel_name, 'Views': views, 'Likes': likes, 'DisLikes': dislikes,'Image-Link': image_source_list})
    writer = pd.ExcelWriter('youtube_data.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
except Exception as e:
    print()
    print(e)
    print("Network Error")
