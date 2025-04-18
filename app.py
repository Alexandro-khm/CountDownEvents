import streamlit as st
st.set_page_config(layout="wide")
from backend import *



events = load_events(JSON_FILENAME)
tab1, tab2, tab3 = st.tabs(['Час що залишився', 'Додати подію', 'Редагувати події'])

with tab1:
    row_tab1 = st.columns(4)
    row_tab1[0].write('Подія')
    row_tab1[1].write('Дата')
    row_tab1[2].write('Час')
    row_tab1[3].write('Час що залишився')
    for event in events:
        d, h, m, s = time_to_go(event['date'], event['time'])
        row_tab1[0].write(event['event'])
        row_tab1[1].write(event['date'])
        row_tab1[2].write(event['time'])
        row_tab1[3].write(f'Залишилось {d} днів {h} годин {m} хвилин {s} секунд')


with tab2:
    with st.container():
        sub_row1 = st.columns(3)
        with sub_row1[0]:
            event_name = st.text_input('Подія')
        with sub_row1[1]:
            event_date = st.date_input('Дата')
        with sub_row1[2]:
            event_time = st.time_input('Час')
    with st.container():
        sub_row2 = st.columns(8)
        with sub_row2[0]:
            if st.button('Додати подію'):
                if not event_name:
                    st.error('Необхідно ввести назву події')
                else:
                    date_str = event_date.strftime('%d-%m-%Y')
                    time_str = event_time.strftime('%H:%M')
                    new_event = add_event(event_name, date_str, time_str, events)
                    save_events(JSON_FILENAME, events)
                    st.rerun()
        with sub_row2[1]:
            if st.button('Оновити'):
                st.rerun()
        with sub_row2[2]:
            if st.button('Сортувати'):
                events = sort_events(events)
        with sub_row2[3]:
            if st.button('Сортувати та зберегти'):
                events = sort_events(events)
                save_events(JSON_FILENAME, events)
                st.rerun()


    with st.container():
        row2_tab1 = st.columns(4)
        row2_tab1[0].write('Подія')
        row2_tab1[1].write('Дата')
        row2_tab1[2].write('Час')
        row2_tab1[3].write('Час що залишився')
        for event in events:
            d, h, m, s = time_to_go(event['date'], event['time'])
            row2_tab1[0].write(event['event'])
            row2_tab1[1].write(event['date'])
            row2_tab1[2].write(event['time'])
            row2_tab1[3].write(f'Залишилось {d} днів {h} годин {m} хвилин {s} секунд')

with tab3:
    st.markdown("### Редагувати події")
    for index, event in enumerate(events):
        with st.expander(f"{event['event']} ({event['date']} {event['time']})", expanded=False):
            new_event = st.text_input("Назва", value=event['event'], key=f"event_{index}")
            new_date = st.date_input("Дата", value=datetime.strptime(event['date'], "%d-%m-%Y"),
                                     key=f"date_{index}")
            new_time = st.time_input("Час", value=datetime.strptime(event['time'], "%H:%M").time(),
                                     key=f"time_{index}")

            row_tab3 = st.columns(8)
            with row_tab3[0]:
                if st.button("Зберегти зміни", key=f"save_{index}"):
                    events[index] = {
                        'event': new_event,
                        'date': new_date.strftime("%d-%m-%Y"),
                        'time': new_time.strftime("%H:%M")
                    }
                    save_events(JSON_FILENAME, events)
                    st.success("Оновлено!")
                    st.rerun()
            with row_tab3[7]:
                if st.button("Видалити подію", key=f"delete_{index}"):
                    events.pop(index)
                    save_events(JSON_FILENAME, events)
                    st.warning("Подію видалено!")
                    st.rerun()
