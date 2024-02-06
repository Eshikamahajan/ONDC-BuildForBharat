import pandas as pd

df=pd.read_csv('DeliveryPointsGenAI.csv')
print(df.head(25))


# Combine "Destination" and "City" into a new column "FullDestination"
df['FullDestination'] = df['Destination'] + ', ' + df['City']

# Display the modified DataFrame
print("DataFrame with Combined Destination:")
print(df[['DeliveryAgencyID', 'AgencyName', 'Source', 'FullDestination', 'AverageDeliveryTime', 'DeliveryRating', 'DeliveryCharges', 'OrderID']].head())

# Basic Analysis Examples:
# 1. Average Delivery Time Analysis
average_delivery_time = df['AverageDeliveryTime'].mean()
print("\nAverage Delivery Time across all agencies:", average_delivery_time)

# 2. Delivery Rating Analysis
average_delivery_rating = df['DeliveryRating'].mean()
print("Average Delivery Rating across all agencies:", average_delivery_rating)

# 3. Delivery Charges Analysis
average_delivery_charges = df['DeliveryCharges'].mean()
print("Average Delivery Charges across all agencies:", average_delivery_charges)

# 4. Destination-wise Analysis
destination_analysis = df.groupby('FullDestination').agg({
    'AverageDeliveryTime': 'mean',
    'DeliveryRating': 'mean',
    'DeliveryCharges': 'mean'
}).reset_index()
print("\nDestination-wise Analysis:")
print(destination_analysis)

# You can perform additional analyses based on your specific goals and questions.




















# import numpy as np

# # Set seed for reproducibility
# np.random.seed(42)

# # Generate sample data
# n_rows = 100
# agencies = ['Dunzo', 'Uber Eats', 'Delivery Express', 'Zomato', 'Swiggy', 'Foodpanda', 'Postmates', 'Grubhub', 'Instacart', 'DoorDash']
# sources = ['Point A'] * n_rows
# destinations = ['Mukherjee Nagar, New Delhi', 'Chandni Chowk, New Delhi', 'Connaught Place, New Delhi', 'Saket, New Delhi',
#                 'Karol Bagh, New Delhi', 'Lajpat Nagar, New Delhi', 'Rajouri Garden, New Delhi', 'Hauz Khas, New Delhi',
#                 'South Extension, New Delhi', 'Paharganj, New Delhi'] * (n_rows // 10)
# average_delivery_time = np.random.randint(15, 60, n_rows)
# delivery_rating = np.random.uniform(3.5, 5.0, n_rows)
# delivery_charges = np.random.uniform(50, 200, n_rows)
# order_ids = np.arange(1, n_rows + 1)

# # Create DataFrame
# data = {'DeliveryAgencyID': np.random.randint(1, 1000, n_rows),
#         'AgencyName': np.random.choice(agencies, n_rows),
#         'Source': sources,
#         'Destination': np.random.choice(destinations, n_rows),
#         'AverageDeliveryTime': average_delivery_time,
#         'DeliveryRating': delivery_rating,
#         'DeliveryCharges': delivery_charges,
#         'OrderID': order_ids}

# df = pd.DataFrame(data)

# # Display the DataFrame
# print(df.head())

# # df.to_csv("Delivery_random.csv")
