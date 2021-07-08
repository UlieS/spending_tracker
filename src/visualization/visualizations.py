import altair as alt
import pandas as pd
import streamlit as st

from config.config import categories, statement_types
from database.database_connection import connect_to_db, read_from_db


def create_graphs(_data, graph_type):
    if graph_type == 'cu_spending':
        _data['cu_Amount'] = None
        for month in _data.month.unique():
            _data.loc[_data.month == month, 'cu_Amount'] = _data[_data.month == month].amount.cumsum()

        return alt.Chart(
            _data,
            width=1200,
            height=600,
            title='Cumulative Monthly Spending'
        ).mark_line(point=True, interpolate='step').encode(
            alt.X('day:O', title='Day of Month', axis=alt.Axis(labelAngle=0)),
            alt.Y('cu_Amount:Q', title='Expenses'),
            alt.Color('month:N', title='Month', sort=['November', 'December', 'January']),
            tooltip=['day', 'cu_Amount', 'month', 'amount']
        )
    elif graph_type == 'monthly_spending':
        return alt.Chart(
            _data,
            width=1200,
            height=600,
            title='Monthly Spending'
        ).mark_bar().encode(
            alt.X('month:N', sort=['2019', '2020']),
            alt.Y('sum(amount):Q'),
            alt.Color('category:N'),
            tooltip=['month', 'category', 'sum(amount)']
        )


def prep_data(transactions_df, tags_df):
    _df = pd.merge(transactions_df, tags_df, right_on=['t_id'], left_on=['transaction_id'])
    _df = _df[_df.type == 'expense']
    _df['date'] = pd.to_datetime(_df['date'])
    _data = _df.sort_values('date')
    _data['day'] = _data.date.dt.day
    _data['month'] = _data.date.dt.strftime('%B %Y')
    return _data


engine = connect_to_db()
transactions, tags = read_from_db(engine)

df = prep_data(transactions, tags)

### STREAMLIT LAYOUT
st.title('Spending Tracking')

st.sidebar.markdown("## Customize Filters")

st.sidebar.markdown("#### Filter by Card")
card_options = [card.name for card in statement_types.values()]
card_container = st.sidebar.beta_container()
selected_cards = card_container.multiselect("Select one or more options:",
                                            card_options)

st.sidebar.markdown("#### Time Period")
start_date = st.sidebar.date_input('Start date', min(df.date))
end_date = st.sidebar.date_input('End date', max(df.date))

st.sidebar.markdown("#### Filter by Category")
category_options = list(categories.keys())

select_all = st.sidebar.checkbox("Select all")
cat_container = st.sidebar.beta_container()
if select_all:
    selected_categories = cat_container.multiselect("Select one or more options:",
                                                    category_options)
else:
    selected_categories = cat_container.multiselect("Select one or more options:",
                                                    category_options)
st.sidebar.markdown("#### Filter by Tags")

tag_options = [tag for tag in df.tag.unique()]
tag_container_include = st.sidebar.beta_container()
included_tags = tag_container_include.multiselect("Select one or more options:",
                                                  tag_options)

### Filter DataFrame
if selected_categories:
    df = df[df.category.isin(selected_categories)]

if start_date and end_date:
    df = df[(df.date > str(start_date)) & (df.date < str(end_date))]

if selected_cards:
    df = df[df.card.isin(selected_cards)]

if included_tags:
    df = df[df.tag.isin(included_tags)]


c = create_graphs(df, 'cu_spending')
st.altair_chart(c)

c = create_graphs(df, 'monthly_spending')
st.altair_chart(c)




