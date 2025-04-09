# import sqlite3
# import matplotlib.pyplot as plt
# import re

# db_file = "brand_data.db"

# def get_data_from_db():
#     try:
#         conn = sqlite3.connect(db_file)
#         cursor = conn.cursor()
#         cursor.execute("SELECT title, rank, networth FROM scraped_data")
#         return cursor.fetchall()
#     except sqlite3.Error as e:
#         print("Database error: {e}")
#         return []
#     finally:
#         conn.close()


# def parse_networth(networth):
#     net_pattern = r"\$([\d\.]+)\s*(Billion|Million)?"
#     match = re.search(net_pattern, networth)
#     if match:
#         number = float(match.group(1))
#         unit = match.group(2)
#         if unit:
#             if unit in ["Million"]:
#                 number /= 1000  # put into billions
#             elif unit in ["Billion"]:
#                 pass  # if already in billions
#         return number
#     return None

# def clean_data(data):
#     cleaned = []
#     for title, rank, networth in data:
#         try:
#             rank_num = int(''.join(filter(str.isdigit, rank)))
#             networth_val = parse_networth(networth)
#             if networth_val is not None:
#                 cleaned.append((title, rank_num, networth_val))
#         except ValueError:
#             continue
#     return cleaned


# def plot_data(data_list):
#     if not data_list:
#         print("No data to plot")
#         return

#     data_list = sorted(data_list, key=lambda x: x[1])  # confirm sorted by rank
#     titles = [item[0] for item in data_list]
#     net_worths = [item[2] for item in data_list]

#     plt.figure(figsize=(12, 6))
#     plt.barh(titles, net_worths, color='blue')
#     plt.xlabel('Net Worth (billions)')
#     plt.title('Makeup Brand Net Worth by Rank')
#     plt.tight_layout()
#     plt.gca().invert_yaxis()  # highest rank at the top
#     plt.show()


# raw_data = get_data_from_db()
# cleaned_data = clean_data(raw_data)
# plot_data(cleaned_data)


            

