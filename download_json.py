import sys
import json
import requests

def create_session(username, password):
    url = "https://bsky.social/xrpc/com.atproto.server.createSession"
    headers = { 
            "Content-Type": "application/json"
            }
    post_data = {
            "identifier": username,
            "password": password
            }
    response = requests.post(url, headers=headers, json = post_data)
    accessJwt = response.json()['accessJwt']
    return accessJwt

def download_post(uri, accessJwt):
    url = "https://bsky.social/xrpc/app.bsky.feed.getPostThread"
    headers = {
            "Authorization": "Bearer " + accessJwt,
            "Content-Type": "application/json"
            }

    params = {
            "uri": uri,
            "depth": "10"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Headers with Authorization Token
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"
}


def download_feed(accessJwt):
    feed_list = []
    url ="https://bsky.social/xrpc/app.bsky.feed.getFeed?feed=at://did:plc:vpkhqolt662uhesyj6nxm7ys/app.bsky.feed.generator/devfeed&limit=100&cursor="
    headers = {
            "Authorization": "Bearer " + accessJwt,
            "Content-Type": "application/json"
            }
    response = requests.get(url, headers = headers)
    for item in response.json()['feed']:
        post_with_replies = download_post(item['post']['uri'], accessJwt)
        feed_list.append(post_with_replies)
    cursor = response.json()['cursor']
    for i in range (0, 20):
        cursored_url = url + cursor
        response = requests.get(cursored_url, headers = headers)
        cursor = response.json()['cursor']
        for item in response.json()['feed']:
            post_with_replies = download_post(item['post']['uri'], accessJwt)
            feed_list.append(post_with_replies)

    return {"feed": feed_list}


if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    accessJwt = create_session(username, password)
    feed = download_feed(accessJwt)
    with open('input.json', 'w') as f:
        json.dump(feed, f, indent=4)
