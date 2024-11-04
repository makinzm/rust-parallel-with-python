import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

# CSV file path (assuming you have saved it already)
csv_file = 'only_python_execution_times.csv'

# Load the CSV file using polars
df = pl.read_csv(csv_file)

# Extract unique task sizes
task_sizes = df['Task Size (n)'].unique().to_list()

# Set up the grid for histograms, one for each task size
sns.set(style="whitegrid")
fig, axes = plt.subplots(len(task_sizes), 1, figsize=(10, 6 * len(task_sizes)), sharex=True)

# Plot histograms of execution times for each task size
for i, n in enumerate(task_sizes):
    ax = axes[i]
    subset = df.filter(pl.col('Task Size (n)') == n)
    
    # Plot histograms for each method's execution time
    sns.histplot(subset.filter(pl.col('Method') == 'Sequential')['Execution Time (s)'], 
                 bins=30, color='blue', alpha=0.5, label='Sequential', ax=ax)
    sns.histplot(subset.filter(pl.col('Method') == 'ThreadPoolExecutor')['Execution Time (s)'], 
                 bins=30, color='green', alpha=0.5, label='ThreadPoolExecutor', ax=ax)
    sns.histplot(subset.filter(pl.col('Method') == 'Multiprocessing')['Execution Time (s)'], 
                 bins=30, color='orange', alpha=0.5, label='Multiprocessing', ax=ax)
    
    # Set title and labels for the current subplot
    ax.set_title(f'Task Size (n) = {n}')
    ax.set_xlabel('Execution Time (s)')
    ax.set_ylabel('Frequency')
    ax.legend()

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig('only_python_execution_times_histograms.png')
plt.show()

# Create scatter plot comparing methods by task size
plt.figure(figsize=(10, 6))

# Sequential execution times
plt.scatter(df.filter(pl.col('Method') == 'Sequential')['Task Size (n)'], 
            df.filter(pl.col('Method') == 'Sequential')['Execution Time (s)'], 
            color='blue', alpha=0.5, label='Sequential')

# ThreadPoolExecutor execution times
plt.scatter(df.filter(pl.col('Method') == 'ThreadPoolExecutor')['Task Size (n)'], 
            df.filter(pl.col('Method') == 'ThreadPoolExecutor')['Execution Time (s)'], 
            color='green', alpha=0.5, label='ThreadPoolExecutor')

# Multiprocessing execution times
plt.scatter(df.filter(pl.col('Method') == 'Multiprocessing')['Task Size (n)'], 
            df.filter(pl.col('Method') == 'Multiprocessing')['Execution Time (s)'], 
            color='orange', alpha=0.5, label='Multiprocessing')

# Add labels and title
plt.xlabel('Task Size (n)')
plt.ylabel('Execution Time (s)')
plt.title('Execution Time by Task Size and Method')
plt.legend()

# Save and show the scatter plot
plt.savefig('only_python_execution_times_comparison.png')
plt.show()

