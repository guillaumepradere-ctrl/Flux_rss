import pandas as pd

# Load the Excel file
df = pd.read_excel(r"C:\Users\g.pradere\NEWHEAT\00_EXPLOITATION - Documents\General\231218_Exploit_Suivi_Centrales.xlsm", sheet_name='Form1')

# Save as CSV in the same folder
df.to_csv(r'C:\Developpement\Flux_rss\Comment.csv', index=False)