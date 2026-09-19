import urllib.request
from bs4 import BeautifulSoup
import json
import os
import sys

URL = 'https://suseovilladegd.com/'
STATE_FILE = 'popup_state.json'

def get_popups():
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    slides_container = soup.find(id='popup-slides')
    
    if not slides_container:
        print("Popup slides container not found.")
        return []
    
    popups = []
    slides = slides_container.find_all('div', class_='swiper-slide')
    for slide in slides:
        a_tag = slide.find('a')
        img_tag = slide.find('img')
        
        link = a_tag['href'] if a_tag and 'href' in a_tag.attrs else ''
        img = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ''
        
        start = slide.get('data-start', '')
        end = slide.get('data-end', '')
        
        popups.append({
            'link': link,
            'image': img,
            'start': start,
            'end': end
        })
        
    return popups

def main():
    current_popups = get_popups()
    if current_popups is None:
        sys.exit(1)
        
    print(f"Found {len(current_popups)} popups.")
    
    # Load previous state
    previous_popups = []
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            try:
                previous_popups = json.load(f)
            except json.JSONDecodeError:
                pass

    if current_popups != previous_popups:
        print("Changes detected in popups!")
        
        # Save new state
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(current_popups, f, ensure_ascii=False, indent=2)
            
        # Export GITHUB_OUTPUT for next steps in GitHub Actions
        if 'GITHUB_OUTPUT' in os.environ:
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                f.write(f"changed=true\n")
        
        # Prepare a markdown message
        message = "🚨 **수서 빌라드지디 팝업 변경 감지!** 🚨\n\n"
        message += "새로운 팝업 목록이 업데이트되었습니다:\n\n"
        for idx, p in enumerate(current_popups, 1):
            message += f"### 팝업 {idx}\n"
            message += f"- **시작일**: {p['start']}\n"
            message += f"- **종료일**: {p['end']}\n"
            message += f"- **연결 링크**: {p['link']}\n"
            message += f"- **이미지**: ![{idx}]({p['image']})\n\n"
            
        with open('message.md', 'w', encoding='utf-8') as f:
            f.write(message)
            
    else:
        print("No changes detected.")
        if 'GITHUB_OUTPUT' in os.environ:
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                f.write(f"changed=false\n")

if __name__ == '__main__':
    main()
