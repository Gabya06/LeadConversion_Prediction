# Lead Conversion Prediction

## Project Overview
The goal of this project is to predict whether a lead will convert into an opportunity or not.

## Data Processing and Cleaning
Data was collected from the Lead table in SalesForce MSSQL server by connecting and querying data using pymssql.
Some of the lead data collected included First Name, Last Name, Title, Email, Country, Company size, Industry, Phone, Website, Created Date, Lead Source and Lead Owner.

Data cleaning involved grouping industries together, assiging a title score, changing data types, mapping the number of employees to categorical values, removing columns with too many missing values, and adding fiscal quarters based on created date.

## Data Exploration & Visualization
Plotting the target variables made it clear that there are more unconverted leads than converted leads.
In looking at the lead source, we can see that Marketing generates more leads, and there is a higher percentage of Marketing leads that convert, whereas there are fewer converted Sales sourced leads. 

When digging deeper and considering industry and source, we can see that Marketing leads with 'Other' industry tend to convert despite not being in one of the dominant industries whereas Sales 'Other' lead dont quite convert as much.
Lastly, I noticed that company size seems to have a larger impact on Sales leads converting than on Marketing leads.

## Machine Learning models: *Decision Tree, Random Forest and Logistic Regression*

*Decision Tree*


I chose to start by using this model because it is the simplest and quite easy to interpret. 
I explored feature importance using 85% training and 15% test sets and without doing much parameter tuning or performing cross validation.

Initially, I set the maximum tree depth to 5 because I didn't want to build a very deep tree and overfit the training data. 
And, I chose to set the minimum sample split to 10 (there needs to be a minimum of 10 observations for there to be a split on a node). 

In looking at the feature importance, the initial tree indicated that title score, lead source, marketing score, and owner were among the important features.

| Feature Importance | Feature        |
| ------------------ |:--------------:|
| 0.931174           | Title Score    | 
| 0.027602           | LeadSource     | 
| 0.013535           | Marketing Score|
| 0.007659           | Source         |
| 0.007086           | OwnerId        |
| 0.004813           | Type           |
| 0.003364           | Owner          |

When performing cross validation to search for best tree depth and minimum sample split, the best score was 82% and 
the minimum samples per split were 5 and max depth found was 3. 

The features with highest feature importance were:

| Feature Importance | Feature        |
| ------------------ |:--------------:|
| 0.956501           | Title Score    | 
| 0.028352           | LeadSource     | 
| 0.007278           | OwnerID        |


After training the model with the best parameters, the model scored 93% on the test set. 
In comparison to the Random Forest and Logistic Regression, the tuned Decision Tree performed the worse.

*Random Forest*

Using 80% training and 20% test set and 1500 estimators, the Random Forest model scored 98.6% accuracy

*Logistic Regression*

Using 80% training and 20% test set, the Logistic Regression model scored 97.3% accuracy

### Conclusion -  Model Summary
While the tuned Decision Tree attributed more information gain to fewer features, the score was 93% and underperformed in comparison to the average scores 
of Random Forest (98.7%) and Logistic Regression (97.3%).
Random Forests beat Logistic Regression by quite a bit, so I think this is the model we should implement for predicting whether a lead will convert to an opportunity or not.

