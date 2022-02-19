# Section 2: Description of Data

In this project , we are using the **Cost of Living - NUMBEO Dataset** which is avaialable in [Kaggle](https://www.kaggle.com/joeypp/cost-of-living-numbeo-dataset) .This data set contains cost of living information of 160 cities across the globe with variety of information such as country, city name, region, rent, cost of owning a house, car etc.
The Kaggle Dataset has been extracted from [numbeo](https://www.numbeo.com/cost-of-living) which is the world’s largest crowd-sourced cost of living database which collects statitics on the quality of life informations including housing indicators, crime rates, and healthcare. The website contains around 7,541,898 prices in 10,529 cities which have been entered by 630,509 contributors.
We will be visualizing the data of 160 cities which was collected in the year 2020.The dataset has 56 different columns that contain cost of living
information which we have processed and broadly classified into major categories such as `monthly salary`, `rent`, `grocery`, `utility`, `shopping`, `entertainment`, `fitness`, `property_price`, `transportation`, `childcare expenses`,`monthly_savings` miscellaneous for ease of visualization and understanding.Although the original dataset contained all the prices in Euro, we have converted the prices to USD.
Our app will allow users to view these categorization which can be easily filtered to view the statistics for different cities or region or country. Since, the main aim of this project is to give an overview of the cost of living standards to new Graduates, we have processed the data based on following assumptions:

* Rent for one person considers the average of rent for a one-bedroom in city center and outside city center 
* Public transportation includes average monthly cost of taxi's and monthly bus passes .
* Liquor, cigarettes, and movie cost were included in entertainment category.
* Fitness fee includes monthly membership in fitness club only(tennis court rent is uncommon and was dropped).
* Shopping includes buying jeans, summer dress, sports shoes, leather shoes one for each in a month.
* Childcare fee includes the monthly cost for one preschool child.
* Monthly saving is how much USD the person is likely to save in a month, which was calculated by monthly salary(after tax) after deducting all the costs mentioned above(except the childcare fee).
* Property price per square meter is the average price of buying a house in city center and outside center.This also includes the price of buying a car.
* The currency unit has been converted from Euro to USD and the current rate is 1 Euro = 1.14 USD

# Section 3: Research questions and usage scenarios

Our project answers the broad research question of: “What is the average
cost of living for a single fresh graduate in different cities in the
world?”. Below we have provided a usage scenario of our product by a
member of our target audience:

Bella is a fresh graduate in Canada and her current marital status is
single. She wants to seek for a job and settle down in some major cities
in the world, but she has concerns about the high living cost in big cities,
including housing, grocery, transportation, entertainment, shopping and
others. In order to help her get a general idea of how much the living
cost is in different major cities in the world, our app provides
immediate visualization of living cost in USD among 160 big cities from
90 countries in the world. Bella is also curious about the property
price and monthly saving as she might want to buy her own house in the
future. Our app takes her concern into account and can display the
property prices per square meter as well as the average monthly surplus
for people living in different cities.
