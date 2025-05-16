import streamlit as st
#import time

st.title("APH AI Quiz Generator")
quiz_type = st.sidebar.selectbox("Select type of Quiz Game", ["Normal Quiz", "Scrambled Words"])
quiz_level = st.sidebar.selectbox("Select difficulty level of Quiz Game", ["Easy", "Medium", "Hard"])
number_of_questions = st.sidebar.number_input("Select number of questions", min_value=1, max_value=20, step=1)
number_of_options = st.sidebar.number_input("Select number of options", min_value=2, max_value=4, step=1)
require_answers = st.sidebar.checkbox("Require Answers?", value=True)
#generate_image = st.sidebar.checkbox("Generate Image?", value=False)
submit = st.sidebar.button("Submit")

if submit:
    status = st.status("Generating Quiz ...")
    instructions = generate_instructions(quiz_type, number_of_options, quiz_level, number_of_questions, require_answers, generate_image=False)
    response = generate_response(user_query, instructions)
    #time.sleep(5)
    status.update(label="Quiz Generated", state="complete", expanded=False)

#st.subheader("Hello from Chai Code")
#st.text("Hello from Chai Code")
#st.write("Hello from Chai Code")

#chai = st.selectbox("Your favorite Chai: ", ["Lemon Tea", "Ice Tea"])
#st.write(f"Your choice {chai} is excellent choice.")
#st.success("Your chai has been brewed.")
#
#st.title("Chai maker app")
#
#if st.button("Make Chai"):
#    st.success("Your Chai is being brewed")
#
#add_masala = st.checkbox("Add masala")
#
#if add_masala:
#    st.write("Masala added to your Chai")
#
#tea_type = st.radio("Pick your chai base: ", ["Milk", "Water", "Almond Milk"])
#
#st.write(f"Selected Base: {tea_type}")
#
#flavour = st.selectbox("Choose flavour: ", ["Adarak", "Elaichi", "Kesar"])
#
#st.write(f"Selected Flavour: {flavour}")
#
#sugar = st.slider("Sugar level: ", 0, 5, 2)
#
#st.write(f"Your sugar level is: {sugar}")
#
#cups = st.number_input("How many cups?", min_value=1, max_value=10, step=1)
#st.write(f"Selected number of cups are: {cups}")
#
#name = st.text_input("Enter your name: ")
#if name:
#    st.write(f"Welcome, {name}! Your chai is on the way.")
#
#dob = st.date_input("Select your DOB: ")
#st.write(f"Your DOB is: {dob}")
#
#st.title("Chai taste poll")
#col1, col2 = st.columns(2)
#
#with col1:
#    st.header("Masala Chai")
#    # st.image('link', width)
#    vote1 = st.button("Vote Masala Chai")
#
#with col2:
#    st.header("Adarak Chai")
#    # st.image('link', width)
#    vote2 = st.button("Vote Adarak Chai")
#
#if vote1:
#    st.success("Thanks for voting Masala Chai")
#elif vote2:
#    st.success("Thanks for voting Adarak Chai")
#
##name2 = st.sidebar.text_input("Enter your name here: ")
##tea = st.sidebar.selectbox("Choose your chai", ["Masala tea", "Adarak tea"])
#
#st.write(f"Welcome {name2} and your {tea} is getting ready.")
#
#with st.expander("Show chai making instructions"):
#    st.write(f""" 
#    1. Boik water with tea leaves
#    2. Add milk and spices
#    3. Serve hot
#    """)
#
#st.markdown('### Welcome to chai app')
#st.markdown('> Blockquote')
#
#file = st.file_uploader("Upload your pdf file", type=["pdf"])
#
#if file:
#    st.success("File uploaded successfully.")
