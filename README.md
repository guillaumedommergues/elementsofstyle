# elementsofstyle
Computer vision applied to French furniture styles.

## Motivation
Many models already do a great job at object classification. It is quite interesting to prove that a model can recognize not only objects, but also styles. A Louis XVI chair is arguably more similar to another chair from a different style than to a Louis XVI table, yet the model is able to group the Louis XVI chair and table together.  

## Structure
model_creation : code to download labelled images and fine tune a RestNet model.<br>
model_deployment: code to deploy the site as a web application.

## Run the code used to create the model
(needs Anaconda or Miniconda)
```
conda create -n python=3.5 <env-name>
conda install requirements.txt
```


## Deploy the code to put the model online
(on Heroku, needs Heroku CLI installed)
```
git init
git add .
git commit -m "first commit"
heroku create
heroku git:remote -a <application_name>
git push heroku master
```

