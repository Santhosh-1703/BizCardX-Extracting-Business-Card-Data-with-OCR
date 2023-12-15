import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image, ImageDraw
import pandas as pd
import numpy as np
import re
import mysql.connector as sql
import pymysql
import sqlalchemy
from sqlalchemy import create_engine,text

#******* Establishing connection with MySQL workbench *********
# CONNECTING WITH MYSQL DATABASE
user="######"
password="######"
host="#######"
database= "project-bizcardx"
port = "3306"

engine = create_engine("mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))
con = engine.connect()
#Webpage customization
icon = Image.open("D:\GUVI Class\download (1).png")
st.set_page_config(page_title='BizCardX: Extracting Business Card Data with OCR',page_icon = icon, layout="wide")
col1,col2,col3 = st.columns([3,10,3])
with col2:
    st.title("***BizCardX: Extracting Business Card Data with OCR***")
    st.subheader("  Hello Connections!:raised_hand_with_fingers_splayed: Welcome to My Project Presentation || By Santhosh")

selected_page = option_menu(
    menu_title='Options',
    options=["Home", "Extract & Preview", "Modify / Delete","About"],
    icons=["house", "clipboard", "scissors","envelope"],
    default_index=1,
    orientation="horizontal",
    styles = {
    "container": {"padding": "0!important", "background-color": "black", "size": "cover", "width": "100"},
    "icon": {"color": "#EADE08", "font-size": "25px"},
    "nav-link": {"font-size": "25px", "text-align": "center", "margin": "-2px", "--hover-color": "#19F10A"},
    "nav-link-selected": {"background-color": "#19F10A"}})

if selected_page == "Home":
    tab1,tab2 = st.tabs(["Business Card Data Scrapping"," "])
    with tab1:
        st.subheader(" Business Card Data scraping from Business Card using a easyOCR module helps organizations gather valuable insights about Business individuals all over India, Type of Business, and Contact Details. By combining this data with information from Business card data, Organizations can get a comprehensive view of easy data use. This approach enables more effective content strategies.")
        col1,col2,col3 = st.columns([4,5,2])
        with col2:
            get_data = st.button("Click here to know about Business Card Data")
        if get_data:
            col1, col2,col3 = st.columns(3)
            with col1:
                st.subheader(':orange[Card Details]', divider='rainbow')
                st.subheader(" :ribbon: From the Business card data provided, Users can able to view & retrieve User details, Business & Communication details")
                st.subheader(" :ribbon: Users can analyse Business wise usage, Frequency, Engagement Metrics.")
            with col2:
                st.subheader(':orange[Applications and Libraries Used!]', divider='rainbow') 
                st.subheader("  :bulb: EasyOCR")
                st.subheader("  :bulb: Python")
                st.subheader("  :bulb: MySQL WorkBench")
                st.subheader("  :bulb: Streamlit")
            with col3:
                st.video(r"D:\GUVI Class\WhatsApp Video 2023-12-12 at 1.13.44 PM.mp4")

elif selected_page == "About":
    st.header(" :silver[Project Conclusion]")
    tab1,tab2 = st.tabs(["Features","Connect with me on"])
    with tab1:
            st.subheader("This Streamlit application allows users to access and analyze data from Business card Data.", divider='rainbow')
            st.markdown ("1.   User can able to extract Business Card Data file and retrieve all the relevant data using EasyOCR(Optical Character Recognition).")
            st.markdown("2.    It can collect required data based upon user experience and store them in the Database by clicking a upload button.")
            st.markdown("3.    It has option to select category and migrate its data from the database to a MySQL database as Tables.")
            st.markdown("4.    Able to search and edit,modify data from the MySQL database using different SQL Query options, including updating data to details.")
    with tab2:
                linkedin_button = st.button("LinkedIn")
                if linkedin_button:
                    st.write("[Redirect to LinkedIn Profile > (https://www.linkedin.com/in/santhosh-r-42220519b/)](https://www.linkedin.com/in/santhosh-r-42220519b/)")

                email_button = st.button("Email")
                if email_button:
                    st.write("[Redirect to Gmail > santhoshsrajendran@gmail.com](santhoshsrajendran@gmail.com)")

                github_button = st.button("GitHub")
                if github_button:
                    st.write("[Redirect to Github Profile > https://github.com/Santhosh-1703](https://github.com/Santhosh-1703)")

elif selected_page == "Extract & Preview":
    import_image = st.file_uploader('**Select a Business card (Image file)**', type=['png', 'jpg', 'jpeg'],
                                    accept_multiple_files=False)
    st.info('''File extension support: **PNG, JPG, JPEG**, File size limit: **2 MB**, Language : **English**.''')
    col1, col2, col3 = st.columns(3)

    with col1:
        if import_image is not None:
            reader = easyocr.Reader(['en'], gpu=False)
            # Read the image file as a PIL Image object
            if isinstance(import_image, str):
                image = Image.open(import_image)
            elif isinstance(import_image, Image.Image):
                image = import_image
            else:
                image = Image.open(import_image)
                st.image(image, width=500, caption='Business card Uploaded')
                get_data = st.button("Click here to Extract Business Card Data")
            image_array = np.array(image)
            text_read = reader.readtext(image_array)

            result = []
            for text in text_read:
                result.append(text[1])

        elif import_image is None:
            st.error("Failed to process the image. Please try again with a different image.", icon="🚨")

    with col2:
        data = {"Company": [], "Name": [], "Designation": [], "Mobile Number": [], "Email": [], "Website": [], "Area": [], "City": [], "State": [], "Pincode": []}
        if get_data:
            def draw_boxes(image, text_read, color='red', width=2):
                # Create a new image with bounding boxes
                image_with_boxes = image.copy()
                draw = ImageDraw.Draw(image_with_boxes)

                # draw boundaries
                for bound in text_read:
                    p0, p1, p2, p3 = bound[0]
                    draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
                return image_with_boxes

            result_image = draw_boxes(image, text_read)
            st.image(result_image, width=500, caption='Business card with Extracted data')
            

    with col3:
            fetch_data = st.button("Fetch Data from Business Data")
            if fetch_data:
                def get_data(res):
                    for index, i in enumerate(res):
                        # To get CARD HOLDER NAME
                        if index == 0:
                            data["Name"].append(i)

                        # To get DESIGNATION
                        elif index == 1:
                            data["Designation"].append(i)
                        # To get WEBSITE_URL
                        if "www " in i.lower() or "www." in i.lower():
                            data["Website"].append(i)
                        elif "WWW" in i:
                            data["Website"].append(res[4] + "." + res[5])
                        # To get EMAIL ID
                        elif "@" in i:
                            data["Email"].append(i)
                        # To get MOBILE NUMBER
                        elif "-" in i:
                            data["Mobile Number"].append(i)
                        if len(data["Mobile Number"]) == 2:
                            data["Mobile Number"] = " & ".join(data["Mobile Number"])
                        # To get COMPANY NAME
                        elif index == len(res) - 1:
                            data["Company"].append(i)
                            if len(data["Company"][0]) < 5:
                                data["Company"][0] = (f'{res[-4]} ' + res[-2])
                            elif len(data["Company"][0]) == 8 and i == 'digitals':
                                data["Company"][0] = (f'{res[-3]} ' + res[-1])
                            elif len(data["Company"][0]) == 8:
                                data["Company"][0] = (f'{res[-2]} ' + res[-1])
                            elif len(data["Company"][0]) <= 10:
                                data["Company"][0] = (f'{res[-3]} ' + res[-1])
                        # To get AREA
                        if re.findall('^[0-9].+, [a-zA-Z]+', i):
                            data["Area"].append((i.split(',')[0]))
                        elif re.findall('[0-9] [a-zA-Z]+', i):
                            data["Area"].append(i + 'St')
                        # To get CITY NAME
                        match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                        match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
                        match3 = re.findall('^[E].*', i)
                        if match1:
                            data["City"].append(match1[0])
                        elif match2:
                            data["City"].append(match2[0])
                        elif match3:
                            data["City"].append(match3[0])
                        # To get STATE
                        state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
                        if state_match:
                            data["State"].append(i[:9])
                        elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
                            data["State"].append(i.split()[-1])
                        if len(data["State"]) == 2:
                            data["State"].pop(0)
                        # To get PINCODE
                        if len(i) >= 6 and i.isdigit():
                            data["Pincode"].append(i)
                        elif re.findall('[a-zA-Z]{9} +[0-9]', i):
                            data["Pincode"].append(i[10:])
                get_data(result)
                
                df = pd.DataFrame(data)
                desired_columns = ["Name", "Designation","Company","Primary Mobile Number", "Secondary Mobile Number", "Email", "Website", "Area", "City", "State","Pincode"]
                df = pd.DataFrame(data, columns=["Company", "Name", "Designation", "Mobile Number", "Email", "Website", "Area", "City", "State", "Pincode"])
                df["Primary Mobile Number"] = df["Mobile Number"].str.split(" & ").str[0]
                df["Secondary Mobile Number"] = df["Mobile Number"].apply(lambda x: x.split(" & ")[1] if len(x.split(" & ")) > 1 else None)
                df = df[desired_columns]
                # Displaying the DataFrame
                df.index = df.index+1
                df = pd.DataFrame(df)
                st.write(df.T)
                
                existing_names_query = f"SELECT Name FROM business_card WHERE Name IN ({', '.join(['%s']*len(df['Name']))})"
                existing_names = pd.read_sql_query(existing_names_query, con=engine, params=tuple(df['Name']))
                df_to_append = df[~df['Name'].isin(existing_names['Name'])]
                if not df_to_append.empty:
                    df_to_append.to_sql("business_card", con=engine, if_exists='append', index=False)
                    st.success('Data Migrated Successfully')
                else:
                    st.warning('Data already exists in SQL.',icon ='⚠️')

elif selected_page == "Modify / Delete":
    tab1,tab2 = st.tabs(['Modify','Delete'])
    with tab1:
        col1,col2 = st.columns([4,4])
        query = "SELECT DISTINCT NAME, DESIGNATION FROM BUSINESS_CARD"
        result = pd.read_sql_query(query, con=con)
        
        names = ["Select"] + result["NAME"].tolist()
        designation = ["Select"] + result["DESIGNATION"].tolist()

        with col1:
            name_selected = st.selectbox("Select the name to modify", options=names)

        with col2:
            query_designations = f"SELECT DISTINCT DESIGNATION FROM BUSINESS_CARD WHERE NAME = '{name_selected}'"
            result_designations = pd.read_sql_query(query_designations, con=con)
            designations = ["Select"] + result_designations["DESIGNATION"].tolist()
            designation_selected = st.selectbox("Select the designation of the chosen name", options=designations)
    
        col5, col6 = st.columns(2)
        with col5:
            query_select = "SELECT * FROM business_card WHERE name = :name AND designation = :designation"
            params_select = {'name': name_selected, 'designation': designation_selected}
            result = con.execute(text(query_select), params_select)
            info = result.fetchone()

            if info:
                mn1 = st.text_input('Name:', info[0])
                md1 = st.text_input('Designation:', info[1])
                mc1 = st.text_input('Company:', info[2])
                mp1 = st.text_input('Primary Contact:', info[3])
                ms1 = st.text_input('Secondary Contact:', info[4])
                me1 = st.text_input('Email ID:', info[5])
                mw1 = st.text_input('Website:', info[6])
                ma1 = st.text_input('Area:', info[7])
                mc11 = st.text_input('City:', info[8])
                ms11 = st.text_input('State:', info[9])
                mp11 = st.text_input('Pincode:', info[10])

                update_data = st.button("Update Data")
                if update_data:
                    val_update = {
                            'new_name': mn1, 'new_designation': md1,
                            'new_company': mc1,'new_primary_mobile': mp1, 'new_secondary_mobile': ms1,
                            'new_email': me1, 'new_website': mw1,
                            'new_area': ma1, 'new_city': mc11, 'new_state': ms11,
                            'new_pincode': mp11,
                            'old_name': name_selected,'old_designation': designation_selected}

                    query_update = """
                                        UPDATE business_card 
                                        SET 
                                            Name = :new_name, 
                                            Designation = :new_designation, 
                                            Company = :new_company, `Primary Mobile Number` = :new_primary_mobile, `Secondary Mobile Number` = :new_secondary_mobile,
                                            Email = :new_email, Website = :new_website, 
                                            Area = :new_area, City = :new_city, State = :new_state, Pincode = :new_pincode
                                        WHERE 
                                            Name = :old_name AND Designation = :old_designation"""
                    con.execute(text(query_update), val_update)
                    con.commit()
                    st.success('Data updated in MySQL DB', icon="✅")
                    with col6:
                            st.write("Values updated:", val_update)
    
    with tab2:
    # Query to get distinct names
        query_names = "SELECT DISTINCT NAME FROM BUSINESS_CARD"
        result_names = pd.read_sql_query(query_names, con=con)
        names1 = ["Select"] + result_names["NAME"].tolist()
        name_selected1 = st.selectbox("Select the name to modify or delete", options=names1)
        st.warning("Attention: Deleted Data will be not recovered once deleted",icon = '⚠️')
        # Button to delete data
        delete_data = st.button("Delete Data")
        
        # Check if the delete button is clicked
        if delete_data:
            if name_selected1 != "Select":
                query_delete = "DELETE FROM BUSINESS_CARD WHERE NAME = :name"
                val_delete = {'name': name_selected1}
                # Execute the delete query
                con.execute(text(query_delete), val_delete)
                con.commit()
                st.success(f'Data for {name_selected1} deleted from MySQL DB', icon="✅")

                # Query to get the remaining DataFrame
                query_remaining_data = "SELECT * FROM BUSINESS_CARD"
                remaining_data = pd.read_sql_query(query_remaining_data, con=con)
                st.write("Available Business Card Details:")
                st.write(remaining_data)
            else:
                # Display a warning if no name is selected
                st.warning("Please select a Name before Deleting.")
