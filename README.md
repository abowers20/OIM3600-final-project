# Project Name: WeatherWise

**Alex Bowers**

## 1. Project Overview
This application can use geolocation or manual user input of a location to return a live weather dashboard. 

## 2. Usage Guidelines
Users can either click the "Use Geolocation" toggle or type the city, state, and country into the form. State is an optional form input. If including the state, make sure to type it out fully. Also make sure to use the country code if possible.

## 3. Dependencies
This project depends on the use of OpenWeather's weather, forecast, and reverse geocoding APIs.

## 4. Project Structure
The "config.py" stores the API key because it is sensitive information. Functions that call and parse data from the API are located in the "weather.py" file in the directory. This data is passed on to app.py which sends all of the information to the weather dashboard page ("weather.html") after the user has selected geolocation or typed manual input on index.html, which are both located in the templates folder. I ended up not needed the css and js files in the static folder. I also had a routes.py file but decided to just go with app.py with this project.

## 5. Collaboration Information
I worked independently on this project.

## 6. Acknowledgments
OpenWeather API and ChatGPT for debugging.

## 7. Reflection
Building and designing the front-end went well. I had challenges linking the front-end to the back-end Python using Flask in app.py. I had never used Flask prior to this project, so I could have done a better job at utilizing its features and potentially separating the "app.py" into this file and a "routes.py" file. I also had to problem solve a lot when trying to parse the correct data from the APIs because I had little prior experience with using APIs. I also need to build my JavaScript knowledge because I was very reliant on ChatGPT. These aren't surprising because I learned each of them for the first time in recent weeks. The most challenging aspect was taking the API information and figuring out how to present it on the website. It took a lot of iterations determining what data was possible to show, to make sure it was accurate, and to make sure it was provided in the correct format. Each time I decided to add more information to my dashboard involved a lot of bug testing with different locations. More practice building applications using Flask and a prior knowledge of a lot of API options would have been helpful because I spent the bulk of my time learning how to use them, but I'm glad for this experience. I also would break out my CSS and JavaScript into files in the static folder next time, but I kept it in the html templates because they were relatively small.

I learned how to use multiple APIs in parallel with eachother in a web application. I also learned how to set up the file directory for a web application. I am confident that I can use this experience to build any web application going forward as long as I have the available APIs for my idea. I need to learn how to integrate static data using SQLite on my next project. ChatGPT helped me debug and provided me with code updates. It also did a great job at adding in checkpoints to catch errors. I wish I had a higher level understanding of Flask and Python libraries before prompting ChatGPT. I'm not the best at prompting ChatGPT, which I had many circular references where it wasn't actually solving any problems for me until I spent time reflecting and learning how to change my prompt to include a bit more insight.