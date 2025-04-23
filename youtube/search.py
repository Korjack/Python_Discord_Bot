import urllib.parse
import urllib.request
import json
import re

def get_video_dict(keyword, max_results=10):
    query = urllib.parse.quote_plus(keyword)
    url = f"https://www.youtube.com/results?search_query={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')

    match = re.search(r"var ytInitialData = ({.*?});</script>", html, re.DOTALL)
    if not match:
        return {}

    data = json.loads(match.group(1))
    results = {}

    try:
        sections = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
        for section in sections:
            for content in section.get("itemSectionRenderer", {}).get("contents", []):
                video = content.get("videoRenderer")
                if not video:
                    continue

                title = video.get("title", {}).get("runs", [{}])[0].get("text", "제목 없음")
                video_id = video.get("videoId")
                url = f"https://www.youtube.com/watch?v={video_id}"

                duration_str = video.get("lengthText", {}).get("simpleText", "0:00")
                parts = duration_str.split(":")
                if len(parts) == 2:
                    duration = int(parts[0]) * 60 + int(parts[1])
                elif len(parts) == 3:
                    duration = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                else:
                    duration = 0

                results[title] = [url, duration]

                if len(results) >= max_results:
                    return results
    except Exception as e:
        print("에러 발생:", e)

    return results
