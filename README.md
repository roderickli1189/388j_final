# 388j_final
Final project for 388j

Write-up

## Q1 Description of your final project idea:

Grading comment:
Our final project idea is a web application that can allow users to track the squirrels on UMD campus.
Users will make posts with pictures of squirrels that they take and then upload it to the website with a location tag where people can comment.
## Q2 Describe what functionality will only be available to logged-in users:

Grading comment:
You can make a post and comment on a post.
## Q3 List and describe at least 4 forms:

Grading comment:
Registration (create an account with user/pass), login (user/pass), post submission (logged-in users can post a squirrel and select where it was seen), update user profile (logged in users can update pfp and username), comment form (allows logged in users to comment on a squirrel post).
## Q4 List and describe your routes/blueprints (don’t need to list all routes/blueprints you may have–just enough for the requirement):

Grading comment:
We will have a users blueprint for user login user/pass, a blueprint for discord login, a blueprint for UMD CAS login, and another blueprint for commenting and posting.
We will have a route to registration, login in, user profile, and home page.

## Q5 Describe what will be stored/retrieved from MongoDB:

Grading comment:
Account information including username password email and profile picture.
Post information including post title, image, date, location, and comments.
## Q6 Describe what Python package or API you will use and how it will affect the user experience:

Grading comment:
We can implement a log in with discord authentication API and log in with the UMD CAS API. Additionally we are using the mongo db api for posts and account information. We offer multiple login options, enabling users to select the method they prefer and find most convenient for accessing our site.
