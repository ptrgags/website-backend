# Backend for ptrgags.github.io
Backend script for ptrgags.github.io

This script fetches my public GitHub data and reformat the JSON into what I need for my website. I use an OAuth token so I can increase my rate limit, since I need to send many different requests to GitHub. 

I run this script from a cron job to generate JSON content for my website automatically, I can put the resulting JSON content on a server and fetch it using a single GET request from ptrgags.github.io
