import requests
import streamlit as st
from PIL import Image

def search_books(title):
    url = f'http://openlibrary.org/search.json?q={title}&limit=5'
    response = requests.get(url)
    data = response.json()
    return data['docs']

def get_similar_books(book):
    genre = book.get('subject', [''])[0]

    # Search for books with the same genre using Open Library API
    url = f'http://openlibrary.org/search.json?subject={genre}&limit=5'
    response = requests.get(url)
    data = response.json()
    books = data.get('docs', [])

    return books

def add_background_image():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.guim.co.uk/img/media/5ab8e74575b394c8380b7eb9f88cef51c4422237/0_0_4134_3223/master/4134.jpg?width=700&quality=85&auto=format&fit=max&s=2dd3bf81932f3024ad1e0db37c3ce094");
             background-attachment: fixed;
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def main():
    add_background_image()
    st.title('📚 Book Recommendation App')
    st.write('This is a simple app to search for books and get recommendations')
    st.write('Enter your favorite book and the app will recommend similar books')

    user_favorite_book = st.text_input('Enter your favorite book: ')

    if user_favorite_book:
        books = search_books(user_favorite_book)
        if books:
            book = books[0]  # Only consider the first book
            st.write('Title:', book.get('title', 'N/A'))
            st.write('Author:', book.get('author_name', ['N/A'])[0])
            st.write('Publish Year:', book.get('first_publish_year', 'N/A'))

            user_book_cover_url = f"http://covers.openlibrary.org/b/id/{book['cover_i']}-L.jpg"
            user_book_cover = Image.open(requests.get(user_book_cover_url, stream=True).raw)
            st.image(user_book_cover, caption='Book Cover', width=300)

            similar_books = get_similar_books(book)
            if similar_books:
                st.write('Similar Books:')

                # Apply CSS styling for the grid-like layout
                st.markdown(
                    """
                    <style>
                    .book-grid-container {
                        display: flex;
                        flex-wrap: wrap;
                        justify-content: space-evenly;
                        gap: 20px;
                    }
                    .book-grid-item {
                        text-align: center;
                        width: 300px;
                    }
                    .book-grid-item img {
                        object-fit: cover;
                        width: 100%;
                        height: 400px;
                    }
                    .book-grid-item hr {
                        margin-top: 10px;
                        margin-bottom: 10px;
                        border: none;
                        border-top: 1px solid #ddd;
                    }
                    .book-details {
                        padding-top: 10px;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Create a container for the grid layout
                st.markdown('<div class="book-grid-container">', unsafe_allow_html=True)

                for similar_book in similar_books:
                    st.markdown('<div class="book-grid-item">', unsafe_allow_html=True)

                    # Display book details at the top
                    st.markdown('<div class="book-details">', unsafe_allow_html=True)
                    st.write('Title:', similar_book.get('title', 'N/A'))
                    st.write('Author:', similar_book.get('author_name', ['N/A'])[0])
                    st.write('Publish Year:', similar_book.get('first_publish_year', 'N/A'))
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Display book cover
                    similar_book_cover_url = f"http://covers.openlibrary.org/b/id/{similar_book['cover_i']}-L.jpg"
                    similar_book_cover = Image.open(requests.get(similar_book_cover_url, stream=True).raw)
                    similar_book_cover = similar_book_cover.resize(user_book_cover.size)
                    st.image(similar_book_cover, caption=similar_book.get('title', 'N/A'), width=300)

                    # Add horizontal line after each book
                    st.markdown('<hr>', unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.write('No similar books found.')
        else:
            st.write('No book found with the given title.')

if __name__ == '__main__':
    main()
