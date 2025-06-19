import streamlit as st
import requests

def search_artworks(query):
    url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    params = {"q": query}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("objectIDs", [])[:10]
    except:
        return []

def get_artwork_details(object_id):
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return None

st.title("🎨 Explore Artworks with MET Museum API")
query = st.text_input("Search for Artworks:")

if query:
    ids = search_artworks(query)
    if not ids:
        st.warning("검색 결과가 없습니다.")
    else:
        for object_id in ids:
            data = get_artwork_details(object_id)
            if data:
                # 제목 표시
                title = data.get("title", "제목 없음")
                st.subheader(title)
                
                # 이미지 안전하게 표시
                image_url = data.get("primaryImageSmall")
                if image_url:
                    try:
                        st.image(image_url, width=300, caption=title)
                    except Exception as e:
                        st.error(f"이미지를 불러올 수 없습니다: {title}")
                else:
                    st.info("이미지가 없습니다.")
                
                # 작품 정보
                artist = data.get('artistDisplayName', '작가 미상')
                year = data.get('objectDate', '연도 미상')
                
                st.write(f"**작가**: {artist}")
                st.write(f"**연도**: {year}")
                st.divider()  # 구분선 추가
