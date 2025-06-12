import streamlit as st
import requests

# 검색
def search_artworks(query):
    url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    params = {"q": query}
    response = requests.get(url, params=params)
    return response.json().get("objectIDs", [])[:10]

# 상세정보
def get_artwork_details(object_id):
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    return requests.get(url).json()

# UI
st.title("🎨 Explore Artworks with MET Museum API")
query = st.text_input("Search for Artworks:")
if query:
    ids = search_artworks(query)
    for object_id in ids:
        data = get_artwork_details(object_id)
        st.subheader(data["title"])
        st.image(data.get("primaryImageSmall"), width=300)
        st.write(f"Artist: {data.get('artistDisplayName')}")
        st.write(f"Year: {data.get('objectDate')}")
