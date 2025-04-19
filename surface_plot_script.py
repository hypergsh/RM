import pandas as pd
import plotly.graph_objects as go

# Setting the data path
data_path = 'Results_21Mar2022.csv'
df = pd.read_csv(data_path)

# Deleting Irrelevant Columns
drop_columns = [
    'sd_ghgs', 'sd_land', 'sd_watscar', 'sd_eut',
    'sd_ghgs_ch4', 'sd_ghgs_n2o', 'sd_bio', 'sd_watuse', 'sd_acid',
    'n_participants', 'grouping', 'mc_run_id'
]
df.drop(columns=[col for col in drop_columns if col in df.columns], inplace=True)

# Meat Group Name Mapping
diet_group_mapping = {
    'meat50': 'meat < 50',
    'meat': 'meat 50 - 99',
    'meat100': 'meat 100+'
}

# User input
# Optional environmental indicators (columns other than age_group, diet_group, sex)
mean_columns = [col for col in df.columns if col not in ['age_group', 'diet_group', 'sex']]
print("\nOptional environmental indicators:")
for idx, col in enumerate(mean_columns):
    print(f"{idx + 1}: {col}")

chosen_idx = int(input("Please enter the number of the environmental indicator you wish to draw (e.g. 1):")) - 1
chosen_mean = mean_columns[chosen_idx]

# Gender options
sex_options = ['All'] + sorted(df['sex'].dropna().unique())
print("\nSelectable gender options:")
for idx, sex in enumerate(sex_options):
    print(f"{idx + 1}: {sex}")

chosen_sex_idx = int(input("Please enter the number of the gender you wish to draw (e.g. 1):")) - 1
chosen_sex = sex_options[chosen_sex_idx]

# Draw 3D Surface Plot
# Filter by gender
if chosen_sex == 'All':
    filtered_df = df
else:
    filtered_df = df[df['sex'] == chosen_sex]

# Generate pivot table (with age_group as rows and diet_group as columns)
pivot_table = filtered_df.pivot_table(
    index='age_group',
    columns='diet_group',
    values=chosen_mean,
    aggfunc='mean'
)
pivot_table.rename(columns=diet_group_mapping, inplace=True)

# Constructing 3D maps
fig = go.Figure()

# Add Surface
fig.add_trace(go.Surface(
    z=pivot_table.values,
    x=pivot_table.columns,
    y=pivot_table.index,
    colorscale='Viridis',
    colorbar=dict(title=chosen_mean),
    contours={
        "z": {"show": True, "usecolormap": True, "highlightcolor": "limegreen", "project_z": True}
    }
))

# Layout settings
fig.update_layout(
    title=f'Surface Plot of {chosen_mean} by Age and Diet Group (Sex: {chosen_sex})',
    scene=dict(
        xaxis_title='Diet Group',
        yaxis_title='Age Group',
        zaxis_title=chosen_mean,
        xaxis=dict(tickangle=-45, title_font=dict(size=16)),
        yaxis=dict(title_font=dict(size=16)),
        zaxis=dict(title_font=dict(size=16))
    ),
    margin=dict(l=50, r=50, b=50, t=100),
    autosize=False,
    width=900,
    height=800,
    template="plotly_white",
)

# Show
fig.show()
