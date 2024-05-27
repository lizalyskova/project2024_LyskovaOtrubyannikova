import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

data = load_data('clean_data.csv')
data_for_regression = load_data('data_for_regression.csv')
predicted_data = load_data('predicted_data.csv')

st.title('Приложение для оценки заработной платы')

age = st.selectbox('Возраст', data['Age'].unique())
gender = st.selectbox('Пол', data['Gender'].unique())
senior_level = st.selectbox('Уровень', ['Senior', 'Junior', 'Middle', 'Lead'])
position = st.selectbox('Позиция', data[data['Position (without seniority)'] != 0]['Position (without seniority)'].unique())

filtered_data = data[
    (data['Age'] == age)
    &
    (data['Gender'] == gender)
    &
    (data['Seniority level'] == senior_level)
    &
    (data['Position (without seniority)'] == position)
]

if filtered_data.shape[0] != 0:
    st.write(f'Под ваш запрос в датасете нашлось {filtered_data.shape[0]} объектов')
    st.write(f"Ожидаемая годовая зарплата по вашим характеристикам : {int(filtered_data['Yearly salary'].mean())}$")
else:
    st.write('К сожалению по таким параметрам мы не можем предсказать зарплату')

st.subheader('Анализ рынка')

# Построение графика с возрастом
gen_data = data[data['Gender'] != '0'].groupby('Gender', as_index=False)['Yearly salary'].mean().round(1)
gen_fig = px.bar(gen_data, y='Yearly salary', x='Gender', title='Распределение зарплаты по полу')
st.plotly_chart(gen_fig)

# Построение графика с уровнем сеньерности
sen_data = data[data['Seniority level'].isin(['Senior', 'Junior', 'Middle', 'Lead'])].groupby('Seniority level', as_index=False)['Yearly salary'].mean().round(1).sort_values(by='Yearly salary')
sen_fig = px.bar(sen_data, y='Yearly salary', x='Seniority level', title='Распределение зарплаты по уровню')
st.plotly_chart(sen_fig)

# Построение графика зависимостью опыта от зарплаты
X = 'Years of experience total'
Y = 'Yearly salary'

fig = px.scatter(data_for_regression, x=X, y=Y, title='Зависимость опыта от зарплаты', trendline="ols")
st.plotly_chart(fig)
