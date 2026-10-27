# Ostrea

Ostrea is an educational website about oyster restoration and conservation created by siblings Shaurya and Shreya Sharma. Ostrea uses numerous data visualizations, images, and field observations to support student learning, but Ostrea is mainly centered around a classroom "adoption" program centered around a real oyster cage hosted by our partner organization, the Tidewater Oyster Gardeners Association (TOGA) and its Oyster Master Gardeners.

Ostrea supports student learning by using a vast collection of custom-built interactives that teach students about key concepts related to oyster conservation, from basic concepts like the oyster life cycle to more advanced concepts like the organisms near an oyster's habitat.

<p align="center">
  <img src="/static/img/oyster-setup-1.jpeg"><br>
  <sub>This image depicts 20 spat in a spat bag, a refractometer (to measure the water's salinity), calipers (to get oyster measurements in metric), and a Fahrenheit temperature gauge (to measure the water temperature). <br> Image Source: Gregory Jesseman, an oyster gardener at TOGA</sub>
</p>

## Main Features
- Interactives: The majority of Ostrea's lesson content is based off of interactives that teach students about key concepts related to oysters, ranging from anatomy to environmental factors that affect population growth.
- Data Visualizations: We use Chart.js in order to make pleasing data visualizations that simplify large amounts of data points into easy-to-read graphs for learners, making oyster data more accessible for more people.
- Oyster Data Exploration: Our "adoption" program centers around students being able to view vast amounts of oyster data, photography, and observation notes provided by TOGA easily. By bringing these resources together, we allow students to make observations, identify patterns, and create hypotheses grounded in real-world evidence.

## Tech Stack

Ostrea is built with Python and Django on the backend, HTML, CSS, and JavaScript on the frontend, and Docker for containerization. WhiteNoise is used to serve static files efficiently in production.

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Backend web framework, routing, and application logic |
| HTML | Web page structure |
| CSS | Styling and responsive layouts |
| JavaScript | Client-side interactivity |
| Docker | Application containerization |
| WhiteNoise | Serving static files in production |

## Security Considerations
Ostrea does not collect any personally identifiable information (PII) from users. Furthermore, we store all user-specific data (i.e., lesson completion data and oyster tokens) on users' local browsers instead of a central server. We also use Django's protections against cross-site request forgery (CSRF), cross-site scripting (XSS), SQL injections, clickjacking, and host header poisoning attacks. These protections help safeguard the Ostrea administrator panel, which only team members have access to. We also use secure hashing to store administrator account passwords in the database.

## License
Ostrea is licensed under the [Mozilla Public License Version 2.0](https://github.com/shaurya-sharma-dev/ostrea/blob/main/LICENSE).

To find the licenses of any of Ostrea's dependencies, please visit the `LICENSE.THIRD-PARTY.md` file [here](https://github.com/shaurya-sharma-dev/ostrea/blob/main/LICENSE.THIRD-PARTY.md).
