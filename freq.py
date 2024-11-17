import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import streamlit.components.v1 as components

# Sample text (you can change this to anything you'd like)
#text = "This is a simple example where we analyze the words in a dynamic way."
text = '''Ulysses is a modernist novel by the Irish writer James Joyce. Partially serialized in the American journal The Little Review from March 1918 to December 1920, the entire work was published in Paris by Sylvia Beach on 2 February 1922, Joyce's fortieth birthday. It is considered one of the most important works of modernist literature[3] and has been called "a demonstration and summation of the entire movement".[4]

The novel chronicles the experiences of three Dubliners over the course of a single day, 16 June 1904, which fans of the novel now celebrate as Bloomsday. Ulysses is the Latinised name of Odysseus, the hero of Homer's epic poem The Odyssey, and the novel establishes a series of parallels between Leopold Bloom and Odysseus, Molly Bloom and Penelope, and Stephen Dedalus and Telemachus. There are also correspondences with Shakespeare's Hamlet and with other literary and mythological figures, including Jesus, Elijah, Moses, Dante, and Don Giovanni.[5] Such themes as antisemitism, human sexuality, British rule in Ireland, Catholicism, and Irish nationalism are treated in the context of early 20th-century Dublin. The novel is highly allusive and written in a variety of styles.

Artist and writer Djuna Barnes quoted Joyce as saying, "The pity is . . . the public will demand and find a moral in my book—or worse they may take it in some more serious way, and on the honour of a gentleman, there is not one single serious line in it. ... In Ulysses I have recorded, simultaneously, what a man says, sees, thinks, and what such seeing, thinking, saying does, to what you Freudians call the subconscious."[6]

According to the writer Declan Kiberd, "Before Joyce, no writer of fiction had so foregrounded the process of thinking".[7] The novel's stream of consciousness technique, careful structuring, and experimental prose—replete with puns, parodies, epiphanies, and allusions—as well as its rich characterisation and broad humour have led it to be regarded as one of the greatest literary works. Since its publication, the book has attracted controversy and scrutiny, ranging from a 1921 obscenity trial in the United States to protracted disputes about the authoritative version of the text.'''
words = text.split()

# Relative frequency of letter appearance
all_letters = [letter.lower() for word in words for letter in word if letter.isalpha()]
total_letters = len(all_letters)
letter_counts = Counter(all_letters)
relative_frequency = {letter: count / total_letters for letter, count in letter_counts.items()}

# Streamlit app
st.title("Word Analysis Slider")

# User slider to pick a word index
word_index = st.slider("Select word index", min_value=0, max_value=len(words)-1, value=0)

# Update relative frequency based on current word index
analyzed_letters = [letter.lower() for word in words[:word_index + 1] for letter in word if letter.isalpha()]
total_analyzed_letters = len(analyzed_letters)
current_letter_counts = Counter(analyzed_letters)
current_relative_frequency = {letter: count / total_analyzed_letters for letter, count in current_letter_counts.items()}

# Prepare data for plotting
letters = sorted(current_relative_frequency.keys())
frequencies = [current_relative_frequency[letter] for letter in letters]

# Create columns for layout
col1, col2, col3 = st.columns(3)

# Plot relative frequency bar chart
with col1:
    st.markdown("### Relative Frequency of Letters (Up to Selected Word)")
    fig, ax = plt.subplots()
    ax.bar(letters, frequencies, color='skyblue')
    ax.set_xlabel('Letters')
    ax.set_ylabel('Relative Frequency')
    ax.set_title('Relative Frequency of Letters')
    st.pyplot(fig)

# Plot pie chart of top 10 most popular letters
with col2:
    st.markdown("### Top 10 Most Frequent Letters (Up to Selected Word)")
    top_10_letters = current_letter_counts.most_common(10)
    letters_pie, frequencies_pie = zip(*top_10_letters) if top_10_letters else ([], [])
    fig, ax = plt.subplots()
    ax.pie(frequencies_pie, labels=letters_pie, autopct='%1.1f%%', colors=plt.cm.Paired(range(len(letters_pie))))
    ax.set_title('Top 10 Letters by Frequency')
    st.pyplot(fig)

# Display top 5 most frequent words
with col3:
    st.markdown("### Top 5 Most Frequent Words:")
    word_counts = Counter([word.lower() for word in words[:word_index + 1]])
    top_5_words = word_counts.most_common(5)
    st.write(pd.DataFrame(top_5_words, columns=['Word', 'Frequency']))

# Display colored text fragment below the charts
st.markdown("### Text Fragment:")
colored_words = []
for i, word in enumerate(words):
    if i <= word_index:
        colored_words.append(f'<span style="color:blue">{word}</span>')
    else:
        colored_words.append(f'<span style="color:red">{word}</span>')
fragment_start = max(0, word_index - 3)
fragment_end = min(len(words), word_index + 4)
fragment = colored_words[fragment_start:fragment_end]
st.markdown(" ".join(fragment), unsafe_allow_html=True)
