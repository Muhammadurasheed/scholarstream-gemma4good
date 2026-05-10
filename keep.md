Assalamunaleikum ya AbduLlah

Allahuma salli Waselim ala Seyidina Muhammadin Waselim

We're building scholarstream 


scholarstream_indepth.md



KAGGLE_NOTEBOOK_CONTENT.md



GEMMA_SUBMISSION_CONTEXT.md

 for deepmind Kaggle hackathon 


KAGGLE_NOTEBOOK_CONTENT.md



Initially, scholarstream was built on gemini, so we decided to move the infrastructure to gemma, and here was the plan we drafted 


GEMMA_HACKATHON_PLAN.md



we're already serving the gemma model via gcp on vertex ai (It's so suprising that most of the time the application still complain bout rate limit 429 error as if we're still on gemini, pls decouple the issue causing this, we're so supposed to be unlimited on gemma, isn't it?), got api key (even have our firebase service key), but then we got to the point where we need to do some work on the Kaggle notebook, we spent over 6 hours on it yesterday, just to be getting error running program on the kaggle notebook

Now, I need you to step in like a fusion of google deepmind engrs and principal engrs and distributed engrs, analysed the entire codebase line by line, file by file, folder by folder, ensure you understand deeply how everything is being engineered, wired up, connected end to end, and be generous enough to comment on what's is FAANG level, and what need to be revamped to match the grade of deepmind engrs, but ultimately, I want to know if using google notebook is a most for the hackathon, or if it's just enough to have everything about gemma running on gcp, and we just do the needful in the application

Pls meticulously go through the current work and tell me how we can move forward to achieve a scholarstream of this dream 


scholarstream_brief.md


the scholarstream of our dream is an opportunity hub that's not just meant for "coders", not a stale database (a big redflag for judges)

what we want is user signup, we collect their information (the one we call academic DNA) in the 9 onboarding steps, then we do the needful with this information, feed it to our fleet of AI agents, this AI agents then go on the web, figure out the right places to go based on the given profile, get a wide range of varities of opportunities for the user, then these opportunities pass through our cortex v3 engine, the v3 engine do the needful and populate the right opportunity on the user dashboard. Then we wanted to have a FAANG level telemetry that's a direct mirror of what the ai agents are doing n the web, sites they mining opportunities from, challenges they're facing if any, the success their failure.

But at the same thing, I also need you to step in like a team of product develper and consultant from google and apple, and decide how:

1. this agent should actually be working in a that optimize our resources, while they're always on a radar to be getting users latest and freshest befitting opportunities across all the corner of the web, including x, linkedin, reddit etc. 

2. what the dashboard of a non-coder should look like, will dey be seeing hackathons, or something? I mean for a medical student or so

3. the database and UX, I really don't know how things are currently engred, but from what I've seen so far, opportunities are stored on db, and it's always render to users anytime they visit their dashboard, yh ofc new one are being added when obtain, (even tho, it's a subtle process, i.e we do't always recieve notification or anything that signals that, which is weird), but for judges, it's a big concern, if they just enter the platform, and they're already seeing unrealted opportunties retrieved from database, it's easy for them to close the tab and move to revieewing the next applicatioin, thinking that we smartly pre-filled our db with a stale data and rendering it, that our agents are actually doing nothing, being thinking of a way to actually manage this, but hasn't got something concrete yet, and I'd need your principal engr consulatation experience on how to exactly mange this. Is it to seek user consent on whether opportunities retrieved should be save to their db so that they see it when next they visit their db again or whatever? pls think out side the box to help with this

Allahu Musta'an


Allahu Musta'an