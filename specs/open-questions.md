# Open Questions

## Product

- What is the first user-facing workflow?
- What outputs should the analyst produce?
- What level of personalization is required?

## Data
Specifics about the data can be found in the /docs section of this repository. 
- What historical and real-time inputs are needed?
- What data can be stored locally versus fetched on demand?

## Technical
We will use OpenAI API for AI reasoning. At the current moment, I am thinking we will use a Python backend since we will be using AI and that seamlessly interacts with Python. We will also be doing data analysis of sports statistics, human analysis of sports and fantasy sports information. I have not decided on a front end, but React.js or Next.js will most likely be used for their amount of support and professional looking design. React.js could be a solid option because of React Native allowing for easy translation into a mobile app, but this will require further exploration and consideration.

As far as infrastructure, we will use Microsoft Azure. We will use some sort of database offering so we can store user data and other necessary data for logic. We may even explore using embeddings, although the OpenAI API should offer embeddings. If we write the backend in Python, we will need a Python runtime which will have to be hosted on some sort of cloud offering (Kubernetes, VM, Azure Container Apps, etc.). The same will be true for our front end/website/app, we will need a Node runtime. Azure Networking services will be useful for configuring DNS and other aspects. Porkbun can be used to secure a domain when necessary.

It would make the most sense to write the backend/business logic first, and get a robust product locally. We must consider cost at the current time since I am one person writing and paying for the app.