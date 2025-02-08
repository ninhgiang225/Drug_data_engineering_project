import data_processing
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_recall_by_country(df):
    recall_count = df['country'].value_counts()
    recall_count.plot(kind='bar', title='Drug Recall Frequency by Country')
    plt.show()

def get_chosen_layer():
    chosen_layer_df = pd.read_sql(stmt, engine)
    print("\n", chosen_layer_df)