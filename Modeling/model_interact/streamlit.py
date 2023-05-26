import streamlit as st
'Would you like to make a Movie or TV Show?'
movie = st.checkbox('Movie')
show = st.checkbox('Show')

if movie:
    option = st.selectbox(
    'Select the Genre of your Movie',
    ('Comedy', 'Romantic', 'Action'))
    'Would you like to assign a director or give an average score?'
    director = st.checkbox('Director')
    if director:
        dir_select = st.selectbox(
        'Select a Director',
        ('James Cameron','Wes Anderson','Christopher Nolan'))
        st.write('You selected:', dir_select,'as your director')
    else: 
        score  = st.slider(
    "Average Score of the Director?", 0, 100, 50)
    cast = st.checkbox('Cast')
    if cast: 
        'Select your cast members.'
        cast_select = st.multiselect(
        'Select your cast members',
        ['Charlie Day', 'Alexandra Daddario','Tom Cruise', 'Jason Segel', 'Ryan Reynolds'])

        st.write('You selected:', cast_select)
    else:
                score  = st.slider(
    "Average Score of the Cast?", 0, 100, 50)

    
if show:
    option = st.selectbox(
    'Select the Genre of your Show',
    ('Comedy', 'Romantic', 'Action'))
    'Would you like to assign a director or give an average score?'
    director = st.checkbox('Director')
    if director:
        dir_select = st.selectbox(
        'Select a Director',
        ('James Cameron','Wes Anderson','Christopher Nolan'))
        st.write('You selected:', dir_select,'as your director')
    else: 
        score  = st.slider(
    "Average Score of the Director?", 0, 100, 50)
    'Would you like to select cast members or give an average score?'
    cast = st.checkbox('Cast')
    if cast: 
        'Select your cast members.'
        cast_select = st.multiselect(
        'Select your cast members',
        ['Charlie Day', 'Alexandra Daddario','Tom Cruise', 'Jason Segel', 'Ryan Reynolds'])

        st.write('You selected:', cast_select)
    else:
                score  = st.slider(
    "Average Score of the Cast?", 0, 100, 50)

