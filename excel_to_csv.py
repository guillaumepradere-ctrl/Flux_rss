import pandas as pd

# Load the Excel file
df = pd.read_excel(r'C:\Developpement\Flux_rss\Comment.xlsx')

# Save as CSV in the same folder
df.to_csv(r'C:\Developpement\Flux_rss\Comment.csv', index=False)