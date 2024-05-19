import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# Sample data: replace this with your actual latitude and longitude data
def kMeans(data):
    plt.close("all")
    # Convert the data to a numpy array
    coordinates = np.array(data)
    
    # Determine the range of k values to test
    max_k = len(data)  # Maximum number of clusters should be <= number of data points
    k_range = range(2, max_k)  # Adjusted range to avoid errors
    
    # Elbow Method
    inertia = []
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=0)
        kmeans.fit(coordinates)
        inertia.append(kmeans.inertia_)
    
    plt.figure(figsize=(10, 5))
    plt.plot(k_range, inertia, 'bx-')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal k')
    
    # Silhouette Score Method
    silhouette_scores = []
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=0)
        labels = kmeans.fit_predict(coordinates)
        score = silhouette_score(coordinates, labels)
        silhouette_scores.append(score)
    
    plt.figure(figsize=(10, 5))
    plt.plot(k_range, silhouette_scores, 'bx-')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score for Optimal k')
    
    # Find the optimal number of clusters based on the highest silhouette score
    optimal_k = k_range[np.argmax(silhouette_scores)]
    print(f"Optimal number of clusters: {optimal_k}")
    
    # Perform K-means clustering with the optimal number of clusters
    kmeans = KMeans(n_clusters=optimal_k, random_state=0)
    labels = kmeans.fit_predict(coordinates)
    centers = kmeans.cluster_centers_
    
    print("Cluster centers:", centers)
    
    # Output the clusters
    clusters = {i: [] for i in range(optimal_k)}
    for idx, label in enumerate(labels):
        clusters[label].append(data[idx])

    # Optional: Visualize the clustering result
    plt.figure(figsize=(10, 5))
    plt.scatter(coordinates[:, 0], coordinates[:, 1], c=labels, cmap='viridis', marker='o')
    plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='x')  # Cluster centers
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('K-means Clustering of Latitude and Longitude')
    return centers