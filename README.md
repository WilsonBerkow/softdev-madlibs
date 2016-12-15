# Reddit Madlibs

## Installation Instructions:
A **keys** file must be placed in the root directory of the application to allow for API use.

## Site Purpose:

Reddit Madlibs is a subreddit content masher that takes content from two different subreddits and produces a post using text processing and merging algorithms. It also analyzes the sentiment (or the **emotion**) expressed in the new post.

## Instructions of Use and Explanation of Backend
To use the application, enter the names of two existing subreddits that you want to mash. The backend component fetches comment and post data from Reddit and passes the data to the text processing component.
The text processing component generates a post using the provided content. Additionally, the text processing API is used to determine the sentiment expressed in the mash.

The finished product is sent back to the user and handled by the bootstrap augmented HTML frontend.

The contents of the currently produced post are accessible from the application homepage.

Developed by:  
Kenneth Li  
Wilson Berkow  
Gabriel Marks  
and Karol Regula  
