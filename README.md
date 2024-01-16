# CCT-App
This is a repository for Covid Care Teens and its applications.


You can test these apps with `streamlit` in `python`.

# Using Available Hospital Beds Discord bot
This bot interacts with users directly on Discord. In any server that the bot is present (including CCT's own server), a user can request the bot for data on available beds. The request can be specific to a location. The response is given as a series of embeds, each of which is an hospital with available beds, matching the user's request.
![available beds demo](https://github.com/Nikhil0504/CCT-App/assets/74148176/56d2a6f4-2936-486d-9455-bab923760ca2) <br>
<img src="https://github.com/Nikhil0504/CCT-App/assets/74148176/a8786bea-7414-455f-b928-52c72abee795" height = 350>
<img src = "https://github.com/Nikhil0504/CCT-App/assets/74148176/34451b1e-9c43-4913-8ecf-e47a7e509f5a" height = 350>

# Using the other apps
1. Clone this repository using `git clone https://github.com/Nikhil0504/CCT-App.git`.
2. Go to the directory and install the repositories using `pip` by doing `pip install -r requirements.txt`.
3. Run `streamlit run app.py` for the CoWIN Vaccination availablity.

NOTE: This app only works with Indian IP addresses.

Now you can access the apps here: 
https://share.streamlit.io/nikhil0504/cct-app/main/apps/app.py
https://share.streamlit.io/nikhil0504/cct-app/main/apps/active_cases.py

# Streamlit
If the app doesn't open you can open it with Local URL: http://localhost:8501 Network URL: http://192.168.1.7:8501
