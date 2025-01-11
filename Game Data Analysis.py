# Import Libraries (LIBRARY)
import pandas as pd
import matplotlib.pyplot as plt

# Define data files
filename_1 = 'bgg_Game_Category.csv'
filename_2 = 'bgg_Game_EIements.csv'

# -------- MAIN Program starts here

# Start Program: Input prompt for name and category
name = input("Hello, what's your name?\n")
response = input(f"Hi {name}! Do you want to know how many games of these topics are published per year? (type yes or no)\n")

# (DECISION)
if response.lower() != 'yes':
    print("Okay, nice to meet you anyway! Bye!")
else:
    try:
        # Load category data by reading 'bgg_Game_Category.csv' (READ DATA)
        categories_def = pd.read_csv(filename_1)
        print("Available topics:")

        # Display the topics as a numbered list (LOOP: Explanation: This for loop iterates over the list of category names (categories_def['category_name']) and prints each topic with a corresponding index.)
        for index, topic in enumerate(categories_def['category_name'], start=1):
            print(f"{index}. {topic}")

        # Prompt user for category number
        category_number = input("Enter the number corresponding to a topic from the list!\n")

        # Validate category number (DECISION)
        if not category_number.isdigit() or int(category_number) < 1 or int(category_number) > len(categories_def):
            print("Invalid category number not found. Please restart and select a valid topic.")
        else:
            category_number = int(category_number)
            category_name = categories_def.iloc[category_number - 1]['category_name']
            category_code = categories_def.iloc[category_number - 1]['category_code']

            # Read game data (READ DATA)
            game_elements_def = pd.read_csv(filename_2)

            # Split 'category_code' column and filter rows where the category_code matches
            game_elements_def['category_code'] = game_elements_def['category_code'].astype(str)
            filtered_data = game_elements_def[game_elements_def['category_code'].str.contains(f'(^|,){category_code}(,|$)', na=False)]

            # (DECISION)
            if filtered_data.empty:
                print(f"No games found for the category '{category_name}'.")
            else:
                # Convert year to numeric and sort
                filtered_data['year'] = pd.to_numeric(filtered_data['year'], errors='coerce')  # Convert to numeric
                filtered_data = filtered_data.dropna(subset=['year'])  # Drop rows with invalid years
                filtered_data['year'] = filtered_data['year'].astype(int)  # Convert valid years to int

                # Calculate games published per year (ARRAY)
                games_per_year = filtered_data.groupby('year').size().sort_index()  # Sort by year
                total_games = games_per_year.sum()

                # Print data
                print("Games published per year:")
                print("\n".join([f"- {year}: {count} games" for year, count in games_per_year.items()]))
                print(f"Total games published: {total_games} games")

                # Visualize Data (DIAGRAM)
                plt.figure(figsize=(12, 8))
                bars = plt.bar(games_per_year.index, games_per_year.values, color='skyblue', edgecolor='blue')

                # Add a title and labels
                plt.title(f"Games Published Per Year: {category_name}", fontsize=18, fontweight='bold')
                plt.xlabel("Year", fontsize=12)
                plt.ylabel("Number of Games", fontsize=12)

                # Add grid lines
                plt.grid(axis='y', linestyle='--', alpha=0.7)

                # Set x-axis ticks and labels
                plt.xticks(ticks=games_per_year.index, labels=games_per_year.index, fontsize=5, rotation=45)

                # Annotate the bar chart with values
                for bar in bars:
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom', fontsize=5, color='black')

                # Customize tick parameters
                plt.yticks(fontsize=5)

                # Add a tight layout for better spacing
                plt.tight_layout()

                # Show the chart
                plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")
        exit()
