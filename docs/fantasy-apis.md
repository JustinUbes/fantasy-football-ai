# Interaction Options for Popular Fantasy Apps

## Popular Fantasy Sites
- [**Sleeper**](https://sleeper.com/)
- [**ESPN**](https://www.espn.com/fantasy/)
- [**Yahoo**](https://sports.yahoo.com/fantasy/)
- [**NFL Fantasy**](https://fantasy.nfl.com/)
- [**Fleaflicker**](https://www.fleaflicker.com/)

### [Sleeper API Docs](https://docs.sleeper.com/)
Sleeper offers a full read-only HTTP API. This will fit our use case because we will be doing all computing here, no changes will be made to a users team by anyone but them.

### [Cwendt94 ESPN API Library](https://github.com/cwendt94/espn-api)
ESPN does not offer a proprietary API, but Cwendt94 has written an espn-api on GitHub that could be of use to us. ESPN themselves uses a wide range of endpoints which are unmapped (this is worth further investigation).

### [Yahoo Fantasy API](https://sports.yahoo.com/developer/)
Yahoo offers an API on a **may issue basis**. You will have to apply for usage of the api which will be accessed through OAuth2.0. You will have to explicitly state that data was gotten using the Yahoo API and use **Yahoo Fantasy branding correctly.**

### NFL Fantasy API
The NFL restricts API access to NFL partners. We will have to incoporate a manual addition option where users can import their NFL Fantasy team.

### [Fleaflicker](https://www.fleaflicker.com/api-docs/index.html)
Fleaflicker offers an API.