import streamlit as st
import pandas as pd
import numpy as np
from enum import Enum

Grade = {
    'AA': 10,
    'AP': 10,
    'AB': 9,
    'BB': 8,
    'BC': 7,
    'CC': 6,
    'CD': 5,
    'DD': 4,
    'II': 0,
    'FR': 0,
    'FF': 0,
    'W': 0,
    'NP': 0,
    'PP': 10,
    'Remaining': 9}


def sort_by_grade(courses_df):
    """Sorts a DataFrame by the 'Grade' column using the Grade enum.

    Args:
        courses_df: The DataFrame to sort.

    Returns:
        A new DataFrame sorted by the 'Grade' column in descending order (A to F).

    """
    courses_df['Grade values'] = courses_df['Grade'].map(Grade)
    return courses_df.sort_values(by='Grade values', ascending=False)


def main():
    st.set_page_config(
        page_title='After Agla Sem cannot be phodenge-d',
        page_icon='🍷',
        layout='wide',
        initial_sidebar_state='collapsed'
    )

    st.title('Telling you the truth about your grades')
    st.write("I am afraid you haven't quite achieved what you aimed for.")

    col_first, col_second = st.columns(2)
    col_first.markdown('# :orange[Upload your courses]')
    col_second.link_button('Tutorial', 'https://youtu.be/g5-WJ-7ieOU')
    st.write('Upload your portal.iitb.ac.in output here')
    grades_df = pd.DataFrame({'Course Code': ['EE 113 (D1)'], 'Course Name': ['	Introduction to Electrical Engineering Practice'], 'Credits': [
                             6], 'Tag': ['Core Course'], 'Grade': ['DD'], 'Credit/Audit': ['C']})
    uploaded_grades_df = st.data_editor(grades_df, num_rows='dynamic', use_container_width=True, column_config={'Grade': st.column_config.SelectboxColumn(
        'Grade',
        width='medium',
        options=[grade for grade in Grade.keys()],
        required=True,
    )},
        key='yaho')

    st.write('# :orange[Choose your credit requirements]')
    st.write('Refer to internal ASC>Academic>All About Courses>View Course Curriculum')
    st.write('The app assumes all courses have to be 6 credit')
    credit_req_df = pd.DataFrame({'Tag': ['Department elective', 'Institute elective',
                                 'Specialisation elective', 'Open elective'], 'Number of courses': [7, 2, 0, 1]})
    uploaded_credit_req_df = st.data_editor(credit_req_df, num_rows='fixed', use_container_width=False, disabled=[
                                            'Tag'], key='nuhuh', hide_index=True)

    st.write('# :orange[Constraints on electives]')
    constraints_df = pd.DataFrame({'Tag': ['Department elective', 'Specialisation elective',
                                  'Honors elective'], 'Number of non-department courses allowed': [1, 1, 1]})
    uploaded_constraints_df = st.data_editor(constraints_df, num_rows='fixed', use_container_width=False, disabled=[
                                             'Tag'], key='nuhuhuh', hide_index=True)

    st.write('# :orange[Pursuing minors?]')
    col1, col2 = st.columns([0.9, 0.1])
    col2.link_button('More info', 'https://publichealth.jhu.edu/moore-center-for-the-prevention-of-child-sexual-abuse/get-support/resources-for-people-concerned-about-their-own-sexual-thoughts-and-behavior#:~:text=The%20helpline%20is%20open%20on,at%20020%2D667%2D778.',
                     help='Get help', type='primary', disabled=False, use_container_width=False)
    minor_course = col1.selectbox('Select your minor', [
                                  None, 'CS', 'DS', 'SC', 'DE', 'DH', 'EC'], help="I don't have respect for people pursuing double minors")

    if st.checkbox('I am ready for the truth. Give it straight to the jaw.'):
        with st.expander('An introduction to my guiding principles'):
            st.markdown('- Main-CPImaxxing is the goal of every retagger')
            st.markdown('- Completing Minors comes before getting Honors')
            st.markdown('- Trump got the sickest ear piercing in the history of mankind')
            st.markdown('- The institute will only allow a few set of courses to be tagged as Hon/ Minor/ DE. I do not concern myself with such intricacies. I only look at the first two letters of the course code :smile:')
            st.markdown("- You are allowed to speculate your CPI based on courses which are not yet complete. Just tag them as 'Remaining' and then use the dropdown to select the grade you think you will get")
            equivalent_course = st.selectbox(
                'All of the *Remaining* courses are assumed to fetch you an', Grade.keys(), index=2)
            Grade['Remaining'] = Grade[equivalent_course]

        uploaded_grades_df['Course Code'] = uploaded_grades_df['Course Code'].str.strip(
        )
        uploaded_grades_df['Course Name'] = uploaded_grades_df['Course Name'].str.strip(
        )
        uploaded_grades_df['Tag'] = uploaded_grades_df['Tag'].str.strip()
        uploaded_grades_df['Grade'] = uploaded_grades_df['Grade'].str.strip()
        uploaded_grades_df['Credit/Audit'] = uploaded_grades_df['Credit/Audit'].str.strip()
        core_courses_df = uploaded_grades_df[((uploaded_grades_df['Tag'] == 'Core course') | (
            uploaded_grades_df['Tag'] == 'HSS elective')) & (uploaded_grades_df['Credit/Audit'] == 'C')]
        electives_df = uploaded_grades_df[(uploaded_grades_df['Tag'] != 'Core course') & (
            uploaded_grades_df['Tag'] != 'HSS elective') & (uploaded_grades_df['Credit/Audit'] == 'C')]

        electives_df = sort_by_grade(electives_df)
        electives_df['Tag'] = None  # Resetting the types to None

        # Choosing the Department Electives
        max_de_count = uploaded_credit_req_df.loc[uploaded_credit_req_df['Tag']
                                                  == 'Department elective', 'Number of courses'].values[0]
        max_non_ee_count = uploaded_constraints_df.loc[uploaded_constraints_df['Tag'] ==
                                                       'Department elective', 'Number of non-department courses allowed'].values[0]
        de_count = 0
        non_ee_count = 0
        for index, row in electives_df.iterrows():
            if de_count < max_de_count:
                # Course is from EE Dept itself
                if row['Course Code'].startswith('EE'):
                    electives_df.at[index, 'Tag'] = '⚡ Department elective'
                    de_count += 1
                elif non_ee_count < max_non_ee_count:
                    electives_df.at[index, 'Tag'] = '⚡ Department elective'
                    de_count += 1
                    non_ee_count += 1

        # Choosing the Specialisation Electives
        max_se_count = uploaded_credit_req_df.loc[uploaded_credit_req_df['Tag']
                                                  == 'Specialisation elective', 'Number of courses'].values[0]
        max_non_ee_count = uploaded_constraints_df.loc[uploaded_constraints_df['Tag'] ==
                                                       'Specialisation elective', 'Number of non-department courses allowed'].values[0]
        se_count = 0
        non_ee_count = 0
        for index, row in electives_df.iterrows():
            if electives_df.at[index, 'Tag'] != None:
                continue
            if se_count < max_se_count:
                # Course is from EE Dept itself
                if row['Course Code'].startswith('EE'):
                    electives_df.at[index, 'Tag'] = '😭 Specialisation elective'
                    se_count += 1
                elif non_ee_count < max_non_ee_count:
                    electives_df.at[index, 'Tag'] = '😭 Specialisation elective'
                    se_count += 1
                    non_ee_count += 1

        # Choosing the Institute Electives
        max_ie_count = uploaded_credit_req_df.loc[uploaded_credit_req_df['Tag']
                                                  == 'Institute elective', 'Number of courses'].values[0]
        ie_count = 0
        for index, row in electives_df.iterrows():
            if electives_df.at[index, 'Tag'] != None:
                continue
            if ie_count < max_ie_count:
                # Course is NOT from EE Dept
                if not row['Course Code'].startswith('EE'):
                    electives_df.at[index, 'Tag'] = '💸 Institute elective'
                    ie_count += 1

        # Choosing the Open Electives
        max_oe_count = uploaded_credit_req_df.loc[uploaded_credit_req_df['Tag']
                                                  == 'Open elective', 'Number of courses'].values[0]
        oe_count = 0
        for index, row in electives_df.iterrows():
            if electives_df.at[index, 'Tag'] != None:
                continue
            if oe_count < max_oe_count:
                electives_df.at[index, 'Tag'] = '🏳️‍🌈 Open elective'
                oe_count += 1

        # Choosing the Minor Courses
        if minor_course != None:
            max_me_count = 5  # You only need 5 courses per minor
            me_count = 0
            for index, row in electives_df.iterrows():
                if electives_df.at[index, 'Tag'] != None:
                    continue
                if me_count < max_me_count:
                    if row['Course Code'].startswith(minor_course):
                        electives_df.at[index, 'Tag'] = '👶 Minor'
                        me_count += 1

        # Choosing the Honors Electives
        max_he_count = 4
        max_non_ee_count = uploaded_constraints_df.loc[uploaded_constraints_df['Tag']
                                                       == 'Honors elective', 'Number of non-department courses allowed'].values[0]
        he_count = 0
        non_ee_count = 0
        for index, row in electives_df.iterrows():
            if electives_df.at[index, 'Tag'] != None:
                continue
            if he_count < max_he_count:
                # Course is from EE Dept itself
                if row['Course Code'].startswith('EE'):
                    electives_df.at[index, 'Tag'] = '🫡 Honor elective'
                    he_count += 1
                elif non_ee_count < max_non_ee_count:
                    electives_df.at[index, 'Tag'] = '🫡 Honor elective'
                    he_count += 1
                    non_ee_count += 1

        # All remaining courses go to ALCs
        electives_df.loc[electives_df['Tag'].isnull(), 'Tag'] = '🤡 ALC'

        change_df = st.data_editor(electives_df[['Tag', 'Course Code', 'Course Name', 'Credits', 'Grade']], num_rows='fixed', disabled=['Course Code', 'Course Name', 'Credits', 'Grade'], column_config={
            'Tag': st.column_config.SelectboxColumn(
                'Tag',
                width='medium',
                options=[
                    '⚡ Department elective',
                    '😭 Specialisation elective',
                    '💸 Institute elective',
                    '🏳️‍🌈 Open elective',
                    '🫡 Honor elective',
                    '👶 Minor',
                    '🤡 ALC'
                ],
                required=True,
            )
        })
        col_display1, col_display2, col_display3 = st.columns(3)
        col_display1.write('## :violet[Department Electives]')
        col_display1.dataframe(change_df[change_df['Tag'] == '⚡ Department elective'][[
                               'Course Code', 'Course Name', 'Credits', 'Grade']], hide_index=True)
        if max_de_count != len(change_df[change_df['Tag'] == '⚡ Department elective']):
            col_display1.write(':red[You need to complete '+str(max_de_count - len(
                change_df[change_df['Tag'] == '⚡ Department elective']))+' more DEs to graduate]')
        else:
            col_display1.write(':green[Done with all DEs]')

        col_display2.write('## :violet[Specialisation Electives]')
        if len(change_df[change_df['Tag'] == '😭 Specialisation elective']) > 0:
            col_display2.dataframe(change_df[change_df['Tag'] == '😭 Specialisation elective'][[
                                   'Course Code', 'Course Name', 'Credits', 'Grade']], hide_index=True)
        if max_se_count != len(change_df[change_df['Tag'] == '😭 Specialisation elective']):
            col_display2.write(':red[You need to complete '+str(max_se_count - len(
                change_df[change_df['Tag'] == '😭 Specialisation elective']))+' more SEs to graduate]')
        else:
            col_display2.write(':green[Done with all SEs]')

        col_display3.write('## :violet[Institute Electives]')
        if len(change_df[change_df['Tag'] == '💸 Institute elective']) > 0:
            col_display3.dataframe(change_df[change_df['Tag'] == '💸 Institute elective'][[
                                   'Course Code', 'Course Name', 'Credits', 'Grade']], hide_index=True)
        if max_ie_count != len(change_df[change_df['Tag'] == '💸 Institute elective']):
            col_display3.write(':red[You need to complete '+str(max_ie_count - len(
                change_df[change_df['Tag'] == '💸 Institute elective']))+' more IEs to graduate]')
        else:
            col_display3.write(':green[Done with all IEs]')

        col_display1.write('## :violet[Open Electives]')
        if len(change_df[change_df['Tag'] == '🏳️‍🌈 Open elective']) > 0:
            col_display1.dataframe(change_df[change_df['Tag'] == '🏳️‍🌈 Open elective'][[
                                   'Course Code', 'Course Name', 'Credits', 'Grade']], hide_index=True)
        if max_oe_count != len(change_df[change_df['Tag'] == '🏳️‍🌈 Open elective']):
            col_display1.write(':red[You need to complete '+str(max_oe_count - len(
                change_df[change_df['Tag'] == '🏳️‍🌈 Open elective']))+' more IEs to graduate]')
        else:
            col_display1.write(':green[Done with all OEs]')

        if minor_course != None:
            col_display2.write('## :violet[Minor Electives]')
            if len(change_df[change_df['Tag'] == '👶 Minor']) > 0:
                col_display2.dataframe(change_df[change_df['Tag'] == '👶 Minor'][[
                                       'Course Code', 'Course Name', 'Credits', 'Grade']], hide_index=True)
            if len(change_df[change_df['Tag'] == '👶 Minor']) != 5:
                col_display2.write(':orange[You need to complete '+str(5 - len(
                    change_df[change_df['Tag'] == '👶 Minor']))+' more Minor courses to get the minor]')
            else:
                col_display2.write(':green[Done with all Minor Courses]')

        col_display3.write('## :violet[Honors Electives]')
        if len(change_df[change_df['Tag'] == '🫡 Honor elective']) > 0:
            col_display3.dataframe(change_df[change_df['Tag'] == '🫡 Honor elective'][[
                                   'Course Code', 'Course Name', 'Credits', 'Grade']], hide_index=True)
        if max_he_count != len(change_df[change_df['Tag'] == '🫡 Honor elective']):
            col_display3.write('You need to complete '+str(max_he_count - len(
                change_df[change_df['Tag'] == '🫡 Honor elective']))+' more Honors Electives to get honors')
        else:
            col_display3.write(':green[You can pass out with honors : )]')

        core_grade_cumulative_earned = sum(
            core_courses_df['Credits'] * core_courses_df['Grade'].map(Grade))

        total_credits = sum(core_courses_df['Credits']) + sum(electives_df[(electives_df['Tag'] == '⚡ Department elective') | (electives_df['Tag'] ==
                                                                                                                               '💸 Institute elective') | (electives_df['Tag'] == '🏳️‍🌈 Open elective') | (electives_df['Tag'] == '😭 Specialisation elective')]['Credits'])

        original_elective_grade_cumulative = np.sum(
            np.multiply(
                electives_df[(electives_df['Tag'] == '⚡ Department elective') | (electives_df['Tag'] == '💸 Institute elective') | (
                    electives_df['Tag'] == '🏳️‍🌈 Open elective') | (electives_df['Tag'] == '😭 Specialisation elective')]['Grade'].map(Grade).to_numpy(),
                electives_df[(electives_df['Tag'] == '⚡ Department elective') | (electives_df['Tag'] == '💸 Institute elective') | (
                    electives_df['Tag'] == '🏳️‍🌈 Open elective') | (electives_df['Tag'] == '😭 Specialisation elective')]['Credits'].to_numpy()
            )
        )
        total_grade_cumulative = core_grade_cumulative_earned + \
            original_elective_grade_cumulative
        original_cpi = total_grade_cumulative/total_credits

        total_credits = sum(core_courses_df['Credits']) + sum(change_df[(change_df['Tag'] == '⚡ Department elective') | (change_df['Tag'] ==
                                                                                                                         '💸 Institute elective') | (change_df['Tag'] == '🏳️‍🌈 Open elective') | (change_df['Tag'] == '😭 Specialisation elective')]['Credits'])
        changed_elective_grade_cumulative = np.sum(
            np.multiply(
                change_df[(change_df['Tag'] == '⚡ Department elective') | (change_df['Tag'] == '💸 Institute elective') | (
                    change_df['Tag'] == '🏳️‍🌈 Open elective') | (change_df['Tag'] == '😭 Specialisation elective')]['Credits'].to_numpy(),
                change_df[(change_df['Tag'] == '⚡ Department elective') | (change_df['Tag'] == '💸 Institute elective') | (
                    change_df['Tag'] == '🏳️‍🌈 Open elective') | (change_df['Tag'] == '😭 Specialisation elective')]['Grade'].map(Grade).to_numpy()
            )
        )
        total_grade_cumulative = core_grade_cumulative_earned + \
            changed_elective_grade_cumulative
        new_cpi = total_grade_cumulative/total_credits

        st.divider()
        st.metric('CPI', round(total_grade_cumulative /
                  total_credits, 2), delta=new_cpi - original_cpi)
        st.write(f"### :violet[Main CPI credits] = {int(total_credits)}")
        try:
            st.image("https://raw.githubusercontent.com/aryacliche/CourseRetagger/refs/heads/main/images%20(2).jpeg", caption="At least you're graduating, eventually") 
        except:
            st.link_button("At least you're graduating ... eventually", "https://raw.githubusercontent.com/aryacliche/CourseRetagger/refs/heads/main/images%20(2).jpeg")
        
        st.divider()
        st.slider("How satisfied are you with this app?", 0, 100, 75)
        if (st.button("Done")):
            st.write("Literally couldn't give lesser shits")


if __name__ == '__main__':
    main()
