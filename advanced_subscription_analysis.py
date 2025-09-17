import duckdb
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Connect to database
conn = duckdb.connect('trail_trekker.db')

print("=== ADVANCED SUBSCRIPTION ANALYSIS ===\n")

# Load comprehensive data with all joins
query = """
SELECT
    s.subscription_id,
    s.customer_id,
    s.plan_id,
    s.subscription_start_date as start_date,
    s.subscription_end_date as end_date,
    s.status,
    c.username,
    c.email,
    c.first_name,
    c.last_name,
    c.profile_created_date,
    p.plan_name,
    p.price,
    s.billing_cycle
FROM subscriptions s
JOIN customers c ON s.customer_id = c.customer_id
JOIN plans p ON s.plan_id = p.plan_id
"""

df = conn.execute(query).fetchdf()
print(f"Loaded {len(df)} subscription records")

# Convert dates (handle NULL values)
df['start_date'] = pd.to_datetime(df['start_date'])
df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
df['profile_created_date'] = pd.to_datetime(df['profile_created_date'], errors='coerce')

# Convert price to numeric (handle NULL values)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Calculate subscription duration and other metrics
df['subscription_duration_days'] = (df['end_date'] - df['start_date']).dt.days
df['subscription_duration_days'] = df['subscription_duration_days'].fillna(
    (datetime.now() - df['start_date']).dt.days
)

# Identify repeat customers
customer_subscription_counts = df.groupby('customer_id').size().reset_index(name='subscription_count')
df = df.merge(customer_subscription_counts, on='customer_id')
df['is_repeat_customer'] = df['subscription_count'] > 1

print("\n=== PLAN SUCCESS RATIOS ===")

# 1. Retention Rate by Plan
retention_by_plan = df.groupby('plan_name').agg({
    'status': lambda x: (x == 'active').sum() / len(x),
    'subscription_duration_days': 'mean',
    'price': 'first',
    'customer_id': 'count'
}).round(3)

retention_by_plan.columns = ['retention_rate', 'avg_duration_days', 'price', 'total_subscriptions']
retention_by_plan = retention_by_plan.sort_values('retention_rate', ascending=False)

print("Retention Rate by Plan:")
print(retention_by_plan)

# 2. Revenue per Customer by Plan
revenue_by_plan = df.groupby('plan_name').agg({
    'price': lambda x: x.iloc[0] * len(x),  # Total revenue
    'customer_id': 'nunique'  # Unique customers
}).round(2)

revenue_by_plan['revenue_per_customer'] = (revenue_by_plan['price'] / revenue_by_plan['customer_id']).round(2)
revenue_by_plan = revenue_by_plan.sort_values('revenue_per_customer', ascending=False)

print("\nRevenue per Customer by Plan:")
print(revenue_by_plan[['revenue_per_customer']])

# 3. Repeat Customer Rate by Plan
repeat_rate_by_plan = df.groupby('plan_name')['is_repeat_customer'].mean().round(3)
repeat_rate_by_plan = repeat_rate_by_plan.sort_values(ascending=False)

print("\nRepeat Customer Rate by Plan:")
print(repeat_rate_by_plan)

# 4. Plan Success Score (composite metric)
success_scores = pd.DataFrame({
    'plan_name': retention_by_plan.index,
    'retention_rate': retention_by_plan['retention_rate'].values,
    'revenue_per_customer': revenue_by_plan.loc[retention_by_plan.index, 'revenue_per_customer'].values,
    'repeat_rate': repeat_rate_by_plan.loc[retention_by_plan.index].values
})

# Normalize metrics to 0-1 scale for composite score (simple min-max normalization)
def normalize_column(col):
    return (col - col.min()) / (col.max() - col.min()) if col.max() != col.min() else col

success_scores['retention_norm'] = normalize_column(success_scores['retention_rate'])
success_scores['revenue_norm'] = normalize_column(success_scores['revenue_per_customer'])
success_scores['repeat_norm'] = normalize_column(success_scores['repeat_rate'])

# Calculate weighted success score
success_scores['success_score'] = (
    0.4 * success_scores['retention_norm'] +
    0.3 * success_scores['revenue_norm'] +
    0.3 * success_scores['repeat_norm']
).round(3)

success_scores = success_scores.sort_values('success_score', ascending=False)

print("\nPlan Success Scores (weighted composite):")
print(success_scores[['plan_name', 'success_score', 'retention_rate', 'revenue_per_customer', 'repeat_rate']])

# Create comprehensive visualizations
fig = plt.figure(figsize=(20, 15))

# 1. Plan Success Metrics Dashboard
ax1 = plt.subplot(3, 3, 1)
bars = ax1.bar(success_scores['plan_name'], success_scores['retention_rate'])
ax1.set_title('Retention Rate by Plan', fontsize=14, fontweight='bold')
ax1.set_ylabel('Retention Rate')
ax1.tick_params(axis='x', rotation=45)
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
             f'{height:.2f}', ha='center', va='bottom')

ax2 = plt.subplot(3, 3, 2)
bars = ax2.bar(success_scores['plan_name'], success_scores['revenue_per_customer'])
ax2.set_title('Revenue per Customer by Plan', fontsize=14, fontweight='bold')
ax2.set_ylabel('Revenue per Customer ($)')
ax2.tick_params(axis='x', rotation=45)
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'${height:.0f}', ha='center', va='bottom')

ax3 = plt.subplot(3, 3, 3)
bars = ax3.bar(success_scores['plan_name'], success_scores['repeat_rate'])
ax3.set_title('Repeat Customer Rate by Plan', fontsize=14, fontweight='bold')
ax3.set_ylabel('Repeat Customer Rate')
ax3.tick_params(axis='x', rotation=45)
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
             f'{height:.2f}', ha='center', va='bottom')

# 4. Composite Success Score
ax4 = plt.subplot(3, 3, 4)
colors = plt.cm.RdYlGn(success_scores['success_score'])
bars = ax4.bar(success_scores['plan_name'], success_scores['success_score'], color=colors)
ax4.set_title('Composite Success Score', fontsize=14, fontweight='bold')
ax4.set_ylabel('Success Score (0-1)')
ax4.tick_params(axis='x', rotation=45)
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
             f'{height:.3f}', ha='center', va='bottom')

# 5. Repeat vs New Customers
ax5 = plt.subplot(3, 3, 5)
repeat_stats = df.groupby(['plan_name', 'is_repeat_customer']).size().unstack(fill_value=0)
repeat_stats.plot(kind='bar', stacked=True, ax=ax5,
                 color=['lightcoral', 'lightgreen'])
ax5.set_title('New vs Repeat Customers by Plan', fontsize=14, fontweight='bold')
ax5.set_ylabel('Number of Customers')
ax5.legend(['New Customer', 'Repeat Customer'])
ax5.tick_params(axis='x', rotation=45)

# 6. Average Subscription Duration by Plan
ax6 = plt.subplot(3, 3, 6)
avg_duration = df.groupby('plan_name')['subscription_duration_days'].mean().sort_values(ascending=False)
bars = ax6.bar(avg_duration.index, avg_duration.values)
ax6.set_title('Average Subscription Duration by Plan', fontsize=14, fontweight='bold')
ax6.set_ylabel('Days')
ax6.tick_params(axis='x', rotation=45)
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax6.text(bar.get_x() + bar.get_width()/2., height + 5,
             f'{height:.0f}', ha='center', va='bottom')

# 7. Price vs Retention Scatter
ax7 = plt.subplot(3, 3, 7)
scatter = ax7.scatter(success_scores['revenue_per_customer'], success_scores['retention_rate'],
                     s=100, alpha=0.7, c=success_scores['success_score'], cmap='RdYlGn')
ax7.set_xlabel('Revenue per Customer ($)')
ax7.set_ylabel('Retention Rate')
ax7.set_title('Price vs Retention Analysis', fontsize=14, fontweight='bold')
for i, plan in enumerate(success_scores['plan_name']):
    ax7.annotate(plan, (success_scores.iloc[i]['revenue_per_customer'],
                       success_scores.iloc[i]['retention_rate']),
                xytext=(5, 5), textcoords='offset points', fontsize=8)


# 9. Monthly Subscription Trends
ax9 = plt.subplot(3, 3, 9)
df['start_month'] = df['start_date'].dt.to_period('M')
monthly_subs = df.groupby(['start_month', 'plan_name']).size().unstack(fill_value=0)
monthly_subs.plot(ax=ax9, marker='o')
ax9.set_title('Monthly Subscription Trends by Plan', fontsize=14, fontweight='bold')
ax9.set_ylabel('New Subscriptions')
ax9.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax9.tick_params(axis='x', rotation=45)

plt.tight_layout(pad=5.0)
plt.savefig('advanced_subscription_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Generate summary insights
print("\n=== KEY INSIGHTS ===")

best_plan = success_scores.iloc[0]['plan_name']
worst_plan = success_scores.iloc[-1]['plan_name']
best_retention = retention_by_plan.iloc[0]
highest_revenue = revenue_by_plan.iloc[0]
most_repeat = repeat_rate_by_plan.iloc[0]

print(f"🏆 Most Successful Plan Overall: {best_plan}")
print(f"   - Success Score: {success_scores.iloc[0]['success_score']:.3f}")
print(f"   - Retention Rate: {success_scores.iloc[0]['retention_rate']:.1%}")
print(f"   - Revenue per Customer: ${success_scores.iloc[0]['revenue_per_customer']:.0f}")

print(f"\n📈 Highest Retention: {best_retention.name} ({best_retention['retention_rate']:.1%})")
print(f"💰 Highest Revenue per Customer: {highest_revenue.name} (${highest_revenue['revenue_per_customer']:.0f})")
print(f"🔄 Most Repeat Customers: {most_repeat} ({repeat_rate_by_plan.iloc[0]:.1%})")

total_repeat_customers = df['is_repeat_customer'].sum()
total_customers = df['customer_id'].nunique()
print(f"\n👥 Total Repeat Customers: {total_repeat_customers}/{total_customers} ({total_repeat_customers/total_customers:.1%})")

conn.close()
print("\nAnalysis complete! Visualizations saved as 'advanced_subscription_analysis.png'")