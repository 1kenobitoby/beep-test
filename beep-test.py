import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Beep / Multi-stage Fitness Test App",
    page_icon="media/favicon.ico",
    layout="centered",
    initial_sidebar_state="auto",
    #menu_items={
        #'Get Help': '<<URL>>',
        #'Report a bug': "<<URL>>",
        #'About': "Made with Streamlit v1.27"
    #}
)

# html strings used to render donate button and link and text
donate_text = '<h6> Useful? Buy us a coffee. </h6>'

html_donate_button = '''
<form action="https://www.paypal.com/donate" method="post" target="_blank">
<input type="hidden" name="hosted_button_id" value="6X8E9CL75SRC2" />
<input type="image" src="https://www.paypalobjects.com/en_GB/i/btn/btn_donate_SM.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button"/>
<img alt="" border="0" src="https://www.paypal.com/en_GB/i/scr/pixel.gif" width="1" height="1" />
</form>
'''   

def redirect_button(url: str):
    st.markdown(
    f"""
    <a href="{url}" target="_blank">
        <div>
        <img src="https://www.paypalobjects.com/en_GB/i/btn/btn_donate_SM.gif" alt="Donate with PayPal button">
        </div>
    </a>
    """,
    unsafe_allow_html=True
    )

st.image('media/logo.png', width=100)
st.title('Beep / Multi-stage Fitness Test App')
   

st.write('This app shows you how to conduct a beep test, [plays the audio](#audio_player) needed for the test and allows you to [enter the test score and interpret the result](#result). The beep test is also known as: the bleep test; the multi-stage fitness test; the 20m progressive shuttle run test (20mPST); and 20m multistage shuttle run test (20mMST). These are all the same thing: a test to determine the maximal aerobic running speed (\'aerobic fitness\') of the subject and often to use this to estimate their maximum rate of oxygen uptake (VO\u2082max) which is a good predictor of running race performance potential. If you need an explanation, expand the Notes section at the bottom of the page.')

tab_text, tab_video = st.tabs(["Text", "Video"])
with tab_text:
    st.subheader('How to set up and perform the test')
    st.write('1.    Find a level surface with good underfoot grip either indoors or on a windless day.')
    st.write('2.    Accurately measure out a 20m long course and mark each end clearly with a line. You can draw on the floor, use tape for the lines or mark the lines out with cones.')
    st.write('3.    Subjects start behind one of the lines. Start the audio player. The audio gives a 5 second warning then a 3 beep ascending tone starts the test. The subject runs to the other line. They must reach the other line by the time the audio next beeps (9 seconds after the start). The subject continues running shuttles from one line to the other in time with the beeps. If the subject reaches the other line before the next beep they must wait for the beep before setting off back. Subjects only have to \'toe the line\' i.e. touching the line with a foot is good enough, there is no requirement for them to completely cross it. At each beep, the audio will read out a level and shuttle number e.g. *"Level 1, 1"* at the beginning of the test, *"Level 1, 2"* at the next beep and so on.')
    st.write('4.    Every minute the audio will play a 3 beep ascending tone and announce the start of the next level. The time between the beeps reduces at every change in level so the subject has to run progressively faster at each change of level. Eventually a point will be reached where the subject has difficulty reaching the opposite line before the next beep. When the subject fails to make the line before the next beep twice in a row the test ends. Note the level and shuttle number *for the last shuttle that was successfully completed*.')

with tab_video:
    st.video("https://www.elephant-stone.com/downloads/beep_test_video.mp4", format='video/mp4')    


st.divider()
st.subheader('Test audio player', anchor='audio_player')
audio_file = open('media/beep_test.mp3', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/mp3')

st.divider()
st.subheader('Interpreting your test score', anchor='result')
level_col, shuttle_col = st.columns([1, 1])
with level_col:
    level = st.number_input('What level did you reach?', min_value=1, max_value=21, step=1, value=None, help='For example, if the audio said "Level 7, 4" before that last shuttle you managed to complete you would enter 7 here')

with shuttle_col:
    shuttle = st.number_input('...and what was the last shuttle number you completed?', min_value=1, max_value=16, step=1, value=None, help='For example, if the audio said "Level 7, 4" before that last shuttle you managed to complete you would enter 4 here') 

st.write('\n')
if shuttle:
    # Concatenate the level and shuttle into a string called lookup in the format '(L)LSS'
    level = str(level)    
    if shuttle < 10:
        shuttle = str(shuttle)
        shuttle = ('0' + shuttle)
    else:
        shuttle = str(shuttle)       
    lookup = level + shuttle
    # Cast 'lookup' back into an integer so you can use it as a lookup value in numerical pandas dataframe
    lookup=int(lookup)
    lookup_table = pd.read_csv('table.csv')
    # Check whether variable 'lookup' is in the 'level' column of the dataframe and either continue or send them back to reenter the level and shuttle.
    check_level = lookup in lookup_table['level'].values
    if check_level:
        # 'lookup' must be present in column 1 so find it in 'level' column and return item value from speed_kph column as mas variable
        mas = lookup_table.loc[lookup_table['level'] == lookup, 'speed_kph'].item()
        mas_string = '<strong><em>Your maximal aerobic speed (MAS), the speed you were running at when the test ended, is <span style="color:#F63366;"> ' + "%.1f" % mas + ' m s\u207B\u00B9</span></em></strong>'
        st.markdown(mas_string,  unsafe_allow_html=True)
        # Wash, rinse repeat for distance covered, time taken and VO2max
        dist = lookup_table.loc[lookup_table['level'] == lookup, 'cum_distance_m'].item()
        time = lookup_table.loc[lookup_table['level'] == lookup, 'cum_time_s'].item()
        run_string = '<strong><em>You ran a total distance of <span style="color:#F63366;"> ' + "%.0f" % dist + ' metres</span> in <span style="color:#F63366;">' + "%.0f" % time + ' seconds</span></em></strong>'
        st.markdown('\n')
        st.markdown(run_string,  unsafe_allow_html=True)
        vo2max = lookup_table.loc[lookup_table['level'] == lookup, 'VO2max'].item()
        vo2max = int(vo2max)
        # vo2max
        vo2_string = '<strong><em>Your VO\u2082max (the maximum rate at which your body can absorb oxygen) is approximately <span style="color:#F63366;"> ' + "%.0f" % vo2max + ' ml kg\u207B\u00B9 min\u207B\u00B9</span></em></strong>'
        st.markdown('\n')
        st.markdown(vo2_string,  unsafe_allow_html=True)
        vdot_table = pd.read_csv('vdot_times_distances_secs.csv')
        # Check whether variable 'vo2max' is in the 'VDOT' column of the dataframe (it should be) and if so spit out the predicted 10k, half marathon and marathon times
        check_vo2max = vo2max in vdot_table['VDOT'].values
        if check_vo2max:
            # 'lookup' must be present in column 1 so find it in 'level' column and return item value from speed_kph column as mas variable
            tenk = vdot_table.loc[vdot_table['VDOT'] == vo2max, '10000m'].item()
            half_marathon = vdot_table.loc[vdot_table['VDOT'] == vo2max, 'Half_marathon'].item()
            marathon = vdot_table.loc[vdot_table['VDOT'] == vo2max, 'Marathon'].item()
            # tenk
            # half_marathon
            # marathon
            tenk_mins = int(tenk/60)
            # tenk_mins
            tenk_secs = tenk - (tenk_mins*60)
            # tenk_secs
            st.markdown('<strong><em>This suggests that with appropriate training to cover the distance you have the potential to run:</em></strong>',  unsafe_allow_html=True)
            tenk_string = '<strong><em>&emsp;A 10k race in about <span style="color:#F63366;"> ' + "%.0f" % tenk_mins + ' minutes</span> and <span style="color:#F63366;">' + "%.0f" % tenk_secs + ' seconds</span></em></strong>'
            st.markdown(tenk_string,  unsafe_allow_html=True)

            half_marathon_mins = int(half_marathon/60)
            # half_marathon_mins
            half_marathon_secs = half_marathon - (half_marathon_mins*60)
            # Initialise half_marathon_hours
            half_marathon_hours = 0
            if half_marathon_mins >= 60:
                half_marathon_hours = int(half_marathon_mins/60)
                half_marathon_mins = int(half_marathon_mins - (half_marathon_hours * 60))
                # half_marathon_hours
                # half_marathon_mins
            # half_marathon_secs
            if half_marathon_hours > 0:
                half_marathon_string = '<strong><em>&emsp;A half marathon race in about <span style="color:#F63366;"> ' + "%.0f" % half_marathon_hours + ' hours, ' + "%.0f" % half_marathon_mins + ' minutes</span> and <span style="color:#F63366;">' + "%.0f" % half_marathon_secs + ' seconds</span></em></strong>'
            else:
                half_marathon_string = '<strong><em>&emsp;A half marathon race in about <span style="color:#F63366;">' + "%.0f" % half_marathon_mins + ' minutes</span> and <span style="color:#F63366;">' + "%.0f" % half_marathon_secs + ' seconds</span></em></strong>'   
            st.markdown(half_marathon_string,  unsafe_allow_html=True)

            marathon_mins = int(marathon/60)
            # marathon_mins
            marathon_secs = marathon - (marathon_mins*60)
            # Initialise marathon_hours
            marathon_hours = 0
            if marathon_mins >= 60:
                marathon_hours = int(marathon_mins/60)
                marathon_mins = int(marathon_mins - (marathon_hours * 60))
                # marathon_hours
                # marathon_mins
            # marathon_secs
            if marathon_hours > 0:
                marathon_string = '<strong><em>&emsp;And a marathon race in about <span style="color:#F63366;"> ' + "%.0f" % marathon_hours + ' hours, ' + "%.0f" % marathon_mins + ' minutes</span> and <span style="color:#F63366;">' + "%.0f" % marathon_secs + ' seconds</span></em></strong>'
            else:
                marathon_string = '<strong><em>&emsp;A half marathon race in about <span style="color:#F63366;">' + "%.0f" % marathon_mins + ' minutes</span> and <span style="color:#F63366;">' + "%.0f" % marathon_secs + ' seconds</span></em></strong>'   
            st.markdown(marathon_string,  unsafe_allow_html=True)
    else:
        st.markdown('<strong><em>You seem to have entered an impossible combination of level and shuttle number. Check your inputs.</em></strong>', unsafe_allow_html=True)     
    

st.divider()





st.write('\n')
st.write('\n')
donate_left, donate_right = st.columns([1, 3])
with donate_left:
    st.write('\n')
    st.markdown(donate_text, unsafe_allow_html=True)

with donate_right:
    st.write('\n')
    redirect_button("https://www.paypal.com/donate/?hosted_button_id=6X8E9CL75SRC2")   

st.write('\n')
st.write('\n')
notes = st.button('Notes')

notes_container1 = st.empty()
notes_image = st.empty()
notes_container2 = st.empty()
notes_container3 = st.empty()
notes_container4 = st.empty()
if notes:
    notes_string = 'Originally called the \'20m shuttle run fitness test\', what is now more commonly known as the \'beep test\' or \'multi-stage fitness test\' is a running test to determine a person\'s aerobic capacity or cardiorespiratory fitness. There are now many different names for this test and even more minor variations on the theme but in all cases the test measures how fast a person can run when their body is absorbing as much oxygen through their lungs as it can. As such, people who score highly on the test tend to be able to run distance races faster than people who score less highly. High scores are associated with a high ability to absorb oxygen from the air, get it to muscles and use it to do aerobic work. The test has become a common means of determining whether a person has sufficient aerobic fitness to meet the demands of the job in fields such as policing and armed forces and many such organisations publish minimum required standards of level and shuttle number that have to be met to be considered for the role.<br><br>The test was originally designed to measure the aerobic fitness of children for health care reasons and adopted its present form in 1984 ([Leger et al, 1984](https://www.elephant-stone.com/downloads/beep-test-refs/Leger_et_al_1984.pdf)). The test involves repeated shuttle runs back and forth over a 20m course in time with audio beeps (some variations now use a 15m course but the protocol in this app uses the original 20m distance). At first the shuttles are run at a slow jog but every minute the level increases and the speed at which the shuttles has to be run increases. Most versions of the test (including the one used in this app) start off at a running speed of 8km h\u207B\u00B9, increase this to 9km h\u207B\u00B9 after one minute and then increase the speed by 0.5km h\u207B\u00B9 every minute thereafter. Some versions of the test start at a running speed of 8.5km h\u207B\u00B9 for Level 1 and increase this by 0.5km h\u207B\u00B9 every minute. (For those who are interested, the confusion has arisen because in the [original paper](https://www.elephant-stone.com/downloads/beep-test-refs/Leger_et_al_1984.pdf) the authors specify a start speed of 8.5km h\u207B\u00B9 in the text but show a start speed of 8km h\u207B\u00B9 in the accompanying figure.) In practice it makes very little difference whether 8 or 8.5km h\u207B\u00B9 is used for the Level 1 speed as hardly anyone goes out at this level. Either way, every minute the level changes and the participant has to run faster to keep up with the audio beeps. At first, in the version of the test used in this app, the participant has 9 seconds to run each 20m shuttle. After 1 minute Level 2 is reached and the participant now has only 8 seconds to run each shuttle. The time to run each shuttle decreases progressively with each change of level. As there are 21 levels in the complete test anyone who could reach the 21st level would be running the shuttles at 18.5km h\u207B\u00B9 by the end giving them just 3.89 seconds to complete each 20m shuttle run.<br><br>When the participant can\'t keep up with the beeps anymore the test ends and the participant notes the level number and shuttle number of the last shuttle run they successfully completed. This forms the input to the app which tells you your performance. In this app we don\'t use what are known as normative tables. These are lookup tables which tell the participant based on their score whether they are \'good\', or \'average\' or \'very poor\' for their age. It\'s self-evident that a score of Level 8, shuttle 3 is a better result than, say, Level 7, shuttle 3 and there are so many different sets of published normative tables, all of which are rather subjective, that comparisons are at best confusing and at worst meaningless. Many people undertaking beep tests are doing so because they need to reach a certain standard for job selection and so know straight away from their level and shuttle number whether their performance is good enough.<br><br>A useful feature of the test result is the ability to use it to predict VO\u2082max. VO\u2082max is a person\'s maximal rate of oxygen consumption expressed in millilitres of oxygen per kilogram of bodyweight per minute. It is useful because it can be used to fairly accurately predict the person\'s finishing time over various distance running races. There have been several published studies over the years which have measured groups of subjects\' beep test scores and VO\u2082max values under laboratory conditions and then used the correlation between the two to predict VO\u2082max from beep test score. This app uses the relationship established by [Flouris et al, 2005](https://www.elephant-stone.com/downloads/beep-test-refs/Flouris_et_al_2005.pdf) which calculates VO\u2082max based on the participant\'s maximal aerobic speed (MAS), the speed they were running at when they were eliminated from the test:<br>&emsp;*VO\u2082max = MAS * 6.65 - 35.8*<br>Other studies have established similar relationships. For example, [Ramsbottom et al, 1988](https://www.elephant-stone.com/downloads/beep-test-refs/Ramsbottom_et_al_1988.pdf) came up with:<br>&emsp;*VO\u2082max = 3.48 * shuttle level + 14.4*<br>which produces almost the same results. The standard deviation in this study was 3.5ml kg\u207B\u00B9 min\u207B\u00B9, meaning that 68% of the population would be within \u00B13.5ml kg\u207B\u00B9 min\u207B\u00B9 of the calculated VO\u2082max value. Strictly speaking, because running speed is being used to calculate VO\u2082max, what is being calculated here is a VDOT; the product of the participant\'s VO\u2082max and their running economy. This is actually the more useful measure as it\'s not just the rate at which you can consume oxygen that is important but how efficiently you turn that into forward motion that\'s important. VDOT values are useful because they are good predictors of distance race performance. The race times predicted by this app come from the work of legendary running coach and exercise physiologist [Jack Daniels](https://en.wikipedia.org/wiki/Jack_Daniels_(coach)) from the second edition of his book Daniels\' Running Formula (2005). The times don\'t necessarily mean you could run the distances that fast now; instead they mean that with suitable training to allow you to cover that distance, your cardiorespiratory fitness is high enough to achieve these sort of race times. If you want to race faster or if you need to achieve a higher beep test score for job selection, you need to increase your VO\u2082max. Many people will find that they can improve their test score somewhat just by repeating the test a few times to gain familiarity with the pacing and technique. Some tips here are: don\'t run any faster than you have to (arrive at the line in time with the next beep rather than getting there early and having to wait); you only have to touch the line with your toe so don\'t run too far by going over the line; and try turning on a different leg at each end to delay fatigue caused by the push-off. Once you\'ve got the technique down though, to improve you\'ll have to get fitter. The beep test is mentally and physically tough because it\'s a maximal effort so don\'t do it more than once or twice a week. If you need to improve, doing repeated runs at about the pace you could maintain for 20 minutes in intervals of about 3 to 5 minutes with similar length rest periods is a good way. If you have a heart rate monitor you can use this app to help you get the training right.<br><small>*Comments, queries or suggestions? [Contact us](https://www.elephant-stone.com/contact.html)*.</small>'
    # There\'s also an intermittent version of the test with includes a short rest at the end of each pair of shuttles which many feel is more relevant to team sports such as football, rugby and cricket. If you'd like to do that one instead, use this app.
    notes_container1.markdown(notes_string, unsafe_allow_html=True)
    hide =st.button('Hide notes')
    if hide:
        notes = not notes
        notes_container1 = st.empty()    

