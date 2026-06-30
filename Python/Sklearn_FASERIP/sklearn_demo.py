import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sklearn as skl
from sklearn.ensemble import IsolationForest
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


heroes = pd.read_csv("../FASERIP.csv")

stats_table = heroes[['F','A','S','E','R','I','P']]


tab1, tab2, tab3, tab4, tab5 = st.tabs(["KMeans clustering", "Cluster Graph", "Decision tree", "Isolation forrest", "Nearest neighbour"])

model = KMeans(n_clusters=4, random_state=42, n_init=10)
model.fit(stats_table)

heroes['Cluster'] = model.labels_


# decision tree


#note that we need a series here, not a dataframe. Hence only one pair of brackets
type_table = heroes['Type']


# Create the tree, but limit how deep it can go (3 or 4 is usually a sweet spot for reading)
tree_model = DecisionTreeClassifier(max_depth=3, random_state=42)

# Teach the tree using your stats (X) and the answers (y)
tree_model.fit(stats_table, type_table)


# Isolation forrest
# Create the forest. 
# 'contamination=0.05' tells it: "Roughly 5% of my data is weird, go find them."
iso_forest = IsolationForest(contamination=0.05, random_state=42)

# Train it on just the stats
iso_forest.fit(stats_table)

# Ask the forest for its verdict on every character
verdicts = iso_forest.predict(stats_table)

# Add the verdicts as a new column in your heroes dataframe
heroes['Anomaly'] = verdicts

# Create a new dataframe that ONLY contains the -1s (the weirdos)
weirdos = heroes[heroes['Anomaly'] == -1]
X_Scaled = StandardScaler().fit_transform(stats_table)

knn = NearestNeighbors(n_neighbors=6, algorithm='ball_tree')
knn.fit(X_Scaled)

with tab1:
    num_clusters = heroes['Cluster'].nunique()
    # Create columns that split the screen equally
    my_columns = st.columns(num_clusters)

    # Loop through the columns and drop data into each
    for i, col in enumerate(my_columns):
        with col:
            st.header(f"Group {i}")
            cluster_heroes = heroes[heroes['Cluster'] == i]
            
            # Just print out a list of the names to keep it tidy
            for name in cluster_heroes['character']: # <-- Make sure 'Name' matches your column!
                st.write(f"• {name}")

with tab2:
        
    # Create the chart using matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(heroes['F'], heroes['S'], c=heroes['Cluster'], cmap='viridis', s=50)
    
    ax.set_xlabel('Fighting')
    ax.set_ylabel('Strength')
    ax.set_title('Marvel Characters Clustered by Stats')
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Add a legend for the colors
    legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
    ax.add_artist(legend1)
    
    # THE STREAMLIT MAGIC TRICK:
    # Instead of plt.show(), you pass the figure to Streamlit!
    st.pyplot(fig)

# ==========================================
    # TAB 3: The Decision Tree Drawing
    # ==========================================
with tab3:
    st.header("How Does the Tree Decide?")
    
    # Create a large canvas for the tree so the text isn't squished
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Draw the tree!
    plot_tree(
        tree_model, 
        feature_names=stats_table.columns,      # Uses your F, A, S, E, R, I, P labels
        class_names=tree_model.classes_, # Uses your actual Type names (e.g., Mutant, Alien)
        filled=True,                  # Colors the boxes based on the dominant class
        rounded=True,                 # Makes the boxes look nice
        ax=ax                         # Tells it to draw on the canvas we made
    )
    
    # Hand the canvas over to Streamlit
    st.pyplot(fig)

    st.subheader("Test a Custom Character!")

    # Let's invent "Star-Girl": 
    # High Strength (60), but terrible everything else
    custom_stats = [[20, 20, 10, 40, 10, 10, 40]] 
    
    # Ask the tree to predict!
    prediction = tree_model.predict(custom_stats)
    
    # Show the result in Streamlit
    st.write(f"The tree predicts this character is a: **{prediction[0]}**")

with tab4:
    st.header("The 5% Anomalies")
    st.write("The Isolation Forest identified these characters as having the most statistically bizarre stat distributions in the Marvel universe.")
    
    # We only want to show the weirdos, and let's drop the 'Anomaly' column 
    # (-1 is just code for "weirdo", no need to show the user that)
    weirdos_display = weirdos[['character', 'F', 'A', 'S', 'E', 'R', 'I', 'P']]
    
    # Display them as a nice, clean table
    st.dataframe(weirdos_display, use_container_width=True)
    
    # A little fun Streamlit formatting
    st.caption("Note: Being an 'anomaly' doesn't mean bad. It just means no one else in the data has a stat block shaped quite like theirs!")



# ==========================================
# TAB 5: The Statistical Twins (KNN)
# ==========================================
with tab5:
    st.header("Find Statistical Twins")
    st.write("Pick a hero. The algorithm will find the 5 characters with the most mathematically similar FASERIP stat blocks.")
    
    # 1. Create a dropdown of all character names
    selected_hero = st.selectbox("Choose a character:", heroes['character'].tolist())
    
    # 2. Find the row number (index) of the selected hero
    hero_index = heroes[heroes['character'] == selected_hero].index[0]

    # 3. Ask KNN for the 6 closest points to that hero's scaled stats
    distances, indices = knn.kneighbors([X_Scaled[hero_index]])
    
    # 4. The first result (index 0) is always the hero themselves. We slice to skip them.
    twin_indices = indices[0][1:] 
    
    # 5. Look up the actual names of those twins
    twin_names = heroes.iloc[twin_indices]['character'].tolist()
    
    # 6. Show the results!
    st.subheader(f"If you like {selected_hero}, you might also like:")
    for name in twin_names:
        st.write(f"🧬 {name}")